import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.ganado.models import Especie, Raza, TipoPasto

# ----------------------------------------------------------
# 1. Actualizar / Crear Especies (con descripciones)
# ----------------------------------------------------------
especies_data = [
    {
        'nombre': 'Bovino',
        'descripcion': 'Ganado vacuno. Incluye razas para producción de carne, leche y doble propósito. Es la especie más común en hatos ganaderos.'
    },
    {
        'nombre': 'Bufalino',
        'descripcion': 'Ganado bubalino. Ideal para zonas tropicales y pantanosas. Produce carne magra y leche con alto contenido de grasa.'
    },
    {
        'nombre': 'Equino',
        'descripcion': 'Ganado caballar. Utilizado principalmente para trabajo de campo, cría y deportes ecuestres.'
    },
    {
        'nombre': 'Ovino',
        'descripcion': 'Ganado lanar. Criado por su lana, carne y leche. Muy resistente a condiciones climáticas adversas.'
    },
    {
        'nombre': 'Caprino',
        'descripcion': 'Ganado cabrío. Excelente para terrenos montañosos y secos. Produce leche de alta calidad y carne magra.'
    },
    {
        'nombre': 'Porcino',
        'descripcion': 'Ganado porcino. Criado principalmente para la producción de carne, con ciclos de engorde rápidos y alta eficiencia.'
    },
]

for item in especies_data:
    especie, created = Especie.objects.get_or_create(
        nombre=item['nombre'],
        defaults={'descripcion': item['descripcion']}
    )
    # Si ya existía, pero no tenía descripción, se la agregamos
    if not created and not especie.descripcion:
        especie.descripcion = item['descripcion']
        especie.save()
        print(f"✏️ Especie actualizada: {item['nombre']} - Se agregó descripción")
    elif created:
        print(f"✅ Especie creada: {item['nombre']}")
    else:
        print(f"ℹ️ Especie ya existía y tiene descripción: {item['nombre']}")

# ----------------------------------------------------------
# 2. Actualizar / Crear Razas (con descripciones)
# ----------------------------------------------------------
razas_data = [
    # Bovinos
    {
        'nombre': 'Brahman',
        'especie': 'Bovino',
        'descripcion': 'Raza cebuína de origen indio. Adaptada al trópico. Extremadamente resistente al calor y a los parásitos. Excelente para carne.'
    },
    {
        'nombre': 'Holstein',
        'especie': 'Bovino',
        'descripcion': 'Raza lechera por excelencia. Originaria de los Países Bajos y Alemania. La más productiva en producción de leche a nivel mundial.'
    },
    {
        'nombre': 'Pardo Suizo',
        'especie': 'Bovino',
        'descripcion': 'Raza de doble propósito (carne y leche). Muy rústica y versátil. Originaria de Suiza. Buena adaptabilidad a diversos climas.'
    },
    {
        'nombre': 'Hereford',
        'especie': 'Bovino',
        'descripcion': 'Raza británica especializada en la producción de carne. Reconocida por su rusticidad y por su color blanco en la cabeza y vientre.'
    },
    {
        'nombre': 'Criollo',
        'especie': 'Bovino',
        'descripcion': 'Raza autóctona de América Latina. Muy resistente y adaptada a las condiciones locales. De gran longevidad y fertilidad.'
    },
    # Bufalinos
    {
        'nombre': 'Murrah',
        'especie': 'Bufalino',
        'descripcion': 'Raza de búfalo de agua originaria de la India. Excelente para producción de leche. Muy resistente al calor.'
    },
    {
        'nombre': 'Jafarabadi',
        'especie': 'Bufalino',
        'descripcion': 'Raza pesada de búfalo de agua. Ideal para trabajo pesado y producción de carne. Originaria de la India.'
    },
    # Equinos
    {
        'nombre': 'Paso Fino',
        'especie': 'Equino',
        'descripcion': 'Raza equina originaria de Puerto Rico y Colombia. Su principal característica es su paso suave y elegante, ideal para cabalgatas.'
    },
    {
        'nombre': 'Criollo',
        'especie': 'Equino',
        'descripcion': 'Caballo criollo latinoamericano. Muy fuerte y resistente. Perfecto para el trabajo de campo y el arreo de ganado.'
    },
    # Ovinos
    {
        'nombre': 'Dorper',
        'especie': 'Ovino',
        'descripcion': 'Raza ovina sudafricana de carne. Muy fértil y resistente. Se adapta bien a climas secos y produce una canal de alta calidad.'
    },
    {
        'nombre': 'Pelibuey',
        'especie': 'Ovino',
        'descripcion': 'Oveja de pelo originaria de Cuba y México. No necesita esquila, ya que no produce lana. Muy resistente al calor.'
    },
]

for item in razas_data:
    try:
        especie_obj = Especie.objects.get(nombre=item['especie'])
        raza, created = Raza.objects.get_or_create(
            nombre=item['nombre'],
            especie=especie_obj,
            defaults={'descripcion': item['descripcion']}
        )
        # Si ya existía, pero no tenía descripción, se la agregamos
        if not created and not raza.descripcion:
            raza.descripcion = item['descripcion']
            raza.save()
            print(f"✏️ Raza actualizada: {item['nombre']} ({item['especie']}) - Se agregó descripción")
        elif created:
            print(f"✅ Raza creada: {item['nombre']} ({item['especie']})")
        else:
            print(f"ℹ️ Raza ya existía y tiene descripción: {item['nombre']}")
    except Especie.DoesNotExist:
        print(f"❌ ERROR: La especie '{item['especie']}' no existe. No se pudo crear '{item['nombre']}'")

# ----------------------------------------------------------
# 3. Actualizar / Crear Tipos de Pasto (con descripciones)
# ----------------------------------------------------------
pastos_data = [
    {
        'nombre': 'Brachiaria',
        'descripcion': 'Género de pasto tropical de alto rendimiento. Muy utilizado en América Latina por su resistencia a la sequía y alto valor nutricional.'
    },
    {
        'nombre': 'Elefante',
        'descripcion': 'Pasto de corte de alta producción. Recomendado para sistemas de pastoreo intensivo y para la alimentación de ganado de alta producción.'
    },
    {
        'nombre': 'Estrella',
        'descripcion': 'Pasto rastrero de crecimiento rápido. Ideal para terrenos húmedos y de ladera. Muy apetecible para el ganado.'
    },
    {
        'nombre': 'Guinea',
        'descripcion': 'Pasto cespitoso de altura. Muy común en zonas tropicales. Ofrece una buena palatabilidad y una alta producción de forraje.'
    },
    {
        'nombre': 'Pangola',
        'descripcion': 'Pasto rastrero de textura suave. Muy apreciado por su valor nutricional y su capacidad para rebrotar después del pastoreo.'
    },
    {
        'nombre': 'Kudzú',
        'descripcion': 'Leguminosa forrajera trepadora de alto valor proteico. Excelente para mezclas con pastos y para mejorar la fertilidad del suelo.'
    },
    {
        'nombre': 'Alfalfa',
        'descripcion': 'Leguminosa forrajera de alta calidad. Conocida como la "reina de los forrajes". Ideal para la alimentación de ganado de alto rendimiento.'
    },
    {
        'nombre': 'Pasto de corte',
        'descripcion': 'Pastos de alta producción cultivados en sistemas de corte y acarreo, como el Pasto Elefante o el Pasto Camerún. Básico para la ganadería.'
    },
]

for item in pastos_data:
    pasto, created = TipoPasto.objects.get_or_create(
        nombre=item['nombre'],
        defaults={'descripcion': item['descripcion']}
    )
    # Si ya existía, pero no tenía descripción, se la agregamos
    if not created and not pasto.descripcion:
        pasto.descripcion = item['descripcion']
        pasto.save()
        print(f"✏️ Pasto actualizado: {item['nombre']} - Se agregó descripción")
    elif created:
        print(f"✅ Pasto creado: {item['nombre']}")
    else:
        print(f"ℹ️ Pasto ya existía y tiene descripción: {item['nombre']}")

print("\n🎉 ¡Actualización de datos completada! (Sin duplicados y con descripciones agregadas)")