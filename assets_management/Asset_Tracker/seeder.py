import os
import sys
import django

# Append the directory containing your Django project to sys.path
sys.path.append(r'/home/neosoft/assesment_asset_tracker/Asset_Tracker')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Asset_Tracker.settings')

# Configure Django settings
django.setup()

# Rest of your seeder script


from django.contrib.auth.models import Group
def seed_roles():
    role_name = 'System Admin'

    # Check if the role already exists
    role, created = Group.objects.get_or_create(name=role_name)

    if created:
        # Remove any other existing roles
        Group.objects.exclude(name=role_name).delete()
        print(f"Role '{role_name}' created successfully.")
    else:
        print(f"Role '{role_name}' already exists.")

    return role

def run():
    role = seed_roles()

if __name__ == '__main__':
    run()
