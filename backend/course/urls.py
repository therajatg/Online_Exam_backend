from django.urls import path
from . import views


urlpatterns = [
    path('course-add/',views.AddCourseAPI.as_view()),
    path('course-update/',views.UpdateCourseAPI.as_view()),
    path('course-delete/',views.DeleteCourseAPI.as_view()),

    path('test-add/',views.AddTestAPI.as_view()),
    path('test-update/<str:pk>/',views.UpdateTestAPI.as_view()),
    path('test-delete/<str:pk>/',views.DeleteTestAPI.as_view()),
]