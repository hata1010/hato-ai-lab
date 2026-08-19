"""Pruebas base del extractor documental de la Fase 4."""

from io import BytesIO
import hashlib
import unittest
import zipfile

from document_extractor import DocumentExtractor, UnsupportedDocumentError


class DocumentExtractorTests(unittest.TestCase):
    def setUp(self):
        self.extractor = DocumentExtractor()

    def test_detect_pdf_by_signature(self):
        self.assertEqual(self.extractor.detect_type(b"%PDF-1.7\n", "archivo.bin"), "pdf")

    def test_detect_png_by_signature(self):
        png_signature = b"\x89PNG\r\n\x1a\n"
        self.assertEqual(self.extractor.detect_type(png_signature, "archivo.bin"), "image")

    def test_detect_docx_by_zip_container(self):
        stream = BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            archive.writestr("[Content_Types].xml", "")
        self.assertEqual(
            self.extractor.detect_type(stream.getvalue(), "archivo.docx"),
            "docx",
        )

    def test_identification_hash_for_image(self):
        data = b"\x89PNG\r\n\x1a\ncontenido-de-prueba"
        model = self.extractor.extract(_NamedBytes(data, "prueba.png"))
        self.assertEqual(model.identificacion["tipo"], "image")
        self.assertEqual(model.identificacion["tamaño"], len(data))
        self.assertEqual(model.identificacion["hash"], hashlib.sha256(data).hexdigest())
        self.assertEqual(len(model.imagenes), 1)

    def test_unsupported_format_is_controlled(self):
        with self.assertRaises(UnsupportedDocumentError):
            self.extractor.detect_type(b"contenido", "archivo.xyz")


class _NamedBytes:
    def __init__(self, data: bytes, name: str):
        self._data = data
        self.name = name

    def read(self):
        return self._data

    def tell(self):
        return 0

    def seek(self, _position):
        return None


if __name__ == "__main__":
    unittest.main()
