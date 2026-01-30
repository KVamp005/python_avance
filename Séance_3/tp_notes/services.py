"""Fonctions métiers pour calculer des statistiques."""

from typing import Iterable, List, Optional

from .models import Student


def validate_grade(grade: float) -> bool:
    """Vérifie qu'une note est comprise entre 0 et 20 inclus."""
    return 0 <= grade <= 20


def valid_grades(grades: Iterable[float]) -> List[float]:
    """Filtre et retourne uniquement les notes valides."""
    return [grade for grade in grades if validate_grade(grade)]


def student_average(student: Student) -> Optional[float]:
    """Calcule la moyenne des notes valides d'un étudiant.

    Returns:
        None si aucune note valide n'est disponible.
    """
    grades = valid_grades(student.grades)
    if not grades:
        return None
    return sum(grades) / len(grades)


def class_average(students: Iterable[Student]) -> Optional[float]:
    """Calcule la moyenne de classe à partir des moyennes valides."""
    averages: List[float] = []
    for student in students:
        avg = student_average(student)
        if avg is not None:
            averages.append(avg)
    if not averages:
        return None
    return sum(averages) / len(averages)


def best_student(students: Iterable[Student]) -> Optional[Student]:
    """Retourne l'étudiant ayant la meilleure moyenne valide."""
    best: Optional[Student] = None
    best_avg: Optional[float] = None

    for student in students:
        avg = student_average(student)
        if avg is None:
            continue
        if best_avg is None or avg > best_avg:
            best = student
            best_avg = avg

    return best
