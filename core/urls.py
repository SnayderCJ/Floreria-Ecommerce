from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Manejador de error 404 personalizado
handler404 = 'core.views.error_404' # Asegúrate que 'core' sea el nombre de tu app

urlpatterns = [
    # --- PÁGINAS PRINCIPALES (PÚBLICO) ---
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('arreglo/<int:pk>/', views.detalle_arreglo, name='detalle'),
    
    # --- GESTIÓN DE ARREGLOS (CRUD ADMIN) ---
    path('subir/', views.subir_arreglo, name='subir_arreglo'),
    path('gestion/', views.gestionar_inventario, name='gestionar_inventario'),
    path('editar/<int:pk>/', views.editar_arreglo, name='editar_arreglo'),
    path('eliminar/<int:pk>/', views.eliminar_arreglo, name='eliminar_arreglo'),

    # --- GESTIÓN DE CATEGORÍAS (CRUD ADMIN) ---
    path('categorias/gestion/', views.gestionar_categorias, name='gestionar_categorias'),
    path('categoria/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),

    # --- AUTENTICACIÓN ---
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Configuración para servir archivos multimedia y estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)