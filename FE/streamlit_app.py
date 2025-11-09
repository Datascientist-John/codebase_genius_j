import streamlit as st
import requests
import json
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="GitHub Documentation Generator",
    page_icon="📚",
    layout="wide",
)

# --- CSS STYLING ---
st.markdown("""
    <style>
        .main > div {
            max-width: 1200px;
            padding: 2rem;
        }
        
        .stButton>button {
            width: 100%;
            background-color: #0366d6;
            color: white;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #0256c7;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(3, 102, 214, 0.3);
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
        }
        
        .status-success {
            background-color: #28a745;
            color: white;
        }
        
        .status-error {
            background-color: #dc3545;
            color: white;
        }
        
        .result-card {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTS ---
BASE_URL = "http://localhost:8000"
GENERATE_DOCS_ENDPOINT = f"{BASE_URL}/walker/generate_docs"
HEALTH_CHECK_ENDPOINT = f"{BASE_URL}/walker/health_check"

# --- SESSION STATE INIT ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Health Check
    st.subheader("Server Status")
    if st.button("🔍 Check Health"):
        try:
            response = requests.post(HEALTH_CHECK_ENDPOINT, timeout=5)
            if response.status_code == 200:
                st.success("✅ Server is healthy!")
            else:
                st.error(f"❌ Server responded with: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to server. Make sure `jac serve main.jac` is running!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # History Management
    st.subheader("📜 History")
    if st.session_state.history:
        st.write(f"Total generations: {len(st.session_state.history)}")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No generation history yet")
    
    st.divider()
    
    # Instructions
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. Make sure Jac server is running:
           ```bash
           jac serve main.jac
           ```
        2. Enter a valid GitHub repository URL
        3. Click "Generate Documentation"
        4. Wait for the AI to analyze the repository
        5. Review the generated documentation
        """)

# --- MAIN CONTENT ---
st.title("📚 GitHub Documentation Generator")
st.markdown("AI-powered documentation generation from GitHub repositories using **Gemini 2.0 Flash**")

# Input Section
st.subheader("🔗 Repository URL")
col1, col2 = st.columns([4, 1])

with col1:
    github_url = st.text_input(
        "Enter GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed"
    )

with col2:
    generate_button = st.button("🚀 Generate", use_container_width=True)

# Validation and Generation
if generate_button:
    if not github_url:
        st.error("⚠️ Please enter a GitHub URL")
    elif not github_url.startswith("https://github.com/"):
        st.error("⚠️ Invalid GitHub URL. Must start with https://github.com/")
    elif len(github_url.split("/")) < 5:
        st.error("⚠️ Invalid GitHub URL format. Expected: https://github.com/owner/repo")
    else:
        # Show loading state
        with st.spinner("🤖 AI is analyzing the repository... This may take a few minutes."):
            try:
                # Make request to Jac server
                response = requests.post(
                    GENERATE_DOCS_ENDPOINT,
                    json={"github_url": github_url},
                    timeout=300  # 5 minute timeout
                )
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        
                        # Add to history
                        st.session_state.history.append({
                            "url": github_url,
                            "timestamp": datetime.now().isoformat(),
                            "result": result,
                            "success": True
                        })
                        
                        # Display success
                        st.success("✅ Documentation generated successfully!")
                        
                        # Display results
                        st.subheader("📄 Generated Documentation")
                        
                        # Pretty print the result
                        st.json(result)
                        
                        # Download button
                        result_json = json.dumps(result, indent=2)
                        st.download_button(
                            label="⬇️ Download Documentation (JSON)",
                            data=result_json,
                            file_name=f"docs_{github_url.split('/')[-1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        
                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON response from server")
                        st.code(response.text)
                else:
                    st.error(f"❌ Server error: {response.status_code}")
                    try:
                        error_detail = response.json()
                        st.json(error_detail)
                    except:
                        st.code(response.text)
                        
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. The repository might be too large or the server is busy.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to server. Make sure `jac serve main.jac` is running on port 8000!")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                
                # Add failed attempt to history
                st.session_state.history.append({
                    "url": github_url,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "success": False
                })

# Display History
if st.session_state.history:
    st.divider()
    st.subheader("📜 Generation History")
    
    for idx, item in enumerate(reversed(st.session_state.history)):
        with st.expander(
            f"{'✅' if item['success'] else '❌'} {item['url']} - {datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}"
        ):
            if item['success']:
                st.json(item['result'])
                
                # Download button for historical items
                result_json = json.dumps(item['result'], indent=2)
                st.download_button(
                    label="⬇️ Download",
                    data=result_json,
                    file_name=f"docs_history_{len(st.session_state.history)-idx}.json",
                    mime="application/json",
                    key=f"download_{idx}"
                )
            else:
                st.error(f"Error: {item.get('error', 'Unknown error')}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.875rem;'>
    <p>Powered by <strong>Gemini 2.0 Flash</strong> • Built with <strong>Jac</strong> and <strong>Streamlit</strong></p>
</div>
""", unsafe_allow_html=True)