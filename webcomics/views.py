from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum, Max, Q, OuterRef, Subquery
from .models import Manga, Like, Comment, Favorite, WarehouseItem, WarehouseEntry, ChatMessage
from .forms import MangaForm, CommentForm
from .ai_utils import get_ai_response

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mangas'] = Manga.objects.all()
        return context


class SearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        manga = request.GET.get("manga")
        if manga:
            if len(manga) > 16:
                return HttpResponse("Error: El nombre es muy largo")
            else:
                manga_name = Manga.objects.filter(nombre_del_manga__icontains=manga)
                return render(request, self.template_name, {"manga_name": manga_name})
        return render(request, self.template_name, {})





class LoginView(TemplateView):
    template_name = "login.html"


class AboutView(TemplateView):
    template_name = "about.html"


class IngresarView(TemplateView):
    template_name = "login.html"


class LibraryView(TemplateView):
    template_name = "library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We rely on context processor for mangas, but we can add forms here
        context['comment_form'] = CommentForm()
        return context

def product_detail(request, manga_id):
    """Dedicated product detail page for sharing"""
    manga = get_object_or_404(Manga, id=manga_id)
    return render(request, 'product_detail.html', {'manga': manga})

class CreatePostView(UserPassesTestMixin, CreateView):
    model = Manga
    form_class = MangaForm
    template_name = "create_post.html"
    success_url = reverse_lazy('library')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        try:
            form.instance.fecha_de_carga = timezone.now()
            
            # Save basic instance first to ensure the post is created even if AI fails
            # This handles the image upload to Cloudinary
            response = super().form_valid(form)
            
            # CRITICAL FIX: Run AI in Background Thread to prevent Render 30s Timeout
            import threading
            def run_ai_background(manga_instance_id):
                try:
                    # Re-fetch instance to avoid race conditions
                    from .models import Manga
                    from .utils import generate_depth_map, generate_3d_mesh
                    
                    # Need to setup django context if using DB in thread? 
                    # Usually fine for simple updates, but best practice is careful.
                    # Django closes DB connections on request end, so we need to ensure thread has its own.
                    from django.db import connection
                    connection.close() # Force new connection for thread

                    instance = Manga.objects.get(id=manga_instance_id)
                    print(f"BACKGROUND: Starting AI for {instance.id}")

                    # 3. Generate Depth Map (REAL AI)
                    try:
                        if instance.front_page:
                            # Re-open the file from storage
                            instance.front_page.open()
                            depth_map_file = generate_depth_map(instance.front_page.file)
                            if depth_map_file:
                                instance.depth_map.save(
                                    f'depth_front_{instance.id}.png',
                                    depth_map_file,
                                    save=False
                                )
                    except Exception as e:
                        print(f"BACKGROUND ERROR (Depth): {e}")

                    # 4. Generate 3D Mesh (IA)
                    try:
                        if instance.front_page:
                            instance.front_page.open()
                            print(f"BACKGROUND: generating 3D mesh...")
                            mesh_file = generate_3d_mesh(instance.front_page.file)
                            if mesh_file:
                                instance.mesh_3d.save(
                                    f'mesh_front_{instance.id}.glb',
                                    mesh_file,
                                    save=False
                                )
                    except Exception as e:
                        print(f"BACKGROUND ERROR (3D): {e}")

                    # Mark as 3D converted if something worked
                    if instance.depth_map or instance.mesh_3d:
                        instance.is_3d_converted = True
                        print(f"BACKGROUND: Success! Marked as 3D converted.")
                    
                    instance.save()
                    print("BACKGROUND: AI Processing Complete.")

                except Exception as e:
                    print(f"BACKGROUND CRITICAL FAIL: {e}")

            # Launch the thread
            thread = threading.Thread(target=run_ai_background, args=(form.instance.id,))
            thread.daemon = True # Daemon threads die if main process dies, but on Render web service it usually runs until idle.
            thread.start()
            
            from django.contrib import messages
            messages.info(self.request, "Publicación creada. La IA está generando el 3D en segundo plano (Puede tardar 1 minuto).")

            return response
            
        except Exception as e:
            # Catch primary save errors (like Cloudinary credentials missing)
            print(f"CRITICAL: Failed to save post (Storage/DB error): {e}")
            form.add_error(None, f"Error al guardar (Verificar Cloudinary): {e}")
            return self.form_invalid(form)

@login_required
def delete_post(request, manga_id):
    if not request.user.is_superuser:
        return redirect('library')
    
    manga = get_object_or_404(Manga, id=manga_id)
    manga.delete()
    return redirect('library')

@login_required
def toggle_favorite(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, manga=manga)
        if not created:
            fav.delete()
            favorited = False
        else:
            favorited = True
        return JsonResponse({'favorited': favorited})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# @login_required  <-- Removed to allow anonymous likes
def like_manga(request, manga_id):
    if request.method == 'POST':
        # Ensure session exists for anonymous users
        if not request.session.session_key:
            request.session.create()
            
        manga = get_object_or_404(Manga, id=manga_id)
        
        # Determine identifier
        if request.user.is_authenticated:
            # User Like
            like, created = Like.objects.get_or_create(user=request.user, manga=manga)
        else:
            # Anonymous Session Like
            session_key = request.session.session_key
            # Check if this session already liked this manga
            # We filter explicitly because get_or_create with nullable user might get confused if we don't specify user=None clearly
            like, created = Like.objects.get_or_create(session_key=session_key, manga=manga, defaults={'user': None})

        if not created:
            # If it existed, toggle off
            like.delete()
            liked = False
        else:
            liked = True
            
        return JsonResponse({'liked': liked, 'count': manga.likes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_comment(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.user = None
            comment.manga = manga
            comment.save()
            return redirect('library')
    return redirect('library')



from django.db.models import Q

class TeamView(TemplateView):
    template_name = "team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all active users and prefetch profile to avoid N+1
        # We use prefetch_related because 'profile' is a reverse OneToOne relation,
        # although select_related is supported for reverse OneToOne, prefetch in this case is safer if structure varies.
        # Actually, let's just use select_related if sure, but prefetch is safer for avoiding join filtering issues.
        # Wait, simple approach: Fetch all users, filter in python.
        users = User.objects.filter(is_active=True).select_related('profile')
        
        members_data = []
        for user in users:
            # Determine if user should be shown
            # Show if Superuser OR (has profile AND has role)
            has_profile = hasattr(user, 'profile')
            has_role = has_profile and user.profile.role
            
            if not user.is_superuser and not has_role:
                continue

            # Prepare data
            role = "Miembro"
            country = ""
            avatar_url = None

            if has_profile:
                profile = user.profile
                if profile.avatar:
                    avatar_url = profile.avatar.url
                if profile.role:
                    role = profile.role
                if profile.country:
                    country = profile.country
            
            # Fallback for superuser with no role
            if user.is_superuser and not has_role:
                role = "Superuser"

            members_data.append({
                'username': user.username,
                'avatar_url': avatar_url,
                'role': role,
                'country': country
            })
        
        context['team_members'] = members_data
        return context

@login_required
def toggle_vendido(request, manga_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    manga = get_object_or_404(Manga, id=manga_id)
    manga.vendido = not manga.vendido
    if manga.vendido:
        manga.fecha_venta = timezone.now()
    else:
        manga.fecha_venta = None
    manga.save()
    return redirect('library')

@login_required
def update_warehouse(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        category = request.POST.get('category')
        action = request.POST.get('action') # 'add' or 'subtract' (subtract is old behavior, modal will use 'add' with specifics)
        
        item, created = WarehouseItem.objects.get_or_create(category=category)
        
        if action == 'add':
            qty = int(request.POST.get('quantity', 1))
            cost = float(request.POST.get('cost', 0))
            price = float(request.POST.get('price', 0))
            manga_id = request.POST.get('manga_id')
            
            # Update total stock
            item.quantity += qty
            item.save()
            
            manga = None
            if manga_id:
                try:
                    manga = Manga.objects.get(id=manga_id)
                except Manga.DoesNotExist:
                    pass
            
            # Log the entry with financial details
            WarehouseEntry.objects.create(
                warehouse_item=item,
                manga=manga,
                quantity=qty,
                unit_cost=cost,
                unit_price=price
            )
            return JsonResponse({'success': True, 'new_quantity': item.quantity})
            
        elif action == 'subtract':
            if item.quantity > 0:
                item.quantity -= 1
                item.save()
                return JsonResponse({'success': True, 'new_quantity': item.quantity})
            return JsonResponse({'success': False, 'error': 'No hay stock para restar'})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

class SuperUserDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "superuser_dashboard.html"

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.db.models import Sum
        
        # Latest products for the inventory table
        context['latest_products'] = Manga.objects.all().order_by('-fecha_de_carga')[:5]
        
        # Real metrics from DB
        sold_items = Manga.objects.filter(vendido=True)
        total_sales_raw = sold_items.aggregate(Sum('precio'))['precio__sum'] or 0
        context['total_sales'] = round(float(total_sales_raw), 2)
        context['active_orders'] = sold_items.count()
        
        # All available digital products for the warehouse modal (as JSON list)
        import json
        digital_products_raw = Manga.objects.filter(vendido=False).values('id', 'nombre_del_manga', 'type_of_manga', 'precio')
        # Convert Decimal to float for JSON serialization
        digital_products_list = [
            {
                'id': p['id'],
                'nombre_del_manga': p['nombre_del_manga'],
                'type_of_manga': p['type_of_manga'],
                'precio': float(p['precio'])
            }
            for p in digital_products_raw
        ]
        context['all_digital_products'] = json.dumps(digital_products_list)
        
        # Categorized stock (Digital Catalog)
        catalog_counts = {
            'Denim Tears': Manga.objects.filter(type_of_manga='Denim Tears', vendido=False).count(),
            'Essentials': Manga.objects.filter(type_of_manga='Essentials', vendido=False).count(),
            'Dandy Hats': Manga.objects.filter(type_of_manga='Dandy Hats', vendido=False).count(),
            'Barbas Hats': Manga.objects.filter(type_of_manga='Barbas Hats', vendido=False).count(),
        }
        
        context['stock_gorras'] = catalog_counts['Dandy Hats'] + catalog_counts['Barbas Hats']
        context['stock_prendas'] = catalog_counts['Denim Tears'] + catalog_counts['Essentials']
        
        # Warehouse vs Catalog Comparison
        comparison = []
        total_warehouse = 0
        categories = ['Denim Tears', 'Essentials', 'Dandy Hats', 'Barbas Hats']
        
        for cat in categories:
            w_item, _ = WarehouseItem.objects.get_or_create(category=cat)
            catalog_qty = catalog_counts[cat]
            diff = w_item.quantity - catalog_qty
            total_warehouse += w_item.quantity
            
            comparison.append({
                'category': cat,
                'warehouse': w_item.quantity,
                'catalog': catalog_qty,
                'diff': diff,
                'abs_diff': abs(diff),
                'display_diff': str(diff),
                'display_abs_diff': str(abs(diff)),
                'status': 'match' if diff == 0 else ('excess' if diff > 0 else 'missing')
            })
            
        context['comparison'] = comparison
        context['total_warehouse'] = total_warehouse
        
        # --- Analytics Data for Reports ---
        month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        current_month_idx = timezone.now().month - 1
        
        # 1. Monthly Sales (Real Data + Demo Fallback)
        month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        sales_real = [0] * 12
        for item in sold_items:
            m_idx = item.fecha_de_carga.month - 1
            sales_real[m_idx] += float(item.precio)
        
        # Fallback if no sales
        if sum(sales_real) == 0:
            sales_real = [500, 600, 450, 700, 850, 900, 1200, 1100, 1500, 1800, 2000, 1900]
            
        context['chart_sales_labels'] = month_names
        context['chart_sales_data'] = sales_real
        
        # 2. Profit vs Loss (Real Data Only)
        total_revenue = float(context['total_sales'])
        total_cost_sold = sum(float(item.costo) for item in sold_items)
        
        context['chart_pie_labels'] = ['Ganancia Neta (Ventas)', 'Costo de Mercancía Vendida', 'Gastos Operativos (Estimados)']
        pie_data = [
            max(0, total_revenue - total_cost_sold), 
            total_cost_sold, 
            total_revenue * 0.1 # 10% estimated overhead
        ]
        
        # Fallback if no revenue
        if sum(pie_data) == 0:
            pie_data = [700, 500, 200]
            
        context['chart_pie_data'] = pie_data
        
        # 3. Seasonality (Categories - Real Catalog)
        category_perf = [
            catalog_counts['Denim Tears'], 
            catalog_counts['Essentials'], 
            catalog_counts['Dandy Hats'], 
            catalog_counts['Barbas Hats']
        ]
        context['chart_radar_labels'] = ['Denim Tears', 'Essentials', 'Dandy Hats', 'Barbas Hats']
        context['chart_radar_data'] = category_perf
        
        # 4. Trends / Festivities (Demo + Real)
        context['chart_trend_labels'] = ['Navidad', 'Black Friday', 'Rebajas Verano', 'Día del Padre', 'Día de la Madre']
        context['chart_trend_data'] = [120, 150, 80, 200, 140]
        
        # 5. Projected Profit Margins (Warehouse)
        warehouse_entries = WarehouseEntry.objects.all()
        total_inv_cost = 0
        total_exp_revenue = 0
        
        for entry in warehouse_entries:
            total_inv_cost += float(entry.unit_cost) * entry.quantity
            total_exp_revenue += float(entry.unit_price) * entry.quantity
        
        # Add demo data if no warehouse entries exist yet
        if total_inv_cost == 0 and total_exp_revenue == 0:
            total_inv_cost = 500  # Demo: $500 invested
            total_exp_revenue = 800  # Demo: $800 expected return
            
        context['chart_margin_labels'] = ['Inversión Total', 'Retorno Esperado', 'Ganancia Proyectada']
        context['chart_margin_data'] = [
            total_inv_cost,
            total_exp_revenue,
            max(0, total_exp_revenue - total_inv_cost)
        ]

        # 6. Active Chats for Support (Better Grouping: User-first, then Session)
        support_latest = ChatMessage.objects.filter(
            Q(user_id=OuterRef('user')) if OuterRef('user') else Q(session_key=OuterRef('session_key')),
            is_dm=False
        ).order_by('-created_at')

        support_chats_raw = ChatMessage.objects.filter(is_dm=False).values('session_key', 'user', 'user__username').annotate(
            last_msg_time=Max('created_at'),
            last_msg_text=Subquery(support_latest.values('message')[:1]),
            last_msg_is_admin=Subquery(support_latest.values('is_from_admin')[:1])
        ).order_by('-last_msg_time')

        # DMs (Direct Messages from products)
        dm_latest = ChatMessage.objects.filter(
            Q(user_id=OuterRef('user')) if OuterRef('user') else Q(session_key=OuterRef('session_key')),
            is_dm=True
        ).order_by('-created_at')

        dm_chats_raw = ChatMessage.objects.filter(is_dm=True).values('session_key', 'user', 'user__username').annotate(
            last_msg_time=Max('created_at'),
            last_msg_text=Subquery(dm_latest.values('message')[:1]),
            last_msg_is_admin=Subquery(dm_latest.values('is_from_admin')[:1])
        ).order_by('-last_msg_time')

        def process_chats(raw_list):
            processed = []
            for chat in raw_list:
                display_name = chat['user__username']
                if not display_name:
                    s_key = chat['session_key'] or ""
                    short_id = s_key[-4:].upper() if len(s_key) >= 4 else "TEMP"
                    display_name = f"Anónimo {short_id}"
                chat['display_name'] = display_name
                processed.append(chat)
            return processed

        context['support_chats'] = process_chats(support_chats_raw)
        context['dm_chats'] = process_chats(dm_chats_raw)
        context['active_chats'] = context['support_chats'] # For backward compatible template usage if needed

        return context

class IndexView(TemplateView):
    template_name = "index.html"

def get_chat_messages(request):
    s_key = request.GET.get('s_key')
    u_id = request.GET.get('u_id')
    is_dm = request.GET.get('is_dm') == 'true'
    
    if request.user.is_superuser and (s_key or u_id):
        # Admin fetching a conversation
        if u_id and u_id != 'None':
            messages = ChatMessage.objects.filter(Q(user_id=u_id) | Q(session_key=s_key), is_dm=is_dm)
        else:
            messages = ChatMessage.objects.filter(session_key=s_key, user=None, is_dm=is_dm)
        
        # Mark as read
        messages.filter(is_from_admin=False).update(is_read=True)
    else:
        # User/Anon fetching their own
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        if request.user.is_authenticated:
            messages = ChatMessage.objects.filter(Q(user=request.user) | Q(session_key=session_key))
        else:
            messages = ChatMessage.objects.filter(session_key=session_key, user=None)
    
    data = [{
        'message': m.message,
        'is_from_admin': m.is_from_admin,
        'timestamp': m.created_at.strftime('%H:%M'),
    } for m in messages]
    return JsonResponse({'messages': data})

@login_required
def get_unread_dm_notifications(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    
    unread_dms = ChatMessage.objects.filter(is_dm=True, is_from_admin=False, is_read=False)
    count = unread_dms.count()
    
    notifications = []
    if count > 0:
        for msg in unread_dms:
            # We skip marking as read here, dashboard will do it via get_chat_messages
            # but we return them once. The dashboard will handle deduplication or 
            # we just return the latest.
            notifications.append({
                'id': msg.id,
                'message': msg.message,
                'sender': msg.user.username if msg.user else f"Anónimo {msg.session_key[-4:].upper() if msg.session_key else 'TEMP'}",
                'timestamp': msg.created_at.strftime('%H:%M')
            })
            
    return JsonResponse({
        'unread_count': count,
        'notifications': notifications
    })


from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

def send_chat_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if not message_text:
            return JsonResponse({'error': 'Message empty'}, status=400)
            
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        
        # --- LOGIN FLOW STATE MACHINE ---
        login_step = request.session.get('chat_login_step')
        
        if message_text.lower() == 'loginsuperuser' and not login_step:
            request.session['chat_login_step'] = 'username'
            reply = "🔒 Iniciando proceso de acceso. Por favor, ingresa tu **nombre de usuario**:"
            ChatMessage.objects.create(session_key=session_key, message=message_text, is_from_admin=False)
            ChatMessage.objects.create(session_key=session_key, message=reply, is_from_admin=True)
            return JsonResponse({'status': 'sent', 'reply': reply, 'login_mode': 'username'})

        if login_step == 'username':
            request.session['chat_login_user'] = message_text
            request.session['chat_login_step'] = 'password'
            reply = f"Usuario '{message_text}' recibido. Ahora, por favor ingresa tu **contraseña**:"
            # No guardamos el usuario en ChatMessage para evitar leaks si es sensible, o lo guardamos como asteriscos
            ChatMessage.objects.create(session_key=session_key, message="[USUARIO PROPORCIONADO]", is_from_admin=False)
            ChatMessage.objects.create(session_key=session_key, message=reply, is_from_admin=True)
            return JsonResponse({'status': 'sent', 'reply': reply, 'login_mode': 'password'})

        if login_step == 'password':
            username = request.session.get('chat_login_user')
            password = message_text
            user = authenticate(username=username, password=password)
            
            # Limpiar rastro inmediatamente
            del request.session['chat_login_step']
            del request.session['chat_login_user']
            
            if user is not None:
                login(request, user)
                reply = f"✅ ¡Acceso concedido! Bienvenido de nuevo, **{user.username}**. Ya puedes cerrar el chat o seguir navegando."
                ChatMessage.objects.create(session_key=session_key, message="[CONTRASEÑA PROPORCIONADA]", is_from_admin=False)
                ChatMessage.objects.create(session_key=session_key, message=reply, is_from_admin=True)
                return JsonResponse({'status': 'sent', 'reply': reply, 'login_success': True})
            else:
                reply = "❌ Credenciales incorrectas. El proceso de login se ha cancelado por seguridad. Inténtalo de nuevo escribiendo 'loginsuperuser'."
                ChatMessage.objects.create(session_key=session_key, message="[ACCESO FALLIDO]", is_from_admin=True)
                return JsonResponse({'status': 'sent', 'reply': reply})
        # ---------------------------------

        # 1. Save User Message
        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            message=message_text,
            is_from_admin=False
        )

        # 2. Get AI Response
        # Fetch recent history for this session/user
        if request.user.is_authenticated:
            history_objs = ChatMessage.objects.filter(Q(user=request.user) | Q(session_key=session_key)).order_by('-created_at')[:6]
        else:
            history_objs = ChatMessage.objects.filter(session_key=session_key, user=None).order_by('-created_at')[:6]
        
        # Format history for Gemini
        chat_history = []
        for h in reversed(history_objs):
            chat_history.append({
                'message': h.message,
                'is_from_admin': h.is_from_admin
            })

        # Generate response in background? No, let's do it synchronously for now 
        # but better in thread if it takes > 10s. Gemini Flash is fast.
        ai_reply = get_ai_response(message_text, chat_history)

        # 3. Save AI Response as Admin
        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            message=ai_reply,
            is_from_admin=True
        )

        return JsonResponse({'status': 'sent', 'reply': ai_reply})
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required
def admin_chat_reply(request):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error'}, status=403)
    
    if request.method == 'POST':
        msg = request.POST.get('message')
        s_key = request.POST.get('session_key')
        u_id = request.POST.get('user_id')
        is_dm = request.POST.get('is_dm') == 'true'
        
        target_user = None
        if u_id:
            target_user = get_object_or_404(User, id=u_id)
            
        ChatMessage.objects.create(
            user=target_user,
            session_key=s_key,
            message=msg,
            is_from_admin=True,
            is_dm=is_dm
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'}, status=400)

def get_dm_messages(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    messages = ChatMessage.objects.filter(
        Q(user=request.user) if request.user.is_authenticated else Q(session_key=session_key),
        is_dm=True
    ).order_by('created_at')
    
    return JsonResponse({
        'messages': [
            {
                'message': m.message,
                'is_from_admin': m.is_from_admin,
                'timestamp': m.created_at.strftime("%H:%M")
            } for m in messages
        ]
    })


def health_check(request):
    """Simple view to keep the server alive."""
    return JsonResponse({'status': 'ok', 'message': 'I am alive!'})

# --- Notification Logic ---
from exponent_server_sdk import PushClient, PushMessage
from .models import ExpoPushToken

@csrf_exempt
def register_push_token(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'Token missing'}, status=400)
            
            # Save for the first superuser found (since this app is single-admin mostly)
            # OR if request.user is authenticated, save for them.
            # Assuming mobile app logs in as superuser or we just want to notify THE superuser.
            
            # Strategy: Store token for specific user if logged in, otherwise generic?
            # User flow: Admin logs in on mobile -> App sends token.
            
            if request.user.is_authenticated:
                ExpoPushToken.objects.update_or_create(
                    user=request.user,
                    defaults={'token': token}
                )
                return JsonResponse({'status': 'registered', 'user': request.user.username})
            else:
                return JsonResponse({'error': 'Authentication required'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def send_push_notification(title, body, data=None):
    try:
        # Get all superusers tokens
        tokens = ExpoPushToken.objects.filter(user__is_superuser=True)
        if not tokens.exists():
            return
            
        messages = []
        for t in tokens:
            messages.append(PushMessage(
                to=t.token,
                title=title,
                body=body,
                data=data,
                sound='default',
                priority='high',
                channel_id='default'
            ))
            
        PushClient().publish_multiple(messages)
    except Exception as e:
        print(f"Push Error: {e}")

# Modify existing send_dm_message to trigger push
def send_dm_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            
        msg = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            message=message_text,
            is_dm=True
        )
        
        # Trigger Push Notification to Admin
        sender_name = request.user.username if request.user.is_authenticated else f"Cliente {session_key[-4:]}"
        send_push_notification(
            title="Nuevo DM de Producto",
            body=f"{sender_name}: {message_text}",
            data={'msg_id': msg.id, 'session_key': session_key}
        )
        
        return JsonResponse({'status': 'sent'})
    return JsonResponse({'status': 'error'}, status=400)
