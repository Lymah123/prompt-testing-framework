import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.storage.manager import StorageManager

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

st.title("📊 Test Results")

storage = StorageManager()
results = storage.get_all_results()

if not results:
    st.info("No test results yet. Run some tests first!")
else:
    st.write(f"Total test runs: {len(results)}")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    passed = sum(1 for r in results if r.get('passed') == True)
    failed = sum(1 for r in results if r.get('passed') == False)
    manual = sum(1 for r in results if r.get('passed') is None)
    avg_time = sum(r['execution_time'] for r in results) / len(results)
    
    with col1:
        st.metric("Passed", passed, f"{passed/len(results)*100:.1f}%")
    with col2:
        st.metric("Failed", failed, f"{failed/len(results)*100:.1f}%")
    with col3:
        st.metric("Manual Review", manual)
    with col4:
        st.metric("Avg Time", f"{avg_time:.2f}s")
    
    st.divider()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.multiselect(
            "Filter by Status",
            ["Passed", "Failed", "Manual Review"],
            default=["Passed", "Failed", "Manual Review"]
        )
    
    with col2:
        test_names = list(set(r['test_name'] for r in results))
        filter_tests = st.multiselect(
            "Filter by Test",
            test_names,
            default=test_names
        )
    
    with col3:
        models = list(set(r['model'] for r in results))
        filter_models = st.multiselect(
            "Filter by Model",
            models,
            default=models
        )
    
    # Filter results
    filtered = results
    
    status_map = {
        "Passed": True,
        "Failed": False,
        "Manual Review": None
    }
    filtered_status = [status_map[s] for s in filter_status]
    filtered = [r for r in filtered if r.get('passed') in filtered_status]
    filtered = [r for r in filtered if r['test_name'] in filter_tests]
    filtered = [r for r in filtered if r['model'] in filter_models]
    
    st.write(f"Showing {len(filtered)} result(s)")
    
    # Sort by timestamp (newest first)
    filtered = sorted(filtered, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Display results
    for result in filtered:
        status_icon = "✅" if result.get('passed') == True else "❌" if result.get('passed') == False else "⚠️"
        timestamp = result.get('timestamp', 'N/A')
        if timestamp != 'N/A':
            timestamp = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        
        with st.expander(f"{status_icon} {result['test_name']} - {timestamp}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**Provider:** {result['provider']}")
            with col2:
                st.write(f"**Model:** {result['model']}")
            with col3:
                st.write(f"**Execution Time:** {result['execution_time']:.2f}s")
            with col4:
                status_text = "Passed" if result.get('passed') == True else "Failed" if result.get('passed') == False else "Manual Review"
                st.write(f"**Status:** {status_text}")
            
            if result.get('error'):
                st.error(f"Error: {result['error']}")
            
            st.markdown("**Prompt:**")
            st.code(result['prompt'], language=None)
            
            st.markdown("**Response:**")
            st.write(result['response'])
            
            if result.get('evaluation_results'):
                st.markdown("**Evaluation Results:**")
                for eval_result in result['evaluation_results']:
                    status = "✅" if eval_result['passed'] else "❌" if eval_result['passed'] is False else "⚠️"
                    st.caption(f"{status} {eval_result['description']} - {eval_result['details']}")
    
    # Export
    st.divider()
    if st.button("📥 Export Results as JSON"):
        import json
        json_str = json.dumps(filtered, indent=2, default=str)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )