"""Integración mínima del extractor documental con Hato.

La integración es un adaptador deliberadamente pequeño entre
``DocumentoAnimal`` y ``DocumentExtractor``. No modifica el modelo Django,
no crea migraciones y no interpreta semánticamente el contenido.

Contrato:
    DocumentoAnimal -> DocumentExtractor -> DocumentModel

El objeto recibido se trata por interfaz: debe exponer ``archivo`` y puede
exponer ``animal_id``, ``tipo`` y ``numero_documento``. Esto permite probar
la integración sin levantar Django y evita acoplar el extractor al ORM.
"""

from __future__ import annotations

from typing import Any

from .document_extractor import DocumentExtractor, DocumentModel


class HatoDocumentIntegrationError(Exception):
    """Error controlado de integración con DocumentoAnimal."""


def extract_documento_animal(
    documento: Any,
    extractor: DocumentExtractor | None = None,
) -> DocumentModel:
    """Extrae el archivo asociado a un ``DocumentoAnimal``.

    El archivo se lee mediante la interfaz estándar de ``FieldFile``
    (``open/read/close``). Los datos propios de Hato se conservan en los
    metadatos del resultado sin alterar el contrato documental.
    """

    archivo = getattr(documento, "archivo", None)
    if not archivo:
        raise HatoDocumentIntegrationError(
            "El DocumentoAnimal no tiene un archivo asociado."
        )

    extractor = extractor or DocumentExtractor()
    opened_here = False

    try:
        if hasattr(archivo, "open"):
            archivo.open("rb")
            opened_here = True

        result = extractor.extract(archivo)
    except Exception as exc:
        if isinstance(exc, HatoDocumentIntegrationError):
            raise
        raise HatoDocumentIntegrationError(
            f"No se pudo extraer el DocumentoAnimal: {exc}"
        ) from exc
    finally:
        if opened_here and hasattr(archivo, "close"):
            archivo.close()

    result.metadatos["hato"] = {
        "documento_animal_id": getattr(documento, "pk", None),
        "animal_id": getattr(documento, "animal_id", None),
        "tipo": getattr(documento, "tipo", None),
        "numero_documento": getattr(documento, "numero_documento", None),
    }
    return result


__all__ = ["HatoDocumentIntegrationError", "extract_documento_animal"]
