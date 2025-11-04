import os
import sys
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymarket.settings')
django.setup()

from productos.models import Producto

def descargar_imagen(url, nombre_archivo):
    """Descarga una imagen desde una URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content, name=nombre_archivo)
    except Exception as e:
        print(f"Error descargando imagen: {e}")
    return None

def populate_supermarket():
    """Crea productos de supermercado con imágenes, categorías y marcas"""
    
    productos_data = [
        # ALMACÉN
        {
            'nombre': 'Arroz Gallo Oro 1kg',
            'descripcion': 'Arroz largo fino de alta calidad, ideal para todo tipo de preparaciones.',
            'precio': 890.00,
            'stock': 100,
            'category': 'almacen',
            'marca': 'Gallo Oro',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400'
        },
        {
            'nombre': 'Fideos Matarazzo Tirabuzón 500g',
            'descripcion': 'Pasta de sémola de trigo candeal, cocción perfecta en 8 minutos.',
            'precio': 650.00,
            'stock': 150,
            'category': 'almacen',
            'marca': 'Matarazzo',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400'
        },
        {
            'nombre': 'Aceite Cocinero Girasol 1.5L',
            'descripcion': 'Aceite de girasol alto oleico, ideal para frituras y ensaladas.',
            'precio': 1250.00,
            'stock': 80,
            'category': 'almacen',
            'marca': 'Cocinero',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400'
        },
        {
            'nombre': 'Azúcar Ledesma 1kg',
            'descripcion': 'Azúcar blanca refinada, endulza tus comidas y bebidas.',
            'precio': 780.00,
            'stock': 120,
            'category': 'almacen',
            'marca': 'Ledesma',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1514568932909-faf3f8642ae2?w=400'
        },
        {
            'nombre': 'Café Nescafé Clásico 170g',
            'descripcion': 'Café instantáneo de grano seleccionado, sabor intenso.',
            'precio': 3200.00,
            'stock': 60,
            'category': 'desayuno',
            'marca': 'Nescafé',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400'
        },
        {
            'nombre': 'Harina 0000 Blancaflor 1kg',
            'descripcion': 'Harina leudante ideal para panes, tortas y masas.',
            'precio': 520.00,
            'stock': 200,
            'category': 'almacen',
            'marca': 'Blancaflor',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1628274877481-4c60f0a52135?w=400'
        },
        {
            'nombre': 'Sal Fina Celusal 500g',
            'descripcion': 'Sal fina de mesa, fortificada con yodo.',
            'precio': 280.00,
            'stock': 150,
            'category': 'almacen',
            'marca': 'Celusal',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1584949091550-c0693fa227d5?w=400'
        },
        {
            'nombre': 'Arvejas Arcor Lata 300g',
            'descripcion': 'Arvejas en conserva, listas para consumir.',
            'precio': 690.00,
            'stock': 90,
            'category': 'almacen',
            'marca': 'Arcor',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1589927986089-35812388d1f8?w=400'
        },
        
        # BEBIDAS
        {
            'nombre': 'Coca Cola 2.25L',
            'descripcion': 'Bebida cola sabor original, refrescante y gasificada.',
            'precio': 1450.00,
            'stock': 200,
            'category': 'bebidas',
            'marca': 'Coca Cola',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400'
        },
        {
            'nombre': 'Agua Villavicencio 2L',
            'descripcion': 'Agua mineral sin gas de manantial natural.',
            'precio': 680.00,
            'stock': 300,
            'category': 'bebidas',
            'marca': 'Villavicencio',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400'
        },
        {
            'nombre': 'Quilmes Clásica Six Pack 410ml',
            'descripcion': 'Cerveza rubia lager argentina, pack x6 latas.',
            'precio': 3200.00,
            'stock': 80,
            'category': 'bebidas',
            'marca': 'Quilmes',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400'
        },
        {
            'nombre': 'Jugo Baggio Naranja 1L',
            'descripcion': 'Jugo concentrado de naranja, listo para tomar.',
            'precio': 890.00,
            'stock': 100,
            'category': 'bebidas',
            'marca': 'Baggio',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400'
        },
        {
            'nombre': 'Vino Toro Malbec 750ml',
            'descripcion': 'Vino tinto Malbec de Mendoza, cuerpo medio.',
            'precio': 2100.00,
            'stock': 50,
            'category': 'bebidas',
            'marca': 'Toro',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400'
        },
        
        # LÁCTEOS
        {
            'nombre': 'Leche La Serenísima Entera 1L',
            'descripcion': 'Leche entera pasteurizada, fuente de calcio.',
            'precio': 850.00,
            'stock': 150,
            'category': 'lacteos',
            'marca': 'La Serenísima',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400'
        },
        {
            'nombre': 'Yogur Ser Natural 190g',
            'descripcion': 'Yogur entero natural, cremoso y saludable.',
            'precio': 450.00,
            'stock': 120,
            'category': 'lacteos',
            'marca': 'Ser',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400'
        },
        {
            'nombre': 'Queso Cremoso La Paulina 500g',
            'descripcion': 'Queso cremoso untable, ideal para desayuno.',
            'precio': 2800.00,
            'stock': 60,
            'category': 'lacteos',
            'marca': 'La Paulina',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400'
        },
        {
            'nombre': 'Manteca La Serenísima 200g',
            'descripcion': 'Manteca sin sal, ideal para cocinar y untar.',
            'precio': 1350.00,
            'stock': 80,
            'category': 'lacteos',
            'marca': 'La Serenísima',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=400'
        },
        
        # CARNES Y PESCADOS
        {
            'nombre': 'Carne Molida Común kg',
            'descripcion': 'Carne vacuna molida especial, fresca del día.',
            'precio': 3500.00,
            'stock': 50,
            'category': 'carnes',
            'marca': 'Carnicería Fresca',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=400'
        },
        {
            'nombre': 'Pollo Entero Granja del Sol kg',
            'descripcion': 'Pollo fresco de granja, alimentación natural.',
            'precio': 2200.00,
            'stock': 40,
            'category': 'carnes',
            'marca': 'Granja del Sol',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=400'
        },
        {
            'nombre': 'Milanesas de Carne Paty kg',
            'descripcion': 'Milanesas de carne vacuna rebozadas.',
            'precio': 4200.00,
            'stock': 35,
            'category': 'carnes',
            'marca': 'Paty',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400'
        },
        {
            'nombre': 'Atún La Campagnola Lata 170g',
            'descripcion': 'Atún al natural en aceite, rico en omega 3.',
            'precio': 1450.00,
            'stock': 100,
            'category': 'carnes',
            'marca': 'La Campagnola',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=400'
        },
        
        # FRUTAS Y VERDURAS
        {
            'nombre': 'Manzana Roja kg',
            'descripcion': 'Manzanas rojas frescas y jugosas.',
            'precio': 980.00,
            'stock': 200,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400'
        },
        {
            'nombre': 'Banana kg',
            'descripcion': 'Bananas amarillas, fuente natural de potasio.',
            'precio': 850.00,
            'stock': 150,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400'
        },
        {
            'nombre': 'Tomate Perita kg',
            'descripcion': 'Tomates peritas frescos, ideales para ensaladas.',
            'precio': 1200.00,
            'stock': 120,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=400'
        },
        {
            'nombre': 'Papa Blanca kg',
            'descripcion': 'Papas blancas de primera calidad.',
            'precio': 650.00,
            'stock': 300,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400'
        },
        {
            'nombre': 'Lechuga Criolla',
            'descripcion': 'Lechuga criolla fresca y crocante.',
            'precio': 580.00,
            'stock': 80,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=400'
        },
        {
            'nombre': 'Cebolla kg',
            'descripcion': 'Cebollas frescas, ingrediente esencial.',
            'precio': 720.00,
            'stock': 200,
            'category': 'frutas',
            'marca': 'Verdulería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400'
        },
        
        # PANADERÍA
        {
            'nombre': 'Pan Francés',
            'descripcion': 'Pan francés tradicional, recién horneado.',
            'precio': 420.00,
            'stock': 100,
            'category': 'panaderia',
            'marca': 'Panadería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400'
        },
        {
            'nombre': 'Medialunas Dulces x6',
            'descripcion': 'Medialunas dulces glaseadas, pack x6 unidades.',
            'precio': 1200.00,
            'stock': 60,
            'category': 'panaderia',
            'marca': 'Panadería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400'
        },
        {
            'nombre': 'Facturas Surtidas x12',
            'descripcion': 'Docena de facturas variadas, dulces y pasteleras.',
            'precio': 2800.00,
            'stock': 40,
            'category': 'panaderia',
            'marca': 'Panadería',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=400'
        },
        
        # LIMPIEZA
        {
            'nombre': 'Detergente Magistral Limón 500ml',
            'descripcion': 'Detergente líquido concentrado para vajilla.',
            'precio': 980.00,
            'stock': 100,
            'category': 'limpieza',
            'marca': 'Magistral',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400'
        },
        {
            'nombre': 'Lavandina Ayudín 2L',
            'descripcion': 'Lavandina concentrada, desinfecta y blanquea.',
            'precio': 850.00,
            'stock': 80,
            'category': 'limpieza',
            'marca': 'Ayudín',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1585421514738-01798e348b17?w=400'
        },
        {
            'nombre': 'Jabón Polvo Skip 800g',
            'descripcion': 'Jabón en polvo para ropa, acción profunda.',
            'precio': 2200.00,
            'stock': 70,
            'category': 'limpieza',
            'marca': 'Skip',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=400'
        },
        {
            'nombre': 'Limpiador CIF Cremoso 500ml',
            'descripcion': 'Limpiador multiuso cremoso, elimina manchas.',
            'precio': 1350.00,
            'stock': 90,
            'category': 'limpieza',
            'marca': 'CIF',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=400'
        },
        
        # HIGIENE PERSONAL
        {
            'nombre': 'Shampoo Sedal 340ml',
            'descripcion': 'Shampoo nutritivo para todo tipo de cabello.',
            'precio': 1450.00,
            'stock': 80,
            'category': 'higiene',
            'marca': 'Sedal',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=400'
        },
        {
            'nombre': 'Jabón Dove Original 90g',
            'descripcion': 'Jabón en barra con crema humectante.',
            'precio': 680.00,
            'stock': 120,
            'category': 'higiene',
            'marca': 'Dove',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1622540493633-e7f820f8548c?w=400'
        },
        {
            'nombre': 'Pasta Dental Colgate Triple Acción 90g',
            'descripcion': 'Pasta dental con protección anticaries.',
            'precio': 950.00,
            'stock': 100,
            'category': 'higiene',
            'marca': 'Colgate',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1622577975474-8c8def94de4d?w=400'
        },
        {
            'nombre': 'Papel Higiénico Elite x4 Rollos',
            'descripcion': 'Papel higiénico doble hoja, extra suave.',
            'precio': 1200.00,
            'stock': 150,
            'category': 'higiene',
            'marca': 'Elite',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1584305574647-0cc949a2bb9f?w=400'
        },
        {
            'nombre': 'Desodorante Rexona Roll-On 50ml',
            'descripcion': 'Desodorante roll-on 48hs de protección.',
            'precio': 1650.00,
            'stock': 70,
            'category': 'higiene',
            'marca': 'Rexona',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1619451334792-150fd785ee74?w=400'
        },
        
        # SNACKS Y GOLOSINAS
        {
            'nombre': 'Galletitas Oreo 118g',
            'descripcion': 'Galletas de chocolate con crema vainilla.',
            'precio': 890.00,
            'stock': 100,
            'category': 'snacks',
            'marca': 'Oreo',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1606312619070-d48b4f0d2e5c?w=400'
        },
        {
            'nombre': 'Alfajor Jorgito x6',
            'descripcion': 'Alfajores de chocolate con dulce de leche.',
            'precio': 1450.00,
            'stock': 80,
            'category': 'snacks',
            'marca': 'Jorgito',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1625869016774-3a92be2ae2cd?w=400'
        },
        {
            'nombre': 'Chocolate Milka 100g',
            'descripcion': 'Chocolate con leche alpina suizo.',
            'precio': 1850.00,
            'stock': 60,
            'category': 'snacks',
            'marca': 'Milka',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400'
        },
        {
            'nombre': 'Papas Fritas Lays 150g',
            'descripcion': 'Papas fritas clásicas sabor original.',
            'precio': 1250.00,
            'stock': 90,
            'category': 'snacks',
            'marca': 'Lays',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400'
        },
        {
            'nombre': 'Caramelos Sugus x150g',
            'descripcion': 'Caramelos masticables sabores surtidos.',
            'precio': 780.00,
            'stock': 120,
            'category': 'snacks',
            'marca': 'Sugus',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=400'
        },
        {
            'nombre': 'Galletitas Pepitos 120g',
            'descripcion': 'Galletas con chips de chocolate.',
            'precio': 850.00,
            'stock': 100,
            'category': 'snacks',
            'marca': 'Bagley',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400'
        },
        
        # CONGELADOS
        {
            'nombre': 'Helado Frigor Dulce de Leche 1kg',
            'descripcion': 'Helado cremoso sabor dulce de leche.',
            'precio': 3200.00,
            'stock': 40,
            'category': 'congelados',
            'marca': 'Frigor',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400'
        },
        {
            'nombre': 'Pizza Muzza Sibarita',
            'descripcion': 'Pizza muzzarella congelada, lista para hornear.',
            'precio': 2400.00,
            'stock': 50,
            'category': 'congelados',
            'marca': 'Sibarita',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400'
        },
        {
            'nombre': 'Hamburguesas Paty x4',
            'descripcion': 'Medallones de carne congelados x4 unidades.',
            'precio': 1850.00,
            'stock': 60,
            'category': 'congelados',
            'marca': 'Paty',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'
        },
        {
            'nombre': 'Papas McCain Pre-Fritas 720g',
            'descripcion': 'Papas pre-fritas congeladas, listas para freír.',
            'precio': 1680.00,
            'stock': 70,
            'category': 'congelados',
            'marca': 'McCain',
            'condition': 'new',
            'imagen_url': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400'
        },
    ]
    
    print("Iniciando creación de productos...")
    print(f"Total de productos a crear: {len(productos_data)}\n")
    
    # PRIMERO: ELIMINAR TODOS LOS PRODUCTOS EXISTENTES
    print("⚠️  ELIMINANDO productos existentes...")
    productos_eliminados = Producto.objects.all().delete()[0]
    print(f"✓ {productos_eliminados} productos eliminados\n")
    
    creados = 0
    errores = 0
    
    for data in productos_data:
        try:
            # Crear el producto
            producto = Producto(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                precio=data['precio'],
                stock=data['stock'],
                category=data['category'],
                marca=data['marca'],
                condition=data['condition']
            )
            
            # Descargar y asignar la imagen
            if 'imagen_url' in data:
                imagen_content = descargar_imagen(
                    data['imagen_url'],
                    f"{data['nombre'].replace(' ', '_').lower()}.jpg"
                )
                if imagen_content:
                    producto.imagen = imagen_content
            
            producto.save()
            print(f"✓ Creado: {data['nombre']} - ${data['precio']} ({data['category']}) - {data['marca']}")
            creados += 1
            
        except Exception as e:
            print(f"✗ Error creando {data['nombre']}: {str(e)}")
            errores += 1
    
    print("\n" + "="*60)
    print("RESUMEN:")
    print(f"✓ Productos creados: {creados}")
    print(f"✗ Errores: {errores}")
    print(f"📦 Total en base de datos: {Producto.objects.count()}")
    print("="*60)

if __name__ == '__main__':
    print("🛒 SCRIPT DE POBLACIÓN DE SUPERMERCADO")
    print("="*60)
    
    respuesta = input("⚠️  ESTO ELIMINARÁ TODOS LOS PRODUCTOS EXISTENTES. ¿Continuar? (s/n): ")
    if respuesta.lower() == 's':
        populate_supermarket()
    else:
        print("Operación cancelada.")