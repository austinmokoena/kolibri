from django.test import override_settings
from django.test import TestCase
from django.utils import timezone

from ..constants import BACKEND
from ..constants import FRONTEND
from ..constants import TASK
from kolibri.core.error_reports.models import ErrorReport


class ErrorReportTestCase(TestCase):
    databases = "__all__"

    def setUp(self):
        self.category_frontend = FRONTEND
        self.category_backend = BACKEND
        self.error_message = "Test Error"
        self.traceback = "Test Traceback"
        self.context_frontend = {
            "browser": {},
            "os": {},
            "component": "HeaderComponent",
            "device": {
                "is_touch_device": True,
                "screen": {
                    "width": 1920,
                    "height": 1080,
                    "available_width": 1920,
                    "available_height": 1040,
                },
            },
        }
        self.context_backend = {
            "request_info": {
                "url": "/api/test",
                "method": "GET",
                "headers": {"User-Agent": "TestAgent"},
                "body": "",
                "query_params": {"test": "true"},
            },
            "server": {"host": "localhost", "port": "8000"},
            "packages": ["django==3.2", "kolibri==0.15.8"],
            "python_version": "3.9.1",
        }
        self.context_task = {
            "job_info": {
                "job_id": "1",
                "func": "test_func",
                "facility_id": None,
                "args": ["test"],
                "kwargs": {"test": "test"},
                "progress": 0,
                "total_progress": 0,
                "extra_metadata": {},
            },
            "worker_info": {
                "worker_host": "localhost",
                "worker_process": "1",
                "worker_thread": "1",
                "worker_extra": None,
            },
        }

    def create_error(
        self,
        category,
        error_message,
        traceback,
        context,
        reported=False,
    ):
        return ErrorReport.objects.create(
            category=category,
            error_message=error_message,
            traceback=traceback,
            context=context,
            reported=reported,
        )

    @override_settings(DEVELOPER_MODE=False)
    def test_insert_or_update_frontend_error_prod_mode(self):
        error = ErrorReport.insert_or_update_error(
            self.category_frontend,
            self.error_message,
            self.traceback,
            self.context_frontend,
        )
        self.assertEqual(error.category, self.category_frontend)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_frontend)
        self.assertEqual(error.events, 1)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

        # Creating the error again, so this time it should update the error
        error = ErrorReport.insert_or_update_error(
            self.category_frontend,
            self.error_message,
            self.traceback,
            self.context_frontend,
        )
        self.assertEqual(error.category, self.category_frontend)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_frontend)
        self.assertEqual(error.events, 2)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

    @override_settings(DEVELOPER_MODE=False)
    def test_insert_or_update_backend_error_prod_mode(self):
        error = ErrorReport.insert_or_update_error(
            self.category_backend,
            self.error_message,
            self.traceback,
            self.context_backend,
        )
        self.assertEqual(error.category, self.category_backend)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_backend)
        self.assertEqual(error.events, 1)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

        # Creating the error again, so this time it should update the error
        error = ErrorReport.insert_or_update_error(
            self.category_backend,
            self.error_message,
            self.traceback,
            self.context_backend,
        )
        self.assertEqual(error.category, self.category_backend)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_backend)
        self.assertEqual(error.events, 2)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

    @override_settings(DEVELOPER_MODE=False)
    def test_insert_or_update_task_error_prod_mode(self):
        error = ErrorReport.insert_or_update_error(
            TASK,
            self.error_message,
            self.traceback,
            self.context_task,
        )
        self.assertEqual(error.category, TASK)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_task)
        self.assertEqual(error.events, 1)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

        # Creating the error again, so this time it should update the error
        error = ErrorReport.insert_or_update_error(
            TASK,
            self.error_message,
            self.traceback,
            self.context_task,
        )
        self.assertEqual(error.category, TASK)
        self.assertEqual(error.error_message, self.error_message)
        self.assertEqual(error.traceback, self.traceback)
        self.assertEqual(error.context, self.context_task)
        self.assertEqual(error.events, 2)
        self.assertFalse(error.reported)
        self.assertLess(
            timezone.now() - error.first_occurred, timezone.timedelta(seconds=1)
        )
        self.assertLess(
            timezone.now() - error.last_occurred, timezone.timedelta(seconds=1)
        )

    @override_settings(DEVELOPER_MODE=True)
    def test_insert_or_update_error_dev_mode(self):
        error = ErrorReport.insert_or_update_error(
            self.category_backend,
            self.error_message,
            self.traceback,
            self.context_backend,
        )
        self.assertIsNone(error)

    def test_get_unreported_errors(self):
        self.create_error(
            self.category_frontend,
            "Error 1",
            "Traceback 1",
            self.context_frontend,
            reported=False,
        )
        self.create_error(
            self.category_backend,
            "Error 2",
            "Traceback 2",
            self.context_backend,
            reported=False,
        )
        self.create_error(
            self.category_backend,
            "Error 3",
            "Traceback 3",
            self.context_backend,
            reported=True,
        )

        # Get unreported errors, should be only 2 as out of 3, 1 is reported
        unreported_errors = ErrorReport.get_unreported_errors()
        self.assertEqual(unreported_errors.count(), 2)
        self.assertFalse(unreported_errors[0].reported)
        self.assertFalse(unreported_errors[1].reported)
