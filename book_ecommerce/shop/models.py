from django.db import models
from django.contrib.auth.models import User
import string,random


def yayinciKoduOlusturma():
    return "".join(random.choices(string.ascii_uppercase + string.digits,k=8))


class ProfilYayinci(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)#burda her yayıncı'nın user modeli olduğunu soyluyor ve Eğer yayıncı profili silinirse user'dan da sil diyoruz.
    yayinci_ismi = models.CharField(max_length=100,unique=True)
    yayinci_kodu = models.CharField(max_length=8,unique=True,default=yayinciKoduOlusturma)

    def __str__(self):
        return f"({self.yayinci_kodu}) {self.yayinci_ismi}"

class KitapOlusturma(models.Model):
    kitapTuru = [ #tuple içinde vermemiz lazım.İlk veritabanına kaydetme,ikinci isim frontende gözükecek alan.
        ("ROMAN","Roman"),
        ("HİKAYE","Hikaye"),
        ("DENEME","deneme"),
        ("SİİR","Şiir"),
        ("BILIM","Bilim"),
        ("CIZGIROMAN","Çizgi roman"),
        ("EKONOMI","Ekonomi"),
        ("FELSEFE","Felsefe"),
    ]
    yayinci = models.ForeignKey(User, on_delete=models.CASCADE)#bir yazarın birden çok eseri olabilir.
    kitap_ismi = models.CharField(max_length=100)
    kitap_yazar_ismi = models.CharField(max_length=100)
    kitap_acıklması = models.TextField(max_length=300)
    kitap_fotografı = models.ImageField()
    yayınlama_yılı = models.DateField()
    olusturulma_zamanı = models.DateTimeField(auto_now_add=True)
    sayfa_sayısı = models.PositiveIntegerField()
    kitap_turu = models.CharField(max_length=20,choices=kitapTuru)
    kitap_fiyat = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"({self.kitap_ismi}) --- ({self.kitap_yazar_ismi}) --- ({self.kitap_acıklması}) ---"


# Create your models here.
