"""Point d'entrée du package."""

import logging

from .data import load_students
from .report import build_report


def configure_logging(level: int = logging.DEBUG) -> None:
    """Configure le système de logs."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """Exécute l'application."""
    configure_logging()
    logging.info("Démarrage du programme")

    students = load_students()
    report = build_report(students)

    logging.info("Rapport généré avec succès")
    logging.info("\n%s", report)


if __name__ == "__main__":
    main()
