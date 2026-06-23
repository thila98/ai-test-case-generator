def validate_test_cases(test_cases: list) -> dict:
    issues = []
    valid_categories = {"Functional", "Negative", "Boundary", "Security", "UI-UX", "Integration"}
    valid_priorities = {"High", "Medium", "Low"}

    if not test_cases:
        return {"valid": False, "issues": ["No test cases were generated"], "count": 0}

    for tc in test_cases:
        tc_id = tc.get("TC_ID", "UNKNOWN")

        if not tc.get("Title"):
            issues.append(f"{tc_id}: Missing title")

        if tc.get("Category") not in valid_categories:
            issues.append(f"{tc_id}: Invalid category '{tc.get('Category')}'")

        if tc.get("Priority") not in valid_priorities:
            issues.append(f"{tc_id}: Invalid priority '{tc.get('Priority')}'")

        if not tc.get("Test Steps"):
            issues.append(f"{tc_id}: Missing test steps")

        if not tc.get("Expected Result"):
            issues.append(f"{tc_id}: Missing expected result")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "count": len(test_cases)
    }


def print_validation_report(validation_result: dict) -> None:
    print(f"Total test cases generated: {validation_result['count']}")

    if validation_result["valid"]:
        print("Validation passed - all test cases are complete")
    else:
        print(f"Validation warnings ({len(validation_result['issues'])} issues):")
        for issue in validation_result["issues"]:
            print(f"  - {issue}")
