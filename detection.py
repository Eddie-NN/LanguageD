import tkinter as tk
from tkinter import messagebox
import fasttext
import pycountry
import numpy as np
import unicodedata

model = fasttext.load_model("lid.176.bin")

def get_language_name(lang_code):
    language = pycountry.languages.get(alpha_2=lang_code)
    return language.name if language else lang_code

def contains_valid_letters(text):
    for char in text:
        if unicodedata.category(char).startswith('L'):
            return True
    return False

def safe_predict(model, text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    try:
        labels, probs = model.predict(text)
        return np.asarray(labels), np.asarray(probs)
    except Exception as e:
        print(f"Prediction error: {e}")
        return np.array(["__label__unknown"]), np.array([0.0])

def detect_language(event=None):
    text = entry.get()
    if not text.strip():
        messagebox.showwarning("Warning", ".متنی برای تشخیص وجود ندارد")
        return

    if not contains_valid_letters(text):
        messagebox.showerror("Error", ".متن باید شامل حروف واقعی از یک زبان باشد")
        return

    labels, probs = safe_predict(model, text)
    confidence = probs[0]
    lang_code = labels[0].replace("__label__", "")
    lang_name = get_language_name(lang_code)

    messagebox.showinfo("Result", f"زبان تشخیص داده شده : {lang_name}\nاعتماد: %{confidence*100:.2f}")
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("تشخیص زبان")
root.geometry("350x150")

label = tk.Label(root, text=":جمله یا کلمه را وارد کنید")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)
entry.focus()

button = tk.Button(root, text="تشخیص", command=detect_language)
button.pack(pady=10)

root.bind('<Return>', detect_language)

root.mainloop()
