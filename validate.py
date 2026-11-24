import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


root = Path(__file__).parent


def validate(value):
    schema = json.loads((root / "schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(value), key=lambda error: str(error.path))
    return [
        f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 validate.py sample.json")

    path = Path(sys.argv[1])
    value = json.loads(path.read_text())
    errors = validate(value)

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print("VALID")


if __name__ == "__main__":
    main()
