from django.urls import path
from createnews import views

app_name = 'createnews'

urlpatterns = [
    path('', views.show_news_list, name='show_news_list'),
    path('detail/<uuid:id>/', views.show_news_detail, name='show_news_detail'),
    path('create/', views.create_news_ajax, name='create_news_ajax'),
    path('edit/<uuid:id>/', views.edit_news_ajax, name='edit_news_ajax'),
    path('delete/<uuid:id>/', views.delete_news_ajax, name='delete_news_ajax'),
]
