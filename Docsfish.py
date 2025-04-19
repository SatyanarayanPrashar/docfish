import streamlit as st
from query import create

st.set_page_config(page_title="Docsfish", page_icon="docsfish.png", layout="wide")
st.markdown("<h1 style='font-size:36px;'>Build Documentation with AI in minutes</h1>", unsafe_allow_html=True)
github_repo_url = st.text_input("Enter the github repo URL", key="repo_url")

def handle_generate_click():
    if github_repo_url:
        st.info(f"Starting documentation generation for: {github_repo_url}")
        repo_name = github_repo_url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        cloned_repo_path = f"./{repo_name}"

        create(cloned_repo_path)
        st.success("Documentation generation process initiated.")
    else:
        st.warning("Please enter a GitHub repository URL.")

st.button("Generate Documentation", key="generate_docs", on_click=handle_generate_click)