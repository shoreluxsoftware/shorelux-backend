#admin_management/bootstrap_admin.py

import os
from django.contrib.auth import get_user_model

User = get_user_model()

def create_bootstrap_admin():
    username = os.getenv("BOOTSTRAP_ADMIN_USERNAME")
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD")
    email = os.getenv("BOOTSTRAP_ADMIN_EMAIL")

    if not username or not password:
        return

    if User.objects.filter(username=username).exists():
        return

    User.objects.create_superuser(
        username=username,
        password=password,
        email=email,
        role="ADMIN",
        can_login=True
    )

    print("✅ Bootstrap admin created")
