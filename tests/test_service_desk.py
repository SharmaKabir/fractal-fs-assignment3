"""
Basic automated tests for Smart Service Desk.

Run from project root with:
    python -m unittest discover -s tests -t . -v

All tests use a temporary file. The real data/requests.json is never modified.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from application.request_service import RequestService
from domain.exceptions import InvalidPriorityError, RequestAlreadyResolvedError, RequestNotFoundError
from domain.service_request import ServiceRequest
from infrastructure.file_repository import FileRepository


class ServiceRequestTests(unittest.TestCase):
    """Tests for domain entity behavior."""

    def test_new_request_starts_open(self):
        request = ServiceRequest(1, "Kabir", "Laptop issue", "HIGH")
        self.assertEqual(request.status, "OPEN")

    def test_resolve_changes_status(self):
        request = ServiceRequest(1, "Kabir", "Laptop issue", "HIGH")
        request.resolve()
        self.assertEqual(request.status, "RESOLVED")

    def test_resolving_twice_is_refused(self):
        request = ServiceRequest(1, "Kabir", "Laptop issue", "HIGH")
        request.resolve()
        with self.assertRaises(RequestAlreadyResolvedError):
            request.resolve()

    def test_invalid_priority_is_refused(self):
        with self.assertRaises(InvalidPriorityError):
            ServiceRequest(1, "Kabir", "Laptop issue", "URGENT")


class ServiceDeskTests(unittest.TestCase):
    """Tests for application + infrastructure layers with temp file persistence."""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.file_path = Path(self.tmp_dir.name) / "requests.json"
        self.service = RequestService(FileRepository(self.file_path))

    def _restart_app(self):
        return RequestService(FileRepository(self.file_path))

    def test_create_and_view(self):
        self.service.create_request("Kabir", "Laptop issue", "HIGH")
        self.service.create_request("Arya", "Wi-Fi issue", "MEDIUM")
        all_requests = self.service.view_requests()
        self.assertEqual(len(all_requests), 2)

    def test_search_unknown_id_raises(self):
        with self.assertRaises(RequestNotFoundError):
            self.service.search_request("999")

    def test_persistence_after_restart(self):
        created = self.service.create_request("Kabir", "VPN issue", "HIGH")
        self.service.resolve_request(str(created.request_id))

        reopened = self._restart_app()
        request = reopened.search_request(str(created.request_id))
        self.assertEqual(request.status, "RESOLVED")
        self.assertEqual(request.employee_name, "Kabir")

    def test_missing_file_is_safe(self):
        self.assertEqual(self.service.view_requests(), [])

    def test_empty_file_is_safe(self):
        self.file_path.write_text("", encoding="utf-8")
        reopened = self._restart_app()
        self.assertEqual(reopened.view_requests(), [])

    def test_save_writes_json_data(self):
        self.service.create_request("Kabir", "Mouse issue", "LOW")
        saved = json.loads(self.file_path.read_text(encoding="utf-8"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]["employee_name"], "Kabir")


if __name__ == "__main__":
    unittest.main()
