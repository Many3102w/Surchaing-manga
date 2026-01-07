
import os
import django
from django.conf import settings
from django.test import RequestFactory

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.views import SuperUserDashboardView
from django.contrib.auth.models import User, AnonymousUser

def debug_view():
    print("--- Starting SuperUserDashboardView Debug ---")
    
    # Create a request
    factory = RequestFactory()
    request = factory.get('/superuser/')
    
    # Simulate a superuser
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("No superuser found, creating one for test.")
            user = User.objects.create_superuser('admin_debug', 'admin@example.com', 'password')
    except Exception as e:
        print(f"Error getting/creating user: {e}")
        return

    request.user = user
    request.session = {} # Mock session

    view = SuperUserDashboardView()
    view.setup(request)
    
    try:
        print("Calling get_context_data...")
        context = view.get_context_data()
        print("SUCCESS! Context generated.")
        print("Keys:", context.keys())
    except Exception as e:
        print("\n!!! CRASH DETECTED !!!")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_view()
