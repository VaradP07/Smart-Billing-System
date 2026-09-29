"""Product management window"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from utils.storage import StorageManager
from utils.barcode import BarcodeManager
from models.models import Product

def get_expiry_status(expiry_date_str):
    if not expiry_date_str: return ""
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
        try:
            exp_date = datetime.strptime(expiry_date_str.strip(), fmt).date()
            today = datetime.now().date()
            if exp_date < today:
                return "expired"
            elif exp_date <= today + timedelta(days=30):
                return "expiring"
            return ""
        except ValueError:
            continue
    return ""


class ProductWindow:
    """Product management UI"""

    def __init__(self, parent, storage: StorageManager, barcode_mgr: BarcodeManager):
        self.parent = parent
        self.storage = storage
        self.barcode_mgr = barcode_mgr
        
        self.window = tk.Toplevel(parent)
        self.window.title("Product Management")
        self.window.geometry("1000x700")
        self.window.minsize(900, 600)
        try:
            self.window.state("zoomed")
        except Exception:
            pass
        self.window.configure(bg='#f5f5f5')
        
        self.setup_ui()
        self.refresh_products()

    def setup_ui(self):
        """Create product management UI"""
        # Search frame
        search_frame = ttk.Frame(self.window)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_products())

        ttk.Button(search_frame, text="Search", command=self.search_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Refresh", command=self.refresh_products).pack(side=tk.LEFT, padx=5)

        # Products treeview
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(tree_frame, columns=(
            "Category", "Cost", "Selling", "Stock", "Barcode", "Expiry"
        ), yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=8)

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        self.tree.column("#0", width=150, minwidth=150)
        self.tree.column("Category", width=100, minwidth=100)
        self.tree.column("Cost", width=80, minwidth=80)
        self.tree.column("Selling", width=80, minwidth=80)
        self.tree.column("Stock", width=80, minwidth=80)
        self.tree.column("Barcode", width=120, minwidth=120)
        self.tree.column("Expiry", width=100, minwidth=100)

        self.tree.heading("#0", text="Product Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Cost", text="Cost Price")
        self.tree.heading("Selling", text="Selling Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Expiry", text="Expiry")

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Right-click menu
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Button-1>", self.on_tree_click)

        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)

        self.selected_item = None

    def on_tree_click(self, event):
        """Handle tree click"""
        item = self.tree.selection()
        if item:
            self.selected_item = item[0]

    def refresh_products(self):
        """Refresh product list"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = self.storage.get_all_products()
        for product in products:
            status = get_expiry_status(product.expiry_date)
            if status == "expired":
                tag = "expired"
            elif status == "expiring":
                tag = "expiring"
            else:
                tag = "low_stock" if product.stock_quantity <= 10 else ""
                
            self.tree.insert("", tk.END, text=product.name, values=(
                product.category,
                f"₹{product.cost_price:.2f}",
                f"₹{product.selling_price:.2f}",
                product.stock_quantity,
                product.barcode,
                product.expiry_date if product.expiry_date else "-"
            ), tags=(tag,))

        self.tree.tag_configure("low_stock", foreground="red")
        self.tree.tag_configure("expired", background="#ffcccc", foreground="black")
        self.tree.tag_configure("expiring", background="#fff3cd", foreground="black")

    def search_products(self):
        """Search products"""
        term = self.search_entry.get().strip()
        if not term:
            self.refresh_products()
            return

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = self.storage.search_products(term)
        for product in products:
            status = get_expiry_status(product.expiry_date)
            if status == "expired":
                tag = "expired"
            elif status == "expiring":
                tag = "expiring"
            else:
                tag = "low_stock" if product.stock_quantity <= 10 else ""
                
            self.tree.insert("", tk.END, text=product.name, values=(
                product.category,
                f"₹{product.cost_price:.2f}",
                f"₹{product.selling_price:.2f}",
                product.stock_quantity,
                product.barcode,
                product.expiry_date if product.expiry_date else "-"
            ), tags=(tag,))

    def add_product(self):
        """Show add product dialog"""
        dialog = ProductDialog(self.window, self.storage, self.barcode_mgr)
        self.window.wait_window(dialog.dialog)
        self.refresh_products()

    def edit_product(self):
        """Edit selected product"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a product")
            return

        # Get product from tree
        product_name = self.tree.item(self.selected_item, "text")
        products = self.storage.get_all_products()
        product = None
        for p in products:
            if p.name == product_name:
                product = p
                break

        if product:
            dialog = ProductDialog(self.window, self.storage, self.barcode_mgr, product)
            self.window.wait_window(dialog.dialog)
            self.refresh_products()

    def delete_product(self):
        """Delete selected product"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a product")
            return

        if messagebox.askyesno("Confirm", "Delete this product?"):
            product_name = self.tree.item(self.selected_item, "text")
            products = self.storage.get_all_products()
            for p in products:
                if p.name == product_name:
                    self.storage.delete_product(p.product_id)
                    self.refresh_products()
                    messagebox.showinfo("Success", "Product deleted")
                    break

    def show_context_menu(self, event):
        """Show context menu"""
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Edit", command=self.edit_product)
        menu.add_command(label="Delete", command=self.delete_product)
        menu.post(event.x_root, event.y_root)


class ProductDialog:
    """Product add/edit dialog"""

    def __init__(self, parent, storage: StorageManager, barcode_mgr: BarcodeManager, product: Product = None):
        self.storage = storage
        self.barcode_mgr = barcode_mgr
        self.product = product
        self.generated_barcode = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Product" if not product else "Edit Product")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)

        self.setup_ui()

        if product:
            self.populate_fields(product)

    def setup_ui(self):
        """Create dialog UI"""
        frame = ttk.Frame(self.dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        # Product Name
        ttk.Label(frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=10)

        # Category
        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.category_entry = ttk.Entry(frame, width=30)
        self.category_entry.grid(row=1, column=1, pady=10)

        # Cost Price
        ttk.Label(frame, text="Cost Price (₹):").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.cost_entry = ttk.Entry(frame, width=30)
        self.cost_entry.grid(row=2, column=1, pady=10)

        # Selling Price
        ttk.Label(frame, text="Selling Price (₹):").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.selling_entry = ttk.Entry(frame, width=30)
        self.selling_entry.grid(row=3, column=1, pady=10)

        # Stock Quantity
        ttk.Label(frame, text="Stock Quantity:").grid(row=4, column=0, sticky=tk.W, pady=10)
        self.stock_entry = ttk.Entry(frame, width=30)
        self.stock_entry.grid(row=4, column=1, pady=10)

        # Barcode
        ttk.Label(frame, text="Barcode:").grid(row=5, column=0, sticky=tk.W, pady=10)
        barcode_frame = ttk.Frame(frame)
        barcode_frame.grid(row=5, column=1, pady=10)
        self.barcode_entry = ttk.Entry(barcode_frame, width=20)
        self.barcode_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(barcode_frame, text="Generate", command=self.generate_barcode).pack(side=tk.LEFT)

        # Expiry Date
        ttk.Label(frame, text="Expiry (YYYY-MM-DD):").grid(row=6, column=0, sticky=tk.W, pady=10)
        self.expiry_entry = ttk.Entry(frame, width=30)
        self.expiry_entry.grid(row=6, column=1, pady=10)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def populate_fields(self, product: Product):
        """Populate fields with existing data"""
        self.name_entry.insert(0, product.name)
        self.category_entry.insert(0, product.category)
        self.cost_entry.insert(0, str(product.cost_price))
        self.selling_entry.insert(0, str(product.selling_price))
        self.stock_entry.insert(0, str(product.stock_quantity))
        self.barcode_entry.insert(0, product.barcode)
        self.expiry_entry.insert(0, product.expiry_date if hasattr(product, 'expiry_date') and product.expiry_date else "")

    def generate_barcode(self):
        """Generate barcode"""
        if self.product:
            barcode_num = BarcodeManager.generate_unique_barcode(self.product.product_id)
        else:
            import uuid
            barcode_num = BarcodeManager.generate_unique_barcode(str(uuid.uuid4()))
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.insert(0, barcode_num)

    def save(self):
        """Save product"""
        try:
            name = self.name_entry.get().strip()
            category = self.category_entry.get().strip()
            cost = float(self.cost_entry.get())
            selling = float(self.selling_entry.get())
            stock = int(self.stock_entry.get())
            barcode = self.barcode_entry.get().strip()
            expiry_date = self.expiry_entry.get().strip()

            if not name or not category or cost < 0 or selling < 0 or stock < 0:
                messagebox.showerror("Error", "Invalid input")
                return

            if self.product:
                # Edit
                self.product.name = name
                self.product.category = category
                self.product.cost_price = cost
                self.product.selling_price = selling
                self.product.stock_quantity = stock
                self.product.barcode = barcode
                self.product.expiry_date = expiry_date
                self.storage.update_product(self.product)
                # Regenerate barcode and QR code images
                if barcode:
                    self.barcode_mgr.generate_barcode(barcode, self.product.product_id)
                    self.barcode_mgr.generate_qr_code(barcode, self.product.product_id)
                messagebox.showinfo("Success", "Product updated")
            else:
                # Add new
                product = Product(
                    name=name,
                    category=category,
                    cost_price=cost,
                    selling_price=selling,
                    stock_quantity=stock,
                    barcode=barcode,
                    expiry_date=expiry_date
                )
                self.storage.add_product(product)
                # Generate barcode image and QR code image
                if barcode:
                    self.barcode_mgr.generate_barcode(barcode, product.product_id)
                    self.barcode_mgr.generate_qr_code(barcode, product.product_id)
                messagebox.showinfo("Success", "Product added")

            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid number format")
