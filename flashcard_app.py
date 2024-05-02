import tkinter as tk
import sqlite3

# Connect to SQLite Database
conn = sqlite3.connect('flashcards.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS flashcards
             (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)''')
conn.commit()

first_run = True

def load_flashcards():
    c.execute('SELECT id, question, answer FROM flashcards')
    return c.fetchall()

flashcards = load_flashcards()

current_card = 0

def show_flashcard():
    global first_run
    if flashcards:
        flashcard_id, question, answer = flashcards[current_card]
        question_label.config(text=question)
        first_run = False
    else:
        if first_run:
            question_label.config(text="Click 'Next' to begin")
        else:
            question_label.config(text="No flashcards available.")

def show_answer():
    if flashcards:
        _, _, answer = flashcards[current_card]
        question_label.config(text=answer)

def next_card():
    global current_card
    if flashcards:
        current_card = (current_card + 1) % len(flashcards)
        flashcard_id, question, answer = flashcards[current_card]
        question_label.config(text=question)
    else:
        question_label.config(text="No flashcards available. Please add a new card.")

def previous_card():
    global current_card
    if flashcards and current_card > 0:
        current_card -= 1
    else:
        current_card = len(flashcards) - 1
    show_flashcard()

def add_flashcard():
    question = question_entry.get()
    answer = answer_entry.get()
    if question and answer:
        c.execute('INSERT INTO flashcards (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
        flashcards.append((c.lastrowid, question, answer))
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
    show_flashcard()

def delete_flashcard():
    if flashcards:
        flashcard_id, _, _ = flashcards[current_card]
        c.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        conn.commit()
        del flashcards[current_card]
        if not flashcards:
            question_label.config(text="No flashcards available.")
        else:
            next_card()

def toggle_add_fields():
    if question_entry.winfo_manager():
        question_entry.pack_forget()
        answer_entry.pack_forget()
        add_button.pack_forget()
    else:
        question_entry.pack(pady=(10,0))
        answer_entry.pack(pady=(5,10))
        add_button.pack(pady=10)

def view_all_cards():
    # Create a new window
    window = tk.Toplevel(root)
    window.title("All Flashcards")

    # Loop through all flashcards and add them to the window
    for flashcard_id, question, answer in flashcards:
        label = tk.Label(window, text=f"ID: {flashcard_id}, Question: {question}, Answer: {answer}")
        label.pack()

root = tk.Tk()
root.title("Flashcard App")

question_label = tk.Label(root, text="Click 'Next' to begin", font=('Helvetica', 18))
question_label.pack(pady=20)

question_entry = tk.Entry(root, font=('Helvetica', 14), width=50)
answer_entry = tk.Entry(root, font=('Helvetica', 14), width=50)
add_button = tk.Button(root, text="Add Flashcard", command=add_flashcard)

show_add_fields_button = tk.Button(root, text="Add New Card", command=toggle_add_fields)
show_add_fields_button.pack(pady=10)

delete_button = tk.Button(root, text="Delete Card", command=delete_flashcard)
delete_button.pack(side='bottom', pady=10)

view_all_button = tk.Button(root, text="View All Cards", command=view_all_cards)
view_all_button.pack(side='bottom', pady=10)

prev_button = tk.Button(root, text="Previous", command=previous_card)
prev_button.pack(side='left', fill='x', expand=True)
next_button = tk.Button(root, text="Next", command=next_card)
next_button.pack(side='right', fill='x', expand=True)
answer_button = tk.Button(root, text="Answer", command=show_answer)
answer_button.pack(side='bottom', fill='x', expand=True)

show_flashcard()

root.mainloop()

# Close the database connection
conn.close()
