from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProfilYayinci
from .serializers import RegisterSerializers,RegisterYayinci,RegisterKitapOlusturma #aynı dosyadan import ettğimiz için .serializers koyduk.
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

class LogInYayıncı(APIView): #endpoint noktaları oluşturuyoruz.
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