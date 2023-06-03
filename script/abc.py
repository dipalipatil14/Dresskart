from django.contrib.auth.hashers import make_password, is_password_usable
from api.models import CustomUser

def hash_existing_passwords():
    for user in CustomUser.objects.all():
        if not is_password_usable(user.password):
            continue
        user.password = make_password(user.password)
        user.save()


hash_existing_passwords()