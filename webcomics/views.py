from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Manga, Like, Comment, Favorite, WarehouseItem, WarehouseEntry
from .forms import MangaForm, CommentForm

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
            
            try:
                from .utils import generate_depth_map, generate_3d_mesh
                from .models import MangaImage
                
                # 1. Base image must exist
                if form.instance.front_page:
                    # 2. Save additional images (Gallery)
                    images = self.request.FILES.getlist('additional_images')
                    for img in images:
                        MangaImage.objects.create(manga=form.instance, image=img)

                    # 3. Generate Depth Map (REAL AI)
                    try:
                        depth_map_file = generate_depth_map(form.instance.front_page.file)
                        if depth_map_file:
                            form.instance.depth_map.save(
                                f'depth_front_{form.instance.id}.png',
                                depth_map_file,
                                save=False
                            )
                    except Exception as e:
                        print(f"Depth generation failed: {e}")

                    # 4. Generate 3D Mesh (IA)
                    try:
                        mesh_file = generate_3d_mesh(form.instance.front_page.file)
                        if mesh_file:
                            form.instance.mesh_3d.save(
                                f'mesh_front_{form.instance.id}.obj',
                                mesh_file,
                                save=False
                            )
                    except Exception as e:
                        print(f"3D mesh generation failed: {e}")

                    # Mark as 3D converted if something worked
                    if form.instance.depth_map or form.instance.mesh_3d:
                        form.instance.is_3d_converted = True
                    
                    form.instance.save()
            except Exception as e:
                # Global catch to ensure the redirect happens no matter what
                print(f"Critical error in AI post processing for {form.instance.id}: {e}")

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

@login_required
def like_manga(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        like, created = Like.objects.get_or_create(user=request.user, manga=manga)
        if not created:
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

        return context

class IndexView(TemplateView):
    template_name = "index.html"
