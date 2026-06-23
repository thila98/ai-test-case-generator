import sys
import os
from src.generator import run
from src.output_formatter import format_and_save
from src.validator import validate_test_cases, print_validation_report


def main():
    print("=" * 60)
    print("   AI Test Case Generator")
    print("   Powered by Claude AI")
    print("=" * 60)

    if len(sys.argv) >= 2:
        feature_input = " ".join(sys.argv[1:])
    else:
        print("\nEnter your feature description below.")
        print("Press Enter twice when done:\n")
        lines = []
        while True:
            line = input()
            if line == "":
                if lines:
                    break
            else:
                lines.append(line)
        feature_input = "\n".join(lines)

    if not feature_input.strip():
        print("Error: No feature description provided.")
        sys.exit(1)

    feature_name = feature_input.split("\n")[0].strip()[:50]

    print(f"\nFeature: {feature_name}")
    print("-" * 60)

    raw_output = run(feature_input)

    result = format_and_save(raw_output, feature_name)

    print("\n" + "=" * 60)
    print_validation_report(validate_test_cases(result["test_cases"]))
    print(f"\nCSV saved to: {result['filename']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
