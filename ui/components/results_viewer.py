import streamlit as st
import json
from datetime import datetime

def format_timestamp(ts):
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts

def color_status(status):
    if status.lower() == "pass":
        return "✅"
    elif status.lower() == "fail":
        return "❌"
    else:
        return "⚪"

def show_results(results_path="data/results.json"):
    st.header("Test Results")
    try:
        with open(results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        if not results:
            st.info("No results found.")
            return

        # Summary Table
        st.subheader("Summary")
        summary_data = [
            {
                "Test Name": r.get("test_name", "Unnamed"),
                "Status": color_status(r.get("status", "unknown")),
                "Score": r.get("score", "-"),
                "Timestamp": format_timestamp(r.get("timestamp", "-")),
            }
            for r in results
        ]
        st.dataframe(summary_data, hide_index=True, use_container_width=True)

        # Detailed View
        st.subheader("Detailed Results")
        for idx, result in enumerate(results, 1):
            with st.expander(f"{color_status(result.get('status', 'unknown'))} {result.get('test_name', 'Unnamed Test')}"):
                st.markdown(f"**Status:** {color_status(result.get('status', 'unknown'))} {result.get('status', '').capitalize()}")
                st.markdown(f"**Score:** {result.get('score', '-')}")
                st.markdown(f"**Timestamp:** {format_timestamp(result.get('timestamp', '-'))}")
                st.markdown("**Prompt:**")
                st.code(result.get("prompt", ""), language="markdown")
                st.markdown("**Expected Output:**")
                st.code(result.get("expected_output", ""), language="markdown")
                st.markdown("**Actual Output:**")
                st.code(result.get("actual_output", ""), language="markdown")
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                if "details" in result:
                    st.markdown("**Details:**")
                    st.json(result["details"])
    except FileNotFoundError:
        st.warning(f"Results file not found at {results_path}.")
    except json.JSONDecodeError:
        st.error("Results file is not valid JSON.")

# Usage in a Streamlit page:
# from ui.components.results_viewer import show_results
# show_results()