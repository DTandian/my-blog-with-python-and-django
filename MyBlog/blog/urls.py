from django.urls import path  # can configure url path
from blog import views  # allows to link with views

urlpatterns = [
    path('posts/', views.post_list, name='home'),
    path('posts/<str:category_name>/', views.post_list, name='post-list'),
    path('posts/detail/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/detail/<int:post_id>/<str:message>/', views.post_detail, name='post-detail-message'),
    #  POST a comment to url post-detail-message

    path('about/', views.about, name='about'),
]
