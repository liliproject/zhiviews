from django.urls import path

from userapp import views

urlpatterns = [
    path('login/',views.login),
    path('regist/',views.regist),
    path('verifycode',views.verifycode),
    path('logout/',views.logout),
    path('modify/',views.modify),
]
