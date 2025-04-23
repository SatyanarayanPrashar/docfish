import streamlit as st

def show():
    st.title("Installation Page")
    st.write("Here's how you install it.")

with open("Document/Installation.md", "r") as file:
        installation_content = file.read()

st.markdown(installation_content)