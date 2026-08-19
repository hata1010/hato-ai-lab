"""Pruebas automatizadas de regresión para la Fase 4 documental."""

import hashlib
import unittest
import zipfile
from io import BytesIO

from tools.document_extractor import (
    DocumentExtractor,
    DocumentExtractionError,
    UnsupportedDocumentError,
)
from tools.hato_document_integration import (
    HatoDocumentIntegrationError,
    extract_documento_animal,
)


class DocumentPipelineRegressionTests(unittest.TestCase):
    def setUp(self):
        self.extractor = DocumentExtractor()

    def test_supported_formats_have_deterministic_detection(self):
        self.assertEqual(self.extractor.detect_type(b"%PDF-1.7\n", "x.bin"), "pdf")
        self.assertEqual(self.extractor.detect_type(b"\x89PNG\r\n\x1a\n", "x.bin"), "image")

        stream = BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("[Content_Types].xml", "")
        self.assertEqual(self.extractor.detect_type(stream.getvalue(), "x.docx"), "docx")

    def test_image_result_is_normalized_and_traceable(self):
        data = b"\x89PNG\r\n\x1a\nphase-4-regression"
        result = self.extractor.extract(_NamedBytes(data, "evidencia.png"))
        self.assertEqual(result.identificacion["nombre"], "evidencia.png")
        self.assertEqual(result.identificacion["tipo"], "image")
        self.assertEqual(result.identificacion["tamaño"], len(data))
        self.assertEqual(result.identificacion["hash"], hashlib.sha256(data).hexdigest())
        self.assertEqual(len(result.imagenes), 1)
        self.assertEqual(result.elementos[0].tipo, "imagen")

    def test_unsupported_document_is_controlled(self):
        with self.assertRaises(UnsupportedDocumentError):
            self.extractor.extract(_NamedBytes(b"abc", "archivo.xyz"))

    def test_empty_source_name_does_not_break_reading(self):
        result = self.extractor.extract(_NamedBytes(b"\x89PNG\r\n\x1a\nabc", ""))
        self.assertEqual(result.identificacion["tipo"], "image")

    def test_hato_integration_preserves_traceability(self):
        data = b"\x89PNG\r\n\x1a\ntrazabilidad"
        documento = _DocumentoAnimal(_NamedFieldFile(data, "animal.png"))
        result = extract_documento_animal(documento)
        hato = result.metadatos["hato"]
        self.assertEqual(hato["documento_animal_id"], 100)
        self.assertEqual(hato["animal_id"], 200)
        self.assertEqual(hato["tipo"], "foto")
        self.assertEqual(result.identificacion["hash"], hashlib.sha256(data).hexdigest())

    def test_hato_missing_file_is_controlled(self):
        with self.assertRaises(HatoDocumentIntegrationError):
            extract_documento_animal(_DocumentoAnimal(None))


class _NamedBytes:
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def read(self):
        return self.data

    def tell(self):
        return 0

    def seek(self, _position):
        return None


class _NamedFieldFile(_NamedBytes):
    def __init__(self, data, name):
        super().__init__(data, name)
        self.opened = False
        self.closed = False

    def open(self, _mode="rb"):
        self.opened = True

    def close(self):
        self.closed = True


class _DocumentoAnimal:
    pk = 100
    animal_id = 200
    tipo = "foto"
    numero_documento = "DOC-100"

    def __init__(self, archivo):
        self.archivo = archivo


if __name__ == "__main__":
    unittest.main(verbosity=2)
