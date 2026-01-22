from django.db import models
from PIL import Image, ImageDraw, ImageFont
import os
import urllib.parse
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    # Ejemplo: 'Ramos', 'Cajas de Rosas', 'Funerarios'
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class ArregloFloral(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='arreglos/')
    
    # Campos específicos para "Bajo Pedido"
    tiempo_preparacion = models.CharField(max_length=100, help_text="Ej: 24 horas de anticipación")
    disponible = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 1. Guardamos la imagen original primero
        super().save(*args, **kwargs)
        
        if self.imagen:
            # 2. Construimos la ruta al logo usando BASE_DIR
            # Asegúrate de guardar la imagen transparente que te envié como: static/img/logo_watermark.png
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_watermark.png')
            
            if os.path.exists(logo_path):
                img = Image.open(self.imagen.path).convert("RGBA")
                logo = Image.open(logo_path).convert("RGBA")

                # 3. Ajustar tamaño del logo (proporcional al 20% del ancho de la imagen)
                ancho_logo = int(img.width * 0.20)
                logo.thumbnail((ancho_logo, ancho_logo))

                # 4. Posición: Esquina inferior derecha
                posicion = (img.width - logo.width - 25, img.height - logo.height - 25)

                # 5. Pegar logo usando el canal alfa (transparencia) como máscara
                img.paste(logo, posicion, logo)

                # 6. Guardar reemplazando la imagen (convertimos a RGB para JPG)
                img.convert("RGB").save(self.imagen.path, quality=90)
            else:
                print(f"DEBUG: No se encontró el logo en {logo_path}")

    def __str__(self):
        return self.nombre

    @property
    def whatsapp_link(self):
        telefono = "593999254571"  # Número de tu mamá
        mensaje = f"¡Hola! Vi el arreglo *{self.nombre}* en la página web y me gustaría pedir uno. 🌸"
        # Codificamos el mensaje para que sea seguro en una URL
        mensaje_url = urllib.parse.quote(mensaje)
        return f"https://wa.me/{telefono}?text={mensaje_url}"