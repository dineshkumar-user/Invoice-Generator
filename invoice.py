import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfgen import canvas

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

@st.cache_data
def load_data(file):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()

def generate_bill_pdf(cid, customer_data, seller_data, items):

    pdf_file = f"Invoice_{cid}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)


    c.setFont("Helvetica-Bold", 20)
    c.drawRightString(550, 750, "INVOICE")

    c.setFont("Helvetica", 11)
    c.drawString(50, 730, f"Invoice Number: INV-{cid}")
    c.drawString(50, 710, f"Invoice Date: {pd.Timestamp.today().strftime('%d/%m/%Y')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 670, "Seller Details:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 650, seller_data['name'])
    c.drawString(50, 635, seller_data['city'])
    c.drawString(50, 620, f"Phone: {seller_data['phone']}")
    c.drawString(50, 605, f"Email: {seller_data['email']}")

    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, 670, "Buyer Details:")
    c.setFont("Helvetica", 11)
    c.drawString(300, 650, customer_data['Name'])
    c.drawString(300, 620, f"Phone: {customer_data['Contact']}")

    c.line(50, 590, 550, 590)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 570, "Item")
    c.drawString(250, 570, "Qty")
    c.drawString(330, 570, "Price")
    c.drawString(450, 570, "Total")
    c.line(50, 560, 550, 560)

    
    y = 540
    subtotal = 0

    c.setFont("Helvetica", 11)

    for item in items:
        name = item['name']
        qty = item['qty']
        price = item['price']
        total = qty * price

        subtotal += total

        c.drawString(50, y, name)
        c.drawString(260, y, str(qty))
        c.drawString(340, y, f"RS {price}")
        c.drawString(460, y, f"RS {total}")

        y -= 20

    c.line(50, y, 550, y)

    
    gst = subtotal * 0.05
    grand_total = subtotal + gst

    y -= 40
    c.drawRightString(500, y, f"Subtotal: RS {subtotal}")
    y -= 20
    c.drawRightString(500, y, f"GST (5%): RS {int(gst)}")
    y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(500, y, f"Grand Total: RS {int(grand_total)}")

    c.save()

    return pdf_file
def set_background(image_path):
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        h1 {{
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
if not st.session_state.logged_in:
    login_page()
    st.stop()

set_background("invoice.jfif")
st.title("INVOICE GENERATOR")

# Logout button (ADD THIS ALSO)
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = st.sidebar.selectbox("Choose an option:", ["Admin", "Exit"])

menu_file = "Products.csv"
customer_file = "Customer.csv"
sales_file = "Sales.csv"

if menu == "Admin":
    admin_option = st.sidebar.selectbox("Admin Options:", [
        "Product Details", "Customer Details", "Sales Report", "Generate Bill", "Exit"
    ])
    
    if admin_option == "Product Details":
        product_action = st.sidebar.selectbox("Choose Action:", [
            "View product", "Add Item", "Search Item", "Change Item", "Remove Item", "Back"
        ])
        
        if product_action == "View product":
            try:
                df = pd.read_csv(menu_file, index_col='Pid')
                st.write("### Product")
                st.write(df)
            except FileNotFoundError:
                st.error("Menu file not found!")
        
        elif product_action == "Add Item":
            Pid = st.number_input("Enter Product ID:", min_value=0, step=1)
            fname = st.text_input("Enter Product Name:")
            price = st.number_input("Enter Price:", min_value=0.0, step=0.1)
            
            if st.button("Add Item"):
                new_item = pd.DataFrame({'Pid': [Pid], 'Name': [fname], 'Price': [price]})
                try:
                    if not pd.read_csv(menu_file).empty:
                        new_item.to_csv(menu_file, mode='a', index=False, header=False)
                    else:
                        new_item.to_csv(menu_file, index=False)
                    st.success("Product item added successfully.")
                except FileNotFoundError:
                    new_item.to_csv(menu_file, index=False)
                    st.success("Menu file created and item added successfully.")
        
        elif product_action == "Search Item":
            try:
                df = pd.read_csv(menu_file, index_col='Pid')
                Pid = st.number_input("Enter Product ID:", min_value=0, step=1)
                
                if st.button("Search"):
                    if Pid in df.index:
                        st.write(df.loc[Pid])
                    else:
                        st.warning("Item not found.")
            except FileNotFoundError:
                st.error("Menu file not found!")
        
        elif product_action == "Change Item":
            try:
                df = pd.read_csv(menu_file, index_col='Pid')
                Pid = st.number_input("Enter Product ID to update:", min_value=0, step=1)
                
                if Pid in df.index:
                    fname = st.text_input("Enter new Product Name:", value=df.loc[Pid, 'Name'])
                    price = st.number_input("Enter new Price:", min_value=0.0, step=0.1, value=float(df.loc[Pid, 'Price']))
                    
                    if st.button("Update Item"):
                        df.loc[Pid] = [fname, price]
                        df.to_csv(menu_file)
                        st.success("Item updated successfully.")
                else:
                    st.warning("Item ID not found.")
            except FileNotFoundError:
                st.error("Product file not found!")
        
        elif product_action == "Remove Item":
            try:
                df = pd.read_csv(menu_file, index_col='Pid')
                Pid = st.number_input("Enter Product ID to remove:", min_value=0, step=1)
                
                if st.button("Remove Item"):
                    if Pid in df.index:
                        df = df.drop(Pid)
                        df.to_csv(menu_file)
                        st.success("Item removed successfully.")
                    else:
                        st.warning("Item ID not found.")
            except FileNotFoundError:
                st.error("Product file not found!")
    elif admin_option == "Customer Details":
        customer_action = st.sidebar.selectbox("Choose Action:", ["View Customers", "Search Customer", "Add Customer", "Update Customer", "Delete Customer", "Back"])

        if customer_action == "View Customers":
            try:
                df = pd.read_csv(customer_file, index_col='Cid')
                st.write("### Customers")
                st.write(df)
            except FileNotFoundError:
                st.error("Customer file not found!")

        elif customer_action == "Search Customer":
            try:
                df = pd.read_csv(customer_file, index_col='Cid')
                cid = st.number_input("Enter Customer ID:", min_value=0, step=1)
                if st.button("Search"):
                    if cid in df.index:
                        st.write(df.loc[cid])
                    else:
                        st.warning("Customer not found.")
            except FileNotFoundError:
                st.error("Customer file not found!")

        elif customer_action == "Add Customer":
            try:
                menu_df = pd.read_csv(menu_file, index_col='Pid')  # Load menu for item selection
            except FileNotFoundError:
                st.error("Menu file not found! Add items to the menu before adding customers.")
                menu_df = None

            if menu_df is not None:
                cid = st.number_input("Enter Customer ID:", min_value=0, step=1)
                name = st.text_input("Enter Name:")
                gender = st.selectbox("Select Gender:", ["Male", "Female", "Other"])
                contact = st.text_input("Enter Contact:")
                email = st.text_input("Enter Email:")

                # Food order selection
                st.write("### Select Items for the Order")
                selected_items = st.multiselect(
                    "Items", menu_df.index,
                    format_func=lambda x: f"{x} - {menu_df.loc[x, 'Name']} (₹{menu_df.loc[x, 'Price']})"
                )

                # Add quantity for selected items
                quantities = {}
                for item in selected_items:
                    quantities[item] = st.number_input(
                        f"Quantity for {menu_df.loc[item, 'Name']}",
                        min_value=1,
                        step=1
                    )

                if selected_items:
                    order_value = sum(menu_df.loc[item, 'Price'] * quantities[item] for item in selected_items)
                else:
                    order_value = 0.0

                gst = order_value * 0.05  # 5% GST
                total_with_gst = order_value + gst

                st.write(f"### Total Order Value: RS{order_value:.2f}")
                st.write(f"### GST (5%): RS{gst:.2f}")
                st.write(f"### Total Bill Amount (with GST): RS{total_with_gst:.2f}")

                if st.button("Add Customer"):
                    items_list = []
                    for item in selected_items:
                        items_list.append({
                            'name': menu_df.loc[item, 'Name'],
                            'qty': int(quantities[item]),
                            'price': float(menu_df.loc[item, 'Price'])
                        })

                    new_customer = pd.DataFrame({
                        'Cid': [cid],
                        'Name': [name],
                        'Gender': [gender],
                        'Contact': [contact],
                        'Email': [email],
                        'Bill_Amt': [total_with_gst],
                        'Items': [json.dumps(items_list)]
                        })

                    try:
                        if not pd.read_csv(customer_file).empty:
                            new_customer.to_csv(customer_file, mode='a', index=False, header=False)
                        else:
                            new_customer.to_csv(customer_file, index=False)
                        st.success("Customer added successfully.")
                    except FileNotFoundError:
                        new_customer.to_csv(customer_file, index=False)
                        st.success("Customer file created and customer added successfully.")

                    sales_data = []
                    for item, qty in quantities.items():
                        sales_data.append({'Item': menu_df.loc[item, 'Name'], 'Quantity': qty})

                    sales_df = pd.DataFrame(sales_data)
                    try:
                        if not pd.read_csv(sales_file).empty:
                            sales_df.to_csv(sales_file, mode='a', index=False, header=False)
                        else:
                            sales_df.to_csv(sales_file, index=False)
                    except FileNotFoundError:
                        sales_df.to_csv(sales_file, index=False)

                    st.write("### Updated Sales Data")
                    try:
                        df = pd.read_csv(sales_file)
                        sales_summary = df.groupby('Item')['Quantity'].sum()
                        fig, ax = plt.subplots()
                        sales_summary.plot(kind='bar', ax=ax, color='skyblue')
                        ax.set_title("Sales Analysis")
                        ax.set_xlabel("Item Names")
                        ax.set_ylabel("Quantity Sold")
                        st.pyplot(fig)
                    except FileNotFoundError:
                        st.warning("Sales file not found! Sales data visualization unavailable.")

        elif customer_action == "Update Customer":
            try:
                df = pd.read_csv(customer_file, index_col='Cid', dtype={'Contact': str})
                cid = st.number_input("Enter Customer ID to update:", min_value=0, step=1)
                if cid in df.index:
                    name = st.text_input("Enter new Name:", value=df.loc[cid, 'Name'])
                    gender = st.text_input("Enter Gender:", value=df.loc[cid, 'Gender'])
                    contact = st.text_input("Enter Contact:", value=df.loc[cid, 'Contact'])
                    gmail = st.text_input("Enter Gmail:", value=df.loc[cid, 'Email'])
                    bill_amt = st.number_input("Enter Bill Amount:", min_value=0.0, step=0.1, value=df.loc[cid, 'Bill_Amt'])
                    if st.button("Update Customer"):
                        df.loc[cid, 'Name'] = name
                        df.loc[cid, 'Gender'] = gender
                        df.loc[cid, 'Contact'] = contact
                        df.loc[cid, 'Email'] = gmail
                        df.loc[cid, 'Bill_Amt'] = bill_amt
                        df.to_csv(customer_file)
                        st.success("Customer updated successfully.")
                else:
                    st.warning("Customer ID not found.")
            except FileNotFoundError:
                st.error("Customer file not found!")

        elif customer_action == "Delete Customer":
            try:
                df = pd.read_csv(customer_file, index_col='Cid')
                cid = st.number_input("Enter Customer ID to delete:", min_value=0, step=1)
                if st.button("Delete Customer"):
                    if cid in df.index:
                        df = df.drop(cid)
                        df.to_csv(customer_file)
                        st.success("Customer deleted successfully.")
                    else:
                        st.warning("Customer ID not found.")
            except FileNotFoundError:
                st.error("Customer file not found!")
    
    elif admin_option == "Sales Report":
        try:
            df = pd.read_csv(sales_file)
            sales_summary = df.groupby('Item')['Quantity'].sum()
            
            st.write("### Sales Report")
            fig, ax = plt.subplots()
            sales_summary.plot(kind='bar', ax=ax, color='red')
            ax.set_title("Sales Analysis")
            ax.set_xlabel("Item Names")
            ax.set_ylabel("Quantity Sold")
            st.pyplot(fig)
        except FileNotFoundError:
            st.error("Sales file not found!")
    
    elif admin_option == "Generate Bill":
        try:
            df = pd.read_csv(customer_file, index_col='Cid')
            cid = st.number_input("Enter Customer ID:", min_value=0, step=1)
            
            st.write("### Seller Details")
            seller_name = st.text_input("Seller Name", "ABC Company")
            seller_city = st.text_input("City", "Chennai, Tamil Nadu")
            seller_phone = st.text_input("Phone", "9876543210")
            seller_email = st.text_input("Email", "abc@gmail.com")

            if st.button("Generate Bill",key="generate_bill_button"):
                if cid in df.index:
                    st.write("### Bill Details")
                    st.write(df.loc[cid])
                    total_bill = df.loc[cid, 'Bill_Amt']
                    st.write(f"**Total Bill Amount (with GST): ₹{total_bill:.2f}**")
                    customer_data = df.loc[cid].to_dict()
                    seller_data = {
                        "name": seller_name,
                        "city": seller_city,
                        "phone": seller_phone,
                        "email": seller_email
                    }

                    items = []
                    if customer_data.get("Items"):
                        try:
                            items = json.loads(customer_data["Items"])
                        except json.JSONDecodeError:
                            items = []

                    pdf_file = generate_bill_pdf(cid, customer_data, seller_data, items)
                    with open(pdf_file, "rb") as f:
                        pdf_bytes = f.read()
                        st.download_button(
                            label="Download Bill",
                            data=pdf_bytes,
                            file_name=pdf_file,
                            mime="application/pdf"
                            )
                else:
                    st.warning("Customer ID not found.")
        except FileNotFoundError:
            st.error("Customer file not found!")


    elif admin_option == "Exit":
        st.sidebar.success("Exiting Admin Panel.")

elif menu == "Exit":
    st.sidebar.success("Exiting Application.")