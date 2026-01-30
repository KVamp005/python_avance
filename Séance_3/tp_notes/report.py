"""Génération d'un rapport textuel."""

import logging
from typing import Iterable, List

from .models import Student
from .services import (
    best_student,
    class_average,
    student_average,
    valid_grades,
)


def build_report(students: Iterable[Student]) -> str:
    """Construit un rapport de moyennes avec logs.

    Args:
        students: liste d'étudiants.

    Returns:
        Une chaîne de caractères contenant le rapport.
    """
    lines: List[str] = []
    students_list = list(students)

    logging.debug("Nombre d'étudiants chargés: %s", len(students_list))

    if not students_list:
        logging.error("Aucun étudiant à traiter")
        return "Aucun étudiant à traiter."

    for student in students_list:
        logging.debug("Traitement de l'étudiant: %s", student.name)
        valid = valid_grades(student.grades)

        if len(valid) != len(student.grades):
            logging.warning(
                "Notes invalides détectées pour %s: %s",
                student.name,
                student.grades,
            )

        avg = student_average(student)
        if avg is None:
            logging.error("Aucune note valide pour %s", student.name)
            lines.append(f"{student.name}: aucune note valide")
            continue

        lines.append(f"{student.name}: moyenne = {avg:.2f}")

    class_avg = class_average(students_list)
    if class_avg is None:
        lines.append("Moyenne de classe: indisponible")
    else:
        lines.append(f"Moyenne de classe: {class_avg:.2f}")

    best = best_student(students_list)
    if best is None:
        lines.append("Meilleur étudiant: indisponible")
    else:
        best_avg = student_average(best)
        lines.append(f"Meilleur étudiant: {best.name} ({best_avg:.2f})")

    return "\n".join(lines)
