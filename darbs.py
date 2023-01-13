import mysql.connector
from tkinter import *


def insert():
    # Get the values from the input fields
    title = column1_input.get()
    number = column2_input.get()
    description = column3_input.get()

    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="test",
        password="qwerty123"

    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute an update query using the values from the input fields

    insert = "INSERT INTO warehouse (title, number, description) VALUES(%s,%s,%s)"
    values = (title, number, description)
    cursor.execute(insert, values)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Update the button text to indicate that the update was successful
    # insert_button.config(text="Insert Successful!")


def view():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="test",
        password="qwerty123"
    )

    # Create a cursor
    cursor = conn.cursor()

    view = "SELECT * FROM warehouse"
    cursor.execute(view)
    results = cursor.fetchall()

    results_text = Text(root)

    for result in results:
        results_text.insert(END, result)
        results_text.insert(END, "\n")

    # Position the Text widget on the window
    results_text.grid(row=5, columnspan=8)

    # Close the cursor and the connection
    cursor.close()
    conn.close()


def update_database():

    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qwerty123",
        database="test"
    )

    # Get the values from the input fields
    title = column1_input.get()
    number = column2_input.get()
    description = column3_input.get()

    # Create a cursor
    cursor = conn.cursor()

    # Execute an update query using the values from the input fields
    cursor.execute("UPDATE warehouse SET number = %s, description=%s WHERE title=%s",
                   (number, description, title))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Update the button text to indicate that the update was successful
    # update_button.config(text="Update Successful!")


def delete_item():

    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="test",
        password="qwerty123"
    )

    # Get the values from the input fields
    title = column1_input.get()

    # Create a cursor
    cursor = conn.cursor()

    delete = "DELETE FROM warehouse WHERE title=%s"
    cursor.execute(delete, (title,))
    conn.commit()


# Create a Tkinter window
root = Tk()
root.geometry("800x500+700+500")

# Title of the window
root.title("Gramatu noliktava")


# Create labels and input fields for column1, column2, and column3
column1_label = Label(root, text="Title:")
column1_input = Entry(root)
column2_label = Label(root, text="Number:")
column2_input = Entry(root)
column3_label = Label(root, text="Description:")
column3_input = Entry(root)

# Position the labels and input fields on the window
column1_label.grid(row=0, column=0)
column1_input.grid(row=0, column=1)
column2_label.grid(row=1, column=0)
column2_input.grid(row=1, column=1)
column3_label.grid(row=2, column=0)
column3_input.grid(row=2, column=1)

# Create a buttons

insert_button = Button(root, text="Insert", command=insert)
insert_button.grid(row=3, column=0)
insert_button.config(fg="black", bg="gray75")


update_button = Button(root, text="Update", command=update_database)
update_button.grid(row=3, column=1)
update_button.config(fg="black", bg="gray75")

view_button = Button(root, text="View", command=view)
view_button.grid(row=4, column=0)
view_button.config(fg="black", bg="gray75")

delete_button = Button(root, text="Delete", command=delete_item)
delete_button.grid(row=4, column=1)
delete_button.config(fg="black", bg="gray75")

# Define a function to close the window


def close():
    root.destroy()


# Create a Button to call close()
quit_button = Button(root, text="Beigt darbu", command=close)
quit_button.grid(row=4, column=2)
quit_button.config(fg="black", bg="gray75")

# Start the event loop
root.mainloop()
