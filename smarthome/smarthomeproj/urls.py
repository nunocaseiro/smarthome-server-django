"""smarthomeproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from django.views.generic import TemplateView
from smarthomeproj.server import views
from smarthomeproj.server import models
from django.contrib.auth.admin import UserAdmin
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'sensors', views.SensorViewSet)
router.register(r'sensorsvalues', views.SensorValueViewSet)
router.register(r'homes',views.HomeViewSet)
router.register(r'rooms',views.RoomViewSet)
router.register(r'photos',views.PhotoViewSet)
router.register(r'profiles',views.ProfileViewSet)
router.register(r'vehicles',views.VehicleViewSet)
router.register(r'favourites',views.FavouriteViewSet)
router.register(r'notifications',views.NotificationViewSet)
router.register(r'housekeys',views.HouseKeyViewSet)


admin.site.register(models.Sensor)
admin.site.register(models.SensorValue)
admin.site.register(models.Home)
admin.site.register(models.Room)
admin.site.register(models.Photo)
admin.site.register(models.Profile)
admin.site.register(models.Vehicle)
admin.site.register(models.Favourite)
admin.site.register(models.Notification)
admin.site.register(models.HouseKey)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('account/register/', views.UserCreate.as_view()),
    path('api/lastvaluesensor/', views.LastValue.as_view()),
    path('api/sensorsofroom/', views.SensorsOfRoom.as_view()),
    path('api/roomsfortesting/', views.RoomsForIOS.as_view()),
    path('api/actualrooms/', views.RoomsForAndroid.as_view()),
    path('api/sensorsoftype/', views.AllSensorsOfType.as_view()),
    path('api/userdetails/', views.GetUserByUsername.as_view()),
    path('api/userprofile/', views.GetUserProfileByUsername.as_view()),
    path('api/statistics/', views.GetStatistics.as_view()),
    path('api/countSensorsByRoom/', views.GetCountSensors.as_view()),
    path('api/vehiclesofhome/', views.GetVehiclesOfHome.as_view()),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^dj-rest-auth/', include('dj_rest_auth.urls')),
    url("api/insertPhoto/", views.postPhoto),
    path('api/changepassword/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('api/register/', views.RegisterView.as_view(), name='auth_register'),
    path('api/getNotificationsByUser/',views.NotificationByUserView.as_view()),
    path('api/sensorsandroid/',views.SensorsForAndroid.as_view()),
    path('api/subscribeMqtt/', views.subscribeMqtt.as_view()),
    path('api/sensortypes/',views.GetTypes.as_view()),
    path('api/favouritesofuser/',views.FavouritesOfUser.as_view()),
    path('api/accounts/',views.AccountsOfHome.as_view()),
    path('api/checkkey/', views.CheckHouseReg.as_view()),
    path('api/gethousewkey/',views.GetHouseWithKey.as_view()),
    path('api/deletephoto/',views.DeleteProfilePhoto.as_view())

    

]
