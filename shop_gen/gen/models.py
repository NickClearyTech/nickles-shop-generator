from django.db.models import Model, CharField, IntegerField, ForeignKey, BooleanField, CASCADE
from django.contrib.auth.models import User


class System(Model):
    abbreviation: CharField(max_length=8, null=False)
    full_name: CharField(max_length=64, null=False)


class Item(Model):
    name: CharField(max_length=128, null=False)
    description: CharField(max_length=4096, null=True)
    system: ForeignKey(System, on_delete=CASCADE, null=False)
    price: IntegerField()
    public: BooleanField()
    owner: ForeignKey(User, on_delete=CASCADE, null=False)
