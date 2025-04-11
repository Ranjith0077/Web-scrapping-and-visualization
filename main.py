import streamlit as st
from src.filter import filtered
from src.visual import visual

def main():
    st.title("Movies 2024 Database")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home", "Filter Movies","Visualization"])

    if page == "Home":
        st.write("Welcome to the Movies 2024 Database!")
    elif page == "Filter Movies":
        st.write("Filter movies based on your preferences.")
        # Here you would call the filter function from filter.py
        # For example:
        
        filtered()
    elif page=="Visualization":
        st.write("Visualize Movies")
        
        visual()

if __name__ == "__main__":
    main()