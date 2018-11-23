from django.contrib import admin

# Register your models here.
from sp_user.models import SpUser

admin.site.register(SpUser)