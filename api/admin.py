from django.contrib import admin

# Register your models here.

from .models import Note
from .models import UserImage
from .models import CustomUser

admin.site.register(Note)
admin.site.register(UserImage)
admin.site.register(CustomUser)

