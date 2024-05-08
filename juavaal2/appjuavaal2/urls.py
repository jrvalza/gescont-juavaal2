

from django.urls import path
from appjuavaal2 import views, viewsUsers




urlpatterns = [    
    path('hello_world/',views.HelloWord.as_view()),
    
    path('not_logged_in/',viewsUsers.notLoggedIn),
    path('app_login/',viewsUsers.AppLogin.as_view()),
    path('app_logout/',viewsUsers.AppLogout.as_view()),


    path('parks/',views.Parks.as_view()),
    path('streets/',views.Streets.as_view()),
    path('people/',views.People.as_view()),

    path('pparks/',views.ProtectedParks.as_view()),
    path('pstreets/',views.ProtectedStreets.as_view()),
    path('ppeople/',views.ProtectedPeople.as_view()),
    
    ]






