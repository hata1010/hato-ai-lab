import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.core.models import Finca, Potrero
from apps.ganado.models import Animal, MovimientoAnimal, EventoSalud, PesajeAnimal

# ============================================================
# 1. Identificar la finca original (NO la borramos)
# ============================================================
coromoto = Finca.objects.filter(nombre='Hato  La Coromoto').first()
if not coromoto:
    print("❌ No se encontró 'Hato La Coromoto'. Abortando.")
    exit()

# Fincas de prueba (todas las que NO son la original)
fincas_prueba = Finca.objects.exclude(id=coromoto.id)

print(f"🔹 Limpiando TODOS los datos de las fincas de prueba: {', '.join([f.nombre for f in fincas_prueba])}")

# ============================================================
# 2. Limpiar en orden inverso (para evitar errores de FK)
# ============================================================

print("  ⏳ Eliminando pesajes...")
pesajes_eliminados = PesajeAnimal.objects.filter(animal__finca__in=fincas_prueba).delete()[0]
print(f"    ✅ Eliminados {pesajes_eliminados} pesajes")

print("  ⏳ Eliminando eventos de salud...")
eventos_eliminados = EventoSalud.objects.filter(animal__finca__in=fincas_prueba).delete()[0]
print(f"    ✅ Eliminados {eventos_eliminados} eventos de salud")

print("  ⏳ Eliminando movimientos...")
movimientos_eliminados = MovimientoAnimal.objects.filter(animal__finca__in=fincas_prueba).delete()[0]
print(f"    ✅ Eliminados {movimientos_eliminados} movimientos")

print("  ⏳ Eliminando animales...")
animales_eliminados = Animal.objects.filter(finca__in=fincas_prueba).delete()[0]
print(f"    ✅ Eliminados {animales_eliminados} animales")

print("  ⏳ Eliminando potreros...")
potreros_eliminados = Potrero.objects.filter(finca__in=fincas_prueba).delete()[0]
print(f"    ✅ Eliminados {potreros_eliminados} potreros")

print("  ⏳ Eliminando fincas de prueba...")
fincas_eliminadas = fincas_prueba.delete()[0]
print(f"    ✅ Eliminadas {fincas_eliminadas} fincas de prueba")

print("\n🎉 LIMPIEZA TOTAL COMPLETADA!")
print(f"✅ La finca original 'Hato La Coromoto' (ID {coromoto.id}) quedó completamente intacta.")