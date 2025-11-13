import streamlit as st
import sys
from pathlib import Path
import subprocess

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Prompt Testing Framework",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧪 Prompt Testing Framework")
st.markdown("""
Welcome to the Prompt Testing Framework! This tool helps you:
- Create and manage prompt test cases
- Run tests against AI models (Claude, OpenAI)
- Evaluate responses with automated assertions
- Track results over time

### Getting Started
1. **Test Cases** - Create and manage your test cases
2. **Run Tests** - Execute tests and see results in real-time
3. **Results** - View historical test results and analytics

Navigate using the sidebar to get started! 👈
""")

# Display quick stats
from src.storage.manager import StorageManager

storage = StorageManager()
test_cases = storage.get_all_test_cases()
results = storage.get_all_results()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Test Cases", len(test_cases))
with col2:
    st.metric("Total Runs", len(results))
with col3:
    passed = sum(1 for r in results if r.get('passed') == True)
    st.metric("Tests Passed", passed)
with col4:
    failed = sum(1 for r in results if r.get('passed') == False)
    st.metric("Tests Failed", failed)

# Show recent results
if results:
    st.subheader("Recent Test Runs")
    recent = sorted(results, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
    
    for result in recent:
        with st.expander(f"📋 {result['test_name']} - {result.get('timestamp', 'N/A')[:19]}"):
            status = "✅ Passed" if result.get('passed') else "❌ Failed" if result.get('passed') is False else "⚠️ Manual Review"
            st.write(f"**Status:** {status}")
            st.write(f"**Model:** {result['model']}")
            st.write(f"**Execution Time:** {result['execution_time']:.2f}s")

def main():
    # Launch the Streamlit app if run as a CLI command
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    main()