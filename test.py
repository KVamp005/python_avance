from pathlib import Path

Path("notes.txt").write_text("Hello world !\n", encoding="utf-8")
print(Path("notes.txt").read_text(encoding="utf-8"))
