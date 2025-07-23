from . import views
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path("signup/",views.signUpView,name="signup"),
    path("login/",views.logInView,name="login"),
    path("logout/",views.logout_view,name="logout-account"),
    path("",views.index,name="home"),

]