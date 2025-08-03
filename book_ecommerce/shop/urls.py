from .views import RegisterView,YayinciView,LoginView,LogInYayinci,KitapOlusturmaView,LogOutView,SepetEkeleme,SepetiListeleView,SatinAlView,SepettenVeriSilme
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path("kayit/",RegisterView.as_view(),name="musteri-kayit"),
    path("giris/",LoginView.as_view(),name="giris-kayit"),
    path("yayinci/kayit/",YayinciView.as_view(),name="yayinci-kayit"),
    path("yayinci/giris/",LogInYayinci.as_view(),name="yayinci-giris"),
    path("yayinci/kitap_ekleme/",KitapOlusturmaView.as_view(),name="yayinci-kitap-eklemesi"),
    path("cikis/", LogOutView.as_view(),name="musteri-yayinci-cikis"),
    path("musteri/sepet_ekleme/",SepetEkeleme.as_view(),name="musteri-sepet-ekleme."),
    path("musteri/sepet_liste/",SepetiListeleView.as_view(),name="musteri-sepet-liste"),
    path("muster/satin_al/",SatinAlView.as_view(),name="musteri-satin-al"),
    path("musteri/sepetten_kitap_sil/",SepettenVeriSilme,name="sepetten-kitap-silme")
]