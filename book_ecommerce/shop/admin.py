from django.contrib import admin
from .models import ProfilYayinci,KitapOlusturma,User,AdresBilgileri
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

# Yeni, özelleştirilmiş UserAdmin sınıfımızı tanımla.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Admin panelde görünen sütunları belirle.
    list_display = (
        "username", 
        "email", 
        "first_name", 
        "last_name", 
        "is_staff", 
        "last_login"  # last_login alanını buraya ekliyoruz.
    )

    # Bu alanların admin panelde değiştirilememesini sağlar.
    readonly_fields = ("last_login",) 


@admin.register(ProfilYayinci)
class ProfilYayinciAdmin(admin.ModelAdmin):
    list_display = ["user","yayinci_ismi","yayinci_kodu"]

admin.site.register(KitapOlusturma)
admin.site.register(AdresBilgileri)
# Register your models here.
