from django.urls import path
from myapp import views


urlpatterns = [
    path('api/transactions/', views.TransactionList.as_view()),
    path('api/transactions/<uuid:pk>/', views.TransactionDetail.as_view()),
    path('api/default/', views.AccountBalance.as_view()),
    path('', views.HomeView.as_view())
]