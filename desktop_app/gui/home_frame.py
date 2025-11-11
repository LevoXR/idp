"""
Home/Landing page frame with app information
"""
import tkinter as tk
from tkinter import ttk


class HomeFrame:
    """Home/Landing page frame widget"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        
        # Main container with light background (very light gray/white)
        main_container = tk.Frame(parent, bg='#FAFAFA')
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Content frame
        content_frame = tk.Frame(main_container, bg='#FAFAFA')
        content_frame.pack(expand=True, fill=tk.BOTH, padx=80, pady=50)
        
        # Main card (large white rectangular card)
        main_card = tk.Frame(content_frame, bg='white', relief=tk.FLAT)
        main_card.pack(expand=True, fill=tk.BOTH, pady=(0, 40))
        
        # Card content with proper spacing
        card_content = tk.Frame(main_card, bg='white')
        card_content.pack(expand=True, fill=tk.BOTH, padx=80, pady=60)
        
        # Large shield/checkmark icon (blue) - VERY LARGE
        icon_frame = tk.Frame(card_content, bg='white')
        icon_frame.pack(pady=(0, 25))
        
        # Large checkmark in shield - matching image size
        shield_icon = tk.Label(
            icon_frame,
            text="✓",
            font=('Segoe UI', 80, 'bold'),
            bg='white',
            fg='#4A90E2'
        )
        shield_icon.pack()
        
        # App title - VERY LARGE dark gray (matching image)
        app_title = tk.Label(
            card_content,
            text="Aditya Setu",
            font=('Segoe UI', 48, 'bold'),
            bg='white',
            fg='#2C3E50'
        )
        app_title.pack(pady=(5, 12))
        
        # Tagline - smaller dark gray
        tagline = tk.Label(
            card_content,
            text="A simple self-assessment tool for public health monitoring",
            font=('Segoe UI', 15),
            bg='white',
            fg='#5A6C7D'
        )
        tagline.pack(pady=(0, 25))
        
        # Description paragraph
        desc_frame = tk.Frame(card_content, bg='white')
        desc_frame.pack(fill=tk.X, pady=(0, 35))
        
        description = tk.Label(
            desc_frame,
            text="Complete a quick health questionnaire to assess your risk level and receive personalized recommendations based on your symptoms and exposure history.",
            font=('Segoe UI', 13),
            bg='white',
            fg='#5A6C7D',
            wraplength=750,
            justify=tk.CENTER
        )
        description.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(card_content, bg='white')
        buttons_frame.pack(pady=(15, 20))
        
        # Get Started button (Primary blue with person+ icon)
        get_started_btn = tk.Button(
            buttons_frame,
            text="👤+ Get Started",
            font=('Segoe UI', 15, 'bold'),
            bg='#4A90E2',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.main_window.show_register(),
            padx=40,
            pady=18,
            width=20,
            activebackground='#357ABD',
            activeforeground='white'
        )
        get_started_btn.pack(side=tk.LEFT, padx=12)
        
        # Login button (White with blue border and arrow)
        login_btn = tk.Button(
            buttons_frame,
            text="→ Login",
            font=('Segoe UI', 15),
            bg='white',
            fg='#4A90E2',
            relief=tk.SOLID,
            borderwidth=2,
            cursor='hand2',
            command=lambda: self.main_window.show_login(),
            padx=40,
            pady=18,
            width=20,
            highlightbackground='#4A90E2',
            highlightthickness=2,
            activebackground='#F0F8FF',
            activeforeground='#4A90E2'
        )
        login_btn.pack(side=tk.LEFT, padx=12)
        
        # Feature cards section (3 cards in a row) - BELOW main card
        features_section = tk.Frame(content_frame, bg='#FAFAFA')
        features_section.pack(fill=tk.X, pady=(0, 0))
        
        # Card 1: Self-Assessment (Blue icon - clipboard with bar chart)
        card1 = self.create_feature_card(
            features_section,
            "📋",
            "Self-Assessment",
            "Complete a simple questionnaire about your symptoms and exposure history.",
            '#4A90E2'
        )
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12)
        
        # Card 2: Risk Analysis (Green icon - upward trending line graph)
        card2 = self.create_feature_card(
            features_section,
            "📈",
            "Risk Analysis",
            "Get instant risk level assessment (Low, Moderate, or High) with detailed recommendations.",
            '#27AE60'
        )
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12)
        
        # Card 3: Health Alerts (Yellow icon - bell)
        card3 = self.create_feature_card(
            features_section,
            "🔔",
            "Health Alerts",
            "Stay informed with official health alerts and recommendations from authorities.",
            '#FDD835'
        )
        card3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12)
    
    def create_feature_card(self, parent, icon, title, description, icon_color):
        """Create a feature card matching the exact design"""
        card = tk.Frame(parent, bg='white', relief=tk.FLAT)
        
        # Card content with proper padding
        card_content = tk.Frame(card, bg='white')
        card_content.pack(fill=tk.BOTH, expand=True, padx=35, pady=35)
        
        # Icon - medium-large size, colored (matching image)
        icon_label = tk.Label(
            card_content,
            text=icon,
            font=('Segoe UI', 45),
            bg='white',
            fg=icon_color
        )
        icon_label.pack(pady=(5, 18))
        
        # Title - bold dark gray
        title_label = tk.Label(
            card_content,
            text=title,
            font=('Segoe UI', 17, 'bold'),
            bg='white',
            fg='#2C3E50'
        )
        title_label.pack(pady=(0, 12))
        
        # Description - lighter gray, centered
        desc_label = tk.Label(
            card_content,
            text=description,
            font=('Segoe UI', 12),
            bg='white',
            fg='#7F8C8D',
            wraplength=300,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 5))
        
        return card

