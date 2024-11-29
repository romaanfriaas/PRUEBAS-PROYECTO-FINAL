from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    # Actualizamos esta ruta para que acepte el parámetro `page`
    path('home/', views.home, name='home'),
    path('home/<int:page>/', views.home, name='home_page'),  # Nueva ruta para manejar páginas específicas
    path('buscar/', views.search, name='buscar'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
]
