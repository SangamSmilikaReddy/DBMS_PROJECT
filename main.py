import tkinter as tk
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox


class DatabaseViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MySQL Database Viewer")
        self.geometry("600x400")

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()
        
    def create_widgets(self):
        self.set_background()
        # Create a label with the background image
        background_label = tk.Label(self, image=self.background_photo, bg='light blue')  # Set label background color
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind click event to open all tables page
        background_label.bind("<Button-1>", self.open_all_tables_page)

    def set_background(self):
        try:
            # Load the image
            background_image = Image.open("Welcome_to.png")  # Change the path to your image file
            background_image = background_image.resize((600, 400))  # Resize the image to fit the window

            # Convert the image to Tkinter format
            self.background_photo = ImageTk.PhotoImage(background_image)
        except Exception as e:
            print("Error setting background:", e)

    def open_all_tables_page(self, event):
        # Connect to the database
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="2003",
                database="gold_loan"
            )

            self.cursor = self.connection.cursor()

            # Open all tables page
            all_tables_page = AllTablesPage(self, self.connection, self.cursor)
            all_tables_page.configure(background='light blue')  # Set window background color
            all_tables_page.mainloop()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

        
        
class AllTablesPage(tk.Toplevel):
    def __init__(self, master, connection, cursor):
        super().__init__(master)

        self.title("All Tables")
        self.geometry("600x400")

        self.connection = connection
        self.cursor = cursor

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()

    def create_widgets(self):
        self.treeview = ttk.Treeview(self)
        self.treeview["columns"] = ("Name")

        self.treeview.heading("#0", text="Table")
        self.treeview.heading("Name", text="Name")

        self.treeview.pack(fill="both", expand=True)

        self.treeview.bind("<Double-1>", self.on_double_click)

        self.fetch_tables()

    def fetch_tables(self):
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()

            for table in tables:
                self.treeview.insert("", "end", text=table[0], values=(table[0],))

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def on_double_click(self, event):
        item = self.treeview.selection()[0]
        table_name = self.treeview.item(item, "text")
        self.open_table_window(table_name)

    def open_table_window(self, table_name):
        table_window = TableWindow(self, table_name, self.connection, self.cursor)
        table_window.configure(background='light blue')  # Set window background color
        table_window.mainloop()

class TableWindow(tk.Toplevel):
    def __init__(self, master, table_name, connection, cursor):
        super().__init__(master)

        self.title(table_name)  # Set window title as table name
        self.geometry("400x200")

        self.table_name = table_name
        self.connection = connection
        self.cursor = cursor

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()

    def create_widgets(self):
        # Create a label to display the table name in a larger font
        table_name_label = tk.Label(self, text=self.table_name, font=("Arial", 16, "bold"), bg='light blue')  # Set label background color
        table_name_label.pack()

        add_button = tk.Button(self, text=f"Add {self.table_name}", command=self.add_data, bg='orange')  # Set button background color
        add_button.pack(pady=3)
        
        tk.Label(self, text="", bg='light blue').pack()  # Add 3 lines of space with window background color

        delete_button = tk.Button(self, text=f"Delete {self.table_name}", command=self.delete_data, bg='orange')  # Set button background color
        delete_button.pack(pady=3)

        # Add extra space
        tk.Label(self, text="", bg='light blue').pack()  # Add 3 lines of space with window background color

        view_button = tk.Button(self, text="View Data", command=self.view_data, bg='orange')  # Set button background color
        view_button.pack(pady=3)

    def add_data(self):
        add_data_window = AddDataWindow(self, self.table_name, self.connection, self.cursor)
        add_data_window.configure(background='light blue')  # Set window background color
        add_data_window.mainloop()

    def delete_data(self):
        try:
            self.cursor.execute(f"SHOW KEYS FROM {self.table_name} WHERE Key_name = 'PRIMARY'")
            primary_key_column = self.cursor.fetchone()
            primary_key_column_name = primary_key_column[4] if primary_key_column else None
            delete_data_window = DeleteDataWindow(self, self.table_name, self.connection, self.cursor,primary_key_column_name)
            delete_data_window.configure(background='light blue')  # Set window background color
            delete_data_window.mainloop()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def view_data(self):
        try:
            # Fetch primary key column name
            self.cursor.execute(f"SHOW KEYS FROM {self.table_name} WHERE Key_name = 'PRIMARY'")
            primary_key_column = self.cursor.fetchone()
            primary_key_column_name = primary_key_column[4] if primary_key_column else None

            view_data_window = ViewDataWindow(self, self.table_name, self.connection, self.cursor, primary_key_column_name)
            view_data_window.configure(background='light blue')  # Set window background color
            view_data_window.mainloop()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class AddDataWindow(tk.Toplevel):
    def __init__(self, master, table_name, connection, cursor):
        super().__init__(master)

        self.title(f"Add Data to {table_name}")
        self.geometry("400x300")

        self.table_name = table_name
        self.connection = connection
        self.cursor = cursor

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()

    def create_widgets(self):
        try:
            table_name_label = tk.Label(self, text=f"Add New {self.table_name} Data", font=("Arial", 14, "bold"), bg='light blue')  # Set label background color
            table_name_label.grid(row=0, column=0, columnspan=2)

            # Add space
            tk.Label(self, text="", bg='light blue').grid(row=1, column=0)  # Add space with window background color

            # Fetch column names and data types from the database
            self.cursor.execute(f"DESCRIBE {self.table_name}")
            columns = self.cursor.fetchall()

            self.entry_fields = {}

            for i, column in enumerate(columns, start=2):
                column_name = column[0]
                entry_label = tk.Label(self, text=column_name, bg='light blue')  # Set label background color
                entry_label.grid(row=i, column=0, sticky="w")

                entry_field = tk.Entry(self)
                entry_field.grid(row=i, column=1)

                self.entry_fields[column_name] = entry_field

            submit_button = tk.Button(self, text="Submit", command=self.insert_data, bg='orange')  # Set button background color
            submit_button.grid(row=len(columns) + 2, columnspan=2)

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def insert_data(self):
        try:
            # Construct INSERT query
            columns = ", ".join(self.entry_fields.keys())
            values = ", ".join(f"'{entry.get()}'" for entry in self.entry_fields.values())
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            
            # Execute INSERT query
            self.cursor.execute(query)
            self.connection.commit()

            print("Data inserted successfully.")

            # Empty entry fields after successful insertion
            for entry_field in self.entry_fields.values():
                entry_field.delete(0, tk.END)

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class DeleteDataWindow(tk.Toplevel):
    def __init__(self, master, table_name, connection, cursor, primary_key_column_name):
        super().__init__(master)

        self.title(f"Delete Data from {table_name}")
        self.geometry("400x200")

        self.table_name = table_name
        self.connection = connection
        self.cursor = cursor
        self.primary_key_column_name = primary_key_column_name  # Assigning primary_key_column_name as an attribute

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()

    def create_widgets(self):
        self.primary_key_label = tk.Label(self, text=f"Delete {self.table_name} using {self.primary_key_column_name}", bg='light blue', font=("Helvetica", 14))
        self.primary_key_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        primary_key_entry_label = tk.Label(self, text="Enter Primary Key:", bg='light blue')
        primary_key_entry_label.grid(row=1, column=0, padx=5, pady=5)

        self.primary_key_entry = tk.Entry(self)
        self.primary_key_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to delete record
        self.delete_button = tk.Button(self, text="Delete Record", command=self.delete_record)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)
        

    def delete_record(self):
        if not self.primary_key_column_name:
            print("Error: Primary key column name not found.")
            return

        try:
            primary_key = self.primary_key_entry.get()
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key_column_name} = %s"
            self.cursor.execute(query, (primary_key,))
            self.connection.commit()

            print("Record deleted successfully.")
            self.primary_key_entry.delete(0, tk.END)  # Clear input space

            # Show message in GUI
            success_label = tk.Label(self, text="Record deleted successfully", bg='light blue')  # Set label background color
            success_label.grid(row=2, columnspan=2)

        except mysql.connector.Error as err:
            print("Error: {}".format(err))



class ViewDataWindow(tk.Toplevel):
    def __init__(self, master, table_name, connection, cursor, primary_key_column_name):
        super().__init__(master)

        self.title(f"View Data from {table_name}")
        self.geometry("600x400")

        self.table_name = table_name
        self.connection = connection
        self.cursor = cursor
        self.primary_key_column_name = primary_key_column_name  # Store primary key column name

        self.configure(background='light blue')  # Set window background color

        self.create_widgets()


    def create_widgets(self):
        try:
            # Add label for the table name with larger font
            table_name_label = tk.Label(self, text=f"View Table {self.table_name}", font=("Arial", 14, "bold"))
            table_name_label.pack()

            # Fetch all records from the table
            self.cursor.execute(f"SELECT * FROM {self.table_name}")
            self.records = self.cursor.fetchall()

            # Create a frame to hold the canvas and scrollbar
            tree_frame = tk.Frame(self)
            tree_frame.pack(fill="both", expand=True)

            # Create a canvas
            canvas = tk.Canvas(tree_frame)
            canvas.pack(side="left", fill="both", expand=True)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=canvas.xview)
            scrollbar.pack(side="bottom", fill="x")

            # Create a treeview inside the canvas
            self.treeview = ttk.Treeview(canvas, show="headings", yscrollcommand=scrollbar.set)
            self.treeview["columns"] = [column[0] for column in self.cursor.description]

            for column in self.cursor.description:
                self.treeview.heading(column[0], text=column[0])
                self.treeview.column(column[0], width=150, minwidth=120)  # Set minimum width for columns

            for record in self.records:
                self.treeview.insert("", "end", values=record)

            # Pack the scrollbar and treeview
            self.treeview.pack(side="top", fill="both", expand=True)
            scrollbar.pack(side="bottom", fill="x")

            # Configure scrollbar and canvas scrolling
            self.treeview.pack(side="top", fill="both", expand=True)
            canvas.create_window((0, 0), window=self.treeview, anchor="nw")
            canvas.update_idletasks()  # Update the canvas idle tasks
            canvas.configure(scrollregion=canvas.bbox("all"))  # Set scroll region to the size of the canvas

            # Bind click event to handle cell editing
            self.treeview.bind("<ButtonRelease-1>", self.edit_cell)

        except mysql.connector.Error as err:
            print("Error: {}".format(err))



    def edit_cell(self, event):
        item = self.treeview.selection()[0]
        column = self.treeview.identify_column(event.x)
        col_index = int(str(column).replace("#", "")) - 1
        row = self.treeview.index(item)

        # Create an entry field to edit the selected cell
        value = self.treeview.item(item, "values")[col_index]
        entry_field = tk.Entry(self.treeview)
        entry_field.insert(0, value)

        # Bind the <Return> key to save changes when editing is done
        entry_field.bind("<Return>", lambda event, item=item, row=row, col_index=col_index, entry_field=entry_field: self.save_changes(item, row, col_index, entry_field))

        # Place the entry field in the cell
        bbox = self.treeview.bbox(item, column)
        if bbox:
            x, y, width, height = bbox
            entry_field.place(x=x+2, y=y+2, width=width-4, height=height-4)
            entry_field.focus_set()  # Set focus to the entry field

    def save_changes(self, item, row, col_index, entry_field):
        new_value = entry_field.get()
        item_values = self.treeview.item(item, "values")
        old_value = item_values[col_index]

        if new_value != old_value:
            self.treeview.set(item, column=col_index, value=new_value)

            # Prompt user to save changes before closing
            if messagebox.askyesno("Save Changes", "Do you want to save changes before closing?"):
                record_id = item_values[0]  # Assuming the record ID is the first column
                column_name = self.treeview.heading(col_index)["text"]
                query = f"UPDATE {self.table_name} SET {column_name} = %s WHERE {self.primary_key_column_name} = %s"
                try:
                    self.cursor.execute(query, (new_value, record_id))
                    self.connection.commit()
                    print("Changes saved successfully.")
                except mysql.connector.Error as err:
                    print("Error: {}".format(err))

        # Destroy the entry field after editing
        entry_field.destroy()


    def close_window(self):
        # Prompt user to save changes before closing
        if tk.messagebox.askyesno("Save Changes", "Do you want to save changes before closing?"):
            # Implement saving changes here before closing
            print("Changes saved successfully.")
        self.destroy()






if __name__ == "__main__":
    app = DatabaseViewer()
    app.mainloop()
