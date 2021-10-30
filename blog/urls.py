from django.urls import path
from .views import Index
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('sousin/', views.Sousin.as_view(), name="sousin"),
    path('jusin/', views.Jusin.as_view(), name="jusin"),
    
    # <pk>にPostのIDを渡すと表示される。
    path('detail/<pk>/', views.Detail.as_view(), name="detail"),
    path('create/', views.Create.as_view(), name="create"),
    path('update/<pk>', views.Update.as_view(), name="update"),
    path('delete/<pk>', views.Delete.as_view(), name="delete"),
]
