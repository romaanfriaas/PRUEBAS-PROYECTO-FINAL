# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.

def home(request):
    # Obtener la página actual y el texto de búsqueda
    page = int(request.GET.get('page', 1))  # Por defecto la página es 1
    search_msg = request.GET.get('query', '').strip()

    if not search_msg:
        search_msg = None  # Si no hay texto de búsqueda, traer todos los personajes
    
    # Obtener imágenes de la API y total de páginas disponibles
    images, total_pages = getAllImages(page=page, input=search_msg)

    favourite_list = []  # Aquí puedes agregar lógica para favoritos si lo necesitas

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list,
        'total_pages': total_pages,
        'current_page': page
    })

def search(request):
    search_msg = request.POST.get('query', '').strip()  # Limpia el texto ingresado

    if not search_msg:
        # Si no se ingresa texto, muestra todas las imágenes
        return redirect('home')

    # Filtra las imágenes basándote en el texto ingresado
    images = getAllImages(input=search_msg)
    favourite_list = []  # Implementa favoritos si es necesario

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

import requests

def getAllImages(page=1, input=None):
    # Construir la URL con la página incluida
    url = f"https://rickandmortyapi.com/api/character/?page={page}"
    if input:
        url += f"&name={input}"  # Si se pasa una búsqueda, añadimos el parámetro 'name'
    
    response = requests.get(url)
    if response.status_code != 200:
        return []  # Manejo de error
    data = response.json()
    print(data)  # Verifica qué datos estás obteniendo desde la API
    characters = data.get('results', [])
    cards = []
    for character in characters:
        cards.append({
            'id': character['id'],
            'name': character['name'],
            'image': character['image'],
            'status': character['status'],
            'location': character['location']['name'],
            'episode': character['episode'][0].split("/")[-1]
        })
    return cards

# Estas funciones se usan cuando el usuario está logueado en la aplicación.

# Manejo de inicio de sesión
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'index.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'index.html')

# Cerrar sesión
@login_required
def logout_user(request):
    logout(request)
    return redirect('index')

# Obtener favoritos del usuario
@login_required
def getAllFavouritesByUser(request):
    return list(request.user.favourites.values())  # Esto asume un modelo relacionado con el usuario

# Guardar favorito
@login_required
def saveFavourite(request):
    if request.method == 'POST':
        image_id = request.POST.get('id')
        if image_id:
            request.user.favourites.create(image_id=image_id)  # Modelo de favoritos asociado
    return redirect('home')

# Eliminar favorito
@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        if fav_id:
            request.user.favourites.filter(id=fav_id).delete()
    return redirect('home')


