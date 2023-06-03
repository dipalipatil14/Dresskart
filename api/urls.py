from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('notes/create/', views.createNote),
    path('media/Image/', views.UploadImageView.as_view()),
    path('register/', views.RegisterAPI.as_view()),
    path('verify/', views.VerifyOTP.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('frontend/', views.createNote),
    path('notes/<str:pk>/update/', views.updateNote),
    path('notes/<str:pk>/delete/', views.deleteNote),
    path('notes/<str:pk>/', views.getNote),
    path('Image/',views.getNote),
]

