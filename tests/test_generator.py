import pytest
import sys
import os

# This line tells Python where to find our src folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.prompt_builder import build_prompt
from src.validator import validate_test_cases
from src.output_formatter import parse_test_cases


# ─────────────────────────────────────────
# TESTS FOR build_prompt()
# ─────────────────────────────────────────

def test_prompt_contains_feature_description():
    """Check that the feature description appears inside the prompt"""
    feature = "User login with email and password"
    result = build_prompt(feature)
    assert feature in result, "Feature description should appear in the prompt"


def test_prompt_is_a_string():
    """Check that build_prompt returns text, not a number or list"""
    result = build_prompt("Some feature")
    assert isinstance(result, str), "Prompt should be a string"


def test_prompt_is_not_empty():
    """Check that build_prompt does not return blank text"""
    result = build_prompt("Some feature")
    assert len(result) > 0, "Prompt should not be empty"


def test_prompt_contains_qa_categories():
    """Check that the prompt asks Claude for all required test categories"""
    result = build_prompt("Some feature")
    assert "Functional" in result, "Prompt should include Functional category"
    assert "Security" in result, "Prompt should include Security category"
    assert "Negative" in result, "Prompt should include Negative category"


def test_prompt_with_empty_feature():
    """Check that build_prompt still works even if feature description is empty"""
    result = build_prompt("")
    assert isinstance(result, str), "Should still return a string for empty input"


# ─────────────────────────────────────────
# TESTS FOR parse_test_cases()
# ─────────────────────────────────────────

def test_parse_returns_list():
    """Check that parse_test_cases returns a list"""
    sample = "TC_001 | Functional | Valid login | User on login page | 1. Enter email 2. Enter password 3. Click login | User redirected to dashboard | High | Not Executed"
    result = parse_test_cases(sample)
    assert isinstance(result, list), "Should return a list"


def test_parse_extracts_correct_number_of_test_cases():
    """Check that two TC lines produce two test cases"""
    sample = """TC_001 | Functional | Valid login | User on login page | 1. Enter email 2. Click login | User redirected to dashboard | High | Not Executed
TC_002 | Negative | Invalid password | User on login page | 1. Enter wrong password 2. Click login | Error message shown | High | Not Executed"""
    result = parse_test_cases(sample)
    assert len(result) == 2, f"Expected 2 test cases but got {len(result)}"


def test_parse_extracts_correct_fields():
    """Check that each test case has all required fields"""
    sample = "TC_001 | Functional | Valid login | User on login page | 1. Enter email 2. Click login | User redirected to dashboard | High | Not Executed"
    result = parse_test_cases(sample)
    assert len(result) == 1
    tc = result[0]
    assert tc["TC_ID"] == "TC_001"
    assert tc["Category"] == "Functional"
    assert tc["Priority"] == "High"
    assert tc["Status"] == "Not Executed"


def test_parse_ignores_non_tc_lines():
    """Check that random text lines are ignored and only TC_ lines are picked up"""
    sample = """Here are your test cases:
TC_001 | Functional | Valid login | Precondition | Steps | Expected | High | Not Executed
Some random text here
Another random line"""
    result = parse_test_cases(sample)
    assert len(result) == 1, "Should only pick up TC_ lines"


def test_parse_empty_input_returns_empty_list():
    """Check that empty input gives back an empty list, not an error"""
    result = parse_test_cases("")
    assert result == [], "Empty input should return empty list"


# ─────────────────────────────────────────
# TESTS FOR validate_test_cases()
# ─────────────────────────────────────────

def test_validate_passes_for_valid_test_cases():
    """Check that a proper test case passes validation"""
    test_cases = [{
        "TC_ID": "TC_001",
        "Category": "Functional",
        "Title": "Valid login",
        "Precondition": "User on login page",
        "Test Steps": "1. Enter email 2. Click login",
        "Expected Result": "User redirected to dashboard",
        "Priority": "High",
        "Status": "Not Executed"
    }]
    result = validate_test_cases(test_cases)
    assert result["valid"] == True
    assert result["count"] == 1


def test_validate_fails_for_empty_list():
    """Check that an empty list fails validation"""
    result = validate_test_cases([])
    assert result["valid"] == False
    assert "No test cases" in result["issues"][0]


def test_validate_catches_missing_title():
    """Check that a test case with no title is flagged"""
    test_cases = [{
        "TC_ID": "TC_001",
        "Category": "Functional",
        "Title": "",
        "Precondition": "User on login page",
        "Test Steps": "1. Do something",
        "Expected Result": "Something happens",
        "Priority": "High",
        "Status": "Not Executed"
    }]
    result = validate_test_cases(test_cases)
    assert result["valid"] == False


def test_validate_catches_invalid_priority():
    """Check that an invalid priority like Extreme is flagged"""
    test_cases = [{
        "TC_ID": "TC_001",
        "Category": "Functional",
        "Title": "Valid login",
        "Precondition": "User on login page",
        "Test Steps": "1. Do something",
        "Expected Result": "Something happens",
        "Priority": "Extreme",
        "Status": "Not Executed"
    }]
    result = validate_test_cases(test_cases)
    assert result["valid"] == False


def test_validate_catches_invalid_category():
    """Check that an invalid category like Random is flagged"""
    test_cases = [{
        "TC_ID": "TC_001",
        "Category": "Random",
        "Title": "Valid login",
        "Precondition": "User on login page",
        "Test Steps": "1. Do something",
        "Expected Result": "Something happens",
        "Priority": "High",
        "Status": "Not Executed"
    }]
    result = validate_test_cases(test_cases)
    assert result["valid"] == False


def test_validate_returns_correct_count():
    """Check that the count field matches the number of test cases passed in"""
    test_cases = [
        {
            "TC_ID": "TC_001",
            "Category": "Functional",
            "Title": "Test 1",
            "Precondition": "Setup",
            "Test Steps": "1. Do something",
            "Expected Result": "Result",
            "Priority": "High",
            "Status": "Not Executed"
        },
        {
            "TC_ID": "TC_002",
            "Category": "Negative",
            "Title": "Test 2",
            "Precondition": "Setup",
            "Test Steps": "1. Do something",
            "Expected Result": "Result",
            "Priority": "Medium",
            "Status": "Not Executed"
        }
    ]
    result = validate_test_cases(test_cases)
    assert result["count"] == 2
