# Šī ir CRUD programma grāmatu noliktavai ar TKinter GUI un Mysql datubāzi.

import re
import mysql.connector as mysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Definē objektu


class Db:

    def __init__(self):
        self.app = Tk()
        w = self.app.winfo_screenwidth()
        h = self.app.winfo_screenheight()
        self.app.columnconfigure(4, weight=1)
        self.app.rowconfigure(3, weight=1)
        self.app.title("Gramatu noliktava")  
        self.app.geometry(f"{w}x{h}")  

        # Datubāzes savienojums

        self.conn = mysql.connect(
            host="localhost",
            user="root",
            database="test",
            password="qwerty123"
        )
        self.cursor = self.conn.cursor()

        # Ievades lauki

        self.column1_input = Entry(self.app)
        self.column2_input = Entry(self.app)
        self.column3_input = Entry(self.app)

        self.column1_label = Label(self.app, text="Nosaukums:")  
        self.column2_label = Label(self.app, text="Skaits:")
        self.column3_label = Label(self.app, text="Apraksts:")

        self.column1_label.grid(row=0, column=0, padx=10, pady=5)
        self.column1_input.grid(row=0, column=1, padx=10, pady=3)
        self.column2_label.grid(row=1, column=0, padx=10, pady=5)
        self.column2_input.grid(row=1, column=1, padx=10, pady=3)
        self.column3_label.grid(row=2, column=0, padx=10, pady=3)
        self.column3_input.grid(row=2, column=1, padx=10, pady=3)

        # Pogas

        self.insert_button = ttk.Button(
            self.app, text="Ievietot", command=self.insert)
        self.insert_button.grid(row=0, column=3, padx=10)   

        self.update_button = ttk.Button(
            self.app, text="Labot", command=self.update_database)
        self.update_button.grid(row=1, column=3)

        self.view_button = ttk.Button(
            self.app, text="Apskatīt", command=self.view)
        self.view_button.grid(row=2, column=3)

        self.delete_button = ttk.Button(
            self.app, text="Izdzēst", command=self.delete_item)
        self.delete_button.grid(row=3, column=3, sticky=N)

        self.quit_button = ttk.Button(
            self.app, text="Beigt darbu", command=self.app.destroy)
        self.quit_button.grid(row=6, column=6, padx=20, pady=20)

        self.app.mainloop()

        # Teksta ievades validācija

    def is_valid_title(self, input_string):
        return bool(re.match(r'^[A-Za-z0-9\sĀČĢĶĻŅŠŪŽāčģīķļņšūž]+$', input_string))

    def is_number(self, input_string):
        return bool(re.match(r'^\d+$', input_string))

        # Ievietošanas funkcija

    def insert(self):

        if self.is_valid_title(self.column1_input.get().strip()):
            title = self.column1_input.get().strip()
        else:
            messagebox.showerror("Kļūda", "Nosaukums nav derīgs")

        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            messagebox.showerror("Kļūda", "Skaits nav derīgs")

        description = self.column3_input.get()

        insert = "INSERT INTO warehouse (title, number, description) VALUES(%s,%s,%s)"
        values = (title, number, description)
        self.cursor.execute(insert, values)
        self.conn.commit()
        print("New records added")

        self.view()

        # Labošanas funkcija

    def update_database(self):

        title = self.column1_input.get().strip()

        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            messagebox.showerror("Kļūda", "Skaits nav derīgs")

        description = self.column3_input.get()

        update = "UPDATE warehouse SET number = %s WHERE title = %s"
        values = (number, title)
        self.cursor.execute(update, values)

        print("Updated")
        self.conn.commit()

        self.view()

        # apskatīšanas funkcija

    def view(self):
        view = "SELECT title, number, description FROM warehouse"  
        self.cursor.execute(view)
        results = self.cursor.fetchall()

        # Create separate Label and Text widgets for each field
        title_label = Label(self.app, text="Nosaukums")
        title_label.grid(row=4, column=4)

        results_text_title = Text(self.app, width=70)
        results_text_title.grid(row=5, column=4, padx=0, pady=0)

        number_label = Label(self.app, text="Skaits")
        number_label.grid(row=4, column=5)

        results_text_number = Text(self.app, width=50)
        results_text_number.grid(row=5, column=5, padx=5, pady=5)

        description_label = Label(self.app, text="Apraksts")
        description_label.grid(row=4, column=6)

        results_text_description = Text(self.app, width=130)
        results_text_description.grid(row=5, column=6, padx=0, pady=0)

        for result in results:
            results_text_title.insert(END, result[0])
            results_text_title.insert(END, "\n")
            results_text_number.insert(END, result[1])
            results_text_number.insert(END, "\n")
            results_text_description.insert(END, result[2])
            results_text_description.insert(END, "\n")

        self.app.columnconfigure(4, weight=1, minsize=50)
        self.app.columnconfigure(5, weight=1, minsize=50)
        self.app.columnconfigure(6, weight=1, minsize=50)

        # Dzēšanas funkcija

    def delete_item(self):

        title = self.column1_input.get()

        delete = "DELETE FROM warehouse WHERE title=%s"
        self.cursor.execute(delete, (title,))
        self.conn.commit()
        print("Deleted")  

        self.view()


if __name__ == '__main__':
    db = Db()
