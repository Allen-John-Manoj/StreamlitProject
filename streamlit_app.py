import streamlit as st
import pandas as pd
import pickle
import subprocess

# Load the data from data.pkl
with open('data.pkl', 'rb') as file:
    data = pickle.load(file)

# Convert the data into a DataFrame for easy display
df = pd.DataFrame(data)

# Define the main app
def main():
    st.title("Automatic Attendance System")
    
    menu = ["Home", "Attendance System", "Voice Recognition", "Data Visualization"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the Automatic Attendance System.")
    
    elif choice == "Attendance System":
        st.subheader("Attendance System")
        st.write("Displaying student details and marking attendance.")
        st.dataframe(df)
        
        # Mark attendance (simplified for demonstration)
        if st.button("Mark Attendance"):
            result = subprocess.run(["python3", "attend_sys.py"], capture_output=True, text=True)
            st.write(result.stdout)
            st.success("Voice recognized and attendance marked.")
    
    elif choice == "Voice Recognition":
        st.subheader("Voice Recognition")
        st.write("Record and recognize voice to mark attendance.")
        
        # Add a button to start the voice recognition process
        if st.button("Start Voice Recognition"):
            result = subprocess.run(["python3", "rec_audio.py"], capture_output=True, text=True)
            st.write(result.stdout)
            st.success("Voice recognized and attendance marked.")
    
    elif choice == "Data Visualization":
        st.subheader("Data Visualization")
        st.write("Displaying data from data.pkl.")
        st.dataframe(df)

if __name__ == '__main__':
    main()
