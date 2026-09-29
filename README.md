Smart Billing System

A desktop-based Smart Retail Billing System built with Python and Tkinter for managing products, billing, inventory, customers, users, reports, and invoice generation.

The application is designed for small retail businesses and provides a local, offline-first workflow with SQLite database storage.

✨ Features

🔐 Authentication & User Management

Secure login system

Admin and Staff roles

Password hashing with bcrypt

User creation and management

Password change functionality

User/activity tracking

📦 Product & Inventory Management

Add, edit, delete, and search products

Product categories

Cost price and selling price

Stock quantity tracking

Expiry date support

Automatic stock reduction after sales

Purchase and stock adjustment entries

Low-stock alerts

Stock movement history

🧾 Billing & Invoices

Create customer invoices

Add multiple products to a bill

Item-wise discounts

Invoice-level discounts

Customizable GST calculation

Payment modes:

Cash

UPI

Card

Automatic subtotal, discount, GST, and grand-total calculation

Auto-generated invoice IDs

PDF invoice generation

Invoice history

📊 Dashboard & Reports

Today's sales

Today's invoice count

Monthly revenue

Low-stock products

Top-selling products

Sales trends

Profit analysis

Product-wise sales analysis

Daily, weekly, and monthly reports

CSV export

🏷️ Barcode & QR Code

Automatic product barcode generation

QR code generation

Barcode image storage

Barcode scanning support through the barcode utility

👥 Customer Management

Customer records

Phone and email information

Purchase history

Total purchase tracking

Loyalty-points foundation

💾 Data Management

Local SQLite database

Automatic database initialization

Backup and restore functionality

CSV export

No cloud database required

🖥️ Desktop GUI

Tkinter-based graphical interface

Login screen

Dashboard

Product management

Billing window

Reports

Settings

Input validation and error messages

🛠️ Tech Stack

Technology

Purpose

Python

Core programming language

Tkinter

Desktop GUI

SQLite

Local database

bcrypt

Password hashing

Matplotlib

Charts and analytics

ReportLab

PDF invoice generation

python-barcode

Barcode generation

qrcode

QR code generation

Pillow

Image processing

OpenCV

Image/camera processing

pyzbar

Barcode scanning

CSV / Python Standard Library

Data export and utilities

🏗️ Project Structure

Smart-Billing-System/
│
├── app.py                         # Main application entry point
├── quick_start.py                 # Creates demo data
├── test_installation.py           # Installation verification
├── requirements.txt               # Python dependencies
│
├── gui/                           # User interface
│   ├── main_window.py
│   ├── login_window.py
│   ├── dashboard.py
│   ├── products.py
│   ├── billing.py
│   ├── reports.py
│   └── settings.py
│
├── models/                        # Application data models
│   └── models.py
│
├── utils/                         # Business logic and utilities
│   ├── storage.py                 # SQLite storage
│   ├── auth.py                    # Authentication
│   ├── billing.py                 # Billing calculations
│   ├── barcode.py                 # Barcode / QR generation
│   └── pdf_generator.py           # PDF invoice generation
│
├── data/                          # Runtime application data
│   └── pos_database.sqlite        # Local SQLite database
│
├── barcodes/                      # Generated barcode/QR images
├── invoices/                      # Generated PDF invoices
│
├── FEATURES.md                    # Detailed feature documentation
├── SETUP.md                       # Detailed setup guide
├── PROJECT_SUMMARY.md             # Project summary
├── Project_Presentation_Guide.md  # Presentation reference
└── INDEX.md                       # File index

data/, barcodes/, and invoices/ contain runtime/generated files and should normally not be committed to Git.

🚀 Installation

1. Clone the repository

git clone https://github.com/VaradP07/Smart-Billing-System.git
cd Smart-Billing-System

2. Create a virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Verify the installation

python test_installation.py

5. Start the application

python app.py

🧪 Demo Data

For testing, the project includes a demo-data script:

python quick_start.py --demo

This creates sample users, products, and customers.

Demo login

Username: admin
Password: admin123

Important: Change the default password after first login. Do not use the demo password for a real deployment.

🧮 Billing Calculation

The application calculates invoice totals using the following flow:

Item Total
    ↓
Item Discount
    ↓
Subtotal
    ↓
Invoice Discount
    ↓
Taxable Amount
    ↓
GST
    ↓
Grand Total

Profit

Profit = (Selling Price - Cost Price) × Quantity

Profit Margin

Profit Margin % =
((Selling Price - Cost Price) / Selling Price) × 100

🗄️ Database

The current implementation uses SQLite through utils/storage.py.

The database is automatically created at:

data/pos_database.sqlite

The application initializes tables for:

Products

Invoices

Bill Items

Customers

Users

Stock Movements

No separate database server is required.

🔒 Security

The project includes:

bcrypt password hashing

Role-based access

Admin/Staff separation

Input validation

Local data storage

Backup and restore functionality

Important

Do not commit:

passwords

.env files

generated databases containing personal/customer data

private backups

generated invoices containing sensitive information

📈 Reports

The reporting module supports:

Daily sales

Weekly sales

Monthly sales

Revenue analysis

Profit analysis

GST summary

Product sales

Top-selling products

Average invoice value

CSV export

Charts are generated using Matplotlib.

🧪 Testing

Run:

python test_installation.py

The test script checks the project environment and required components.

For a clean test environment, create a new virtual environment before installing the dependencies.

🖼️ Screenshots

Add screenshots of the following screens to make the repository easier to understand:

screenshots/
├── login.png
├── dashboard.png
├── products.png
├── billing.png
├── reports.png
└── settings.png

Then reference them in this README, for example:

![Dashboard](screenshots/dashboard.png)

🔮 Future Enhancements

Possible future improvements include:

Cloud database support

Multi-store / multi-location support

Email receipts

SMS notifications

Advanced inventory forecasting

Mobile application

Cloud synchronization

Multi-language support

Custom themes

Advanced analytics

🎓 Project Information

Project: Smart Billing System
Type: Desktop Retail Billing & Inventory Management System
Language: Python
GUI: Tkinter
Database: SQLite
Version: 1.0.0

👨‍💻 Author

Varad Patil

GitHub: VaradP07

📄 License

This project is intended for educational and project-development purposes.

If you plan to distribute or deploy it commercially, add an appropriate open-source or proprietary license.