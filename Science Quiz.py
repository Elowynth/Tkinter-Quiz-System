import tkinter as tk
from tkinter import messagebox
import random
import os
 
QUESTIONS = [
    {
        "question": "Which part of a plant absorbs water and nutrients from the soil?",
        "choices": ["A. Leaves", "B. Roots", "C. Flowers", "D. Seeds"],
        "answer": "B"
    },
    {
        "question": "What is the chemical symbol for water?",
        "choices": ["A. O2", "B. CO2", "C. H2O", "D. NaCl"],
        "answer": "C"
    },
    {
        "question": "Which planet in our solar system is known as the Red Planet?",
        "choices": ["A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "B"
    },
    {
        "question": "What force keeps planets in orbit around the Sun?",
        "choices": ["A. Magnetism", "B. Friction", "C. Gravity", "D. Electricity"],
        "answer": "C"
    },
    {
        "question": "Which organ in the human body pumps blood throughout the body?",
        "choices": ["A. Lungs", "B. Liver", "C. Brain", "D. Heart"],
        "answer": "D"
    },
    {
        "question": "What gas do plants take in from the air during photosynthesis?",
        "choices": ["A. Oxygen", "B. Carbon dioxide", "C. Nitrogen", "D. Helium"],
        "answer": "B"
    },
    {
        "question": "At what temperature does pure water freeze at standard sea-level pressure?",
        "choices": ["A. 0 °C", "B. 32 °C", "C. 50 °C", "D. 100 °C"],
        "answer": "A"
    },
    {
        "question": "Which state of matter has a definite volume but takes the shape of its container?",
        "choices": ["A. Solid", "B. Liquid", "C. Gas", "D. Plasma"],
        "answer": "B"
    },
    {
        "question": "Which human sense organ is primarily responsible for detecting light?",
        "choices": ["A. Ear", "B. Nose", "C. Eye", "D. Tongue"],
        "answer": "C"
    },
    {
        "question": "What causes day and night on Earth?",
        "choices": ["A. The Moon blocking the Sun", "B. Earth rotating on its axis", "C. The Sun orbiting Earth", "D. Earth moving closer to the Sun"],
        "answer": "B"
    }
]
 
TIME_LIMIT = 15  
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)
 
# DESIGN SETTINGS 
BG_COLOR = "#F5F3FF"          
CARD_COLOR = "#FFFFFF"       
PRIMARY_COLOR = "#6D28D9"     
HOVER_COLOR = "#5B21B6"       
SELECT_COLOR = "#DDD6FE"      
BORDER_COLOR = "#C4B5FD"
TEXT_COLOR = "#1F2937"
MUTED_COLOR = "#6B7280"
CORRECT_COLOR = "#16A34A"     
WRONG_COLOR = "#DC2626"       
FONT = "Segoe UI"
CONFETTI_COLORS = ["#F43F5E", "#F59E0B", "#10B981", "#3B82F6",
                   "#8B5CF6", "#EC4899", "#FACC15"]
PROGRESS_WIDTH = 760
CONFETTI_HEIGHT = 90
 
root = tk.Tk()
root.title("Science Quiz Challenge")
root.geometry("820x780")
root.configure(bg=BG_COLOR)
root.resizable(False, False)
 
# QUIZ STATE VARIABLES
quiz_questions = []      
current_question = 0    
score = 0
time_left = TIME_LIMIT
wrong_answers = []      
timer_job = None         
answered = False         
selected_answer = tk.StringVar()
 
timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []
progress_canvas = None
confetti_canvas = None
confetti_job = None
confetti_pieces = []
 
# Header bar 
header_frame = tk.Frame(root, bg=PRIMARY_COLOR)
header_frame.pack(fill="x")
tk.Label(header_frame, text="SCIENCE QUIZ CHALLENGE",
         font=(FONT, 20, "bold"), bg=PRIMARY_COLOR,
         fg="white").pack(pady=14)
 
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=30, pady=15)
 
 
# HIGH SCORE FUNCTIONS 
def get_high_score():
    """Read the saved high score. Return 0 if there is no valid file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0
 
 
def save_high_score(new_score):
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False
 
 
# HELPER FUNCTIONS
def clear_screen():
  
    stop_confetti()
    for widget in main_frame.winfo_children():
        widget.destroy()
 
 
def get_choice_text(question, letter):
    
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"
 
 
def make_button(parent, text, command, bg=PRIMARY_COLOR, width=15, size=13):
   
    button = tk.Button(parent, text=text, command=command,
                       font=(FONT, size, "bold"), bg=bg, fg="white",
                       activebackground=HOVER_COLOR, activeforeground="white",
                       disabledforeground="#DDD6FE", relief="flat", bd=0,
                       cursor="hand2", width=width, pady=8)
 
    def on_enter(event):
        if str(button["state"]) == "normal":
            button.config(bg=HOVER_COLOR)
 
    def on_leave(event):
        button.config(bg=bg)
 
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button
 
 
# PROGRESS BAR
def draw_progress(done):
    total = len(quiz_questions)
    progress_canvas.delete("all")
    progress_canvas.create_rectangle(0, 0, PROGRESS_WIDTH, 14,
                                     fill=SELECT_COLOR, outline="")
    if done > 0:
        progress_canvas.create_rectangle(0, 0, PROGRESS_WIDTH * done / total, 14,
                                         fill=PRIMARY_COLOR, outline="")
 
 
# CONFETTI ANIMATION
def launch_confetti():
    global confetti_pieces
    stop_confetti()
    confetti_canvas.delete("all")
    for _ in range(70):
        x = random.randint(0, PROGRESS_WIDTH)
        y = random.randint(-150, 0)
        size = random.randint(6, 11)
        color = random.choice(CONFETTI_COLORS)
        if random.random() < 0.5:
            item = confetti_canvas.create_rectangle(x, y, x + size, y + size,
                                                    fill=color, outline="")
        else:
            item = confetti_canvas.create_oval(x, y, x + size, y + size,
                                               fill=color, outline="")
       
        confetti_pieces.append([item, random.uniform(-2, 2),
                                random.uniform(1.5, 3.5)])
    animate_confetti(0)
 
 
def animate_confetti(frame):
    global confetti_job
    try:
        for piece in confetti_pieces:
            confetti_canvas.move(piece[0], piece[1], piece[2])
            piece[2] += 0.1          
    except tk.TclError:             
        return
    if frame < 45:
        confetti_job = root.after(30, animate_confetti, frame + 1)
    else:
        confetti_canvas.delete("all")
        confetti_pieces.clear()
        confetti_job = None
 
 
def stop_confetti():
  
    global confetti_job
    if confetti_job is not None:
        root.after_cancel(confetti_job)
        confetti_job = None
    confetti_pieces.clear()
 
 
# SCREENS
def show_start_screen():
    clear_screen()
    tk.Label(main_frame, text="Ready to test your science skills?",
             font=(FONT, 26, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR,
             wraplength=700).pack(pady=(50, 10))
    tk.Label(main_frame,
             text=f"{len(QUESTIONS)} questions  |  {TIME_LIMIT} seconds per question",
             font=(FONT, 13), bg=BG_COLOR, fg=MUTED_COLOR).pack(pady=5)
 
    card = tk.Frame(main_frame, bg=CARD_COLOR, highlightthickness=1,
                    highlightbackground=BORDER_COLOR)
    card.pack(pady=30, ipadx=40, ipady=15)
    tk.Label(card, text="HIGH SCORE", font=(FONT, 11, "bold"),
             bg=CARD_COLOR, fg=MUTED_COLOR).pack(pady=(10, 0))
    tk.Label(card, text=f"{get_high_score()} / {len(QUESTIONS)}",
             font=(FONT, 28, "bold"), bg=CARD_COLOR,
             fg=PRIMARY_COLOR).pack()
 
    make_button(main_frame, "Start Quiz", start_quiz, width=18,
                size=16).pack(pady=20)
 
 
def start_quiz():
    """Reset everything and shuffle the questions."""
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()
 
 
def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons
    global progress_canvas, confetti_canvas
 
    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]
 
    # Progress and timer
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x")
    tk.Label(top_frame,
             text=f"Question {current_question + 1} of {len(quiz_questions)}",
             font=(FONT, 13, "bold"), bg=BG_COLOR,
             fg=TEXT_COLOR).pack(side="left")
    timer_label = tk.Label(top_frame, text="", font=(FONT, 13, "bold"),
                           bg=BG_COLOR, fg=TEXT_COLOR)
    timer_label.pack(side="right")
 
    # Progress bar
    progress_canvas = tk.Canvas(main_frame, width=PROGRESS_WIDTH, height=14,
                                bg=BG_COLOR, highlightthickness=0)
    progress_canvas.pack(pady=(8, 5))
    draw_progress(current_question)
 
    tk.Label(main_frame, text=f"Score: {score}", font=(FONT, 12, "bold"),
             bg=BG_COLOR, fg=PRIMARY_COLOR).pack(anchor="w", pady=(0, 5))
 
    # Question text (inside a white card)
    question_card = tk.Frame(main_frame, bg=CARD_COLOR, highlightthickness=1,
                             highlightbackground=BORDER_COLOR)
    question_card.pack(fill="x", pady=10)
    tk.Label(question_card, text=question["question"],
             font=(FONT, 17, "bold"), wraplength=700, justify="left",
             bg=CARD_COLOR, fg=TEXT_COLOR).pack(padx=20, pady=20, anchor="w")
 
    # Answer choices (the value of each button is its letter)
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(main_frame, text=choice,
                                variable=selected_answer, value=letter,
                                font=(FONT, 13), bg=CARD_COLOR, fg=TEXT_COLOR,
                                selectcolor=SELECT_COLOR,
                                activebackground=SELECT_COLOR,
                                activeforeground=TEXT_COLOR,
                                disabledforeground=MUTED_COLOR,
                                indicatoron=0, anchor="w", relief="flat",
                                bd=0, padx=15, pady=8, cursor="hand2",
                                highlightthickness=1,
                                highlightbackground=BORDER_COLOR,
                                highlightcolor=PRIMARY_COLOR)
        button.pack(fill="x", pady=3)
        choice_buttons.append(button)
 
    # Confetti area (confetti falls here when the answer is correct)
    confetti_canvas = tk.Canvas(main_frame, width=PROGRESS_WIDTH,
                                height=CONFETTI_HEIGHT, bg=BG_COLOR,
                                highlightthickness=0)
    confetti_canvas.pack(pady=(5, 0))
 
    feedback_label = tk.Label(main_frame, text="", font=(FONT, 14, "bold"),
                              bg=BG_COLOR, wraplength=700)
    feedback_label.pack(pady=(0, 10))
 
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack()
    submit_button = make_button(button_frame, "Submit Answer", submit_answer)
    submit_button.pack(side="left", padx=10)
 
    last_question = current_question == len(quiz_questions) - 1
    next_button = make_button(button_frame,
                              "See Results" if last_question else "Next Question",
                              next_question, bg="#8B5CF6")
    next_button.config(state="disabled")
    next_button.pack(side="left", padx=10)
 
    update_timer()
 
 
# TIMER
def update_timer():
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"Time left: {time_left}s",
                       fg=WRONG_COLOR if time_left <= 5 else TEXT_COLOR)
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)
 
 
def stop_timer():
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None
 
 
# ANSWER CHECKING
def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")
 
 
def submit_answer():
    global score, answered
    if answered:                     
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return
 
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
    draw_progress(current_question + 1)
 
    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct! Great job!", fg=CORRECT_COLOR)
        launch_confetti()
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(
            text="Wrong! Correct answer: "
                 + get_choice_text(question, question["answer"]),
            fg=WRONG_COLOR)
    next_button.config(state="normal")
 
 
def time_up():
    global answered
    answered = True
    lock_choices()
    submit_button.config(state="disabled")
    draw_progress(current_question + 1)
 
    question = quiz_questions[current_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })
    feedback_label.config(
        text="Time is up! Correct answer: "
             + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR)
    next_button.config(state="normal")
 
 
def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()
 
 
# RESULTS, REVIEW, RESTART
def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)
 
    if percentage >= 90:
        message = "Excellent work!"
    elif percentage >= 70:
        message = "Good job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."
 
    tk.Label(main_frame, text="Quiz Complete!", font=(FONT, 26, "bold"),
             bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=(10, 5))
 
    score_card = tk.Frame(main_frame, bg=CARD_COLOR, highlightthickness=1,
                          highlightbackground=BORDER_COLOR)
    score_card.pack(fill="x", pady=8)
    tk.Label(score_card, text=f"Score: {score} / {total}  ({percentage:.0f}%)",
             font=(FONT, 20, "bold"), bg=CARD_COLOR,
             fg=TEXT_COLOR).pack(pady=(12, 0))
    tk.Label(score_card, text=message, font=(FONT, 14), bg=CARD_COLOR,
             fg=MUTED_COLOR).pack(pady=3)
 
    record_text = "New high score!" if new_record else f"High Score: {get_high_score()} / {total}"
    tk.Label(score_card, text=record_text, font=(FONT, 13, "bold"),
             bg=CARD_COLOR, fg=CORRECT_COLOR).pack(pady=(3, 12))
 
    tk.Label(main_frame, text="Answer Review (incorrect answers)",
             font=(FONT, 13, "bold"), bg=BG_COLOR,
             fg=TEXT_COLOR).pack(pady=(10, 3), anchor="w")
 
    review_frame = tk.Frame(main_frame, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, height=10, wrap="word",
                         font=(FONT, 11), bg=CARD_COLOR, fg=TEXT_COLOR,
                         relief="flat", highlightthickness=1,
                         highlightbackground=BORDER_COLOR, padx=10, pady=8,
                         yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)
 
    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")
 
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=15)
    make_button(button_frame, "Restart Quiz",
                restart_quiz).pack(side="left", padx=10)
    make_button(button_frame, "Exit", on_close,
                bg="#4B5563").pack(side="left", padx=10)
 
 
def restart_quiz():
    start_quiz()  # reshuffles questions and resets score
 
 
def on_close():
    stop_timer()
    stop_confetti()
    root.destroy()
 
 
# START THE PROGRAM
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()
