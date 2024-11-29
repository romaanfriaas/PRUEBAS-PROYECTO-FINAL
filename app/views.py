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

def home(request, page=1):
    # Llamada a la API de Rick & Morty con el número de página
    images = getAllImages(page=page)

    # Hacer la solicitud a la API de Rick & Morty para obtener los datos
    response = requests.get(f"https://rickandmortyapi.com/api/character/?page={page}")
    data = response.json()
    info = data.get('info', {})

    # Generamos el rango de páginas con un máximo de 40 páginas
    total_pages = min(info['pages'], 40)

    # Aquí estamos limitando el rango a un máximo de 3 páginas alrededor de la página actual
    # Este rango de páginas será de 3 páginas alrededor de la página actual (page)
    if total_pages <= 3:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 2:
            page_range = range(1, 4)
        elif page >= total_pages - 1:
            page_range = range(total_pages - 2, total_pages + 1)
        else:
            page_range = range(page - 1, page + 2)

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': [],  # Si tienes favoritos, añade la lógica aquí
        'info': info,
        'page_range': page_range,
        'current_page': page  # Asegúrate de que se pase la página actual
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


