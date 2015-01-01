from django.contrib import admin
from .models import RegKey,ResetKey

# Register your models here.

admin.autodiscover()

admin.site.register(RegKey)
admin.site.register(ResetKey)

