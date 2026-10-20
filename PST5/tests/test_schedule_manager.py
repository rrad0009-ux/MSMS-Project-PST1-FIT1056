# tests/test_schedule_manager.py
import pytest
import os
from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager(tmp_path):
    """Pytest fixture providing an isolated ScheduleManager backed by a temporary file."""
    test_json_file = tmp_path / "test_msms.json"
    manager = ScheduleManager(data_file=str(test_json_file))
    return manager


def test_register_student(fresh_manager):
    """Tests registering a new student."""
    student = fresh_manager.register_student("Rahul")
    assert student is not None
    assert student.name == "Rahul"
    assert len(fresh_manager.students) == 1


def test_record_payment_and_history(fresh_manager):
    """Tests recording a payment and retrieving payment history."""
    student = fresh_manager.register_student("Alex")
    payment = fresh_manager.record_payment(student.id, 150.00, "Credit Card")

    assert payment is not None
    assert payment["student_id"] == student.id
    assert payment["amount"] == 150.00

    history = fresh_manager.get_payment_history(student.id)
    assert len(history) == 1
    assert history[0]["method"] == "Credit Card"


def test_export_report_finance(fresh_manager, tmp_path):
    """Tests exporting the financial report to a CSV file."""
    student = fresh_manager.register_student("Taylor")
    fresh_manager.record_payment(student.id, 75.00, "Cash")

    output_csv = tmp_path / "finance_report.csv"
    result = fresh_manager.export_report("finance", str(output_csv))

    assert result is True
    assert os.path.exists(output_csv)
    