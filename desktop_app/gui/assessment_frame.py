"""
Assessment frame for health questionnaire
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import get_db, Assessment
from utils import get_assessment_questions, calculate_risk_score, generate_recommendations


class AssessmentFrame:
    """Assessment frame widget"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.user = main_window.current_user
        self.questions = get_assessment_questions()
        self.answers = {}
        
        # Create main frame with white background
        main_frame = tk.Frame(parent, bg='white')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Close button (top right in header area)
        close_btn = tk.Label(
            parent,
            text="✕",
            font=('Segoe UI', 18),
            bg='white',
            fg='#999999',
            cursor='hand2'
        )
        close_btn.place(relx=0.98, rely=0.02, anchor=tk.NE)
        close_btn.bind('<Button-1>', lambda e: self.main_window.show_dashboard())
        
        # Blue header bar (lighter)
        header_bar = tk.Frame(main_frame, bg='#4A90E2', height=50)
        header_bar.pack(fill=tk.X, pady=(0, 20))
        header_bar.pack_propagate(False)
        
        header_label = tk.Label(
            header_bar,
            text="✓ Health Self-Assessment",
            font=('Segoe UI', 14, 'bold'),
            bg='#4A90E2',
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=30, pady=15)
        
        # Instructional info box
        info_box = tk.Frame(main_frame, bg='#E3F2FD', relief=tk.FLAT)
        info_box.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        info_label = tk.Label(
            info_box,
            text="ℹ Please answer all questions honestly to get an accurate risk assessment. This assessment is for informational purposes only and does not replace professional medical advice.",
            font=('Segoe UI', 10),
            bg='#E3F2FD',
            fg='#1976D2',
            wraplength=1100,
            justify=tk.LEFT,
            anchor=tk.W
        )
        info_label.pack(anchor=tk.W, padx=20, pady=15)
        
        # Canvas with scrollbar for questions
        canvas_frame = tk.Frame(main_frame, bg='white')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_canvas_width(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', configure_canvas_width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Smooth scrolling with mousewheel
        def on_mousewheel(event):
            # Scroll more smoothly
            delta = event.delta
            if delta:
                canvas.yview_scroll(int(-1 * (delta / 120) * 3), "units")
            return "break"
        
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', bind_mousewheel)
        canvas.bind('<Leave>', unbind_mousewheel)
        
        # Also allow scrolling when hovering over scrollable_frame
        scrollable_frame.bind('<Enter>', bind_mousewheel)
        scrollable_frame.bind('<Leave>', unbind_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Questions container
        questions_container = tk.Frame(scrollable_frame, bg='white')
        questions_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.question_widgets = []
        
        for idx, question in enumerate(self.questions):
            # Question frame with spacing
            q_frame = tk.Frame(questions_container, bg='white', relief=tk.FLAT)
            q_frame.pack(fill=tk.X, pady=20)
            
            # Question number and text
            q_number_label = tk.Label(
                q_frame,
                text=f"Question {idx + 1} of {len(self.questions)}",
                font=('Segoe UI', 9),
                bg='white',
                fg='#999999',
                anchor=tk.W
            )
            q_number_label.pack(anchor=tk.W, pady=(0, 5))
            
            # Question text
            q_label = tk.Label(
                q_frame,
                text=question['question'],
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg='#333333',
                wraplength=1000,
                justify=tk.LEFT,
                anchor=tk.W
            )
            q_label.pack(anchor=tk.W, pady=(0, 15))
            
            # Answer widget
            if question['type'] == 'yes_no':
                var = tk.StringVar()
                var.set('')
                
                answer_frame = tk.Frame(q_frame, bg='white')
                answer_frame.pack(anchor=tk.W, padx=30)
                
                # Bigger radio buttons with more padding
                yes_radio = tk.Radiobutton(
                    answer_frame,
                    text="Yes",
                    variable=var,
                    value='yes',
                    font=('Segoe UI', 14),
                    bg='white',
                    fg='#333333',
                    activebackground='white',
                    activeforeground='#4A90E2',
                    selectcolor='white',
                    cursor='hand2',
                    padx=25,
                    pady=10
                )
                yes_radio.pack(side=tk.LEFT, padx=(0, 40))
                
                no_radio = tk.Radiobutton(
                    answer_frame,
                    text="No",
                    variable=var,
                    value='no',
                    font=('Segoe UI', 14),
                    bg='white',
                    fg='#333333',
                    activebackground='white',
                    activeforeground='#4A90E2',
                    selectcolor='white',
                    cursor='hand2',
                    padx=25,
                    pady=10
                )
                no_radio.pack(side=tk.LEFT)
                
                self.question_widgets.append({'var': var, 'id': question['id']})
                
            elif question['type'] == 'numeric':
                var = tk.StringVar()
                var.set('0')
                
                answer_frame = tk.Frame(q_frame, bg='white')
                answer_frame.pack(anchor=tk.W, padx=30)
                
                entry = tk.Entry(
                    answer_frame,
                    textvariable=var,
                    font=('Segoe UI', 11),
                    bg='white',
                    fg='#333333',
                    relief=tk.SOLID,
                    borderwidth=1,
                    width=10
                )
                entry.pack(side=tk.LEFT)
                
                self.question_widgets.append({'var': var, 'id': question['id']})
            
            # Separator line
            separator = tk.Frame(q_frame, bg='#E0E0E0', height=1)
            separator.pack(fill=tk.X, pady=(15, 0))
        
        # Buttons frame (fixed at bottom)
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=('Segoe UI', 11),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=lambda: self.main_window.show_dashboard(),
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        submit_btn = tk.Button(
            button_frame,
            text="Submit Assessment",
            font=('Segoe UI', 12, 'bold'),
            bg='#4A90E2',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.submit_assessment,
            padx=20,
            pady=10
        )
        submit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def submit_assessment(self):
        """Submit assessment and calculate results"""
        # Collect answers
        answers = {}
        all_answered = True
        
        for widget in self.question_widgets:
            answer = widget['var'].get().strip()
            if not answer:
                all_answered = False
                break
            answers[widget['id']] = answer
        
        if not all_answered:
            messagebox.showerror("Error", "Please answer all questions")
            return
        
        # Calculate risk score
        risk_score = calculate_risk_score(answers)
        
        # Determine risk level
        if risk_score <= 2:
            risk_level = "Low"
        elif risk_score <= 5:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        # Generate recommendations
        recommendations = generate_recommendations(risk_level, answers)
        
        # Save assessment to database
        db = get_db()
        try:
            assessment = Assessment(
                user_id=self.user['id'],
                answers=answers,
                risk_score=risk_score,
                risk_level=risk_level,
                recommendations=recommendations
            )
            
            db.add(assessment)
            db.commit()
            
            # Show result
            assessment_data = {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'recommendations': recommendations,
                'answers': answers
            }
            
            self.main_window.show_result(assessment_data)
            
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to save assessment: {str(e)}")
        finally:
            db.close()
