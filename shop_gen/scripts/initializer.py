from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from settings import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_USERNAME
from gen.serializers import UserSerializer


def run():
    print("Running initializer")
    if User.objects.filter(email=DEFAULT_ADMIN_EMAIL, is_superuser=True).count() == 1:
        print("Admin user found")
    else:
        print("No admin found")
        admin_user = User.objects.create_superuser(
            DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD
        )
        print("Created admin user")
        token: Token = Token.objects.create(user=admin_user)
        token.save()
        print(f"Token {token.key}")
