def build_prompt(feature_description: str) -> str:
    return f"""You are a Senior QA Engineer with 10 years of experience in software testing.

Given the following feature description, generate comprehensive test cases.

FEATURE:
{feature_description}

Generate test cases in the following categories:
1. Functional (positive) - happy path scenarios
2. Negative - invalid inputs, error handling
3. Boundary - edge values, limits
4. Security - injection, unauthorised access
5. UI/UX - usability, content, labels
6. Integration - how this feature connects to other modules

For each test case provide exactly these fields separated by | symbol:
TC_ID | Category | Title | Precondition | Test Steps | Expected Result | Priority | Status

Rules:
- TC_ID format: TC_001, TC_002 etc
- Category: Functional / Negative / Boundary / Security / UI-UX / Integration
- Priority: High / Medium / Low
- Status: Not Executed
- Test Steps: number each step like 1. 2. 3.
- Be specific, clear, and concise
- Cover at least 15 test cases minimum
- Do not add any explanation before or after the test cases
- Start directly with TC_001

OUTPUT FORMAT EXAMPLE:
TC_001 | Functional | Valid login with correct credentials | User is on login page | 1. Enter valid email 2. Enter valid password 3. Click Login | User is redirected to dashboard | High | Not Executed
"""
