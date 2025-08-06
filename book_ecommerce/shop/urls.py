from .views import RegisterView,YayinciView,LoginView,LogInYayinci,KitapOlusturmaView,LogOutView,SepetEkeleme,SepetiListeleView,SatinAlView,SepettenVeriSilme,KitapListelemeView,KitapDetayView,GeminiView,FiltrelemeView
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path("kayit/",RegisterView.as_view(),name="musteri-kayit"),
    path("giris/",LoginView.as_view(),name="musteri-giris"),
    path("yayinci/kayit/",YayinciView.as_view(),name="yayinci-kayit"),
    path("kitaplar/",KitapListelemeView.as_view(),name="kitaplar"),
    path("yayinci/giris/",LogInYayinci.as_view(),name="yayinci-giris"),
    path("kitap/filtreleme/",FiltrelemeView.as_view(),name="filtreleme-kitap"),
    path("bugün_ne_okusam/",GeminiView.as_view(),name="bugün-ne-okusam"),
    path("yayinci/kitap_ekleme/",KitapOlusturmaView.as_view(),name="yayinci-kitap-eklemesi"),
    path("kitaplar/<int:pk>/",KitapDetayView.as_view(),name="kitap-detay"),
    path("cikis/", LogOutView.as_view(),name="musteri-yayinci-cikis"),
    path("musteri/sepet_ekleme/",SepetEkeleme.as_view(),name="musteri-sepet-ekleme."),
    path("musteri/sepet_liste/",SepetiListeleView.as_view(),name="musteri-sepet-liste"),
    path("muster/satin_al/",SatinAlView.as_view(),name="musteri-satin-al"),
    path("musteri/sepetten_kitap_sil/",SepettenVeriSilme.as_view(),name="sepetten-kitap-silme")
]