# tests/test_schedule_manager.py
import pytest
import os
from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager(tmp_path):
    """
    Pytest fixture that creates a clean ScheduleManager instance 
    backed by a temporary JSON file path to ensure test isolation.
    """
    test_json_file = tmp_path / "test_msms.json"
    manager = ScheduleManager(data_file=str(test_json_file))
    return manager


def test_register_student(fresh_manager):
    """Tests registering a new student in ScheduleManager."""
    # ARRANGE: Fresh manager provided by fixture
    student_name = "Rahul"

    # ACT: Register a new student
    student = fresh_manager.register_student(student_name)

    # ASSERT: Student is created and added to manager state
    assert student is not None
    assert student.name == student_name
    assert len(fresh_manager.students) == 1


def test_record_payment_and_history(fresh_manager):
    """Tests recording a payment and retrieving student payment history."""
    # ARRANGE: Register a student to test against
    student = fresh_manager.register_student("Alex")

    # ACT: Record a payment
    payment = fresh_manager.record_payment(student.id, 150.00, "Credit Card")

    # ASSERT: Payment record is properly populated
    assert payment is not None
    assert payment["student_id"] == student.id
    assert payment["amount"] == 150.00
    assert payment["method"] == "Credit Card"

    # ACT & ASSERT: Verify history lookup
    history = fresh_manager.get_payment_history(student.id)
    assert len(history) == 1
    assert history[0]["amount"] == 150.00


def test_export_report_finance(fresh_manager, tmp_path):
    """Tests exporting the financial report to a CSV file."""
    # ARRANGE: Seed a student and payment record
    student = fresh_manager.register_student("Taylor")
    fresh_manager.record_payment(student.id, 75.00, "Cash")
    
    output_csv = tmp_path / "finance_report.csv"

    # ACT: Export the report
    result = fresh_manager.export_report("finance", str(output_csv))

    # ASSERT: Export succeeds and file is created on disk
    assert result is True
    assert os.path.exists(output_csv)
    