import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import uuid

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.storage.manager import StorageManager
from src.core.models import TestCase, Expectation, EvaluationType

st.set_page_config(page_title="Test Cases", page_icon="📝", layout="wide")

st.title("📝 Test Cases")

storage = StorageManager()

# Sidebar for creating/editing
with st.sidebar:
    st.header("Create/Edit Test Case")
    
    # Load existing test cases for editing
    test_cases = storage.get_all_test_cases()
    test_case_names = ["+ New Test Case"] + [f"{tc['name']} ({tc['id'][:8]})" for tc in test_cases]
    selected = st.selectbox("Select Test Case", test_case_names)
    
    # Determine if editing or creating
    if selected == "+ New Test Case":
        editing = False
        test_data = None
    else:
        editing = True
        test_id = selected.split("(")[-1].strip(")")
        test_data = next((tc for tc in test_cases if tc['id'].startswith(test_id)), None)
    
    # Form
    with st.form("test_case_form"):
        name = st.text_input("Test Name", value=test_data['name'] if test_data else "")
        
        col1, col2 = st.columns(2)
        with col1:
            provider = st.selectbox(
                "Provider",
                ["claude", "openai", "goose"],
                index=0 if not test_data else (0 if test_data['provider'] == "claude" else 1)
            )
        with col2:
            model = st.text_input(
                "Model",
                value=test_data.get('model', 'claude-sonnet-4-20250514') if test_data else 'claude-sonnet-4-20250514'
            )
        
        prompt = st.text_area(
            "Prompt",
            value=test_data['prompt'] if test_data else "",
            height=150
        )
        
        system_prompt = st.text_area(
            "System Prompt (optional)",
            value=test_data.get('system_prompt', '') if test_data else "",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider(
                "Temperature",
                0.0, 2.0,
                value=test_data.get('temperature', 1.0) if test_data else 1.0,
                step=0.1
            )
        with col2:
            max_tokens = st.number_input(
                "Max Tokens",
                100, 4000,
                value=test_data.get('max_tokens', 1024) if test_data else 1024
            )
        
        tags = st.text_input(
            "Tags (comma-separated)",
            value=", ".join(test_data.get('tags', [])) if test_data else ""
        )
        
        st.subheader("Expectations")
        st.caption("Add automated checks for the response")
        
        # Expectations
        num_expectations = st.number_input("Number of Expectations", 0, 10, value=len(test_data.get('expectations', [])) if test_data else 0)
        
        expectations = []
        for i in range(num_expectations):
            st.markdown(f"**Expectation {i+1}**")
            exp_data = test_data['expectations'][i] if test_data and i < len(test_data.get('expectations', [])) else {}
            
            col1, col2 = st.columns([1, 2])
            with col1:
                exp_type = st.selectbox(
                    "Type",
                    [e.value for e in EvaluationType],
                    key=f"exp_type_{i}",
                    index=[e.value for e in EvaluationType].index(exp_data.get('type', 'contains')) if exp_data else 0
                )
            with col2:
                exp_value = st.text_input(
                    "Value",
                    key=f"exp_value_{i}",
                    value=str(exp_data.get('value', '')) if exp_data else ""
                )
            
            exp_desc = st.text_input(
                "Description (optional)",
                key=f"exp_desc_{i}",
                value=exp_data.get('description', '') if exp_data else ""
            )
            
            expectations.append({
                'type': exp_type,
                'value': exp_value,
                'description': exp_desc
            })
        
        submitted = st.form_submit_button("💾 Save Test Case", use_container_width=True)
        
        if submitted:
            if not name or not prompt:
                st.error("Name and Prompt are required!")
            else:
                try:
                    # Create expectations
                    exp_objects = [
                        Expectation(
                            type=EvaluationType(exp['type']),
                            value=exp['value'],
                            description=exp['description'] or None
                        )
                        for exp in expectations
                    ]
                    
                    # Create test case
                    test_case = TestCase(
                        id=test_data['id'] if test_data else str(uuid.uuid4()),
                        name=name,
                        prompt=prompt,
                        provider=provider,
                        model=model,
                        system_prompt=system_prompt or None,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        expectations=exp_objects,
                        tags=[t.strip() for t in tags.split(",") if t.strip()]
                    )
                    
                    storage.save_test_case(test_case)
                    st.success(f"✅ Test case {'updated' if editing else 'created'} successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Main area - Display test cases
st.header("All Test Cases")

test_cases = storage.get_all_test_cases()

if not test_cases:
    st.info("No test cases yet. Create one using the sidebar!")
else:
    # Filter
    search = st.text_input("🔍 Search test cases", "")
    
    filtered_cases = test_cases
    if search:
        filtered_cases = [
            tc for tc in test_cases
            if search.lower() in tc['name'].lower() or search.lower() in tc['prompt'].lower()
        ]
    
    st.write(f"Showing {len(filtered_cases)} test case(s)")
    
    for tc in filtered_cases:
        with st.expander(f"📋 {tc['name']}", expanded=False):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**ID:** `{tc['id'][:8]}...`")
                st.write(f"**Provider:** {tc['provider']}")
                st.write(f"**Model:** {tc['model']}")
            
            with col2:
                st.write(f"**Temperature:** {tc.get('temperature', 1.0)}")
                st.write(f"**Max Tokens:** {tc.get('max_tokens', 1024)}")
            
            with col3:
                if tc.get('tags'):
                    st.write("**Tags:**")
                    for tag in tc['tags']:
                        st.caption(f"🏷️ {tag}")
            
            st.markdown("**Prompt:**")
            st.code(tc['prompt'], language=None)
            
            if tc.get('system_prompt'):
                st.markdown("**System Prompt:**")
                st.code(tc['system_prompt'], language=None)
            
            if tc.get('expectations'):
                st.markdown("**Expectations:**")
                for i, exp in enumerate(tc['expectations'], 1):
                    st.caption(f"{i}. {exp['type']}: {exp['value']}")
            
            # Delete button
            if st.button(f"🗑️ Delete", key=f"delete_{tc['id']}"):
                storage.delete_test_case(tc['id'])
                st.success("Test case deleted!")
                st.rerun()