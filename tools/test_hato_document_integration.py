"""Pruebas de la integración mínima DocumentoAnimal -> extractor."""

import hashlib
import unittest

from tools.document_extractor import DocumentExtractor
from tools.hato_document_integration import (
    HatoDocumentIntegrationError,
    extract_documento_animal,
)


class _NamedFieldFile:
    def __init__(self, data: bytes, name: str):
        self._data = data
        self.name = name
        self.opened = False
        self.closed = False

    def open(self, _mode="rb"):
        self.opened = True

    def read(self):
        return self._data

    def tell(self):
        return 0

    def seek(self, _position):
        return None

    def close(self):
        self.closed = True


class _DocumentoAnimal:
    pk = 17
    animal_id = 42
    tipo = "pedigree"
    numero_documento = "PED-001"

    def __init__(self, archivo):
        self.archivo = archivo


class HatoDocumentIntegrationTests(unittest.TestCase):
    def test_extracts_fieldfile_and_preserves_hato_context(self):
        data = b"\x89PNG\r\n\x1a\ncontenido"
        archivo = _NamedFieldFile(data, "pedigree.png")
        documento = _DocumentoAnimal(archivo)

        result = extract_documento_animal(documento)

        self.assertEqual(result.identificacion["tipo"], "image")
        self.assertEqual(result.identificacion["hash"], hashlib.sha256(data).hexdigest())
        self.assertEqual(result.metadatos["hato"]["documento_animal_id"], 17)
        self.assertEqual(result.metadatos["hato"]["animal_id"], 42)
        self.assertEqual(result.metadatos["hato"]["tipo"], "pedigree")
        self.assertTrue(archivo.opened)
        self.assertTrue(archivo.closed)

    def test_missing_file_is_controlled(self):
        documento = _DocumentoAnimal(None)
        with self.assertRaises(HatoDocumentIntegrationError):
            extract_documento_animal(documento)


if __name__ == "__main__":
    unittest.main()
