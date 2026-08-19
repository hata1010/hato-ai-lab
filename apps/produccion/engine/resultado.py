"""Resultado unificado con trazabilidad para el Motor de Métricas Hato V1."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class ResultadoMetrica:
    metrica: str
    nombre: str
    valor: Any
    unidad: str
    es_valido: bool
    precision_decimales: int = 2
    trazabilidad: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    ejecutado_en: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def explain(self) -> str:
        lineas = [
            f"=== Métrica: {self.nombre} [{self.metrica}] ===",
            f"Resultado: {self.valor} {self.unidad}".strip(),
            f"Válido: {'SÍ' if self.es_valido else 'NO'}",
        ]
        if self.error:
            lineas.append(f"Error: {self.error}")
        if self.trazabilidad:
            lineas.append(f"Trazabilidad: {self.trazabilidad}")
        return "\n".join(lineas)
