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
        ("HIKAYE","Hikaye"),
        ("DENEME","deneme"),
        ("SIIR","Şiir"),
        ("BILIM","Bilim"),
        ("CIZGI_ROMAN","Çizgi roman"),
        ("EKONOMI","Ekonomi"),
        ("FELSEFE","Felsefe"),
    ]
    yayinci = models.ForeignKey(ProfilYayinci, on_delete=models.CASCADE)#bir yazarın birden çok eseri olabilir. #userdan silinirse yayincinin yayınladığı kitaplar da silinsin diye models.CASCADE yazıyoruz.
    kitap_ismi = models.CharField(max_length=100)
    kitap_isbn = models.CharField(max_length=13,unique=True,null=False)
    kitap_yazar_ismi = models.CharField(max_length=100)
    kitap_acıklması = models.TextField(max_length=300)
    kitap_fotografı = models.ImageField(null=True,blank=True)
    yayınlama_yılı = models.DateField()
    olusturulma_zamanı = models.DateTimeField(auto_now_add=True)
    sayfa_sayısı = models.PositiveIntegerField()
    kitap_turu = models.CharField(max_length=20,choices=kitapTuru)
    kitap_fiyat = models.DecimalField(max_digits=6,decimal_places=2)
    stok_adedi = models.IntegerField(default=0) #stok adedini 0 olarak ayarlıyoruz başta.
    satısta_mı = models.BooleanField(default=True)
    def __str__(self):
        return f"({self.kitap_ismi}) --- ({self.kitap_yazar_ismi}) --- ({self.kitap_acıklması}) ---"


class Sepet(models.Model):
    musteri = models.ForeignKey(User,on_delete=models.CASCADE) #id'sini verir bize.
    kitap = models.ForeignKey(KitapOlusturma,on_delete=models.CASCADE)
    adet = models.PositiveIntegerField(default=1)
    ekleme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.musteri} müşteri {self.kitap} kitabindan {self.adet} adet. {self.ekleme_tarihi} tarihinde."
    
    @property
    def toplam_fiyat(self):
        return self.adet * self.kitap.kitap_fiyat
    

class AdresBilgileri(models.Model):
    musteri = models.ForeignKey(User,on_delete=models.CASCADE)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    sehir = models.CharField(max_length=20)
    ilce = models.CharField(max_length=30)  
    ev_adres = models.TextField() 
    telefon_numarisi = models.CharField(max_length=10,)
    kart_numarisi = models.CharField(max_length=16,null=True, blank=True)
    cvv = models.CharField(max_length=3,null=True, blank=True)
    son_kullanma_tarihi = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.musteri}-- {self.ad} {self.soyad} --{self.ev_adres}"
 

class Siparisimler(models.Model):
    musteri = models.ForeignKey(User, on_delete=models.CASCADE)
    siparis_tarihi = models.DateTimeField(auto_now_add=True)
    toplam_tutar = models.DecimalField(max_digits=10,decimal_places=2)
    adres = models.ForeignKey(AdresBilgileri,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.musteri}--- {self.siparis_tarihi}--- {self.toplam_tutar}"
    
class SiparisDetay(models.Model):
    siparis = models.ForeignKey(Siparisimler,on_delete=models.CASCADE,related_name='detaylar') #related_name koymamızın sebebi Siparisimlerden direkt siparisDetaya erişmek istediğimiz variable name atıyoruz.
    kitap = models.ForeignKey(KitapOlusturma, on_delete=models.CASCADE)
    adet = models.IntegerField(default=1)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.kitap.kitap_ismi} --- {self.adet} --- {self.fiyat}"
   




# Create your models here.
