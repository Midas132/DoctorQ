import datetime
import pytest

from models import Gender, Patient
from patient_queue import PatientQueue

@pytest.fixture
def queue():
    return PatientQueue()

@pytest.fixture
def sample_patient_1():
    return Patient(first_name="John", last_name="Doe", pesel="12345678901", age=30, gender=Gender.MALE, appointment_time=datetime.datetime.now() + datetime.timedelta(hours=10, minutes=5))

@pytest.fixture
def sample_patient_2():
    return Patient(first_name="Jane", last_name="Smith", pesel="98765432109", age=25, gender=Gender.FEMALE, appointment_time=datetime.datetime.now() + datetime.timedelta(hours=10, minutes=30))

@pytest.fixture
def priority_patient():
    return Patient(first_name="Alice", last_name="Brown", pesel="56789012345", age=40, gender=Gender.FEMALE, appointment_time=datetime.datetime.now() + datetime.timedelta(hours=9, minutes=45))

def test_add_patient(queue: PatientQueue, sample_patient_1: Patient, sample_patient_2: Patient):
    queue.add_patient(sample_patient_1)
    queue.add_patient(sample_patient_2)

    patients = queue.list_patients()
    assert len(patients) == 2
    assert patients[0].pesel == "12345678901"
    assert patients[1].pesel == "98765432109"

def test_add_priority_patient(queue: PatientQueue, sample_patient_1: Patient, sample_patient_2: Patient, priority_patient: Patient):
    queue.add_patient(sample_patient_1)
    queue.add_patient(sample_patient_2)
    queue.add_priority_patient(priority_patient, position=1)

    patients = queue.list_patients()
    assert len(patients) == 3
    assert patients[0].pesel == "12345678901"
    assert patients[1].pesel == "56789012345"  # Priority patient
    assert patients[2].pesel == "98765432109"

def test_remove_patient(queue: PatientQueue, sample_patient_1: Patient, sample_patient_2: Patient):
    queue.add_patient(sample_patient_1)
    queue.add_patient(sample_patient_2)

    removed = queue.remove_patient("12345678901")
    assert removed is True

    patients = queue.list_patients()
    assert len(patients) == 1
    assert patients[0].pesel == "98765432109"

def test_remove_nonexistent_patient(queue: PatientQueue, sample_patient_1: Patient):
    queue.add_patient(sample_patient_1)

    removed = queue.remove_patient("00000000000")
    assert removed is False

    patients = queue.list_patients()
    assert len(patients) == 1
    assert patients[0].pesel == "12345678901"

def test_list_patients_empty(queue: PatientQueue):
    patients = queue.list_patients()
    assert len(patients) == 0

def test_add_patient_to_empty_queue(queue: PatientQueue, sample_patient_1: Patient):
    queue.add_patient(sample_patient_1)

    patients = queue.list_patients()
    assert len(patients) == 1
    assert patients[0].pesel == "12345678901"