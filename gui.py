import tkinter as tk
from tkinter import ttk
import threading
import attend_sys as a
import pickle

class AttendanceApp:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Attendance System")
        self.load_data()
        self.setup_widgets()
        self.running = False
        self.thread = None

    def load_data(self):
        try:
            with open('data.pkl', 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Returning empty data structure.")
            self.data = {}

    def setup_widgets(self):
        self.tree = ttk.Treeview(self.master, columns=('Roll No', 'Status'), show='headings')
        self.tree.heading('Roll No', text='Roll No')
        self.tree.heading('Status', text='Status')
        for roll_no in self.data.keys():
            if roll_no!='noise':
                self.tree.insert('', 'end', values=(roll_no, 'Absent'))
        self.tree.pack(expand=True, fill='both')

        self.start_button = ttk.Button(self.master, text="Start", command=self.start_matching)
        self.start_button.pack(side=tk.LEFT, padx=(20, 10), pady=20)

        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_matching)
        self.stop_button.pack(side=tk.LEFT, padx=(10, 20), pady=20)

    def start_matching(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.thread = threading.Thread(target=self.process_audio_loop)
            self.thread.start()

    def stop_matching(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def process_audio_loop(self):
        while self.running:
            matched_student = a.continuous_matching()  # Ensure this function returns the matched student ID
            self.update_status(matched_student)

    def update_status(self, match):
        self.master.after(0, self.update_tree_view, match)

    def update_tree_view(self, match):
        for item in self.tree.get_children():
            roll_no = self.tree.item(item, "values")[0]
            attendance = self.tree.item(item, "values")[1]
            if roll_no != match and attendance == "Absent":
                self.tree.item(item, tags=())

        if match:
            for item in self.tree.get_children():
                roll_no = self.tree.item(item, 'values')[0]
                if roll_no == match and roll_no:
                    self.tree.item(item, values=(roll_no, 'Present'), tags=('present',))
                    self.tree.tag_configure('present', background='light green')

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
