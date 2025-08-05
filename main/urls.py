from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('search/', views.SearchView.as_view(), name='search'),
]