97
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page.as_view(), name="page1"),
    path('posts', views.all_posts.as_view(), name="page2"),
    path('posts/<slug:slug>', views.blog_page.as_view(), name="page3"),
    path('read-later', views.ReadLaterView.as_view(), name="page4")
]