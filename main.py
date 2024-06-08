import json
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet

# Encryption key and Fernet object
key = Fernet.generate_key()
fernet = Fernet(key)

DATABASE_FILE = 'text_storage.json'


class TextStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Storage Application")
        self.root.configure(bg='black')

        self.current_mode = 'normal'

        self.database = self.load_database()

        self.setup_ui()

    def load_database(self):
        try:
            with open(DATABASE_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"normal": {}, "line_by_line": {}}

    def save_database(self):
        with open(DATABASE_FILE, 'w') as file:
            json.dump(self.database, file, indent=4)

    def setup_ui(self):
        self.root.state('zoomed')  # Make window full screen
        self.font = ('Arial', 14)
        self.title_font = ('Arial', 24, 'bold')

        # Title
        title_label = tk.Label(self.root, text="Text Storer", bg='black', fg='white', font=self.title_font)
        title_label.pack(pady=10)

        self.mode_var = tk.StringVar(value=self.current_mode)

        # Mode Switch Buttons
        modes_frame = tk.Frame(self.root, bg='black')
        modes_frame.pack(pady=10)

        tk.Radiobutton(modes_frame, text="Normal Mode", variable=self.mode_var, value='normal',
                       command=self.switch_mode, bg='black', fg='white', selectcolor='blue', font=self.font).pack(side='left')
        tk.Radiobutton(modes_frame, text="Line-by-Line Mode", variable=self.mode_var, value='line_by_line',
                       command=self.switch_mode, bg='black', fg='white', selectcolor='blue', font=self.font).pack(side='left')
        tk.Radiobutton(modes_frame, text="Normal Retrieval", variable=self.mode_var, value='normal_retrieval',
                       command=self.switch_mode, bg='black', fg='white', selectcolor='blue', font=self.font).pack(side='left')
        tk.Radiobutton(modes_frame, text="Line-by-Line Retrieval", variable=self.mode_var,
                       value='line_by_line_retrieval', command=self.switch_mode, bg='black', fg='white',
                       selectcolor='blue', font=self.font).pack(side='left')

        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(pady=20)

        self.switch_mode()

    def switch_mode(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        mode = self.mode_var.get()

        if mode == 'normal':
            self.setup_normal_mode()
        elif mode == 'line_by_line':
            self.setup_line_by_line_mode()
        elif mode == 'normal_retrieval':
            self.setup_normal_retrieval_mode()
        elif mode == 'line_by_line_retrieval':
            self.setup_line_by_line_retrieval_mode()

    def setup_normal_mode(self):
        tk.Label(self.main_frame, text="Subject:", bg='black', fg='white', font=self.font).grid(row=0, column=0, padx=5, pady=5)
        self.normal_subject_entry = tk.Entry(self.main_frame, width=50, font=self.font)
        self.normal_subject_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.main_frame, text="Text:", bg='black', fg='white', font=self.font).grid(row=1, column=0, padx=5, pady=5)
        self.normal_text_entry = tk.Text(self.main_frame, width=50, height=10, font=self.font)
        self.normal_text_entry.grid(row=1, column=1, padx=5, pady=5)

        commit_button = tk.Button(self.main_frame, text="Commit", command=self.commit_normal, bg='blue', fg='white', font=self.font)
        commit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def commit_normal(self):
        subject = self.normal_subject_entry.get().strip()
        text = self.normal_text_entry.get("1.0", tk.END).strip()

        if subject and text:
            enc_text = fernet.encrypt(text.encode()).decode()
            self.database["normal"][subject] = enc_text
            self.save_database()
            self.normal_subject_entry.delete(0, tk.END)
            self.normal_text_entry.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Text committed successfully!")
        else:
            messagebox.showwarning("Input Error", "Subject and Text cannot be empty.")

    def setup_line_by_line_mode(self):
        tk.Label(self.main_frame, text="Subject:", bg='black', fg='white', font=self.font).grid(row=0, column=0, padx=5, pady=5)
        self.line_subject_entry = tk.Entry(self.main_frame, width=50, font=self.font)
        self.line_subject_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.main_frame, text="Line:", bg='black', fg='white', font=self.font).grid(row=1, column=0, padx=5, pady=5)
        self.line_text_entry = tk.Entry(self.main_frame, width=50, font=self.font)
        self.line_text_entry.grid(row=1, column=1, padx=5, pady=5)

        commit_line_button = tk.Button(self.main_frame, text="Commit Line", command=self.commit_line_by_line, bg='blue',
                                       fg='white', font=self.font)
        commit_line_button.grid(row=2, column=0, columnspan=2, pady=10)

    def commit_line_by_line(self):
        subject = self.line_subject_entry.get().strip()
        line = self.line_text_entry.get().strip()

        if subject and line:
            enc_line = fernet.encrypt(line.encode()).decode()

            if subject not in self.database["line_by_line"]:
                self.database["line_by_line"][subject] = []
            self.database["line_by_line"][subject].append(enc_line)
            self.save_database()
            self.line_text_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Line committed successfully!")
        else:
            messagebox.showwarning("Input Error", "Subject and Line cannot be empty.")

    def setup_normal_retrieval_mode(self):
        view_button = tk.Button(self.main_frame, text="View Note Subjects", command=self.view_normal_subjects,
                                bg='blue', fg='white', font=self.font)
        view_button.pack(pady=20)

    def view_normal_subjects(self):
        subjects = list(self.database["normal"].keys())

        if not subjects:
            messagebox.showinfo("No Data", "No subjects available.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Select Subject")
        popup.configure(bg='black')

        self.selected_subject_var = tk.StringVar(value=subjects[0])

        for subject in subjects:
            tk.Radiobutton(popup, text=subject, variable=self.selected_subject_var, value=subject, bg='black',
                           fg='white', selectcolor='blue', font=self.font).pack(anchor='w')

        choose_button = tk.Button(popup, text="Choose Subject", command=lambda: self.display_normal_text(popup),
                                  bg='blue', fg='white', font=self.font)
        choose_button.pack(pady=10)

    def display_normal_text(self, popup):
        subject = self.selected_subject_var.get()
        enc_text = self.database["normal"][subject]
        text = fernet.decrypt(enc_text.encode()).decode()

        popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("View Text")
        popup.configure(bg='black')

        tk.Label(popup, text="Subject:", bg='black', fg='white', font=self.font).grid(row=0, column=0, padx=5, pady=5)
        subject_entry = tk.Entry(popup, width=50, state='readonly', readonlybackground='black', fg='white', font=self.font)
        subject_entry.grid(row=0, column=1, padx=5, pady=5)
        subject_entry.insert(0, subject)

        tk.Label(popup, text="Text:", bg='black', fg='white', font=self.font).grid(row=1, column=0, padx=5, pady=5)
        text_box = tk.Text(popup, width=50, height=10, font=self.font)
        text_box.grid(row=1, column=1, padx=5, pady=5)
        text_box.insert(tk.END, text)
        text_box.configure(state='disabled', bg='black', fg='white')

        done_button = tk.Button(popup, text="Done", command=popup.destroy, bg='blue', fg='white', font=self.font)
        done_button.grid(row=2, column=0, columnspan=2, pady=10)

    def setup_line_by_line_retrieval_mode(self):
        view_button = tk.Button(self.main_frame, text="View Line Subjects", command=self.view_line_subjects, bg='blue',
                                fg='white', font=self.font)
        view_button.pack(pady=20)

    def view_line_subjects(self):
        subjects = list(self.database["line_by_line"].keys())

        if not subjects:
            messagebox.showinfo("No Data", "No subjects available.")
            return

        self.line_subject_index = 0

        popup = tk.Toplevel(self.root)
        popup.title("Select Subject")
        popup.configure(bg='black')

        self.line_subject_var = tk.StringVar(value=subjects[0])

        subject_label = tk.Entry(popup, width=50, state='readonly', textvariable=self.line_subject_var,
                                 readonlybackground='black', fg='white', font=self.font)
        subject_label.pack(pady=10)

        prev_button = tk.Button(popup, text="Previous",
                                command=lambda: self.navigate_subjects(-1, subjects, self.line_subject_var), bg='blue',
                                fg='white', font=self.font)
        prev_button.pack(side='left', padx=10)

        next_button = tk.Button(popup, text="Next",
                                command=lambda: self.navigate_subjects(1, subjects, self.line_subject_var), bg='blue',
                                fg='white', font=self.font)
        next_button.pack(side='left', padx=10)

        choose_button = tk.Button(popup, text="Choose",
                                  command=lambda: self.display_line_text(popup, self.line_subject_var.get()),
                                  bg='blue', fg='white', font=self.font)
        choose_button.pack(pady=10)

    def navigate_subjects(self, direction, subjects, var):
        self.line_subject_index = (self.line_subject_index + direction) % len(subjects)
        var.set(subjects[self.line_subject_index])

    def display_line_text(self, popup, subject):
        enc_lines = self.database["line_by_line"][subject]
        lines = [fernet.decrypt(enc_line.encode()).decode() for enc_line in enc_lines]

        popup.destroy()

        popup = tk.Toplevel(self.root)
        popup.title("View Lines")
        popup.configure(bg='black')

        self.line_index = 0

        tk.Label(popup, text="Subject:", bg='black', fg='white', font=self.font).grid(row=0, column=0, padx=5, pady=5)
        subject_entry = tk.Entry(popup, width=50, state='readonly', readonlybackground='black', fg='white', font=self.font)
        subject_entry.grid(row=0, column=1, padx=5, pady=5)
        subject_entry.insert(0, subject)

        tk.Label(popup, text="Line:", bg='black', fg='white', font=self.font).grid(row=1, column=0, padx=5, pady=5)
        self.line_text_var = tk.StringVar(value=lines[0])
        line_entry = tk.Entry(popup, width=50, state='readonly', textvariable=self.line_text_var,
                              readonlybackground='black', fg='white', font=self.font)
        line_entry.grid(row=1, column=1, padx=5, pady=5)

        prev_button = tk.Button(popup, text="Previous", command=lambda: self.navigate_lines(-1, lines), bg='blue',
                                fg='white', font=self.font)
        prev_button.grid(row=2, column=0, padx=5, pady=5)

        next_button = tk.Button(popup, text="Next", command=lambda: self.navigate_lines(1, lines), bg='blue',
                                fg='white', font=self.font)
        next_button.grid(row=2, column=1, padx=5, pady=5)

        done_button = tk.Button(popup, text="Done", command=popup.destroy, bg='blue', fg='white', font=self.font)
        done_button.grid(row=3, column=0, columnspan=2, pady=10)

    def navigate_lines(self, direction, lines):
        self.line_index = (self.line_index + direction) % len(lines)
        self.line_text_var.set(lines[self.line_index])


if __name__ == "__main__":
    root = tk.Tk()
    app = TextStorageApp(root)
    root.mainloop()
