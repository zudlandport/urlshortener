from django.contrib import admin

# Register your models here.

from django.contrib import admin

## core
from .models import myfwd, myfwdhit

admin.site.register(myfwd)
admin.site.register(myfwdhit)
