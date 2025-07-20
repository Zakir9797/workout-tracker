# TRAINING TRACKER  
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import os
import csv
import matplotlib.pyplot as plt
import re

#  Settings 
CALORIES_PER_REP = {
    "push-ups": 0.29,
    "squats": 0.32,
    "pull-ups": 1.0,
    "abs": 0.25,
    "jumps": 0.2,
    "burpees": 1.2,
    "plank (1 min)": 3.5,
    "running in place": 0.5,
    "lunges": 0.4,
    "leg raises": 0.3,
}

#  User setup 
root = tk.Tk()
root.withdraw()
user_name = simpledialog.askstring("User", "Enter your username:")
if not user_name:
    exit()

user_name = re.sub(r"\W+", "_", user_name.strip().lower())
data_dir = "data"
import os
print(">> Working directory:", os.getcwd())
os.makedirs(data_dir, exist_ok=True)

csv_file = os.path.join(data_dir, f"training_{user_name}.csv")
log_file = os.path.join(data_dir, f"log_{user_name}.txt")
root.deiconify()

# Global variables 
stats = {}
last_saved_graph = ""

#  Helper functions 
def parse_sets_and_reps():
    try:
        sets_raw = sets_entry.get().replace("x", "x").lower()
        reps_raw = reps_entry.get().replace("x", "x").lower()
        if "x" in sets_raw:
            parts = sets_raw.split("x")
            sets, reps = int(parts[0]), int(parts[1])
        elif "x" in reps_raw:
            parts = reps_raw.split("x")
            sets, reps = int(parts[0]), int(parts[1])
        else:
            sets = int(sets_entry.get())
            reps = int(reps_entry.get())
        if sets <= 0 or reps <= 0:
            raise ValueError
        return sets, reps
    except:
        return None, None

def clear_form():
    exercise_entry.set("")
    sets_entry.delete(0, tk.END)
    reps_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    exercise_entry.focus()
def clear_form_and_notify():
    clear_form()
    status_label.config(text="Form cleared", fg="blue")

#  Core logic 
def add_exercise():
    exercise = exercise_entry.get().strip().lower()
    if not exercise:
        status_label.config(text="Enter exercise name", fg="red")
        return
    if not re.match(r"^[a-zA-Z\s-]+$", exercise):
        status_label.config(text="Name must contain only letters!", fg="red")
        return
    sets, reps = parse_sets_and_reps()
    if sets is None:
        status_label.config(text="Invalid sets and reps", fg="red")
        return

    calories_per_rep = CALORIES_PER_REP.get(exercise)
    if calories_per_rep is None:
        try:
            calories_per_rep = float(calories_entry.get())
        except ValueError:
            status_label.config(text="Enter calories per rep", fg="red")
            return
    else:
        calories_entry.delete(0, tk.END)
        calories_entry.insert(0, str(calories_per_rep))
    total_reps = sets * reps
    total_calories = round(total_reps * calories_per_rep, 2)
    stats.setdefault(exercise, {"reps": 0, "calories": 0.0})
    stats[exercise]["reps"] += total_reps
    stats[exercise]["calories"] += total_calories
    with open(csv_file, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime('%Y-%m-%d'), exercise, total_reps, total_calories])

    status_label.config(text=f"Added: {exercise.title()} — {total_reps} reps", fg="green")
    clear_form()

def show_summary():
    total_reps = sum(e['reps'] for e in stats.values())
    total_calories = sum(e['calories'] for e in stats.values())
    summary = "Workout Summary:\n"
    for ex, e in stats.items():
        summary += f"- {ex.title()}: {e['reps']} reps, {e['calories']:.2f} kcal\n"
    summary += f"\nTotal reps: {total_reps}\nTotal calories: {total_calories:.2f} kcal"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%d.%m.%Y %H:%M')}]:\n{summary}\n\n")
    messagebox.showinfo("Summary", summary)

def show_history():
    if not os.path.exists(log_file):
        history = "No history yet."
    else:
        with open(log_file, "r", encoding="utf-8") as f:
            history = f.read()

    history_window = tk.Toplevel(root)
    history_window.title("Workout History")
    history_text = tk.Text(history_window, wrap="word")
    history_text.insert(tk.END, history)
    history_text.config(state="disabled")
    history_text.pack(fill="both", expand=True, padx=10, pady=10)

def show_graph():
    if not os.path.exists(csv_file):
        messagebox.showinfo("Graph", "No data to show.")
        return
    day_reps = {}
    day_calories = {}
    exercise_filter = {}
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            date, exercise, reps, calories = row
            reps = int(reps)
            calories = float(calories)

            day_reps[date] = day_reps.get(date, 0) + reps
            day_calories[date] = day_calories.get(date, 0) + calories

            if exercise not in exercise_filter:
                exercise_filter[exercise] = {}
            exercise_filter[exercise][date] = exercise_filter[exercise].get(date, 0) + reps
    dates = sorted(day_reps.keys())
    plt.figure(figsize=(10, 4))
    plt.plot(dates, [day_reps[d] for d in dates], marker="o", label="Reps")
    plt.xticks(rotation=45)
    plt.title("Progress by Day")
    plt.xlabel("Date")
    plt.ylabel("Reps")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    plt.figure(figsize=(10, 4))
    plt.plot(dates, [day_calories[d] for d in dates], marker="s", color="orange", label="Calories")
    plt.xticks(rotation=45)
    plt.title("Calories Burned")
    plt.xlabel("Date")
    plt.ylabel("Kcal")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    plt.figure(figsize=(10, 5))
    for ex, series in exercise_filter.items():
        edates = sorted(series.keys())
        plt.plot(edates, [series[d] for d in edates], marker='o', label=ex.title())
    plt.xticks(rotation=45)
    plt.title("Exercises by Day")
    plt.xlabel("Date")
    plt.ylabel("Reps")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

#  GUI 
root.title(f"Workout Tracker — {user_name.capitalize()}")
root.geometry("480x500")
root.resizable(False, False)

tk.Label(root, text=f"User: {user_name.capitalize()}", font=("Arial", 12, "italic")).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(root, text="Enter exercise data", font=("Arial", 14, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

tk.Label(root, text="Exercise:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
exercise_entry = ttk.Combobox(root, values=list(CALORIES_PER_REP.keys()))
exercise_entry.grid(row=2, column=1, padx=5, pady=5)
exercise_entry.focus()

tk.Label(root, text="Sets:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
sets_entry = tk.Entry(root)
sets_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Reps:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
reps_entry = tk.Entry(root)
reps_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Calories/Rep:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
calories_entry = tk.Entry(root)
calories_entry.grid(row=5, column=1, padx=5, pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(root, text="Add Exercise", command=add_exercise, width=20).grid(row=7, column=0, padx=10, pady=5)
tk.Button(root, text="Show Summary", command=show_summary, width=20).grid(row=7, column=1, padx=10, pady=5)
tk.Button(root, text="Clear Form", command=clear_form_and_notify, width=20).grid(row=8, column=0, padx=10, pady=5)
tk.Button(root, text="History", command=show_history, width=20).grid(row=8, column=1, padx=10, pady=5)
tk.Button(root, text="Show Graph", command=show_graph, width=42).grid(row=9, column=0, columnspan=2, pady=10)
root.mainloop()