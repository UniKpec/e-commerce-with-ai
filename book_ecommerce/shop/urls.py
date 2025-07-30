from .views import RegisterView,YayinciView,LoginView,LogInYayıncı,KitapOlusturmaView
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path("kayit/",RegisterView.as_view(),name="musteri-kayit"),
    path("giris/",LoginView.as_view(),name="giris-kayit"),
    path("yayinci/kayit/",YayinciView.as_view(),name="yayinci-kayit"),
    path("yayinci/giris/",LogInYayıncı.as_view(),name="yayinci-giris"),
    path("yayinci/kitap_ekleme/",KitapOlusturmaView.as_view(),name="yayinci-kitap-eklemesi")
]