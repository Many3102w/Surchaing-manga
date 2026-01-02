from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def perfil_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            try:
                u_form.save()
                p_form.save()
                messages.success(request, f'¡Tu cuenta ha sido actualizada!')
                return redirect('perfil')
            except Exception as e:
                print(f"Error saving profile: {e}")
                messages.error(request, f"Error al guardar: {e}")
        else:
            # Debugging: Print errors to console
            print(f"User Form Errors: {u_form.errors}")
            print(f"Profile Form Errors: {p_form.errors}")
            messages.error(request, 'Por favor corrige los errores abajo.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # Ensure profile exists (it should via signals but double check prevents 500)
        if not hasattr(request.user, 'profile'):
            from .models import UserProfile
            UserProfile.objects.create(user=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'perfil.html', context)

