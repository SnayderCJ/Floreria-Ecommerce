from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import ArregloForm, CategoriaForm
from .models import ArregloFloral, Categoria

# --- VISTAS PÚBLICAS ---

def error_404(request, exception):
    return render(request, 'pages/404.html', status=404)

def index(request):
    recientes = ArregloFloral.objects.filter(disponible=True).order_by('-id')[:4]
    return render(request, 'pages/index.html', {'recientes': recientes})

def catalogo(request):
    categorias = Categoria.objects.all()
    productos = ArregloFloral.objects.filter(disponible=True)
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
        
    return render(request, 'pages/catalogo.html', {
        'productos': productos,
        'categorias': categorias
    })

def detalle_arreglo(request, pk):
    arreglo = get_object_or_404(ArregloFloral, pk=pk)
    return render(request, 'pages/detalle.html', {'arreglo': arreglo})

# --- VISTAS ADMINISTRATIVAS: ARREGLOS (CRUD) ---

@staff_member_required
def gestionar_inventario(request):
    productos = ArregloFloral.objects.all().order_by('-id')
    return render(request, 'pages/inventario.html', {'productos': productos})

@staff_member_required
def subir_arreglo(request):
    if request.method == 'POST':
        form = ArregloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Arreglo publicado con éxito!")
            return redirect('gestionar_inventario')
    else:
        form = ArregloForm()
    return render(request, 'pages/subir.html', {'form': form, 'titulo': 'Subir Nuevo Arreglo'})

@staff_member_required
def editar_arreglo(request, pk):
    arreglo = get_object_or_404(ArregloFloral, pk=pk)
    if request.method == 'POST':
        form = ArregloForm(request.POST, request.FILES, instance=arreglo)
        if form.is_valid():
            form.save()
            messages.success(request, f"El arreglo '{arreglo.nombre}' ha sido actualizado.")
            return redirect('gestionar_inventario')
    else:
        form = ArregloForm(instance=arreglo)
    
    return render(request, 'pages/subir.html', {
        'form': form, 
        'editando': True, 
        'titulo': f'Editando: {arreglo.nombre}'
    })

@staff_member_required
def eliminar_arreglo(request, pk):
    arreglo = get_object_or_404(ArregloFloral, pk=pk)
    if request.method == 'POST':
        nombre = arreglo.nombre
        arreglo.delete()
        messages.warning(request, f"Se ha eliminado el arreglo: {nombre}")
        return redirect('gestionar_inventario')
    return render(request, 'pages/confirmar_eliminacion.html', {'arreglo': arreglo})

# --- VISTAS ADMINISTRATIVAS: CATEGORÍAS (CRUD) ---

@staff_member_required
def gestionar_categorias(request):
    """Lista todas las categorías para editar o borrar"""
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'pages/gestionar_categorias.html', {'categorias': categorias})

@staff_member_required
def crear_categoria(request):
    """Crea una nueva categoría y redirige al formulario de subida"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Nueva categoría creada correctamente!")
            return redirect('subir_arreglo')
    else:
        form = CategoriaForm()
    return render(request, 'pages/crear_categoria.html', {'form': form, 'titulo': 'Crear Categoría'})

@staff_member_required
def editar_categoria(request, pk):
    """Edita el nombre de una categoría existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría '{categoria.nombre}' actualizada.")
            return redirect('gestionar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'pages/crear_categoria.html', {
        'form': form, 
        'editando': True, 
        'titulo': f'Editando Categoría: {categoria.nombre}'
    })

@staff_member_required
def eliminar_categoria(request, pk):
    """Confirma y elimina una categoría"""
    categoria = get_object_or_404(Categoria, pk=pk)
    # Verificamos si hay productos vinculados
    tiene_productos = ArregloFloral.objects.filter(categoria=categoria).exists()
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.warning(request, f"Categoría '{nombre}' eliminada.")
        return redirect('gestionar_categorias')
    
    return render(request, 'pages/confirmar_eliminar_categoria.html', {
        'categoria': categoria,
        'tiene_productos': tiene_productos
    })