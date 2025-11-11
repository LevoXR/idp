"""
Login frame for user authentication
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import get_db, User


class LoginFrame:
    """Login frame widget"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        # Create main frame with white background
        main_container = tk.Frame(parent, bg='white')
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Centered card frame
        card_frame = tk.Frame(main_container, bg='white', relief=tk.FLAT)
        card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Back button (top left)
        back_btn = tk.Label(
            card_frame,
            text="← Back",
            font=('Segoe UI', 12),
            bg='white',
            fg='#4A90E2',
            cursor='hand2'
        )
        back_btn.pack(anchor=tk.NW, padx=10, pady=10)
        back_btn.bind('<Button-1>', lambda e: self.main_window.show_home())
        
        # Blue header bar (lighter)
        header_bar = tk.Frame(card_frame, bg='#4A90E2', height=50)
        header_bar.pack(fill=tk.X, pady=(0, 0))
        header_bar.pack_propagate(False)
        
        header_label = tk.Label(
            header_bar,
            text="→ Login",
            font=('Segoe UI', 14, 'bold'),
            bg='#4A90E2',
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Form content frame
        form_frame = tk.Frame(card_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Email field
        email_label = tk.Label(
            form_frame,
            text="Email Address",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        email_label.pack(fill=tk.X, pady=(0, 5))
        
        self.email_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.email_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        password_label.pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg='#333333',
            show='*',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        
        # Login button (lighter blue)
        login_btn = tk.Button(
            form_frame,
            text="→ Login",
            font=('Segoe UI', 12, 'bold'),
            bg='#4A90E2',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.login,
            padx=20,
            pady=12
        )
        login_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Register link
        register_frame = tk.Frame(form_frame, bg='white')
        register_frame.pack(fill=tk.X)
        
        register_label = tk.Label(
            register_frame,
            text="Don't have an account? ",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666666'
        )
        register_label.pack(side=tk.LEFT)
        
        register_link = tk.Label(
            register_frame,
            text="Register here",
            font=('Segoe UI', 10, 'underline'),
            bg='white',
            fg='#4A90E2',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT)
        register_link.bind('<Button-1>', lambda e: self.main_window.show_register())
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())
    
    def login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        db = get_db()
        try:
            user = db.query(User).filter_by(email=email).first()
            if user and user.check_password(password):
                # Set current user
                self.main_window.current_user = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'mobile': user.mobile,
                    'age': user.age,
                    'gender': user.gender,
                    'location': user.location,
                    'is_admin': user.is_admin
                }
                messagebox.showinfo("Success", f"Welcome, {user.name}!")
                self.main_window.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
        finally:
            db.close()
