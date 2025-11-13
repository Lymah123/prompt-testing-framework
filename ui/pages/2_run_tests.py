import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.storage.manager import StorageManager
from src.core.runner import TestRunner
from src.core.models import TestCase, Expectation
from datetime import datetime

st.set_page_config(page_title="Run Tests", page_icon="▶️", layout="wide")

st.title("▶️ Run Tests")

storage = StorageManager()
runner = TestRunner()

# Load test cases
test_cases = storage.get_all_test_cases()

if not test_cases:
    st.warning("No test cases available. Create some in the Test Cases page first!")
else:
    st.write(f"Found {len(test_cases)} test case(s)")
    
    # Select tests to run
    st.subheader("Select Tests to Run")
    
    run_all = st.checkbox("Run All Tests", value=False)
    
    if not run_all:
        selected_tests = st.multiselect(
            "Select specific tests",
            options=[tc['id'] for tc in test_cases],
            format_func=lambda x: next(tc['name'] for tc in test_cases if tc['id'] == x),
            default=[]
        )
    else:
        selected_tests = [tc['id'] for tc in test_cases]
    
    if st.button("▶️ Run Selected Tests", type="primary", disabled=len(selected_tests) == 0):
        st.divider()
        st.subheader("Test Results")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results_container = st.container()
        
        for idx, test_id in enumerate(selected_tests):
            # Update progress
            progress = (idx) / len(selected_tests)
            progress_bar.progress(progress)
            
            # Get test case
            test_data = storage.get_test_case(test_id)
            status_text.text(f"Running: {test_data['name']}...")
            
            # Convert to TestCase object
            expectations = [
                Expectation(**exp) for exp in test_data.get('expectations', [])
            ]
            
            test_case = TestCase(
                id=test_data['id'],
                name=test_data['name'],
                prompt=test_data['prompt'],
                provider=test_data['provider'],
                model=test_data['model'],
                system_prompt=test_data.get('system_prompt'),
                temperature=test_data.get('temperature', 1.0),
                max_tokens=test_data.get('max_tokens', 1024),
                expectations=expectations,
                tags=test_data.get('tags', [])
            )
            
            # Run test
            with results_container:
                with st.expander(f"📋 {test_case.name}", expanded=True):
                    result_placeholder = st.empty()
                    
                    with result_placeholder.container():
                        st.info("⏳ Running test...")
                    
                    result = runner.run_test(test_case)
                    
                    # Save result
                    storage.save_result(result)
                    
                    # Display result
                    with result_placeholder.container():
                        if result.error:
                            st.error(f"❌ Error: {result.error}")
                        else:
                            # Status
                            if result.passed is True:
                                st.success("✅ Test Passed")
                            elif result.passed is False:
                                st.error("❌ Test Failed")
                            else:
                                st.warning("⚠️ Manual Review Required")
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Execution Time", f"{result.execution_time:.2f}s")
                            with col2:
                                st.metric("Model", result.model)
                            with col3:
                                st.metric("Provider", result.provider)
                            
                            # Prompt
                            st.markdown("**Prompt:**")
                            st.code(result.prompt, language=None)
                            
                            # Response
                            st.markdown("**Response:**")
                            st.write(result.response)
                            
                            # Evaluation Results
                            if result.evaluation_results:
                                st.markdown("**Evaluation Results:**")
                                for eval_result in result.evaluation_results:
                                    status_icon = "✅" if eval_result['passed'] else "❌" if eval_result['passed'] is False else "⚠️"
                                    st.caption(f"{status_icon} {eval_result['description']} - {eval_result['details']}")
        
        # Complete
        progress_bar.progress(1.0)
        status_text.text("✅ All tests completed!")
        st.balloons()