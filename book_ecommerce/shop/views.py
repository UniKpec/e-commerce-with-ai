from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated
from .models import ProfilYayinci,KitapOlusturma,Sepet
from .serializers import RegisterSerializers,RegisterYayinci,RegisterKitapOlusturma, RegisterSepet,RegisterOdemeBilgileri,RegisterAdresBilgileri#aynı dosyadan import ettğimiz için .serializers koyduk.
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken


class YayinciView(APIView):
    def post(self,request):
        serialize_publisher = RegisterYayinci(data=request.data)
        if serialize_publisher.is_valid():
            yayinciProfil = serialize_publisher.save()
            yayinci_kodu = yayinciProfil.yayinci_kodu
            return Response({
                "message": "Kayıt başarlı",
                "yayincikodu":yayinci_kodu,
            },status=status.HTTP_201_CREATED)
        
        return Response(serialize_publisher.errors,status=status.HTTP_400_BAD_REQUEST)

class LogInYayinci(APIView): #endpoint noktaları oluşturuyoruz.
    def post(self,request):
        yayinci_kodu = request.data.get("yayinci_kodu")
        password = request.data.get("password")
        try:
            profil = ProfilYayinci.objects.get(yayinci_kodu=yayinci_kodu)
            user = profil.user
        except ProfilYayinci.DoesNotExist:
            return Response({"detail":"Yayıncı kodu bulunmamıştır"},status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request,username=user.username,password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access":str(refresh.access_token),
                "message":"Giriş başaralı",
            },status=status.HTTP_200_OK)
        return Response({"detail:Giriş başarılısız."},status=status.HTTP_401_UNAUTHORIZED)



class RegisterView(APIView):
    def post(self,request):#request Kullanıcdan gelen json verisini alır.
        print(f"{request.data} view kısmı")
        serializer = RegisterSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED,)# otomatik olarak json dondurur.
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)# frontend tarafı internet diliyle konuşulduğu için status codes gonderiyoruz. 
    

class LoginView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request,username=username,password=password) #doğru bir şekilde girilmişse  user döner girilmmemisşe None doner.

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_200_OK)
    
        return Response({"detail":"Geçersiz kullanıcı adı veya şifre"},status=status.HTTP_401_UNAUTHORIZED)


class KitapOlusturmaView(APIView):
    def post(self,request):
        serializers_kitap_olusturma = RegisterKitapOlusturma(data=request.data)
        if serializers_kitap_olusturma.is_valid():
            serializers_kitap_olusturma.save()
            return Response(serializers_kitap_olusturma.data,status=status.HTTP_201_CREATED)
        return Response(serializers_kitap_olusturma.errors,status=status.HTTP_400_BAD_REQUEST)
    
class KitapListelemeView(APIView):
    def get(self,request):

        kitaplar = KitapOlusturma.objects.all()

        serializers = RegisterKitapOlusturma(kitaplar,many=True)

        return Response(serializers.data,status=status.HTTP_200_OK)
    
class KitapDetayView(APIView):
    def get(self,requesxt,pk):
        try:
            kitap = KitapOlusturma.objects.get(pk=pk)
        except KitapOlusturma.DoesNotExist:
            return Response({"detail":"kitap bulunumadı."},status=status.HTTP_404_NOT_FOUND)

        serializers = RegisterKitapOlusturma(kitap)
        kitap_data = serializers.data
        return Response({"kitap":kitap_data},status=status.HTTP_200_OK)


class SepetEkeleme(APIView):
    permission_classes = [IsAuthenticated] #sepete eklemesi için giriş yapmış veyahut kayıtlı olması ilk şartımız.
    
    def post(self,request): 
        kitap_id = request.data.get("kitap") #kitap ID'si alarak oyle bir kitap var mı yok mu? kontrol edecez.
        adet = int(request.data.get("adet"))#adet bilgisini int olarak almamız lazım.
        try:
            kitap = KitapOlusturma.objects.get(id=kitap_id)
        except KitapOlusturma.DoesNotExist:
            return Response({"error":"Oyle bir kitap bulunmamaktadır."},status=status.HTTP_404_NOT_FOUND)

        sepet_ogesi , created = Sepet.objects.get_or_create( #(model instance, boolean.) created false çıkarsa yeni bir sepet_ogesi nesnesi oluşturulacak.    
        musteri = request.user, kitap = kitap,defaults={'adet': adet}
        )
        if not created:
            sepet_ogesi.adet += adet
            sepet_ogesi.save()
        
        serializers = RegisterSepet(sepet_ogesi)
        return Response(serializers.data,status=status.HTTP_201_CREATED) 
    

class SatinAlView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self,request):

        adres_serializer = RegisterAdresBilgileri(data=request.data.get('adres'))
        odeme_serializer = RegisterOdemeBilgileri(data=request.data.get('odeme'))

        if not adres_serializer.is_valid():
            return Response(adres_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not odeme_serializer.is_valid():
            return Response(odeme_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adres = adres_serializer.save(musteri=request.user)
        odeme = odeme_serializer.save(kullanici=request.user, adres=adres)
        
        sepet_ogeleri= Sepet.objects.get(musteri=request.user)
        if not sepet_ogeleri.exists(): 
            return Response({"detail":"Sepetiniz boş"},status=status.HTTP_400_BAD_REQUEST)
        
        for oge in sepet_ogeleri: #stok adedinden fazla kitap alınmasın diye kontrol ediyoruz.
            kitap = oge.kitap
            if kitap.stok_adedi < oge.adet:
                return Response({"detail":f"{kitap.kitap_ismi} kitabın stok adedini kontrol ediniz."},status=status.HTTP_400_BAD_REQUEST)
            

            for oge in sepet_ogeleri:
                kitap = oge.kitap
                kitap.stok_adedi -= oge.adet #kitabın stok adedini düşürüyoruz.
                kitap.save()
                oge.delete()#sepetten ürünü siliyoruz.
            
            return Response({"message":"Satın alımı başırılı şekilde gerçekleşmiştir."},)#başarılı durumlarda status code yazmamıza gerek yok.
        
            

class SepetiListeleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        sepet = Sepet.objects.filter(musteri = request.user)
        serializers = RegisterSepet(sepet,many=True)#birden çok obje olacağı için many=true yapıyoruz.ve json verisi olarak dönsün seriler.
        return Response(serializers.data) #get durumlarında status yazmamıza gerek yok.
    

class SepettenVeriSilme(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,kitap_id):#url kısmından gelecek olan id var.
        try:
            sepet_ogesi = Sepet.objects.get(musteri=request.user,kitap=kitap_id)
            sepet_ogesi.delete()
            return Response({"detail":"Sepetten silindi"},status=status.HTTP_205_RESET_CONTENT)
        except Sepet.DoesNotExist:
            return Response({"detail":"Kitap sepette bulunamadı."},status=status.HTTP_404_NOT_FOUND)
        



class LogOutView(APIView):
    def post(self,request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()#Refresh tokenı direkt blacklist alıyoruz.Access tokenı silmek yeterli olmaz,root olan refresh tokenı blackliste almamız lazım.
            Response({"message:Çıkış işlemi başarılı bir şekilde gerçekleşti"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
