"""
main.py – Entry point for GBT‑Editor (flat layout)
Run with:
    streamlit run main.py
"""

import streamlit as st
import os
import json
import importlib
import subprocess
import uuid

# -----------------------------------------------------------------------------
# 1. Config loader (flat path)
# -----------------------------------------------------------------------------
def load_config(file_name="production.json"):
    if not os.path.exists(file_name):
        st.error(f"Config file '{file_name}' not found.")
        st.stop()
    with open(file_name, "r") as cfg:
        return json.load(cfg)

CONFIG = load_config()

# -----------------------------------------------------------------------------
# 2. Dynamic module imports (flat layout → direct import by filename)
# -----------------------------------------------------------------------------
chat_engine = importlib.import_module("chat_engine")
utils       = importlib.import_module("utils")
ui_editor   = importlib.import_module("editor")
versioning  = importlib.import_module("versioning")
deployer    = importlib.import_module("deployer")
deploy_hook = importlib.import_module("deploy_hook")
# (github_plugin or others can be imported similarly if needed)

# -----------------------------------------------------------------------------
# 3. Basic authentication (demo only)
# -----------------------------------------------------------------------------
def simple_auth():
    user = st.sidebar.text_input("Username")
    pwd  = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user == CONFIG.get("developer", {}).get("username", "admin") and \
           pwd  == CONFIG.get("developer", {}).get("password", "admin123"):
            st.session_state.user = user
            st.success("Logged in!")
        else:
            st.error("Bad credentials")

if "user" not in st.session_state:
    simple_auth()
    st.stop()

# -----------------------------------------------------------------------------
# 4. Main UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="GBT‑Editor", page_icon="🧠", layout="wide")
st.title("🧠  GBT‑Editor – Flat Layout")

st.sidebar.markdown("### Project actions")
action = st.sidebar.selectbox("Choose action", ["Create / Edit App", "Deploy", "Version Info"])

# -----------------------------------------------------------------------------
# 4A. Create / Edit App (openAI → Streamlit generator, simplified)
# -----------------------------------------------------------------------------
if action == "Create / Edit App":
    prompt = st.text_area("Describe the Streamlit app you want to build or update:", height=150)
    if st.button("Generate / Update Code"):
        code = chat_engine.generate_streamlit_code(prompt)   # Must exist in chat_engine.py
        file_name = f"{st.session_state.user}_app.py"
        with open(file_name, "w") as f:
            f.write(code)
        st.success(f"Saved to {file_name}")
        st.code(code, language="python")

# -----------------------------------------------------------------------------
# 4B. Deploy (simple subprocess using deployer.py)
# -----------------------------------------------------------------------------
elif action == "Deploy":
    st.write("Enter the filename you want to deploy (e.g., `john_app.py`):")
    app_file = st.text_input("App filename")
    if st.button("Deploy App"):
        if os.path.exists(app_file):
            port = deployer.deploy_streamlit(app_file)  # Must exist in deployer.py
            st.success(f"App deployed on http://localhost:{port}")
        else:
            st.error("File not found.")

# -----------------------------------------------------------------------------
# 4C. Version info
# -----------------------------------------------------------------------------
elif action == "Version Info":
    st.write(f"Current version: **{versioning.get_version()}**")
    if st.button("Bump patch version"):
        versioning.bump_version("patch")
        st.experimental_rerun()

# -----------------------------------------------------------------------------
# 5. Footer
# -----------------------------------------------------------------------------
st.write("---")
st.write("© 2025 GBT‑Editor Flat Edition")

