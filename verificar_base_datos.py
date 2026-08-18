import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.core.models import Finca, Potrero
from apps.ganado.models import (
    Especie, Raza, TipoPasto, Animal, MovimientoAnimal, 
    EventoSalud, PesajeAnimal
)

print("\n" + "="*60)
print("📊 INVENTARIO ACTUAL DE LA BASE DE DATOS")
print("="*60)

# ============================================================
# 1. CATÁLOGOS BÁSICOS
# ============================================================
print("\n🔹 CATÁLOGOS BÁSICOS")
especies = Especie.objects.all()
print(f"  • Especies: {especies.count()}")
for e in especies:
    print(f"      - {e.nombre} (ID: {e.id})")

razas = Raza.objects.all()
print(f"  • Razas: {razas.count()}")
for r in razas:
    print(f"      - {r.nombre} (Especie: {r.especie.nombre})")

pastos = TipoPasto.objects.all()
print(f"  • Tipos de Pasto: {pastos.count()}")
for p in pastos:
    print(f"      - {p.nombre}")

# ============================================================
# 2. FINCAS Y POTREROS
# ============================================================
print("\n🔹 FINCAS Y POTREROS")
fincas = Finca.objects.all()
print(f"  • Fincas: {fincas.count()}")
for f in fincas:
    print(f"      - {f.nombre} (ID: {f.id})")
    potreros_finca = Potrero.objects.filter(finca=f)
    print(f"          Potreros: {potreros_finca.count()}")
    for p in potreros_finca[:3]:  # Mostrar solo los primeros 3 para no saturar
        print(f"              - {p.nombre} (Capacidad: {p.capacidad_animales})")
    if potreros_finca.count() > 3:
        print(f"              ... y {potreros_finca.count() - 3} más")

# ============================================================
# 3. ANIMALES
# ============================================================
print("\n🔹 ANIMALES")
animales = Animal.objects.all()
print(f"  • Total de animales: {animales.count()}")
if animales.count() > 0:
    print(f"  • Animales activos: {animales.filter(estado='activo').count()}")
    print(f"  • Animales vendidos: {animales.filter(estado='vendido').count()}")
    
    # Distribución por sexo
    machos = animales.filter(sexo='M').count()
    hembras = animales.filter(sexo='H').count()
    print(f"  • Machos: {machos} | Hembras: {hembras}")

# ============================================================
# 4. MOVIMIENTOS
# ============================================================
print("\n🔹 MOVIMIENTOS")
movimientos = MovimientoAnimal.objects.all()
print(f"  • Total de movimientos registrados: {movimientos.count()}")
activos = movimientos.filter(activo=True).count()
print(f"  • Movimientos activos (animales en potrero): {activos}")

# ============================================================
# 5. SALUD
# ============================================================
print("\n🔹 EVENTOS DE SALUD")
eventos = EventoSalud.objects.all()
print(f"  • Eventos de salud registrados: {eventos.count()}")
if eventos.count() > 0:
    vacunas = eventos.filter(tipo='vacunacion').count()
    desparasitaciones = eventos.filter(tipo='desparasitacion').count()
    print(f"      - Vacunas: {vacunas}")
    print(f"      - Desparasitaciones: {desparasitaciones}")

# ============================================================
# 6. PESAJES
# ============================================================
print("\n🔹 PESAJES")
pesajes = PesajeAnimal.objects.all()
print(f"  • Pesajes registrados: {pesajes.count()}")

print("\n" + "="*60)
print("✅ INVENTARIO COMPLETADO")
print("="*60)