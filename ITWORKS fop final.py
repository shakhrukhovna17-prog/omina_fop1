import json
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

# -------- VARIABLE TYPES --------
version_float = 2.0                      # float
max_score = 80                           # int
app_title = "Morning Routine Survey"     # str
used_files = set()                       # set
allowed_ext = frozenset({".json"})       # frozenset

# -------- QUESTIONS --------
questions = [
    {"q": "How consistent is your wake-up time on weekdays?",
     "opts": [("Always consistent",0),("Mostly consistent",1),("Sometimes varies",2),("Often varies",3),("Completely irregular",4)]},

    {"q": "How refreshed do you feel upon waking up?",
     "opts": [("Fully refreshed",0),("Mostly refreshed",1),("Neutral",2),("Slightly tired",3),("Very exhausted",4)]},

    {"q": "How often do you delay getting out of bed after waking up?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "Do you follow a planned sequence of morning activities?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How much time do you dedicate to your morning routine?",
     "opts": [("More than 60 minutes",0),("45–60 minutes",1),("30–45 minutes",2),("15–30 minutes",3),("Less than 15 minutes",4)]},

    {"q": "How often do you include physical activity?",
     "opts": [("Daily",0),("Frequently",1),("Occasionally",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you skip breakfast?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How quickly do you check your phone after waking up?",
     "opts": [("After 1+ hour",0),("After 30–60 min",1),("After 15–30 min",2),("Within 15 min",3),("Immediately",4)]},

    {"q": "How much time do you spend on your phone in the morning?",
     "opts": [("None",0),("Less than 15 min",1),("15–30 min",2),("30–60 min",3),("More than 1 hour",4)]},

    {"q": "How prepared do you feel before starting classes?",
     "opts": [("Fully prepared",0),("Mostly prepared",1),("Somewhat prepared",2),("Slightly unprepared",3),("Not prepared at all",4)]},

    {"q": "How often are you late or rushed in the morning?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How well can you concentrate during your first class?",
     "opts": [("Excellent",0),("Good",1),("Average",2),("Poor",3),("Very poor",4)]},

    {"q": "What is your typical mood in the morning?",
     "opts": [("Very positive",0),("Positive",1),("Neutral",2),("Negative",3),("Very negative",4)]},

    {"q": "How motivated do you feel at the start of the day?",
     "opts": [("Highly motivated",0),("Motivated",1),("Neutral",2),("Low motivation",3),("No motivation",4)]},

    {"q": "How often do you feel mentally alert in the morning?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How organized is your morning preparation?",
     "opts": [("Fully organized",0),("Mostly organized",1),("Somewhat organized",2),("Disorganized",3),("Completely chaotic",4)]},

    {"q": "Do you prepare for the next day the night before?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "Do you include calm activities (reading, journaling)?",
     "opts": [("Daily",0),("Frequently",1),("Occasionally",2),("Rarely",3),("Never",4)]},

    {"q": "How often do you feel stressed in the morning?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How balanced does your morning feel overall?",
     "opts": [("Very balanced",0),("Balanced",1),("Neutral",2),("Unbalanced",3),("Very chaotic",4)]},
]

# -------- STATES --------
psych_states = {
    "Excellent Routine — Highly effective start": (0, 15),
    "Good Routine — Minor improvements needed": (16, 30),
    "Moderate Routine — Inconsistent habits": (31, 45),
    "Poor Routine — Affects academic performance": (46, 60),
    "Very Poor Routine — High disruption": (61, 70),
    "Critical Routine — Immediate lifestyle changes needed": (71, 80),
}

# -------- FUNCTIONS --------
def validate_name(name):
    name = name.strip()

    if name == "":
        return False

    for c in name:
        if not c.isalpha():
            return False
        return True

def validate_dob(dob):
    try:
        datetime.strptime(dob.strip(), "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score):
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_csv(file, data):
    with open(file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer", "Score"])
        for row in data["answers"]:
            writer.writerow([row["question"], row["answer"], row["score"]])

# -------- GUI --------
class App:
    def __init__(self, root):
        self.root = root
        root.title(app_title)
        root.geometry("600x500")
        root.configure(bg="#f5f7fa")

        self.main()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def create_card(self):
        card = tk.Frame(self.root, bg="white")
        card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=420)
        return card

    def create_button(self, parent, text, command):
        tk.Button(parent,
                  text=text,
                  command=command,
                  font=("Helvetica", 11),
                  bg="#4a90e2",
                  fg="white",
                  activebackground="#357ABD",
                  activeforeground="white",
                  bd=0,
                  padx=10,
                  pady=8,
                  width=25).pack(pady=10)

    def main(self):
        self.clear()
        card = self.create_card()

        tk.Label(card, text=app_title,
                 font=("Helvetica", 18, "bold"),
                 bg="white", fg="#333").pack(pady=20)

        self.create_button(card, "Start Survey", self.user_form)
        self.create_button(card, "Load Questions (JSON)", self.load_questions)

    def load_questions(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if not path:
            return

        ext = "." + path.split(".")[-1]

        if ext not in allowed_ext:
            messagebox.showerror("Error", "Invalid file type")
            return

        if path in used_files:
            messagebox.showerror("Error", "File already used")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            global questions
            questions = data
            used_files.add(path)

            messagebox.showinfo("Success", "Questions loaded!")
        except:
            messagebox.showerror("Error", "Invalid file")

    def user_form(self):
        self.clear()
        card = self.create_card()

        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.dob = tk.StringVar()
        self.sid = tk.StringVar()

        tk.Label(card, text="Enter Your Details",
                 font=("Helvetica", 16, "bold"),
                 bg="white").pack(pady=10)

        self.add(card, "Name:", self.name)
        self.add(card, "Surname:", self.surname)
        self.add(card, "Date of Birth (YYYY-MM-DD):", self.dob)
        self.add(card, "Student ID:", self.sid)

        self.create_button(card, "Start", self.validate)

    def add(self, parent, text, var):
        frame = tk.Frame(parent, bg="white")
        frame.pack(pady=5)

        tk.Label(frame, text=text, width=25,
                 anchor="w", bg="white").pack(side="left")

        tk.Entry(frame,
                 textvariable=var,
                 width=20,
                 bd=1,
                 relief="solid").pack(side="left")

    def validate(self):
        if not validate_name(self.name.get()):
            return messagebox.showerror("Error", "Invalid name")

        elif not validate_name(self.surname.get()):
            return messagebox.showerror("Error", "Invalid surname")

        elif not validate_dob(self.dob.get()):
            return messagebox.showerror("Error", "Invalid DOB. Use format: YYYY-MM-DD")

        elif not self.sid.get().isdigit():
            return messagebox.showerror("Error", "Student ID must be digits")

        else:
            self.index = 0
            self.score = 0
            self.answers = []
            self.ask()

    def ask(self):
        self.clear()
        card = self.create_card()

        q = questions[self.index]

        tk.Label(card, text=f"Question {self.index+1}",
                 font=("Helvetica", 14, "bold"),
                 bg="white").pack(pady=10)

        tk.Label(card, text=q["q"],
                 wraplength=350,
                 bg="white").pack(pady=10)

        self.choice = tk.IntVar(value=-1)

        for i in range(len(q["opts"])):
            tk.Radiobutton(card,
                           text=q["opts"][i][0],
                           variable=self.choice,
                           value=i,
                           bg="white",
                           anchor="w").pack(fill="x", padx=40)

        self.create_button(card, "Next", self.next_q)

    def next_q(self):
        if self.choice.get() == -1:
            return messagebox.showerror("Error", "Select an option")

        q = questions[self.index]
        text, score = q["opts"][self.choice.get()]

        self.score += score
        self.answers.append({
            "question": q["q"],
            "answer": text,
            "score": score
        })

        self.index += 1

        if self.index < len(questions):
            self.ask()
        else:
            self.finish()

    def finish(self):
        result = interpret_score(self.score)

        self.clear()
        card = self.create_card()

        tk.Label(card, text="Survey Completed!",
                 font=("Helvetica", 16, "bold"),
                 bg="white").pack(pady=15)

        tk.Label(card, text=f"Score: {self.score}/{max_score}",
                 bg="white").pack()

        tk.Label(card, text=result,
                 wraplength=350,
                 bg="white",
                 fg="#4a90e2",
                 font=("Helvetica", 11, "bold")).pack(pady=10)

        self.create_button(card, "Save JSON", self.save_json_btn)
        self.create_button(card, "Save CSV", self.save_csv_btn)

    def save_json_btn(self):
        file = filedialog.asksaveasfilename(defaultextension=".json")
        if file:
            data = {"score": self.score, "answers": self.answers}
            save_json(file, data)

    def save_csv_btn(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if file:
            data = {"answers": self.answers}
            save_csv(file, data)

# -------- RUN --------
root = tk.Tk()
root.geometry("600x500")

app = App(root)
root.mainloop()