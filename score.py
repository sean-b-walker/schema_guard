import json
import sys
from pathlib import Path

from validate import validate
from llm import call_model, load_env


def main():
    load_env()

    root = Path(__file__).parent
    cases = json.loads((root / "cases.json").read_text())
    passed = 0

    for name, case in cases.items():
        result = call_model(case["input"])
        errors = validate(result)

        if case.get("expected") and not isinstance(result, dict):
            errors.append("expected a JSON object to check expected values")
        else:
            for key, expected in case.get("expected", {}).items():
                if result.get(key) != expected:
                    errors.append(
                        f"{key}: expected {expected!r}, got {result.get(key)!r}"
                    )

        if errors:
            print(f"FAIL {name}")
            for error in errors:
                print(f"- {error}")
            print(json.dumps(result, indent=2))
        else:
            passed += 1
            print(f"PASS {name}")

    print(f"\n{passed}/{len(cases)} cases passed")
    if passed != len(cases):
        sys.exit(1)


if __name__ == "__main__":
    main()
