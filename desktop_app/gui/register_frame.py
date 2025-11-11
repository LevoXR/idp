"""
Registration frame for new user signup
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import get_db, User


class RegisterFrame:
    """Registration frame widget"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        # Create main frame with light gray background
        main_container = tk.Frame(parent, bg='#F8F9FA')
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Canvas for scrolling if needed
        canvas = tk.Canvas(main_container, bg='#F8F9FA', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#F8F9FA')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=50, pady=30)
        scrollbar.pack(side="right", fill="y")
        
        # Centered card frame
        card_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.FLAT)
        card_frame.pack(expand=True, fill=tk.BOTH, padx=100, pady=20)
        
        # Back button (top left)
        back_btn = tk.Label(
            scrollable_frame,
            text="← Back to Login",
            font=('Segoe UI', 12),
            bg='#F8F9FA',
            fg='#4A90E2',
            cursor='hand2'
        )
        back_btn.place(relx=0.05, rely=0.05, anchor=tk.NW)
        back_btn.bind('<Button-1>', lambda e: self.main_window.show_login())
        
        # Blue header bar (lighter)
        header_bar = tk.Frame(card_frame, bg='#4A90E2', height=50)
        header_bar.pack(fill=tk.X)
        header_bar.pack_propagate(False)
        
        header_label = tk.Label(
            header_bar,
            text="👤+ Create Account",
            font=('Segoe UI', 14, 'bold'),
            bg='#4A90E2',
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Form content frame
        form_frame = tk.Frame(card_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Full Name field
        name_label = tk.Label(
            form_frame,
            text="Full Name *",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        name_label.pack(fill=tk.X, pady=(0, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Email field
        email_label = tk.Label(
            form_frame,
            text="Email Address *",
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
        self.email_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Mobile field
        mobile_label = tk.Label(
            form_frame,
            text="Mobile Number *",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        mobile_label.pack(fill=tk.X, pady=(0, 5))
        
        self.mobile_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.mobile_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password *",
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
        self.password_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Age and Gender in a row
        age_gender_frame = tk.Frame(form_frame, bg='white')
        age_gender_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Age field (left)
        age_subframe = tk.Frame(age_gender_frame, bg='white')
        age_subframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        age_label = tk.Label(
            age_subframe,
            text="Age (Optional)",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        age_label.pack(fill=tk.X, pady=(0, 5))
        
        self.age_entry = tk.Entry(
            age_subframe,
            font=('Segoe UI', 11),
            bg='white',
            fg='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.age_entry.pack(fill=tk.X, ipady=8)
        
        # Gender field (right)
        gender_subframe = tk.Frame(age_gender_frame, bg='white')
        gender_subframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        gender_label = tk.Label(
            gender_subframe,
            text="Gender (Optional)",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        gender_label.pack(fill=tk.X, pady=(0, 5))
        
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(
            gender_subframe,
            textvariable=self.gender_var,
            font=('Segoe UI', 11),
            state='readonly',
            values=('', 'Male', 'Female', 'Other', 'Prefer not to say')
        )
        gender_combo.current(0)
        gender_combo.pack(fill=tk.X, ipady=8)
        
        # State field
        state_label = tk.Label(
            form_frame,
            text="State (Optional)",
            font=('Segoe UI', 10),
            bg='white',
            fg='#333333',
            anchor=tk.W
        )
        state_label.pack(fill=tk.X, pady=(0, 5))
        
        self.state_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg='#999999',
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=0,
            insertbackground='#333333'
        )
        self.state_entry.insert(0, "e.g., Maharashtra")
        self.state_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        self.state_entry.bind('<FocusIn>', lambda e: self.on_state_focus_in())
        self.state_entry.bind('<FocusOut>', lambda e: self.on_state_focus_out())
        
        # Register button (lighter blue)
        register_btn = tk.Button(
            form_frame,
            text="✓ Register",
            font=('Segoe UI', 12, 'bold'),
            bg='#4A90E2',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.register,
            padx=20,
            pady=12
        )
        register_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Login link
        login_frame = tk.Frame(form_frame, bg='white')
        login_frame.pack(fill=tk.X)
        
        login_label = tk.Label(
            login_frame,
            text="Already have an account? ",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666666'
        )
        login_label.pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text="Login here",
            font=('Segoe UI', 10, 'underline'),
            bg='white',
            fg='#4A90E2',
            cursor='hand2'
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind('<Button-1>', lambda e: self.main_window.show_login())
    
    def on_state_focus_in(self):
        """Handle state field focus in"""
        if self.state_entry.get() == "e.g., Maharashtra":
            self.state_entry.delete(0, tk.END)
            self.state_entry.config(fg='#333333')
    
    def on_state_focus_out(self):
        """Handle state field focus out"""
        if not self.state_entry.get().strip():
            self.state_entry.insert(0, "e.g., Maharashtra")
            self.state_entry.config(fg='#999999')
    
    def register(self):
        """Handle registration"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        password = self.password_entry.get()
        age_str = self.age_entry.get().strip()
        gender = self.gender_var.get().strip()
        state = self.state_entry.get().strip()
        
        # Remove placeholder text
        if state == "e.g., Maharashtra":
            state = ""
        
        # Validate required fields
        if not all([name, email, mobile, password]):
            messagebox.showerror("Error", "Please fill in all required fields (*)")
            return
        
        # Validate age if provided
        age = None
        if age_str:
            try:
                age = int(age_str)
                if age < 1 or age > 120:
                    messagebox.showerror("Error", "Age must be between 1 and 120")
                    return
            except ValueError:
                messagebox.showerror("Error", "Age must be a valid number")
                return
        
        db = get_db()
        try:
            # Check if user exists
            existing_user = db.query(User).filter_by(email=email).first()
            if existing_user:
                messagebox.showerror("Error", "Email already exists. Please use a different email.")
                return
            
            # Create new user
            new_user = User(
                name=name,
                email=email,
                mobile=mobile,
                age=age if age else None,
                gender=gender if gender else None,
                location=state if state else None
            )
            new_user.set_password(password)
            
            db.add(new_user)
            db.commit()
            
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.main_window.show_login()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
        finally:
            db.close()
