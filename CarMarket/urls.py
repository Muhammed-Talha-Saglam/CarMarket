"""CarMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CarMarket import views

urlpatterns = [
    path('', views.showCars),
    path('admin/', admin.site.urls),
    path('showCars/', views.showCars),
    path('color_ajax/', views.color_ajax),
    path('year_ajax/', views.year_ajax),
    path('model_ajax/', views.model_ajax),
    path('km_ajax/', views.km_ajax),
    path('price_ajax/', views.price_ajax),
    path('send_ajax/', views.send_ajax),
]
