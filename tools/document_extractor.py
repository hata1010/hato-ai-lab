"""Extractor documental independiente para la Fase 4 de Hato.

Contrato de entrada/salida:
    archivo -> DocumentExtractor -> DocumentModel

El extractor no interpreta semánticamente el contenido ni modifica
DocumentoAnimal. Las dependencias de PDF/DOCX son opcionales para mantener
la capa de contrato utilizable aun cuando una librería concreta no esté
instalada.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, BinaryIO, Iterable
import zipfile


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp"}


@dataclass
class DocumentElement:
    """Elemento ordenable del documento normalizado."""

    tipo: str
    orden: int
    contenido: Any = None
    pagina: int | None = None
    metadatos: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentModel:
    """Representación estructurada definida en el contrato documental V1."""

    identificacion: dict[str, Any]
    metadatos: dict[str, Any] = field(default_factory=dict)
    estructura: dict[str, Any] = field(default_factory=dict)
    texto: list[dict[str, Any]] = field(default_factory=list)
    tablas: list[dict[str, Any]] = field(default_factory=list)
    imagenes: list[dict[str, Any]] = field(default_factory=list)
    elementos: list[DocumentElement] = field(default_factory=list)
    advertencias: list[str] = field(default_factory=list)


class DocumentExtractionError(Exception):
    """Error controlado durante la identificación o extracción."""


class UnsupportedDocumentError(DocumentExtractionError):
    """El archivo no pertenece a los formatos soportados."""


class DocumentExtractor:
    """Extractor común para PDF, DOCX e imágenes independientes."""

    def extract(self, source: str | Path | BinaryIO) -> DocumentModel:
        data, name = self._read_source(source)
        document_type = self.detect_type(data, name)
        identification = {
            "nombre": name,
            "tipo": document_type,
            "tamaño": len(data),
            "hash": sha256(data).hexdigest(),
        }

        if document_type == "pdf":
            return self._extract_pdf(data, identification)
        if document_type == "docx":
            return self._extract_docx(data, identification)
        if document_type == "image":
            return self._extract_image(data, identification)
        raise UnsupportedDocumentError(f"Formato no soportado: {document_type}")

    @staticmethod
    def _read_source(source: str | Path | BinaryIO) -> tuple[bytes, str]:
        if isinstance(source, (str, Path)):
            path = Path(source)
            try:
                return path.read_bytes(), path.name
            except OSError as exc:
                raise DocumentExtractionError(f"No se pudo leer el archivo: {path}") from exc

        name = getattr(source, "name", "documento")
        try:
            position = source.tell()
        except (AttributeError, OSError):
            position = None
        data = source.read()
        if position is not None:
            try:
                source.seek(position)
            except (AttributeError, OSError):
                pass
        return data, Path(str(name)).name

    @staticmethod
    def detect_type(data: bytes, name: str = "") -> str:
        """Detecta por firma cuando es posible y usa extensión como respaldo."""
        lower = name.lower()
        if data.startswith(b"%PDF-"):
            return "pdf"
        if data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff"):
            return "image"
        if data.startswith((b"GIF87a", b"GIF89a", b"BM")):
            return "image"
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return "image"
        if lower.endswith(".pdf"):
            return "pdf"
        if lower.endswith(".docx") and zipfile.is_zipfile(_bytes_file(data)):
            return "docx"
        if Path(lower).suffix in IMAGE_EXTENSIONS:
            return "image"
        raise UnsupportedDocumentError(f"No se pudo identificar el formato: {name}")

    def _extract_pdf(self, data: bytes, identification: dict[str, Any]) -> DocumentModel:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise DocumentExtractionError(
                "La extracción PDF requiere la dependencia opcional 'pypdf'."
            ) from exc

        reader = PdfReader(_bytes_file(data))
        metadata = self._pdf_metadata(reader.metadata)
        pages: list[dict[str, Any]] = []
        text_blocks: list[dict[str, Any]] = []
        images: list[dict[str, Any]] = []
        tables: list[dict[str, Any]] = []
        elements: list[DocumentElement] = []
        order = 0

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"numero": page_number, "texto": bool(text.strip())})
            if text.strip():
                text_blocks.append({"pagina": page_number, "texto": text})
                elements.append(DocumentElement("texto", order, text, page_number))
                order += 1

            try:
                page_images = list(page.images)
            except Exception as exc:  # pragma: no cover - depende de PDF concreto
                page_images = []
                identification.setdefault("advertencias", []).append(
                    f"No se pudieron enumerar imágenes de la página {page_number}: {exc}"
                )
            for image in page_images:
                image_data = getattr(image, "data", b"")
                item = {
                    "pagina": page_number,
                    "nombre": getattr(image, "name", None),
                    "tamaño": len(image_data),
                    "hash": sha256(image_data).hexdigest() if image_data else None,
                    "contenido": image_data,
                }
                images.append(item)
                elements.append(DocumentElement("imagen", order, item, page_number))
                order += 1

            # pdfplumber es opcional: las tablas PDF no tienen una
            # representación universal en pypdf.
            try:
                import pdfplumber  # type: ignore
            except ImportError:
                pdfplumber = None
            if pdfplumber is not None:
                with pdfplumber.open(_bytes_file(data)) as pdf:
                    extracted = pdf.pages[page_number - 1].extract_tables() or []
                for table in extracted:
                    item = {"pagina": page_number, "filas": table}
                    tables.append(item)
                    elements.append(DocumentElement("tabla", order, item, page_number))
                    order += 1

        return DocumentModel(
            identificacion=identification,
            metadatos=metadata,
            estructura={
                "paginas": pages,
                "numero_paginas": len(reader.pages),
                "orden": [e.orden for e in elements],
            },
            texto=text_blocks,
            tablas=tables,
            imagenes=images,
            elementos=elements,
        )

    def _extract_docx(self, data: bytes, identification: dict[str, Any]) -> DocumentModel:
        try:
            from docx import Document
        except ImportError as exc:
            raise DocumentExtractionError(
                "La extracción DOCX requiere la dependencia opcional 'python-docx'."
            ) from exc

        document = Document(_bytes_file(data))
        properties = document.core_properties
        metadata = {
            key: value
            for key, value in {
                "title": properties.title,
                "subject": properties.subject,
                "author": properties.author,
                "keywords": properties.keywords,
                "comments": properties.comments,
                "last_modified_by": properties.last_modified_by,
                "created": properties.created.isoformat() if properties.created else None,
                "modified": properties.modified.isoformat() if properties.modified else None,
            }.items()
            if value not in (None, "")
        }

        text_blocks: list[dict[str, Any]] = []
        tables: list[dict[str, Any]] = []
        images: list[dict[str, Any]] = []
        elements: list[DocumentElement] = []
        order = 0

        # El recorrido XML conserva el orden relativo de párrafos y tablas.
        from docx.document import Document as DocumentClass
        from docx.table import Table
        from docx.text.paragraph import Paragraph
        from docx.oxml.ns import qn

        def iter_blocks(parent: Any) -> Iterable[Any]:
            parent_elm = parent.element.body if isinstance(parent, DocumentClass) else parent._tc
            for child in parent_elm.iterchildren():
                if child.tag == qn("w:p"):
                    yield Paragraph(child, parent)
                elif child.tag == qn("w:tbl"):
                    yield Table(child, parent)

        def paragraph_image_relationships(paragraph: Paragraph) -> list[str]:
            relationship_ids: list[str] = []
            for node in paragraph._p.iter():
                if node.tag.endswith("}blip"):
                    embed = node.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                    if embed:
                        relationship_ids.append(embed)
            return relationship_ids

        def append_docx_image(relationship_id: str) -> None:
            nonlocal order
            rel = document.part.rels[relationship_id]
            image_data = rel.target_part.blob
            item = {
                "relacion": relationship_id,
                "tipo": rel.target_part.content_type,
                "tamaño": len(image_data),
                "hash": sha256(image_data).hexdigest(),
                "contenido": image_data,
            }
            images.append(item)
            elements.append(DocumentElement("imagen", order, item))
            order += 1

        for block in iter_blocks(document):
            if isinstance(block, Paragraph):
                text = block.text or ""
                style = getattr(block.style, "name", "") if block.style else ""
                if text.strip():
                    kind = "titulo" if style and (
                        style.lower().startswith("heading") or style.lower().startswith("título")
                    ) else "parrafo"
                    item = {"texto": text, "estilo": style or None}
                    text_blocks.append(item)
                    elements.append(DocumentElement(kind, order, item))
                    order += 1
                for relationship_id in paragraph_image_relationships(block):
                    append_docx_image(relationship_id)
            elif isinstance(block, Table):
                rows = [[cell.text for cell in row.cells] for row in block.rows]
                item = {
                    "filas": rows,
                    "filas_count": len(rows),
                    "columnas_count": max((len(r) for r in rows), default=0),
                }
                tables.append(item)
                elements.append(DocumentElement("tabla", order, item))
                order += 1

        return DocumentModel(
            identificacion=identification,
            metadatos=metadata,
            estructura={
                "secciones": len(document.sections),
                "orden": [e.orden for e in elements],
            },
            texto=text_blocks,
            tablas=tables,
            imagenes=images,
            elementos=elements,
        )

    @staticmethod
    def _pdf_metadata(metadata: Any) -> dict[str, Any]:
        if not metadata:
            return {}
        return {str(key).lstrip("/"): value for key, value in metadata.items()}

    @staticmethod
    def _extract_image(data: bytes, identification: dict[str, Any]) -> DocumentModel:
        metadata: dict[str, Any] = {}
        try:
            from io import BytesIO
            from PIL import Image

            with Image.open(BytesIO(data)) as image:
                metadata.update(
                    {
                        "formato": image.format,
                        "ancho": image.width,
                        "alto": image.height,
                        "modo": image.mode,
                        "metadatos_exif": dict(image.getexif()),
                    }
                )
        except ImportError:
            metadata["advertencia"] = "Pillow no está instalada; no se extrajeron dimensiones/EXIF."
        except Exception as exc:
            metadata["advertencia"] = f"No se pudieron leer metadatos de imagen: {exc}"

        item = {"tamaño": len(data), "hash": identification["hash"], "contenido": data}
        element = DocumentElement("imagen", 0, item)
        return DocumentModel(
            identificacion=identification,
            metadatos=metadata,
            estructura={"orden": [0]},
            imagenes=[item],
            elementos=[element],
        )


def _bytes_file(data: bytes) -> Any:
    from io import BytesIO

    return BytesIO(data)


__all__ = [
    "DocumentElement",
    "DocumentModel",
    "DocumentExtractor",
    "DocumentExtractionError",
    "UnsupportedDocumentError",
]
