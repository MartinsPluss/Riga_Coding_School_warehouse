import re
import mysql.connector as mysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Db:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x500+700+500")  # Martins
        self.root.title("Gramatu noliktava")  # Martins
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        self.conn = mysql.connect(
            host="localhost",
            user="root",
            database="test",
            password="qwerty123"
        )
        self.cursor = self.conn.cursor()

        self.column1_input = Entry(self.root)
        self.column2_input = Entry(self.root)
        self.column3_input = Entry(self.root)

        self.column1_label = Label(self.root, text="Nosaukums:")  # Martins
        self.column2_label = Label(self.root, text="Skaits:")
        self.column3_label = Label(self.root, text="Apraksts:")

        self.column1_label.grid(row=0, column=0)
        self.column1_input.grid(row=0, column=1)
        self.column2_label.grid(row=1, column=0)
        self.column2_input.grid(row=1, column=1)
        self.column3_label.grid(row=2, column=0)
        self.column3_input.grid(row=2, column=1)

        self.insert_button = ttk.Button(
            self.root, text="Ievietot", command=self.insert)
        self.insert_button.grid(row=3, column=4)  # Martins

        self.update_button = ttk.Button(
            self.root, text="Labot", command=self.update_database)
        self.update_button.grid(row=3, column=5)

        self.view_button = ttk.Button(
            self.root, text="Apskatīt", command=self.view)
        self.view_button.grid(row=3, column=6)

        self.delete_button = ttk.Button(
            self.root, text="Izdzēst", command=self.delete_item)
        self.delete_button.grid(row=3, column=7)

        def close():  # Martins
            self.root.destroy()

        # Create a Button to call close()
        quit_button = ttk.Button(self.root, text="Beigt darbu", command=close)
        quit_button.grid(row=6, column=7)
        self.root.mainloop()

    def is_valid_title(self, input_string):
        return bool(re.match(r'^[a-zA-Z0-9\s]+$', input_string))

    def is_number(self, input_string):
        return bool(re.match(r'^\d+$', input_string))

    def insert(self):

        # Get the values from the input fields

        if self.is_valid_title(self.column1_input.get().strip()):
            title = self.column1_input.get().strip()
        else:
            messagebox.showerror("Error", "Title input is not valid") 

        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            messagebox.showerror("Error", "Number input is not valid")

        description = self.column3_input.get()

        insert = "INSERT INTO warehouse (title, number, description) VALUES(%s,%s,%s)"
        values = (title, number, description)
        self.cursor.execute(insert, values)
        self.conn.commit()
        print("New records added")
        
        self.view()

    def update_database(self):

        title = self.column1_input.get().strip()

        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            messagebox.showerror("Error", "Number input is not valid")

        description = self.column3_input.get()

        update = "UPDATE warehouse SET number = %s WHERE title = %s"
        values = (number, title)
        self.cursor.execute(update, values)

        print("Updated")
        self.conn.commit()
        
        self.view()

        # # Update the button text to indicate that the update was successful
        # update_button.config(text="Update Successful!")
        
    def view(self):

        view = "SELECT title, number, description FROM warehouse"  # Martins
        self.cursor.execute(view)
        results = self.cursor.fetchall()

        results_text = Text(self.root)

        # The code below formats the output and gets rid of the curly brackets
        for result in results:
            result_str = [str(field) if not isinstance(field, str) else field.replace("{", "").replace("}", "") for field in result]
            results_text.insert(END, " ".join(result_str))
            results_text.insert(END, "\n")

        # Position the Text widget on the window # Martins
        results_text.grid(row=4, columnspan=2)

    def delete_item(self):

        title = self.column1_input.get()

        delete = "DELETE FROM warehouse WHERE title=%s"
        self.cursor.execute(delete, (title,))
        self.conn.commit()
        print("Deleted")  # Martins

        self.view()

if __name__ == '__main__':
    db = Db()
