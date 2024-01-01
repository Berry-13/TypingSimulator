import time
import random
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from pynput import keyboard

class InputDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.value = ""
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Inserisci il testo da scrivere:").grid(row=0, sticky="w")
        self.entry = tk.Text(master, width=40, height=10, wrap=tk.WORD)
        self.entry.grid(row=1, padx=10, pady=5)
        return self.entry

    def apply(self):
        self.value = self.entry.get("1.0", tk.END).strip()

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale

    dialog = InputDialog(root, "Input Testo")
    user_input = dialog.value
    return user_input

class ProgressWindow:
    def __init__(self, total):
        self.root = tk.Tk()
        self.root.title("Progresso")
        self.root.geometry("200x50+0+0")
        self.progress_bar = ttk.Progressbar(self.root, length=200, mode="determinate")
        self.progress_bar.pack()
        self.total = total
        self.current = 0
        self.update_progress()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)

    def update_progress(self):
        percentage = int((self.current / self.total) * 100)
        self.progress_bar["value"] = percentage
        self.root.update()

    def increment_progress(self):
        self.current += 1
        self.update_progress()

    def on_close(self):
        self.root.destroy()
        exit()

def on_press(key, progress_window):
    try:
        # Stampa il tasto premuto
        print(f'Tasto premuto: {key.char}')

    except AttributeError:
        # Se il tasto non è un carattere, ignoralo
        pass

def on_release(key, progress_window, listener):
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        progress_window.on_close()
        listener.stop()

def simulate_typing(text, progress_window, mean_speed, speed_deviation, error_probability):
    chars = list(text)
    total_chars = len(chars)
    punctuation_chars = set(".,")

    for idx, char in enumerate(chars):
        # Introduce una pausa più lunga dopo dei punti o alcune virgole
        if char in punctuation_chars and random.random() < 0.2:  # 20% di probabilità
            time.sleep(random.uniform(5, 10))  # Pausa di 5-10 secondi
        else:
            # Simula la velocità di scrittura con una distribuzione normale
            pause_interval = random.gauss(mean_speed, speed_deviation)
            time.sleep(max(0, pause_interval))

        # Introduce un errore con la probabilità specificata
        if random.random() < error_probability:
            if random.random() < 0.2:  # 20% di probabilità di cancellare una parola intera
                keyboard.Controller().press(keyboard.Key.backspace)
                time.sleep(0.5)
                keyboard.Controller().press(keyboard.Key.backspace)
                time.sleep(0.5)
                keyboard.Controller().type(char)
            else:
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
                keyboard.Controller().type(wrong_char)
                time.sleep(0.5)
                keyboard.Controller().press(keyboard.Key.backspace)
                time.sleep(0.3)
                keyboard.Controller().type(char)
        else:
            keyboard.Controller().type(char)
            progress_window.increment_progress()

    progress_window.on_close()

def generate_smooth_variation(initial_value, variation_range, num_steps):
    values = [initial_value]
    for _ in range(num_steps - 1):
        next_value = values[-1] + random.uniform(-variation_range, variation_range)
        values.append(next_value)
    return values[-1]

if __name__ == "__main__":
    text_to_type = get_user_input()

    total_chars = len(text_to_type)

    progress_window = ProgressWindow(total_chars)

    print("Lo script inizierà a scrivere tra 3 secondi. Premi Ctrl + C per interrompere.")
    time.sleep(3)

    listener = keyboard.Listener(on_press=lambda k: on_press(k, progress_window),
                                 on_release=lambda k: on_release(k, progress_window, listener))

    # Genera valori casuali senza ripetizioni per le variabili
    mean_speed = generate_smooth_variation(0.5, 0.03, total_chars)
    speed_deviation = generate_smooth_variation(0.3, 0.01, total_chars)
    error_probability = generate_smooth_variation(0.1, 0.005, total_chars)

    threading.Thread(target=simulate_typing, args=(text_to_type, progress_window,
                                                   mean_speed, speed_deviation,
                                                   error_probability)).start()

    listener.start()
    progress_window.root.mainloop()
    listener.join()
