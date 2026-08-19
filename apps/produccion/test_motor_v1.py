"""Pruebas unitarias del Motor de Métricas Hato V1."""
import unittest
from datetime import date
from decimal import Decimal
from apps.produccion.engine.catalogo_v1 import obtener_metrica_v1
from apps.produccion.engine.ejecutor import EjecutorMotorV1

class MockPesaje:
    def __init__(self,peso_kg,fecha): self.peso_kg=Decimal(str(peso_kg)); self.fecha=fecha
class MockAnimal:
    def __init__(self,numero_arete,sexo="H",estado="activo",pesajes=None): self.numero_arete=numero_arete; self.sexo=sexo; self.estado=estado; self._pesajes=pesajes or []
    @property
    def pesajes(self):
        items=self._pesajes
        class MockQuerySet:
            def __init__(self,items): self._items=items
            def order_by(self,field):
                rev=field.startswith("-"); f=field.lstrip("-"); return MockQuerySet(sorted(self._items,key=lambda x:getattr(x,f),reverse=rev))
            def first(self): return self._items[0] if self._items else None
            def __getitem__(self,value): return self._items[value]
        return MockQuerySet(items)

class TestMotorMetricasV1(unittest.TestCase):
    def setUp(self):
        self.ejecutor=EjecutorMotorV1()
        self.animales=[
            MockAnimal("H001","H","activo",[MockPesaje("200",date(2026,6,1))]),MockAnimal("H002","H","activo",[MockPesaje("300",date(2026,6,1))]),MockAnimal("H003","H","activo",[MockPesaje("400",date(2026,6,1))]),
            MockAnimal("H004","H","activo"),MockAnimal("H005","H","activo"),MockAnimal("H006","H","activo"),MockAnimal("H007","H","vendido",[MockPesaje("800",date(2026,6,1))]),
            MockAnimal("M001","M","activo"),MockAnimal("M002","M","activo"),MockAnimal("M003","M","activo"),MockAnimal("M004","M","activo"),MockAnimal("M005","M","muerto",[MockPesaje("900",date(2026,6,1))]),
        ]
    def test_01_cant_animales_total(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("CANT_ANIMALES_TOTAL"),self.animales); self.assertTrue(r.es_valido); self.assertEqual(r.valor,12)
    def test_02_cant_animales_activos(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("CANT_ANIMALES_ACTIVOS"),self.animales); self.assertTrue(r.es_valido); self.assertEqual(r.valor,10)
    def test_03_animales_por_sexo(self):
        m=obtener_metrica_v1("ANIMALES_POR_SEXO"); self.assertEqual(self.ejecutor.ejecutar(m,self.animales,{"sexo":"H"}).valor,7); self.assertEqual(self.ejecutor.ejecutar(m,self.animales,{"sexo":"M"}).valor,5)
    def test_04_peso_promedio_finca(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("PESO_PROMEDIO_FINCA"),self.animales); self.assertTrue(r.es_valido); self.assertEqual(r.valor,Decimal("300.00"))
    def test_05_peso_total_finca(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("PESO_TOTAL_FINCA"),self.animales); self.assertTrue(r.es_valido); self.assertEqual(r.valor,Decimal("900.00"))
    def test_06_gmd_individual(self):
        a=MockAnimal("A001",pesajes=[MockPesaje("225",date(2026,7,1)),MockPesaje("200",date(2026,6,1))]); r=self.ejecutor.ejecutar(obtener_metrica_v1("GMD_INDIVIDUAL"),a); self.assertTrue(r.es_valido); self.assertEqual(r.valor,Decimal("0.833"))
    def test_07_sup_total_potreros(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("SUP_TOTAL_POTREROS"),[Decimal("10.50"),Decimal("20.00"),Decimal("15.25")]); self.assertTrue(r.es_valido); self.assertEqual(r.valor,Decimal("45.75"))
    def test_08_carga_animal_ha(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("CARGA_ANIMAL_HA"),{"animales":12,"hectareas":Decimal("45.75")}); self.assertTrue(r.es_valido); self.assertEqual(r.valor,Decimal("0.26"))
    def test_09_finca_vacia(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("CANT_ANIMALES_TOTAL"),[]); self.assertTrue(r.es_valido); self.assertEqual(r.valor,0)
    def test_10_gmd_insuficientes(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("GMD_INDIVIDUAL"),MockAnimal("SOLO1",pesajes=[MockPesaje("200",date(2026,6,1))])); self.assertFalse(r.es_valido); self.assertIn("requiere al menos 2 pesajes",r.error)
    def test_11_gmd_mismo_dia(self):
        a=MockAnimal("MISMO_DIA",pesajes=[MockPesaje("205",date(2026,6,1)),MockPesaje("200",date(2026,6,1))]); r=self.ejecutor.ejecutar(obtener_metrica_v1("GMD_INDIVIDUAL"),a); self.assertFalse(r.es_valido); self.assertIn("Intervalo de fechas inválido",r.error)
    def test_12_promedio_sin_pesajes(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("PESO_PROMEDIO_FINCA"),[MockAnimal("S1"),MockAnimal("S2")]); self.assertFalse(r.es_valido); self.assertIn("No existen valores para calcular el promedio",r.error)
    def test_13_carga_cero_hectareas(self):
        r=self.ejecutor.ejecutar(obtener_metrica_v1("CARGA_ANIMAL_HA"),{"animales":10,"hectareas":0}); self.assertFalse(r.es_valido); self.assertIn("no puede ser menor o igual a cero",r.error)

if __name__ == "__main__": unittest.main()
