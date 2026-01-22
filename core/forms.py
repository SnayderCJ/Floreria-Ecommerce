from django import forms
from .models import ArregloFloral, Categoria

class ArregloForm(forms.ModelForm):
    class Meta:
        model = ArregloFloral
        fields = ['categoria', 'nombre', 'descripcion', 'precio_base', 'imagen', 'tiempo_preparacion']
        labels = {
            'categoria': '¿A qué categoría pertenece?',
            'precio_base': 'Precio (ej: 15.00)',
            'imagen': 'Selecciona la Foto',
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la nueva categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control border-2',
                'style': 'border-radius: 12px;',
                'placeholder': 'Ej: Edición Especial'
            })
        }