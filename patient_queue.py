import datetime
from typing import Optional

from models import Patient


class Node:
    def __init__(self, patient: Patient):
        self.patient: Patient = patient
        self.next: Optional[Node] = None


class PatientQueue:
    def __init__(self):
        self.head: Optional[Node] = None

    def add_patient(self, patient: Patient):
        """Add a patient to the end of the queue."""
        new_node = Node(patient)
        if not self.head:
            # Round to the nearest 30 minutes
            new_node.patient.appointment_time += datetime.timedelta(
                minutes=60 - new_node.patient.appointment_time.minute, hours=1
            )
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            new_node.patient.appointment_time = (
                current.patient.appointment_time + datetime.timedelta(minutes=30)
            )
            current.next = new_node

    def add_priority_patient(self, patient: Patient, position: int):
        """Add a priority patient at a specific position in the queue."""
        if not self.head:
            self.add_patient(patient)
            return

        new_node = Node(patient)
        if position <= 0:
            # Insert at the head if position is <= 0 or the list is empty
            new_node.patient.appointment_time = self.head.patient.appointment_time
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            prev = None
            current_position = 0

            while current and current_position < position:
                prev = current
                current = current.next
                current_position += 1

            if not current:
                raise

            new_node.patient.appointment_time = current.patient.appointment_time
            new_node.next = current
            if prev:
                prev.next = new_node

        current = new_node
        while current and current.next:
            current = current.next
            current.patient.appointment_time += datetime.timedelta(minutes=30)

    def remove_patient(self, pesel: str):
        """Remove a patient from the queue by their PESEL."""
        current = self.head
        prev = None

        while current:
            if current.patient.pesel == pesel:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True  # Patient removed
            prev = current
            current = current.next

        return False  # Patient not found

    def list_patients(self):
        """List all patients in the queue."""
        patients: list[Patient] = []
        current = self.head
        while current:
            patients.append(current.patient)
            current = current.next
        return patients
