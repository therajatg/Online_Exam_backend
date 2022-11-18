from django.urls import path
from . import views


urlpatterns = [
    path('student-register/',views.RegisterAPI.as_view()),
    path('student-login/',views.LoginAPI.as_view()),
    path('student-update/',views.StudentUpdateAPI.as_view()),
    path('student-view/',views.StudentViewAPI.as_view()),
    path('student-logout/',views.LogoutAPI.as_view()),
    path('student-disable/',views.DisableStudentAPI.as_view()),
]