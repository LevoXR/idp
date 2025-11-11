"""
Dashboard frame showing user info, assessments, and alerts
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import get_db, Assessment, Alert
from utils import load_covid_data


class DashboardFrame:
    """Dashboard frame widget"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.user = main_window.current_user
        
        # Create main frame with white background
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Canvas with scrollbar for content
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        content_frame = tk.Frame(scrollable_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Dashboard Card (Top Section)
        dashboard_card = self.create_card(content_frame)
        dashboard_card.pack(fill=tk.X, pady=(0, 20))
        
        # Dashboard header
        dashboard_header = tk.Frame(dashboard_card, bg='#0066cc', height=50)
        dashboard_header.pack(fill=tk.X)
        dashboard_header.pack_propagate(False)
        
        dashboard_title = tk.Label(
            dashboard_header,
            text="📊 Dashboard",
            font=('Segoe UI', 14, 'bold'),
            bg='#0066cc',
            fg='white'
        )
        dashboard_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Dashboard content
        dashboard_content = tk.Frame(dashboard_card, bg='white')
        dashboard_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(
            dashboard_content,
            text=f"Welcome, {self.user['name']}!",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#333333'
        )
        welcome_label.pack(anchor=tk.W, pady=(0, 10))
        
        # User info
        info_text = f"Email: {self.user['email']} | Mobile: {self.user['mobile']}"
        if self.user.get('location'):
            info_text += f" | State: {self.user['location']}"
        
        info_label = tk.Label(
            dashboard_content,
            text=info_text,
            font=('Segoe UI', 11),
            bg='white',
            fg='#666666'
        )
        info_label.pack(anchor=tk.W, pady=(0, 15))
        
        # COVID Cases button (if state is set)
        if self.user.get('location'):
            covid_frame = tk.Frame(dashboard_content, bg='white')
            covid_frame.pack(anchor=tk.W, pady=(0, 10))
            
            covid_data = load_covid_data()
            user_state = self.user['location'].strip()
            cases = None
            
            if user_state in covid_data:
                cases = covid_data[user_state]
            else:
                for state, case_count in covid_data.items():
                    if state.lower() == user_state.lower():
                        cases = case_count
                        break
            
            if cases is not None:
                covid_btn = tk.Button(
                    covid_frame,
                    text=f"🦠 COVID Cases: {cases:,}",
                    font=('Segoe UI', 10, 'bold'),
                    bg='#e74c3c',
                    fg='white',
                    relief=tk.FLAT,
                    padx=15,
                    pady=8,
                    cursor='hand2'
                )
                covid_btn.pack(side=tk.LEFT)
        
        # Latest Assessment Card
        db = get_db()
        try:
            latest_assessment = db.query(Assessment).filter_by(user_id=self.user['id'])\
                .order_by(Assessment.created_at.desc()).first()
            
            if latest_assessment:
                latest_card = self.create_card(content_frame)
                latest_card.pack(fill=tk.X, pady=(0, 20))
                
                # Latest Assessment header
                latest_header = tk.Frame(latest_card, bg='#0066cc', height=50)
                latest_header.pack(fill=tk.X)
                latest_header.pack_propagate(False)
                
                latest_title = tk.Label(
                    latest_header,
                    text="✓ Latest Assessment",
                    font=('Segoe UI', 14, 'bold'),
                    bg='#0066cc',
                    fg='white'
                )
                latest_title.pack(side=tk.LEFT, padx=20, pady=15)
                
                # Latest Assessment content
                latest_content = tk.Frame(latest_card, bg='white')
                latest_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
                
                # Risk Level
                risk_frame = tk.Frame(latest_content, bg='white')
                risk_frame.pack(fill=tk.X, pady=(0, 10))
                
                risk_label = tk.Label(
                    risk_frame,
                    text="Risk Level:",
                    font=('Segoe UI', 12, 'bold'),
                    bg='white',
                    fg='#333333'
                )
                risk_label.pack(side=tk.LEFT)
                
                # Risk level badge
                risk_color = {'Low': '#27ae60', 'Moderate': '#f39c12', 'High': '#e74c3c'}
                color = risk_color.get(latest_assessment.risk_level, '#333333')
                
                risk_badge = tk.Label(
                    risk_frame,
                    text=latest_assessment.risk_level,
                    font=('Segoe UI', 11, 'bold'),
                    bg=color,
                    fg='white',
                    padx=15,
                    pady=5,
                    relief=tk.FLAT
                )
                risk_badge.pack(side=tk.LEFT, padx=10)
                
                # Risk Score
                score_label = tk.Label(
                    risk_frame,
                    text=f"Risk Score: {latest_assessment.risk_score}",
                    font=('Segoe UI', 11),
                    bg='white',
                    fg='#666666'
                )
                score_label.pack(side=tk.LEFT, padx=20)
                
                # Recommendations box
                rec_box = tk.Frame(latest_content, bg='#E3F2FD', relief=tk.FLAT)
                rec_box.pack(fill=tk.X, pady=(10, 15))
                
                rec_title = tk.Label(
                    rec_box,
                    text="⚠️ Recommendations:",
                    font=('Segoe UI', 12, 'bold'),
                    bg='#E3F2FD',
                    fg='#1976D2'
                )
                rec_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
                
                # Recommendations list
                recommendations = latest_assessment.recommendations or ""
                rec_lines = recommendations.split('\n')
                for rec in rec_lines:
                    if rec.strip():
                        rec_item = tk.Label(
                            rec_box,
                            text=f"• {rec.strip()}",
                            font=('Segoe UI', 10),
                            bg='#E3F2FD',
                            fg='#333333',
                            anchor=tk.W,
                            justify=tk.LEFT
                        )
                        rec_item.pack(anchor=tk.W, padx=15, pady=2)
                
                # Take New Assessment button
                new_assessment_btn = tk.Button(
                    latest_content,
                    text="🔄 Take New Assessment",
                    font=('Segoe UI', 12, 'bold'),
                    bg='#0066cc',
                    fg='white',
                    relief=tk.FLAT,
                    cursor='hand2',
                    command=self.main_window.show_assessment,
                    padx=20,
                    pady=12
                )
                new_assessment_btn.pack(fill=tk.X, pady=(10, 0))
            
            # Recent Assessments Card
            recent_assessments = db.query(Assessment).filter_by(user_id=self.user['id'])\
                .order_by(Assessment.created_at.desc()).limit(5).all()
            
            if recent_assessments:
                recent_card = self.create_card(content_frame)
                recent_card.pack(fill=tk.X, pady=(0, 20))
                
                # Recent Assessments header
                recent_header = tk.Frame(recent_card, bg='#0066cc', height=50)
                recent_header.pack(fill=tk.X)
                recent_header.pack_propagate(False)
                
                recent_title = tk.Label(
                    recent_header,
                    text="🕐 Recent Assessments",
                    font=('Segoe UI', 14, 'bold'),
                    bg='#0066cc',
                    fg='white'
                )
                recent_title.pack(side=tk.LEFT, padx=20, pady=15)
                
                # Recent Assessments content
                recent_content = tk.Frame(recent_card, bg='white')
                recent_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
                
                # Table headers
                headers_frame = tk.Frame(recent_content, bg='white')
                headers_frame.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(
                    headers_frame,
                    text="Date",
                    font=('Segoe UI', 11, 'bold'),
                    bg='white',
                    fg='#333333'
                ).grid(row=0, column=0, padx=10, sticky=tk.W)
                
                tk.Label(
                    headers_frame,
                    text="Risk Level",
                    font=('Segoe UI', 11, 'bold'),
                    bg='white',
                    fg='#333333'
                ).grid(row=0, column=1, padx=10, sticky=tk.W)
                
                tk.Label(
                    headers_frame,
                    text="Score",
                    font=('Segoe UI', 11, 'bold'),
                    bg='white',
                    fg='#333333'
                ).grid(row=0, column=2, padx=10, sticky=tk.W)
                
                # Table rows
                for idx, assessment in enumerate(recent_assessments):
                    row_frame = tk.Frame(recent_content, bg='white')
                    row_frame.pack(fill=tk.X, pady=5)
                    
                    date_str = assessment.created_at.strftime('%b %d, %Y %I:%M %p')
                    tk.Label(
                        row_frame,
                        text=date_str,
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#666666'
                    ).grid(row=0, column=0, padx=10, sticky=tk.W)
                    
                    tk.Label(
                        row_frame,
                        text=assessment.risk_level or "",
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#666666'
                    ).grid(row=0, column=1, padx=10, sticky=tk.W)
                    
                    tk.Label(
                        row_frame,
                        text=str(assessment.risk_score),
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#666666'
                    ).grid(row=0, column=2, padx=10, sticky=tk.W)
        
        finally:
            db.close()
        
        # Health Alerts Card
        db = get_db()
        try:
            alerts = db.query(Alert).filter_by(is_active=True)\
                .order_by(Alert.created_at.desc()).limit(5).all()
            
            alerts_card = self.create_card(content_frame)
            alerts_card.pack(fill=tk.X, pady=(0, 20))
            
            # Alerts header (Yellow)
            alerts_header = tk.Frame(alerts_card, bg='#FFD700', height=50)
            alerts_header.pack(fill=tk.X)
            alerts_header.pack_propagate(False)
            
            alerts_title_frame = tk.Frame(alerts_header, bg='#FFD700')
            alerts_title_frame.pack(side=tk.LEFT, padx=20, pady=15)
            
            alerts_title = tk.Label(
                alerts_title_frame,
                text="🔔 Health Alerts & Announcements",
                font=('Segoe UI', 14, 'bold'),
                bg='#FFD700',
                fg='#333333'
            )
            alerts_title.pack(side=tk.LEFT)
            
            # Close button for alerts
            close_alerts_btn = tk.Label(
                alerts_header,
                text="✕",
                font=('Segoe UI', 16),
                bg='#FFD700',
                fg='#333333',
                cursor='hand2'
            )
            close_alerts_btn.pack(side=tk.RIGHT, padx=20, pady=15)
            close_alerts_btn.bind('<Button-1>', lambda e: alerts_card.pack_forget())
            
            # Filter section
            alerts_content = tk.Frame(alerts_card, bg='white')
            alerts_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
            
            filter_frame = tk.Frame(alerts_content, bg='white')
            filter_frame.pack(fill=tk.X, pady=(0, 15))
            
            filter_entry = tk.Entry(
                filter_frame,
                font=('Segoe UI', 10),
                bg='white',
                fg='#333333',
                relief=tk.SOLID,
                borderwidth=1,
                highlightthickness=0
            )
            filter_entry.insert(0, "Filter by location (optional)")
            filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
            filter_entry.bind('<FocusIn>', lambda e: self.on_filter_focus_in(filter_entry))
            filter_entry.bind('<FocusOut>', lambda e: self.on_filter_focus_out(filter_entry))
            
            filter_btn = tk.Button(
                filter_frame,
                text="Filter",
                font=('Segoe UI', 10, 'bold'),
                bg='#FFD700',
                fg='#333333',
                relief=tk.FLAT,
                cursor='hand2',
                padx=15,
                pady=6
            )
            filter_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            clear_btn = tk.Button(
                filter_frame,
                text="Clear",
                font=('Segoe UI', 10),
                bg='white',
                fg='#333333',
                relief=tk.SOLID,
                borderwidth=1,
                cursor='hand2',
                padx=15,
                pady=6
            )
            clear_btn.pack(side=tk.LEFT)
            
            # Alerts display
            if alerts:
                for alert in alerts:
                    alert_item = tk.Frame(alerts_content, bg='#FFF9C4', relief=tk.FLAT)
                    alert_item.pack(fill=tk.X, pady=5)
                    
                    tk.Label(
                        alert_item,
                        text=alert.title,
                        font=('Segoe UI', 11, 'bold'),
                        bg='#FFF9C4',
                        fg='#856404',
                        anchor=tk.W
                    ).pack(anchor=tk.W, padx=15, pady=(10, 5))
                    
                    message_text = alert.message[:200] + '...' if len(alert.message) > 200 else alert.message
                    tk.Label(
                        alert_item,
                        text=message_text,
                        font=('Segoe UI', 10),
                        bg='#FFF9C4',
                        fg='#856404',
                        anchor=tk.W,
                        wraplength=1000,
                        justify=tk.LEFT
                    ).pack(anchor=tk.W, padx=15, pady=(0, 10))
            else:
                # No alerts message
                no_alerts_frame = tk.Frame(alerts_content, bg='#E3F2FD', relief=tk.FLAT)
                no_alerts_frame.pack(fill=tk.X, pady=10)
                
                tk.Label(
                    no_alerts_frame,
                    text="ℹ No active alerts at this time.",
                    font=('Segoe UI', 11),
                    bg='#E3F2FD',
                    fg='#1976D2',
                    anchor=tk.W
                ).pack(anchor=tk.W, padx=15, pady=15)
        
        finally:
            db.close()
    
    def create_card(self, parent):
        """Create a modern card frame with shadow effect"""
        card = tk.Frame(parent, bg='white', relief=tk.FLAT)
        return card
    
    def on_filter_focus_in(self, entry):
        """Handle filter entry focus in"""
        if entry.get() == "Filter by location (optional)":
            entry.delete(0, tk.END)
            entry.config(fg='#333333')
    
    def on_filter_focus_out(self, entry):
        """Handle filter entry focus out"""
        if not entry.get().strip():
            entry.insert(0, "Filter by location (optional)")
            entry.config(fg='#999999')
