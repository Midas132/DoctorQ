import datetime

from nicegui import ui

from models import Gender, Patient
from patient_queue import PatientQueue

queue = PatientQueue()

ui.label("DoctorQ")
with ui.row():
    is_priority: ui.toggle
    position: ui.number
    name: ui.input
    with ui.column():
        is_priority = ui.toggle(
            {False: "Zwykły", True: "Priorytet"},
            value=False,
        )
        with ui.column().bind_visibility_from(is_priority, "value"):
            position = ui.number(
                "Miejsce w kolejce: ",
            )
    with ui.column():
        name = ui.input("imię").classes("inline-flex").props("dense outlined")
        surname = ui.input("nazwisko").classes("inline-flex").props("dense outlined")
        pesel = (
            ui.input(
                "PESEL",
                validation={
                    "musi być 11 cyfr": lambda e: e is None
                    or (len(e) == 11 and e.isnumeric()),
                    "PESEL istnieje": lambda e: e
                    not in [x.pesel for x in queue.list_patients()],
                },
            )
            .classes("inline-flex")
            .props("dense outlined")
        )
        age = (
            ui.number(
                "Wiek",
                validation={"musi być wiekszy od 0": lambda e: e is None or int(e) > 0},
            )
            .classes("inline-flex")
            .props("dense outlined")
        )
        gender = (
            ui.select(
                {
                    Gender.MALE.value: "Mężczyzna",
                    Gender.FEMALE.value: "Kobieta",
                    Gender.OTHER.value: "Inne",
                },
                label="Płeć",
                value=Gender.MALE.value,
            )
            .classes("inline-flex")
            .props("dense outlined")
        )

        def add_patient():
            new_patient = Patient(
                first_name=name.value,
                last_name=surname.value,
                pesel=pesel.value,
                age=age.value,
                gender=Gender[gender.value or ""],
                appointment_time=datetime.datetime.now(),
            )
            if is_priority.value and position.value is not None:
                queue.add_priority_patient(new_patient, position.value)
                is_priority.set_value(None)
            else:
                queue.add_patient(new_patient)
            ui.notify(
                f"Dodano pacjenta: {new_patient.first_name} {new_patient.last_name}"
            )
            name.set_value(None)
            surname.set_value(None)
            pesel.set_value(None)
            age.set_value(None)
            gender.set_value(Gender.MALE)
            patient_rows = [  # type: ignore
                {
                    **patient.model_dump(),
                    "gender": patient.gender.polish(),
                    "appointment_date": patient.appointment_time.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }
                for patient in queue.list_patients()
            ]
            table.update_rows(  # type: ignore
                patient_rows
            )
            ui.notify("Dodano pacjenta")

        ui.button("Zatwierdź", on_click=add_patient)
columns = [
    {"name": "Imie", "field": "first_name", "label": "Imię"},
    {"name": "Nazwisko", "field": "last_name", "label": "Nazwisko"},
    {"name": "PESEL", "field": "pesel", "label": "PESEL"},
    {"name": "Wiek", "field": "age", "label": "Wiek"},
    {"name": "Płeć", "field": "gender", "label": "Płeć"},
    {"name": "Data", "field": "appointment_date", "label": "Data"},
]

table = ui.table(columns=columns, rows=[x.model_dump() for x in queue.list_patients()])


def delete_patient():
    queue.remove_patient(pesel_do_usuniecia.value)
    patient_rows = [  # type: ignore
        {
            **patient.model_dump(),
            "gender": patient.gender.polish(),
            "appointment_date": patient.appointment_time.strftime("%Y-%m-%d %H:%M"),
        }
        for patient in queue.list_patients()
    ]
    table.update_rows(  # type: ignore
        patient_rows
    )
    pesel_do_usuniecia.set_value(None)


pesel_do_usuniecia = ui.input("wpisz PESEL do usunięcia")
ui.button("usun", on_click=delete_patient)
ui.run()
