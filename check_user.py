import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
print(f"Total Users: {users.count()}")

for u in users:
    print(f"Username: {u.username}")
    print(f"  Superuser: {u.is_superuser}")
    if hasattr(u, 'profile'):
        print(f"  Profile Role: '{u.profile.role}'")
        print(f"  Profile Country: '{u.profile.country}'")
        print(f"  Profile Avatar: {u.profile.avatar}")
    else:
        print("  No Profile!")
