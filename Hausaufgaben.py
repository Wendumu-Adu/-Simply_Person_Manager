from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

import tkinter as tk
from tkinter import filedialog, messagebox

from manager import PersonManager
from person import Person


class PersonApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Person Manager")
        self.root.geometry("780x520")
        self.root.minsize(650, 420)

     
        self.manager = PersonManager()

        menubar = tk.Menu(root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.menu_open)
        file_menu.add_command(label="New", command=self.menu_new)
        file_menu.add_command(label="Save", command=self.menu_save)
        file_menu.add_command(label="Save As...", command=self.menu_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.menu_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menubar)
        
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)

        frame_top = tk.LabelFrame(
            root, text=" Eingabe & Verwaltung ", padx=15, pady=15
        )
        frame_top.grid(
            row=0, column=0, sticky="ew", padx=15, pady=10
        )

        frame_top.columnconfigure(1, weight=1)
        frame_top.columnconfigure(4, weight=1)

        tk.Label(frame_top, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_name = tk.Entry(frame_top, width=22)
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_top, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_age = tk.Entry(frame_top, width=22)
        self.entry_age.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_top, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_email = tk.Entry(frame_top, width=22)
        self.entry_email.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame_top, text="File name:").grid(row=0, column=3, sticky="w", padx=15, pady=5)
        self.entry_filename = tk.Entry(frame_top, width=18)
        self.entry_filename.insert(0, "persons")
        self.entry_filename.grid(row=0, column=4, sticky="ew", padx=5, pady=5)

        frame_buttons = tk.Frame(root)
        frame_buttons.grid(row=1, column=0, sticky="ew", padx=15, pady=5)

        btn_add = tk.Button(
            frame_buttons, text="Add Person", width=18, bg="#00b4d8", fg="white", font=("Arial", 10, "bold"), command=self.add_person
        )
        btn_add.pack(side=tk.LEFT, padx=5)

        btn_show = tk.Button(
            frame_buttons, text="Show Persons", width=18, bg="#48cae4", fg="white", font=("Arial", 10, "bold"), command=self.show_persons
        )
        btn_show.pack(side=tk.RIGHT, padx=5)

        frame_output = tk.LabelFrame(
            root, text=" Gespeicherte Personen ", padx=10, pady=10
        )
        frame_output.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        root.rowconfigure(2, weight=1)
        frame_output.rowconfigure(0, weight=1)
        frame_output.columnconfigure(0, weight=1)

        self.text_output = tk.Text(frame_output, bg="white", wrap=tk.WORD, font=("Courier", 10))
        scrollbar = tk.Scrollbar(frame_output, orient="vertical", command=self.text_output.yview)
        self.text_output.configure(yscrollcommand=scrollbar.set)

        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def update_status(self, msg):
        pass

    def add_person(self):
        name = self.entry_name.get().strip()
        age_str = self.entry_age.get().strip()
        email = self.entry_email.get().strip()

        if not name or not email:
            messagebox.showerror("Error", "Name and Email cannot be empty!")
            return

        try:
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return

        if any(p.email == email for p in self.manager.persons):
            messagebox.showwarning("Warning", "Person with this email already exists!")
            return

        person = Person(name, age, email)
        self.manager.persons.append(person)
        self.manager.save_json()

        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

        self.show_persons()
        self.update_status(f"Added: {name}")

    def show_persons(self):
        self.text_output.delete("1.0", tk.END)
        if not self.manager.persons:
            self.text_output.insert(tk.END, "No available persons.\n")
            self.update_status("List is empty")
            return

        for p in self.manager.persons:
            line = f"Name: {p.name:<15} | Age: {str(p.age):<5} | Email: {p.email}\n"
            self.text_output.insert(tk.END, line)

        self.update_status("Refreshed list")

    def menu_open(self):
        file_path = filedialog.askopenfilename(initialdir=str(self.manager.data_dir))
        if file_path:
            self.update_status(f"Opened: {Path(file_path).name}")

    def menu_new(self):
        self.manager.persons.clear()
        self.show_persons()
        self.update_status("Created new list")

    def menu_save(self):
        fname = self.entry_filename.get().strip() or "persons"
        ext = Path(fname).suffix.lower()
        
        if ext == ".csv":
            self.manager.save_csv(fname)
        elif ext == ".xml":
            self.manager.save_xml(fname)
        else:
            if not ext:
                fname += ".json"
            self.manager.save_json(fname)
            
        self.update_status(f"Saved to {fname}")

    def menu_save_as(self):
        fname_default = self.entry_filename.get().strip() or "persons"
        file_path = filedialog.asksaveasfilename(
            initialdir=str(self.manager.data_dir),
            initialfile=fname_default,
            defaultextension=".json",
            filetypes=[
                ("JSON File (*.json)", "*.json"),
                ("CSV File (*.csv)", "*.csv"),
                ("XML File (*.xml)", "*.xml"),
                ("All Files (*.*)", "*.*")
            ]
        )
        if file_path:
            path_obj = Path(file_path)
            ext = path_obj.suffix.lower()
            filename = path_obj.name
            
            if ext == ".csv":
                self.manager.save_csv(filename)
            elif ext == ".xml":
                self.manager.save_xml(filename)
            else:
                self.manager.save_json(filename)
                
            self.update_status(f"Saved as {filename}")

    def menu_about(self):
        messagebox.showinfo("About", "Person Manager\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonApp(root)
    root.mainloop()