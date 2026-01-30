"""Modèles de données pour le TP."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Student:
    """Représente un étudiant et ses notes."""

    name: str
    grades: List[float]

    def average(self) -> float:
        """Calcule la moyenne brute des notes.

        Note: cette méthode ne filtre pas les notes invalides.
        """
        return sum(self.grades) / len(self.grades)
