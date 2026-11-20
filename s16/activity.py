"""Complete the IFCOpenShell activity on AC20-FZK-Haus.ifc."""

from pathlib import Path

import ifcopenshell


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "AC20-FZK-Haus.ifc"
OUTPUT_FILE = BASE_DIR / "AC20-FZK-Haus_renamed.ifc"


def display(value):
    """Return a readable value for optional IFC attributes."""
    return value if value not in (None, "") else "(not set)"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input IFC file was not found: {INPUT_FILE}")

    model = ifcopenshell.open(str(INPUT_FILE))
    print(f"IFC file loaded: {model.schema}")

    stairs = model.by_type("IfcStair")
    print(f"\nStairs ({len(stairs)}):")
    for stair in stairs:
        print(f"  ID #{stair.id()}: {display(stair.Name)}")

    slabs = model.by_type("IfcSlab")
    print(f"\nSlabs ({len(slabs)}):")
    for index, slab in enumerate(slabs, start=1):
        print(f"  ID #{slab.id()}: {display(slab.Name)}")
        slab.Name = f"Renamed_Slab_{index}"
        print(f"    Updated name: {slab.Name}")

    storeys = model.by_type("IfcBuildingStorey")
    print(f"\nBuilding storeys ({len(storeys)}):")
    for storey in storeys:
        print(
            f"  {display(storey.Name)} - elevation: "
            f"{display(getattr(storey, 'Elevation', None))}"
        )

    print("\nUnique IFC entity types:")
    entity_types = set()
    for entity in model:
        entity_types.add(entity.is_a())
    for entity_type in sorted(entity_types):
        print(f"  {entity_type}")

    projects = model.by_type("IfcProject")
    if projects:
        project_name = display(projects[0].Name)
        print(f"\nProject name: {project_name}")
    else:
        print("\nProject name: (no IfcProject found)")

    model.write(str(OUTPUT_FILE))
    print(f"\nSaved modified IFC file: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
