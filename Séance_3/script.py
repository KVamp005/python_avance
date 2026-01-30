"""Script monolithique avant refactorisation."""

from typing import List, Optional


def validate_grade(grade: float) -> bool:
    """Vérifie qu'une note est comprise entre 0 et 20 inclus."""
    return 0 <= grade <= 20


def student_average(grades: List[float]) -> Optional[float]:
    """Calcule la moyenne d'une liste de notes valides."""
    valid_grades = [g for g in grades if validate_grade(g)]
    if not valid_grades:
        return None
    return sum(valid_grades) / len(valid_grades)


def main() -> None:
    """Exécute un petit calcul de moyennes pour des étudiants."""
    students = {
        "Alice": [12, 15, 18],
        "Brahim": [9, -2, 14],
        "Chloé": [20, 19, 21],
    }

    for name, grades in students.items():
        avg = student_average(grades)
        if avg is None:
            print(f"{name}: aucune note valide")
        else:
            print(f"{name}: moyenne = {avg:.2f}")


if __name__ == "__main__":
    main()
