from django.urls import path
from . import views


urlpatterns = [
    path('staff-register/',views.RegisterAPI.as_view()),
    path('staff-login/',views.LoginAPI.as_view()),
    path('staff-update/',views.StaffUpdateAPI.as_view()),
    path('staff-view/',views.StaffViewAPI.as_view()),
    path('staff-logout/',views.LogoutAPI.as_view()),

]