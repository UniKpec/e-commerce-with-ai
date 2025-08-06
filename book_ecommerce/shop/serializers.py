from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import ProfilYayinci,KitapOlusturma,Sepet,AdresBilgileri,OdemeBilgileri

class RegisterYayinci(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),message="Zaten boyle bir Yayıncı Emaili Kayıtlı.")])

    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only =True)

    yayinci_ismi = serializers.CharField(required=True,validators=[UniqueValidator(queryset=ProfilYayinci.objects.all(),message="Zaten böyle bir yayıncı ismi kayıtlı.")])
    class Meta:
        model = User
        fields=[
            "email","password","password2","yayinci_ismi"
        ]

    def validate(self,data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        return data
    
    def validate_email(self,value): #validate_<field_name>(self, value)(Field-level )
        if "@gmail.com"  not in value and "@outlook.com" not in value:
            raise serializers.ValidationError("Sadece gmail(@gmail) ve outlook(@outlook) formatında giriniz.")
        return value
    
    def validate_password(self,value):
        if len(value) < 12 :
            raise serializers.ValidationError("Lütfen en az 12 karakter giriniz.")
        if "!" not in value or "." not in value:
            raise serializers.ValidationError("Lütfen en az 1 tane ! ve . kullananız.") 
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        email = validated_data["email"]
        yayinci_ismi = validated_data.pop("yayinci_ismi")

        user = User.objects.create_user(
            email=email,
            username=yayinci_ismi,
            password=password,
        )

        profil = ProfilYayinci.objects.create(
            user=user,  
            yayinci_ismi = yayinci_ismi,
        )

        return profil



class RegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators =[UniqueValidator(queryset=User.objects.all(),message="Bu email zaten kullanılıyor")])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),message="Bu kullanacı zaten alınmış.")])
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ["email","username","password","password2"]


    def validate_email(self,value): #validate_<field_name>(self, value)(Field-level )
        if "@gmail.com"  not in value and "@outlook.com" not in value:
            raise serializers.ValidationError("Sadece gmail(@gmail) ve outlook(@outlook) formatında giriniz.")
        return value
    

    def validate_username(self,value):
        if any(char in value for char in [".","?","@","/"]):
            raise serializers.ValidationError("Kullanacı adınızda noktalama işaretleri kullanmayınız.")
        return value

    def validate_password(self,value):
        if len(value) < 12:
            raise serializers.ValidationError("Lütfen en az 12 karakter giriniz.")
        if "!" not in value or "." not in value:
            raise serializers.ValidationError("Lütfen en az 1 tane ! ve . kullananız.") 
        return value
    
    def validate(self, data): #dict formatında.
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        return data
    
    
    def create(self, validated_data):
        validated_data.pop("password2") #user modelinde gözükmüyor bu.
        print("Serializer create metodu validated_data:", validated_data)
        user =User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"], 
            password=validated_data["password"],
        )
        return user



class RegisterKitapOlusturma(serializers.ModelSerializer):
    
    class Meta:
        model = KitapOlusturma
        fields = "__all__"
        read_only_fields = ["yayinci","olusturulma_tarihi"] #sistem kendisi gireceği için kullanıcının doldurmasına gerek yok.


    def validate_sayfa_sayısı(self, value):
        if value < 0:
            raise serializers.ValidationError("Sayfa sayısı 0'dan küçük olamaz.")
        return value
    
   
    def validate_kitap_fiyat(self,value):
        if value <= 0:
            raise serializers.ValidationError("Kitap fiyatı 0 ve eksi olamaz. ")
        return value
   
   
    def validate_kitap_turu(self,value):
        valid_choice = [choice[0] for choice in KitapOlusturma.kitapTuru]
        if value not in valid_choice:
            raise serializers.ValidationError("Geçersiz Kitap türü seçildi.")
        return value
   
    def validate_kitap_acıklaması(self,value):
        listString = str(value).split()
        number = 0
        for num in listString:
            number = number+ 1
        if number < 30:
            raise serializers.ValidationError("En az 30 kelime yazınız.")
        return value
        
        
    def create(self, validated_data):
        return KitapOlusturma.objects.create(**validated_data)
        


class RegisterSepet(serializers.ModelSerializer):
    toplam_fiyat = serializers.SerializerMethodField() #property'deki toplam_fiyat metodunu almak için

    class Meta:
        model = Sepet
        fields = "__all__"
        read_only_fields = ["ekleme_tarihi","toplam_fiyat"]

    def get_toplam_fiyat(self,obj):
        return obj.toplam_fiyat



class RegisterAdresBilgileri(serializers.ModelSerializer):
    class Meta:
        model = AdresBilgileri
        fields = ["ad","soyad","sehir","ilce","ev_adres","telefon_numarisi"]
        read_only_fields = ["musteri"]

        

class RegisterOdemeBilgileri(serializers.ModelSerializer):
    class Meta:
        model=OdemeBilgileri
        fields = ["kart_numarasi","cvv","son_kullanma_tarihi"]
        read_only_fields = ["adres","kullanici"]