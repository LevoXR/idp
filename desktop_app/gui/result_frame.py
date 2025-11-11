"""
Result frame showing assessment results
"""
import tkinter as tk
from tkinter import ttk


class ResultFrame:
    """Assessment result frame widget"""
    
    def __init__(self, parent, main_window, assessment_data):
        self.parent = parent
        self.main_window = main_window
        self.assessment_data = assessment_data
        
        # Create main frame with white background
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel to canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Result card
        result_card = tk.Frame(scrollable_frame, bg='white', relief=tk.FLAT)
        result_card.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Blue header bar
        header_bar = tk.Frame(result_card, bg='#0066cc', height=50)
        header_bar.pack(fill=tk.X)
        header_bar.pack_propagate(False)
        
        header_label = tk.Label(
            header_bar,
            text="✓ Assessment Result",
            font=('Segoe UI', 14, 'bold'),
            bg='#0066cc',
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=30, pady=15)
        
        # Result content
        result_content = tk.Frame(result_card, bg='white')
        result_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title
        title_label = tk.Label(
            result_content,
            text="Your Risk Assessment",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#333333'
        )
        title_label.pack(pady=(10, 30))
        
        # Risk level with color
        risk_level = self.assessment_data['risk_level']
        risk_color = {'Low': '#27ae60', 'Moderate': '#f39c12', 'High': '#e74c3c'}
        color = risk_color.get(risk_level, '#333333')
        
        risk_frame = tk.Frame(result_content, bg='white')
        risk_frame.pack(pady=(0, 20))
        
        risk_label = tk.Label(
            risk_frame,
            text=f"{risk_level} RISK",
            font=('Segoe UI', 28, 'bold'),
            bg='white',
            fg=color
        )
        risk_label.pack()
        
        # Risk score
        score_label = tk.Label(
            result_content,
            text=f"Risk Score: {self.assessment_data['risk_score']}",
            font=('Segoe UI', 14),
            bg='white',
            fg='#666666'
        )
        score_label.pack(pady=(0, 30))
        
        # Recommendations frame
        rec_frame = tk.Frame(result_content, bg='#E3F2FD', relief=tk.FLAT)
        rec_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 30))
        
        rec_title = tk.Label(
            rec_frame,
            text="⚠️ Recommendations:",
            font=('Segoe UI', 14, 'bold'),
            bg='#E3F2FD',
            fg='#1976D2'
        )
        rec_title.pack(anchor=tk.W, padx=25, pady=(25, 15))
        
        # Recommendations text
        recommendations = self.assessment_data.get('recommendations', '')
        rec_lines = recommendations.split('\n')
        
        rec_text_frame = tk.Frame(rec_frame, bg='#E3F2FD')
        rec_text_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        for rec in rec_lines:
            if rec.strip():
                rec_item = tk.Label(
                    rec_text_frame,
                    text=f"• {rec.strip()}",
                    font=('Segoe UI', 11),
                    bg='#E3F2FD',
                    fg='#333333',
                    anchor=tk.W,
                    justify=tk.LEFT,
                    wraplength=900
                )
                rec_item.pack(anchor=tk.W, pady=3)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=50, pady=20)
        
        dashboard_btn = tk.Button(
            button_frame,
            text="Go to Dashboard",
            font=('Segoe UI', 12, 'bold'),
            bg='#0066cc',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.main_window.show_dashboard(),
            padx=20,
            pady=12
        )
        dashboard_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        new_assessment_btn = tk.Button(
            button_frame,
            text="Take New Assessment",
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.main_window.show_assessment(),
            padx=20,
            pady=12
        )
        new_assessment_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
