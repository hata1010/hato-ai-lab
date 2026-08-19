"""Estructura de definición para el catálogo de métricas V1."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class DefinicionMetrica:
    codigo: str
    nombre: str
    version: str = "1.0"
    tipo: str = "atomica"
    familia: str = "poblacion"
    unidad: str = ""
    precision_decimales: int = 2
    estrategia: Dict[str, Any] = field(default_factory=dict)
    descripcion: str = ""

    @property
    def pasos(self) -> List[Dict[str, Any]]:
        return self.estrategia.get("pasos", [])

    @property
    def formula(self) -> Optional[str]:
        return self.estrategia.get("formula")

    @property
    def dependencias(self) -> List[str]:
        return self.estrategia.get("dependencias", [])
