from pathlib import Path

source = Path("test.log")
destination = source.with_name(source.stem + "_trimmed" + source.suffix)

text = source.read_text(encoding="utf-8", errors="replace")
parts = text.split("Launching")

# Each part after the first starts with content following "Launching".
sections = ["Launching" + part for part in parts[1:]]

if len(sections) < 4:
    raise ValueError(f"Found only {len(sections)} 'Launching' sections")

destination.write_text("".join(sections[-4:]), encoding="utf-8")
print(f"Kept the last 4 sections in {destination}")