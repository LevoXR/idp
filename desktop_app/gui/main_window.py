"""
Main application window using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .home_frame import HomeFrame
from .login_frame import LoginFrame
from .register_frame import RegisterFrame
from .dashboard_frame import DashboardFrame
from .assessment_frame import AssessmentFrame
from .result_frame import ResultFrame
from models import get_db, User


class MainWindow:
    """Main application window controller"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aditya Setu - Health Assessment")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#F8F9FA')
        
        # Center the window
        self.center_window()
        
        # Current user session
        self.current_user = None
        
        # Style configuration
        self.setup_styles()
        
        # Create header frame (will be shown when logged in)
        self.header_frame = None
        
        # Create main container (full window)
        self.container = tk.Frame(self.root, bg='#F8F9FA')
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Start with home page
        self.show_home()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles with lighter, brighter colors
        style.configure('Primary.TButton', 
                       padding=(12, 8), 
                       font=('Segoe UI', 10, 'bold'),
                       background='#4A90E2',
                       foreground='white')
        style.map('Primary.TButton',
                 background=[('active', '#357ABD')])
        
        style.configure('Success.TButton', 
                       padding=(12, 8), 
                       font=('Segoe UI', 10),
                       background='#27AE60',
                       foreground='white')
        style.map('Success.TButton',
                 background=[('active', '#229954')])
        
        style.configure('Danger.TButton', 
                       padding=(12, 8), 
                       font=('Segoe UI', 10),
                       background='#E74C3C',
                       foreground='white')
        style.map('Danger.TButton',
                 background=[('active', '#C0392B')])
        
        style.configure('Yellow.TButton',
                       padding=(10, 6),
                       font=('Segoe UI', 10),
                       background='#FDD835',
                       foreground='#333333')
        style.map('Yellow.TButton',
                 background=[('active', '#FBC02D')])
        
        style.configure('Clear.TButton',
                       padding=(10, 6),
                       font=('Segoe UI', 10),
                       background='white',
                       foreground='#333333',
                       borderwidth=1)
    
    def clear_container(self):
        """Clear all widgets from container"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def create_header(self, show_nav=True):
        """Create modern purple gradient header with navigation"""
        if self.header_frame:
            self.header_frame.destroy()
        
        self.header_frame = tk.Frame(self.root, bg='#9C88FF', height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)
        
        # Left side - Logo
        logo_frame = tk.Frame(self.header_frame, bg='#9C88FF')
        logo_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Shield icon (simplified as text)
        logo_text = tk.Label(
            logo_frame,
            text="✓ Aditya Setu",
            font=('Segoe UI', 16, 'bold'),
            bg='#9C88FF',
            fg='white'
        )
        logo_text.pack(side=tk.LEFT)
        
        # Navigation links (center)
        if show_nav and self.current_user:
            nav_frame = tk.Frame(self.header_frame, bg='#9C88FF')
            nav_frame.pack(side=tk.LEFT, padx=40)
            
            nav_links = [
                ("Home", lambda: self.show_dashboard()),
                ("Dashboard", lambda: self.show_dashboard()),
                ("Take Assessment", lambda: self.show_assessment()),
            ]
            
            for text, command in nav_links:
                link = tk.Label(
                    nav_frame,
                    text=text,
                    font=('Segoe UI', 11),
                    bg='#9C88FF',
                    fg='white',
                    cursor='hand2'
                )
                link.pack(side=tk.LEFT, padx=15)
                link.bind('<Button-1>', lambda e, cmd=command: cmd())
        
        # Right side - User info or Login/Register or Alerts
        right_frame = tk.Frame(self.header_frame, bg='#9C88FF')
        right_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        if self.current_user:
            # Alerts link (on right side)
            alerts_link = tk.Label(
                right_frame,
                text="Alerts",
                font=('Segoe UI', 11),
                bg='#9C88FF',
                fg='white',
                cursor='hand2'
            )
            alerts_link.pack(side=tk.LEFT, padx=15)
            alerts_link.bind('<Button-1>', lambda e: self.show_dashboard())
            
            # User dropdown
            user_text = tk.Label(
                right_frame,
                text=f"👤 {self.current_user['name']}",
                font=('Segoe UI', 11),
                bg='#9C88FF',
                fg='white',
                cursor='hand2'
            )
            user_text.pack(side=tk.LEFT, padx=10)
            user_text.bind('<Button-1>', lambda e: self.logout())
        else:
            # Login/Register links
            login_link = tk.Label(
                right_frame,
                text="Login",
                font=('Segoe UI', 11),
                bg='#9C88FF',
                fg='white',
                cursor='hand2'
            )
            login_link.pack(side=tk.LEFT, padx=10)
            login_link.bind('<Button-1>', lambda e: self.show_login())
            
            register_link = tk.Label(
                right_frame,
                text="Register",
                font=('Segoe UI', 11),
                bg='#9C88FF',
                fg='white',
                cursor='hand2'
            )
            register_link.pack(side=tk.LEFT, padx=10)
            register_link.bind('<Button-1>', lambda e: self.show_register())
    
    def remove_header(self):
        """Remove header (for login/register pages)"""
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
    
    def show_home(self):
        """Show home/landing page"""
        self.clear_container()
        self.create_header(show_nav=False)
        HomeFrame(self.container, self)
    
    def show_login(self):
        """Show login frame"""
        self.clear_container()
        self.create_header(show_nav=False)
        LoginFrame(self.container, self)
    
    def show_register(self):
        """Show registration frame"""
        self.clear_container()
        self.create_header(show_nav=False)
        RegisterFrame(self.container, self)
    
    def show_dashboard(self):
        """Show dashboard frame"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            self.show_login()
            return
        
        self.create_header(show_nav=True)
        self.clear_container()
        DashboardFrame(self.container, self)
    
    def show_assessment(self):
        """Show assessment frame"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            self.show_login()
            return
        
        self.create_header(show_nav=True)
        self.clear_container()
        AssessmentFrame(self.container, self)
    
    def show_result(self, assessment_data):
        """Show assessment result frame"""
        if not self.current_user:
            messagebox.showerror("Error", "Please login first")
            self.show_login()
            return
        
        self.create_header(show_nav=True)
        self.clear_container()
        ResultFrame(self.container, self, assessment_data)
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.show_home()
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

