import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.ganado.models import (
    Adquisicion,
    AdquisicionAnimal,
    DocumentoAnimal,
    Animal
)

# ============================================================
# 1. CREAR UN PROVEEDOR (ADQUISICIÓN)
# ============================================================

proveedor, created = Adquisicion.objects.get_or_create(
    proveedor="Ganadería El Rosario",
    fecha="2025-06-15",
    numero_documento="FAC-2025-00123",
    costo_total=12500.00,
    observaciones="Compra de 2 animales para cría."
)
if created:
    print(f"✅ Proveedor creado: {proveedor.proveedor}")
else:
    print(f"ℹ️ Proveedor ya existía: {proveedor.proveedor}")

# ============================================================
# 2. VINCULAR UN ANIMAL A ESA ADQUISICIÓN (OPCIONAL)
# ============================================================
# Nota: Para que esto funcione, DEBES tener al menos un Animal creado en el sistema.
# Si no tienes animales, comenta este bloque o ejecútalo después de crear tu primer animal.

try:
    # Intenta obtener el primer animal registrado
    animal_ejemplo = Animal.objects.first()
    
    if animal_ejemplo:
        vinculo, created = AdquisicionAnimal.objects.get_or_create(
            adquisicion=proveedor,
            animal=animal_ejemplo,
            precio_individual=6250.00,
            observaciones="Animal comprado para engorde."
        )
        if created:
            print(f"✅ Adquisición vinculada al animal: {animal_ejemplo.numero_arete}")
        else:
            print(f"ℹ️ Vínculo ya existía para {animal_ejemplo.numero_arete}")
    else:
        print("⚠️ No hay animales registrados. No se creó el vínculo.")

except Exception as e:
    print(f"⚠️ No se pudo vincular un animal: {e}")

# ============================================================
# 3. CREAR UN DOCUMENTO GENÉRICO (OPCIONAL)
# ============================================================

try:
    animal_ejemplo = Animal.objects.first()
    if animal_ejemplo:
        doc, created = DocumentoAnimal.objects.get_or_create(
            animal=animal_ejemplo,
            tipo="pedigree",
            numero_documento="PED-2025-001",
            fecha_documento="2025-06-15",
            observaciones="Certificado de pedigree del criador."
        )
        if created:
            print(f"✅ Documento creado para {animal_ejemplo.numero_arete}")
        else:
            print(f"ℹ️ Documento ya existía para {animal_ejemplo.numero_arete}")
    else:
        print("⚠️ No hay animales. No se creó el documento.")

except Exception as e:
    print(f"⚠️ No se pudo crear el documento: {e}")

print("\n🎉 ¡Carga de proveedores y documentos completada!")