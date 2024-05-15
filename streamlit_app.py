import streamlit as st
import pandas as pd
import pickle

# Assuming attend_sys has functions to load and save data, which it now needs to export
import attend_sys

def load_data():
    try:
        with open('data.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("Data file not found. Please ensure data exists before matching.")
        return {}
    return data

def display_data(data):
    if data:
        df = pd.DataFrame(data).T  # Transpose to align with Streamlit's preferred DataFrame structure
        st.dataframe(df)
    else:
        st.write("No data available.")

def main():
    st.title('Student Attendance System')

    data = load_data()
    display_data(data)

    if st.button('Refresh Data'):
        data = load_data()  # Reload data
        display_data(data)

if __name__ == "__main__":
    main()
