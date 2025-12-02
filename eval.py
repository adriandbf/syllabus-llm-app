import json
import re
from rag import answer_question

TEST_FILE = "tests.json"


def run_evaluation():
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        tests = json.load(f)

    total = len(tests)
    passed = 0

    print("Offline Evaluation Results:\n")

    for i, test in enumerate(tests, start=1):
        question = test["input"]
        expected_pattern = test["expected_pattern"]

        try:
            answer = answer_question(question)
        except Exception as e:
            print(f"{i}. Question: {question}\n   Error: {e}\n")
            continue

        if re.search(expected_pattern, answer, re.IGNORECASE):
            result = "PASS"
            passed += 1
        else:
            result = "FAIL"

        print(f"{i}. Question: {question}\n   Answer: {answer}\n   Result: {result}\n")

    pass_rate = (passed / total) * 100
    print(f"Overall Pass Rate: {passed}/{total} = {pass_rate:.1f}%")


if __name__ == "__main__":
    run_evaluation()