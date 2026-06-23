import csv
import os
from datetime import datetime


def parse_test_cases(raw_output: str) -> list:
    test_cases = []
    lines = raw_output.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line or not line.startswith("TC_"):
            continue

        parts = [p.strip() for p in line.split("|")]

        if len(parts) >= 8:
            test_cases.append({
                "TC_ID": parts[0],
                "Category": parts[1],
                "Title": parts[2],
                "Precondition": parts[3],
                "Test Steps": parts[4],
                "Expected Result": parts[5],
                "Priority": parts[6],
                "Status": parts[7]
            })

    return test_cases


def save_to_csv(test_cases: list, feature_name: str = "feature") -> str:
    output_dir = os.getenv("OUTPUT_DIR", "reports")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = feature_name.replace(" ", "_").lower()[:30]
    filename = f"{output_dir}/TC_{clean_name}_{timestamp}.csv"

    headers = [
        "TC_ID", "Category", "Title", "Precondition",
        "Test Steps", "Expected Result", "Priority", "Status"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(test_cases)

    return filename


def format_and_save(raw_output: str, feature_name: str = "feature") -> dict:
    test_cases = parse_test_cases(raw_output)
    filename = save_to_csv(test_cases, feature_name)

    return {
        "total": len(test_cases),
        "filename": filename,
        "test_cases": test_cases
    }
