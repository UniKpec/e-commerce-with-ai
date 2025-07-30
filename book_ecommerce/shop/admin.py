from django.contrib import admin
from .models import ProfilYayinci,KitapOlusturma

@admin.register(ProfilYayinci)
class ProfilYayinciAdmin(admin.ModelAdmin):
    list_display = ["user","yayinci_ismi","yayinci_kodu"]

admin.site.register(KitapOlusturma)
# Register your models here.
