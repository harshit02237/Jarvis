import tkinter as tk
import pyttsx3
import speech_recognition as sr
from openai import OpenAI

# --- OpenAI Setup ---
client = OpenAI(api_key="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")  # Replace with your real API key

# --- Text-to-Speech Setup (female voice) ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- Chat Function ---
def chat_with_riya(prompt):
    intro = "You are Riya, a soft-spoken emotional AI who listens to Harshit and replies with warmth and care."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": intro},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- GUI Response ---
def ask_riya():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    response = chat_with_riya(user_input)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"\nYou: {user_input}\nRiya (softly): {response}\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)
    speak(response)
    entry.delete(0, tk.END)

# --- Voice Input ---
def ask_by_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "\n🎙️ Listening...\n")
        output_text.config(state=tk.DISABLED)
        root.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, user_input)
            ask_riya()
        except sr.UnknownValueError:
            speak("Sorry Harshit, I couldn't understand that.")
        except sr.RequestError:
            speak("Network error, can't reach OpenAI servers.")
        except sr.WaitTimeoutError:
            speak("You were silent for too long, try again.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Riya - Your Soft AI Companion 💖")
root.geometry("520x450")
root.config(bg="#ffe6f0")

title = tk.Label(root, text="Talk to Riya 💬", font=("Helvetica", 18, "bold"), bg="#ffe6f0")
title.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=40)
entry.pack(pady=10)

frame = tk.Frame(root, bg="#ffe6f0")
frame.pack()

ask_btn = tk.Button(frame, text="Send Text", font=("Arial", 12), command=ask_riya, bg="#ff99cc", fg="white")
ask_btn.grid(row=0, column=0, padx=10)

voice_btn = tk.Button(frame, text="🎙️ Talk to Riya", font=("Arial", 12), command=ask_by_voice, bg="#cc66ff", fg="white")
voice_btn.grid(row=0, column=1, padx=10)

output_text = tk.Text(root, font=("Arial", 12), wrap=tk.WORD, state=tk.DISABLED, width=60, height=15, bg="#fff0f5")
output_text.pack(pady=10)

root.mainloop()
