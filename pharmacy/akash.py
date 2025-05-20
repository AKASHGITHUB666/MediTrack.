import mysql.connector


from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox, ttk

# Global variables for username and password fields
entry_username = None
entry_password = None


# Connect to the database

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='akash2005',
        database='PharmacyDB'
    )

# Function to validate user login
def validate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to handle login
def login():
    global entry_username, entry_password
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        user = validate_user(username, password)
        if user:
            messagebox.showinfo("Login", "Login Successful")
            login_window.destroy()  # Close login window
            open_inventory_window()  # Open inventory management
        else:
            messagebox.showerror("Login", "Invalid username or password")
    else:
        messagebox.showerror("Login", "Please enter both username and password")



def sign_up():
    # Create the sign-up window
    sign_up_window = Toplevel(login_window)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("400x300")
    sign_up_window.configure(bg="#2b2b3d")

    def register_user():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()

        if new_username and new_password:
            conn = create_connection()
            cursor = conn.cursor()
            # Check if the username already exists
            query_check = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query_check, (new_username,))
            if cursor.fetchone():
                messagebox.showerror("Sign Up", "Username already exists!")
            else:
                # Insert the new user into the database
                query_insert = "INSERT INTO Users (username, password) VALUES (%s, %s)"
                cursor.execute(query_insert, (new_username, new_password))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sign Up", "Registration successful!")
                sign_up_window.destroy()
        else:
            messagebox.showerror("Sign Up", "All fields are required!")

    # Sign-Up Window Layout
    Label(
        sign_up_window, text="Create New Account", font=("Arial", 14, "bold"), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=10)

    Label(
        sign_up_window, text="Username", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=5)
    entry_new_username = Entry(sign_up_window, font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
    entry_new_username.pack(pady=5)

    Label(
        sign_up_window, text="Password", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=5)
    entry_new_password = Entry(sign_up_window, show="*", font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
    entry_new_password.pack(pady=5)

    Button(
        sign_up_window,
        text="Register",
        font=("Arial", 12, "bold"),
        bg="#00aaff",
        fg="#ffffff",
        command=register_user,
    ).pack(pady=20)

# Function to open the enhanced inventory management window
def open_inventory_window():
    inventory_window = Tk()
    inventory_window.title("Inventory Management")
    inventory_window.geometry("1000x650")
    inventory_window.configure(bg="#1e1e2f")

    title_label = Label(
        inventory_window,
        text="PHARMACY MANAGEMENT",
        font=("Arial", 16, "bold"),
        bg="#1e1e2f",
        fg="#ffffff",
    )
    title_label.pack(pady=10)

    # Frame for Input Fields
    frame_top = Frame(inventory_window, bg="#2b2b3d", relief=RIDGE, bd=2)
    frame_top.pack(side=TOP, fill=X, padx=10, pady=10)

    # Input Labels and Entry Fields
    Label(frame_top, text="Item Name", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff").grid(
        row=0, column=0, padx=10, pady=10, sticky=W
    )
    entry_item_name = Entry(frame_top, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_item_name.grid(row=0, column=1, padx=10, pady=10, sticky=W)

    Label(frame_top, text="Price", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff").grid(
        row=0, column=2, padx=10, pady=10, sticky=W
    )
    entry_item_price = Entry(frame_top, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_item_price.grid(row=0, column=3, padx=10, pady=10, sticky=W)

    Label(frame_top, text="Quantity", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff").grid(
        row=1, column=0, padx=10, pady=10, sticky=W
    )
    entry_item_quantity = Entry(frame_top, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_item_quantity.grid(row=1, column=1, padx=10, pady=10, sticky=W)

    Label(frame_top, text="Category", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff").grid(
        row=1, column=2, padx=10, pady=10, sticky=W
    )
    entry_item_category = Entry(frame_top, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_item_category.grid(row=1, column=3, padx=10, pady=10, sticky=W)

    Label(frame_top, text="Discount", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff").grid(
        row=2, column=0, padx=10, pady=10, sticky=W
    )
    entry_item_discount = Entry(frame_top, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_item_discount.grid(row=2, column=1, padx=10, pady=10, sticky=W)

    # Add Item Functionality
    def add_item():
        item_name = entry_item_name.get()
        item_price = entry_item_price.get()
        item_quantity = entry_item_quantity.get()
        item_category = entry_item_category.get()
        item_discount = entry_item_discount.get()

        if item_name and item_price and item_quantity and item_category and item_discount:
            conn = create_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Inventory (item_name, item_price, item_quantity, item_category, item_discount) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (item_name, item_price, item_quantity, item_category, item_discount))
            conn.commit()
            conn.close()
            messagebox.showinfo("Inventory", "Item added successfully")
            view_items()  # Refresh table
        else:
            messagebox.showerror("Inventory", "All fields must be filled")

    # Remove Item Functionality
    def remove_item():
        selected_item = inventory_table.focus()
        if selected_item:
            item_details = inventory_table.item(selected_item)['values']
            item_name = item_details[0]
            conn = create_connection()
            cursor = conn.cursor()
            query = "DELETE FROM Inventory WHERE item_name = %s"
            cursor.execute(query, (item_name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Inventory", "Item removed successfully")
            view_items()  # Refresh table
        else:
            messagebox.showerror("Inventory", "Please select an item to remove")

    # View Items Functionality
    def view_items():
        for row in inventory_table.get_children():
            inventory_table.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT item_name, item_price, item_quantity, item_category,item_discount FROM Inventory"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        for result in results:
            inventory_table.insert('', 'end', values=result)

    # Buy Medicine Functionality
    def buy_medicine():
        def process_purchase():
            customer_name = entry_customer_name.get()
            customer_phone = entry_customer_phone.get()
            medicine_name = entry_medicine_name.get()
            requested_quantity = int(entry_quantity.get())

            if customer_name and customer_phone and medicine_name and requested_quantity > 0:
                conn = create_connection()
                cursor = conn.cursor()
                query = "SELECT item_price, item_quantity, item_discount FROM Inventory WHERE item_name = %s"
                cursor.execute(query, (medicine_name,))
                result = cursor.fetchone()
                if result:
                    item_price, available_quantity, discount = result
                    if requested_quantity <= available_quantity:
                        total_price = (item_price * requested_quantity) * ((100 - discount) / 100)
                        updated_quantity = available_quantity - requested_quantity

                        # Update the inventory
                        update_query = "UPDATE Inventory SET item_quantity = %s WHERE item_name = %s"
                        cursor.execute(update_query, (updated_quantity, medicine_name))

                        # Record the sale in the Sales table
                        insert_sale_query = """
                            INSERT INTO Sales (customer_name, customer_phoneno, medicine_name, quantity, total_price) 
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_sale_query,
                                       (customer_name, customer_phone, medicine_name, requested_quantity, total_price))

                        conn.commit()
                        conn.close()

                        bill_window = Toplevel(purchase_window)
                        bill_window.title("Purchase Bill")
                        bill_window.geometry("400x400")
                        bill_window.configure(bg="#2b2b3d")

                        Label(
                            bill_window,
                            text="Pharmacy Management - Purchase Bill",
                            font=("Arial", 14, "bold"),
                            bg="#2b2b3d",
                            fg="#ffffff"
                        ).pack(pady=10)

                        messagebox.showinfo("PURCHASE BILL",
                                            f"Name: {customer_name}\n"
                                            f"Phone: {customer_phone}\n"
                                            f"Medicine: {medicine_name}\n"
                                            f"Total Price: Rs.{total_price:.2f}\n"
                                            f"Purchase Successful! \n"
                                            f"eBill has been sent to the mobile number")
                        purchase_window.destroy()
                        view_items()  # Refresh table
                    else:
                        messagebox.showerror("Purchase", "Requested quantity exceeds available stock!")
                else:
                    messagebox.showerror("Purchase", "Medicine not found!")
                conn.close()
            else:
                messagebox.showerror("Purchase", "All fields are required!")

        # Create a new purchase window
        purchase_window = Toplevel(inventory_window)
        purchase_window.title("Buy Medicine")
        purchase_window.geometry("400x400")
        purchase_window.configure(bg="#1e1e2f")

        Label(purchase_window, text="Customer Name", font=("Arial", 12,"bold"), bg="red").pack(pady=10)
        entry_customer_name = Entry(purchase_window, font=("Arial", 12))
        entry_customer_name.pack(pady=5)

        Label(purchase_window, text="Phone Number", font=("Arial", 12,"bold"), bg="orange").pack(pady=10)
        entry_customer_phone = Entry(purchase_window, font=("Arial", 12))
        entry_customer_phone.pack(pady=5)

        Label(purchase_window, text="Medicine Name", font=("Arial", 12,"bold"), bg="pink").pack(pady=10)
        entry_medicine_name = Entry(purchase_window, font=("Arial", 12))
        entry_medicine_name.pack(pady=5)

        Label(purchase_window, text="Quantity", font=("Arial", 12,"bold"), bg="yellow").pack(pady=10)
        entry_quantity = Entry(purchase_window, font=("Arial", 12))
        entry_quantity.pack(pady=5)

        Button(purchase_window, text="Confirm Purchase", font=("Arial", 12,"bold"), bg="blue", fg="white",command=process_purchase).pack(pady=20)
        

    # Inventory Window Layout
    # Top Frame for Entry Fields
    frame_top = Frame(inventory_window, bg="#ffffff", relief=SOLID, bd=2)
    frame_top.pack(side=TOP, fill=X, padx=10, pady=10)


    # Buttons
    add_button = Button(frame_top, text="Add Item", font=("Arial", 12,"bold"), bg="#1e1e2f", fg="#ffffff", command=add_item)
    add_button.grid(row=2, column=5, padx=10, pady=10)

    remove_button = Button(frame_top, text="Remove Item", font=("Arial", 12,"bold"), bg="#1e1e2f",foreground="black", fg="#ffffff", command=remove_item)
    remove_button.grid(row=2, column=7, padx=10, pady=10)

    buy_button = Button(frame_top, text="Buy Medicine", font=("Arial", 12,"bold"), bg="#1e1e2f",foreground="black", fg="#ffffff", command=buy_medicine)
    buy_button.grid(row=2, column=9, padx=10, pady=10)




    # Bottom Frame for Table
    frame_bottom = Frame(inventory_window, bg="#1e1e2f")
    frame_bottom.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Inventory Table
    columns = ("Item Name", "Price", "Quantity", "Category", "Discount")
    inventory_table = ttk.Treeview(frame_bottom, columns=columns, show='headings')
    inventory_table.pack(fill=BOTH, expand=True)

    # Set Table Headings
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#ffffff",
        fieldbackground="#ffffff",
        foreground="black",
        rowheight=25,
    )
    style.configure(
        "Treeview.Heading",
        font=("Arial", 12, "bold"),
        background="#2b2b3d",
        foreground="#ffffff",
    )
    style.map("Treeview.Heading", background=[("active", "#00aaff")])
    for col in columns:
        inventory_table.heading(col, text=col)
        inventory_table.column(col, anchor=CENTER, width=150)

    # Initial Data Load
    view_items()

    inventory_window.mainloop()

# Login Screen
def show_login_screen():
    global login_window, entry_username, entry_password
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#2b2b3d")

    def sign_up():
        # Create the sign-up window
        sign_up_window = Toplevel(login_window)
        sign_up_window.title("Sign Up")
        sign_up_window.geometry("400x300")
        sign_up_window.configure(bg="#2b2b3d")

        def register_user():
            new_username = entry_new_username.get()
            new_password = entry_new_password.get()

            if new_username and new_password:
                conn = create_connection()
                cursor = conn.cursor()
                # Check if the username already exists
                query_check = "SELECT * FROM Users WHERE username = %s"
                cursor.execute(query_check, (new_username,))
                if cursor.fetchone():
                    messagebox.showerror("Sign Up", "Username already exists!")
                else:
                    # Insert the new user into the database
                    query_insert = "INSERT INTO Users (username, password) VALUES (%s, %s)"
                    cursor.execute(query_insert, (new_username, new_password))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Sign Up", "Registration successful!")
                    sign_up_window.destroy()
            else:
                messagebox.showerror("Sign Up", "All fields are required!")

        # Sign-Up Window Layout
        Label(
            sign_up_window, text="Create New Account", font=("Arial", 14, "bold"), bg="#2b2b3d", fg="#ffffff"
        ).pack(pady=10)

        Label(
            sign_up_window, text="Username", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
        ).pack(pady=5)
        entry_new_username = Entry(sign_up_window, font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
        entry_new_username.pack(pady=5)

        Label(
            sign_up_window, text="Password", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
        ).pack(pady=5)
        entry_new_password = Entry(sign_up_window, show="*", font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
        entry_new_password.pack(pady=5)

        Button(
            sign_up_window,
            text="Register",
            font=("Arial", 12, "bold"),
            bg="#00aaff",
            fg="#ffffff",
            command=register_user,
        ).pack(pady=20)

    # Existing Login Page Layout
    Label(
        login_window, text="PHARMACY MANAGEMENT", font=("Arial", 14, "bold"), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=10)

    Label(
        login_window, text="Username", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=5)
    entry_username = Entry(login_window, font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
    entry_username.pack(pady=5)

    Label(
        login_window, text="Password", font=("Arial", 12), bg="#2b2b3d", fg="#ffffff"
    ).pack(pady=5)
    entry_password = Entry(login_window, show="*", font=("Arial", 12), bg="#3b3b4f", fg="#ffffff", insertbackground="#ffffff")
    entry_password.pack(pady=5)

    # Login Button
    Button(
        login_window,
        text="Login",
        font=("Arial", 12, "bold"),
        bg="#00aaff",
        fg="#ffffff",
        command=login,
    ).pack(side=LEFT, padx=(80, 10), pady=20)

    # Sign-Up Button
    Button(
        login_window,
        text="Sign Up",
        font=("Arial", 12, "bold"),
        bg="#00aaff",
        fg="#ffffff",
        command=sign_up,
    ).pack(side=RIGHT, padx=(10, 80), pady=20)

    login_window.mainloop()

# Run the application
show_login_screen()
