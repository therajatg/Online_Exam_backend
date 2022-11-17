from django.urls import path
from . import views


urlpatterns = [
    path('student-register/',views.RegisterAPI.as_view()),
    path('student-login/',views.LoginAPI.as_view()),
    path('student-update/',views.StudentUpdateAPI.as_view()),
    path('student-view/',views.StudentViewAPI.as_view()),
    path('student-logout/',views.LogoutAPI.as_view()),
    # path('students/<int:pk>/', views.StudentDetail.as_view()),
    # path('students/', views.StudentList.as_view()),

]