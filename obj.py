import re
import mysql.connector as mysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Db:

    # Definē objektu
    def __init__(self):
        # Create the main Tkinter window
        self.app = Tk()

        # Set the window size to the full screen size
        w = self.app.winfo_screenwidth()
        h = self.app.winfo_screenheight()
        self.app.columnconfigure(4, weight=1)
        self.app.rowconfigure(3, weight=1)
        self.app.title("Gramatu noliktava")
        self.app.geometry(f"{w}x{h}")

        # Connect to the MySQL database
        self.conn = mysql.connect(
            host="localhost",
            user="root",
            database="test",
            password="qwerty123"
        )
        self.cursor = self.conn.cursor()

        # Create the input fields for the book title, number, and description

        self.column1_input = Entry(self.app)
        self.column2_input = Entry(self.app)
        self.column3_input = Entry(self.app)

        # Create the labels for the input fields
        self.column1_label = Label(self.app, text="Nosaukums:")

        # Create the labels for the input fields
        self.column1_label = Label(self.app, text="Nosaukums:")  # Martins

        self.column2_label = Label(self.app, text="Skaits:")
        self.column3_label = Label(self.app, text="Apraksts:")

        # Position the labels and input fields in the window
        self.column1_label.grid(row=0, column=0, padx=10, pady=5)
        self.column1_input.grid(row=0, column=1, padx=10, pady=3)
        self.column2_label.grid(row=1, column=0, padx=10, pady=5)
        self.column2_input.grid(row=1, column=1, padx=10, pady=3)
        self.column3_label.grid(row=2, column=0, padx=10, pady=3)
        self.column3_input.grid(row=2, column=1, padx=10, pady=3)

        # Create the buttons for inserting, updating, viewing, and deleting books
        self.insert_button = ttk.Button(
            self.app, text="Ievietot", command=self.insert)
        self.insert_button.grid(row=0, column=3, padx=10)  # Martins

        # Create the buttons for inserting, updating, viewing, and deleting book
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

        # Create the quit button to close the application
        self.quit_button = ttk.Button(
            self.app, text="Beigt darbu", command=self.app.destroy)
        self.quit_button.grid(row=6, column=6, padx=20, pady=20)

        # Start the main Tkinter event loop
        self.app.mainloop()

    def is_valid_title(self, input_string):
        # Check if the input string is a valid book title using a regular expression
        return bool(re.match(r'^[A-Za-z0-9\sĀČĢĶĻŅŠŪŽāčģīķļņšūž]+$', input_string))

    def is_number(self, input_string):

        # Check if the input string is a number using a regular expression

        return bool(re.match(r'^\d+$', input_string))

    def insert(self):
        # Get the values from the input fields
        # Check if the title input is valid
        # Ievietošanas funkcija

        # Check if the title input is valid
        if self.is_valid_title(self.column1_input.get().strip()):
            title = self.column1_input.get().strip()
        else:
            # Show an error message if the title is not valid
            messagebox.showerror("Kļūda", "Nosaukums nav derīgs")

        # Check if the number input is valid
        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            # Show an error message if the number is not valid
            messagebox.showerror("Kļūda", "Skaits nav derīgs")

        description = self.column3_input.get()

        # Insert the new book into the database
        insert = "INSERT INTO warehouse (title, number, description) VALUES(%s,%s,%s)"
        values = (title, number, description)
        self.cursor.execute(insert, values)
        self.conn.commit()
        print("New records added")
        # Refresh the view
        self.view()

    def update_database(self):
        # Labošanas funkcija

        # Get the title input and assign it to a variable
        title = self.column1_input.get().strip()

        # Check if the input for number is a valid number
        if self.is_number(self.column2_input.get().strip()):
            number = int(self.column2_input.get().strip())
        else:
            messagebox.showerror("Kļūda", "Skaits nav derīgs")

        # Update the number in the warehouse table where the title matches the input
        update = "UPDATE warehouse SET number = %s WHERE title = %s"
        values = (number, title)
        self.cursor.execute(update, values)

        print("Updated")
        self.conn.commit()

        # Refresh the view
        self.view()

    def view(self):

        # Retrieve all rows from the warehouse table
        view = "SELECT title, number, description FROM warehouse"  # Martins

        self.cursor.execute(view)
        self.results = self.cursor.fetchall()

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

        # Insert the results into the Text widgets
        for result in self.results:
            results_text_title.insert(END, result[0])
            results_text_title.insert(END, "\n")
            results_text_number.insert(END, result[1])
            results_text_number.insert(END, "\n")
            results_text_description.insert(END, result[2])
            results_text_description.insert(END, "\n")

        # Configure the columns for the grid layout
        self.app.columnconfigure(4, weight=1, minsize=50)
        self.app.columnconfigure(5, weight=1, minsize=50)
        self.app.columnconfigure(6, weight=1, minsize=50)

    def delete_item(self):

        # Get the title input and assign it to a variable

        title = self.column1_input.get()

        # creates a list of titles and checks if the title to delete is present in the list
        res_title = [result[0] for result in self.results]
        if title not in res_title:
            messagebox.showerror(
                "Kļūda", "Grāmatas ar tādu nosaukumu nav sarakstā!")

            messagebox.showerror("Kļūda", "Grāmatas ar tādu nosauku nav sarakstā!")

        # Delete the row in the warehouse table where the title matches the input
        delete = "DELETE FROM warehouse WHERE title=%s"
        self.cursor.execute(delete, (title,))
        self.conn.commit()

        print("Deleted")

        # Refresh the view
        self.view()


if __name__ == '__main__':
    db = Db()