"""Données factices pour le TP."""

from typing import List

from .models import Student


def load_students() -> List[Student]:
    """Retourne une liste d'étudiants de démonstration."""
    return [
        Student(name="Alice", grades=[12, 15, 18]),
        Student(name="Brahim", grades=[9, -2, 14]),
        Student(name="Chloé", grades=[20, 19, 21]),
        Student(name="Dina", grades=[]),
    ]
