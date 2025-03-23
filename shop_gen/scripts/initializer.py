from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from settings import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_USERNAME


def run():

    print("Importing users")
    call_command("loaddata", "fixtures/users.json")

    print("Importing systems")
    call_command("loaddata", "fixtures/systems.json")

    print("Importing books")
    call_command("loaddata", "fixtures/books.json")

    print("Importing spells")
    call_command("loaddata", "fixtures/spells.json")

    # print("Importing items")
    # call_command("loaddata", "fixtures/items.json")

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
