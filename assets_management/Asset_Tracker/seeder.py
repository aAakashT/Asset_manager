import os
import sys
import django

sys.path.append(r'/home/neosoft/assesment_asset_tracker/Asset_Tracker')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Asset_Tracker.settings')


django.setup()


from django.contrib.auth.models import Group
def seed_roles():
    role_name = 'System Admin'

    role, created = Group.objects.get_or_create(name=role_name)

    if created:
        Group.objects.exclude(name=role_name).delete()
        print(f"Role '{role_name}' created successfully.")
    else:
        print(f"Role '{role_name}' already exists.")

    return role

def run():
    role = seed_roles()

if __name__ == '__main__':
    run()
