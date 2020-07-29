from django.urls import path

from tagging_system import views

urlpatterns = [
    path('images/', views.AddImage.as_view(), name='add-view-images'),
    path('tags/', views.AddTag.as_view(), name='add-view-tags'),

    path('image_list/', views.ListImage.as_view(), name='list-images'),
    path('images/<int:pk>/', views.LikeDislikeAPI.as_view(), name='like-images'),

    path('images/liked/<int:pk>/', views.LikedUsersAPI.as_view(), name='liked-users')

]
