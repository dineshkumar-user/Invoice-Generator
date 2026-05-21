INVOICE GENERATOR SYSTEM USING PYTHON

A Streamlit-based Invoice Generator application that allows admins to manage products, customers, sales, and generate professional PDF invoices.
Features

Authentication:
* Simple login system
* Default credentials

Product Management:
* View all products
* Add new products
* Search products by ID
* Update product details
* Delete products

Customer Management:
* View all customers
* Add new customers with order details
* Search customers
* Update customer details
* Delete customers

Billing System
* Select products and quantities
* Automatic calculation:
  * Total amount
  * GST (5%)
  * Final bill amount
* Stores order details in structured format

Sales Analysis:
* Tracks item-wise sales
* Displays bar chart visualization using Matplotlib

PDF Invoice Generation:
Generates professional invoices using ReportLab
* Includes:
  * Seller details
  * Customer details
  * Itemized billing
  * GST calculation
  * Grand total
* Downloadable invoice file

---

Tech Stack:
* **Frontend & Backend:Streamlit
* **Data Handling:Pandas
* **Visualization:Matplotlib
* **PDF Generation:ReportLab
* **Storage:CSV files

File Structure:
project/
│── app.py
│── Products.csv
│── Customer.csv
│── Sales.csv
│── invoice.jfif

How It Works:
1. Login as admin
2. Add products to the system
3. Add customers and select items
4. System calculates total + GST automatically
5. Generate and download invoice as PDF
6. View sales analytics


UI Features:
* Background image support
* Sidebar navigation
* Interactive forms
* Dynamic charts

Future Enhancements:
* Database integration (MySQL)
* User roles (Admin/User)
* Email invoice sending
* Dashboard analytics
* AI-based sales insights
