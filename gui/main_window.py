"""Main application window"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.login_window import LoginWindow
from gui.dashboard import DashboardWindow
from gui.products import ProductWindow
from gui.billing import BillingWindow
from gui.reports import ReportsWindow
from gui.settings import SettingsWindow
from utils.storage import StorageManager
from utils.auth import AuthManager
from utils.billing import BillingEngine
from utils.barcode import BarcodeManager
from models.models import User
import tkinter.simpledialog as simpledialog


class MainWindow:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Smart Retail Billing System")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # apply global style/theme colors
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabelframe', background='#f5f5f5', foreground='#333333')
        style.configure('TLabel', background='#f5f5f5', foreground='#333333')
        style.configure('TButton', background='#007acc', foreground='white')
        style.map('TButton',
                  background=[('active', '#005f99'), ('disabled', '#cccccc')],
                  foreground=[('disabled', '#888888')])
        style.configure('TCombobox', fieldbackground='white', background='white')

        # Initialize managers
        self.storage = StorageManager()
        self.auth = AuthManager(self.storage)
        self.billing = BillingEngine(self.storage)
        self.barcode_mgr = BarcodeManager()
        
        self.current_user = None
        self.login_window = None
        # track currently opened Toplevel (dashboard/products/etc)
        self.active_window = None
        
        # Ensure at least one admin user exists
        self.ensure_admin_exists()
        
        # Show login
        self.show_login()

    def close_active_window(self):
        """Close any previously opened Toplevel window"""
        if self.active_window is not None:
            try:
                self.active_window.destroy()
            except Exception:
                pass
            self.active_window = None

    def ensure_admin_exists(self):
        """Ensure at least one admin user exists"""
        users = self.storage.get_all_users()
        if not users:
            # Create default admin
            self.auth.create_user("admin", "admin123", "admin", "Administrator")

    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow(self.root, self.storage, self.auth)
        self.login_window.on_login_success = self.on_login_success

    def on_login_success(self, user: User):
        """Handle successful login"""
        self.current_user = user
        # login_window is rendered on the same root; no separate
        # window object exists. Setup_main_ui will clear the root
        # widgets, so simply call it directly.
        self.setup_main_ui()

    def setup_main_ui(self):
        """Setup main UI after login"""
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()

        # Header frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(header_frame, text="Smart Retail Billing System", font=("Arial", 16, "bold")).pack(anchor=tk.W)
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(anchor=tk.E)
        ttk.Label(user_frame, text=f"User: {self.current_user.name} ({self.current_user.role})", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        ttk.Button(user_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X)

        # Menu buttons frame
        menu_frame = ttk.Frame(self.root, padding="10")
        menu_frame.pack(fill=tk.X)

        # Configure grid columns to be expandable
        for i in range(5):
            menu_frame.columnconfigure(i, weight=1)

        ttk.Button(menu_frame, text="📊 Dashboard", command=self.open_dashboard).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(menu_frame, text="📦 Products", command=self.open_products).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(menu_frame, text="💳 Billing", command=self.open_billing).grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(menu_frame, text="📈 Reports", command=self.open_reports).grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(menu_frame, text="⚙️ Settings", command=self.open_settings).grid(row=0, column=4, padx=5, pady=5, sticky=tk.EW)

        # Main content area
        content_frame = ttk.LabelFrame(self.root, text="Welcome", padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        welcome_label = ttk.Label(content_frame, text=f"Welcome, {self.current_user.name}!", 
                                 font=("Arial", 18, "bold"))
        welcome_label.pack(pady=20)

        info_text = f"""
Smart Retail Billing System - Advanced Features:

✓ Product Management - Add, edit, and manage products with barcodes
✓ Billing System - Create invoices with GST and discount calculations
✓ Inventory Tracking - Track stock movements and low stock alerts
✓ Reports & Analytics - View sales, profit, and product analytics
✓ User Management - Manage staff and admin accounts
✓ Backup & Restore - Backup and restore your data
✓ PDF Invoices - Generate professional PDF invoices

Click on the menu buttons above to get started!
        """
        info_label = ttk.Label(content_frame, text=info_text, justify=tk.LEFT, font=("Arial", 10))
        info_label.pack(anchor=tk.W, padx=20)

    def open_dashboard(self):
        """Open dashboard window"""
        self.close_active_window()
        win = DashboardWindow(self.root, self.storage, self.current_user)
        # track its Toplevel to allow closing later
        self.active_window = getattr(win, 'window', None)

    def open_products(self):
        """Open products window"""
        self.close_active_window()
        win = ProductWindow(self.root, self.storage, self.barcode_mgr)
        self.active_window = getattr(win, 'window', None)

    def open_billing(self):
        """Open billing window"""
        self.close_active_window()
        win = BillingWindow(self.root, self.storage, self.billing, self.barcode_mgr, self.current_user)
        self.active_window = getattr(win, 'window', None)

    def open_reports(self):
        """Open reports window"""
        self.close_active_window()
        win = ReportsWindow(self.root, self.storage, self.billing)
        self.active_window = getattr(win, 'window', None)

    def open_settings(self):
        """Open settings window"""
        self.close_active_window()
        win = SettingsWindow(self.root, self.storage, self.auth, self.current_user)
        self.active_window = getattr(win, 'window', None)

    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Confirm", "Logout?"):
            self.current_user = None
            self.show_login()

    def on_closing(self):
        """Handle window closing"""
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    root.geometry("1000x600")
    root.minsize(800, 600)
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam')
    
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
