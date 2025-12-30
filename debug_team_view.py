import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Q

print("--- Debugging Team View Logic ---")

# Mimic the view logic exactly
users = User.objects.filter(is_active=True).select_related('profile')
print(f"Total active users found: {users.count()}")

members_data = []
for user in users:
    print(f"Checking user: {user.username} (Superuser: {user.is_superuser})")
    
    has_profile = hasattr(user, 'profile')
    has_role = False
    profile_role = None
    
    if has_profile:
        profile_role = user.profile.role
        has_role = bool(profile_role)
        print(f"  - Profile found. Role: '{profile_role}' (Truthiness: {has_role})")
    else:
        print("  - No profile found.")

    if not user.is_superuser and not has_role:
        print("  -> SKIPPED (Not superuser and no role)")
        continue

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
    
    if user.is_superuser and not has_role:
        role = "Superuser"
    
    data = {
        'username': user.username,
        'role': role,
        'country': country,
        'avatar_url': avatar_url
    }
    members_data.append(data)
    print(f"  -> ADDED: {data}")

print(f"Final Count in Team List: {len(members_data)}")
