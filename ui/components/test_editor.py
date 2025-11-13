import streamlit as st
import json
import os

TEST_CASES_PATH = "data/test_cases.json"

def load_test_cases():
    if not os.path.exists(TEST_CASES_PATH):
        return []
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_test_cases(test_cases):
    with open(TEST_CASES_PATH, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

def test_editor():
    st.header("Test Case Editor")
    test_cases = load_test_cases()

    # List existing test cases
    st.subheader("Existing Test Cases")
    for idx, tc in enumerate(test_cases):
        with st.expander(f"{tc.get('test_name', f'Test {idx+1}')}"):
            st.markdown(f"**Prompt:**\n{tc.get('prompt', '')}")
            st.markdown(f"**Expected Output:**\n{tc.get('expected_output', '')}")
            if st.button("Delete", key=f"delete_{idx}"):
                test_cases.pop(idx)
                save_test_cases(test_cases)
                st.experimental_rerun()

    # Add new test case
    st.subheader("Add New Test Case")
    with st.form("add_test_case"):
        test_name = st.text_input("Test Name")
        prompt = st.text_area("Prompt")
        expected_output = st.text_area("Expected Output")
        submitted = st.form_submit_button("Add Test Case")
        if submitted:
            if test_name and prompt and expected_output:
                test_cases.append({
                    "test_name": test_name,
                    "prompt": prompt,
                    "expected_output": expected_output
                })
                save_test_cases(test_cases)
                st.success("Test case added!")
                st.experimental_rerun()
            else:
                st.warning("Please fill in all fields.")

# Usage in a Streamlit page:
# from ui.components.test_editor import test_editor
# test_editor()