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
        self.progress_bar = tk.Label(self.root, text="0%", width=10, font=("Helvetica", 12))
        self.progress_bar.pack()
        self.total = total
        self.current = 0
        self.update_progress()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)

    def update_progress(self):
        percentage = int((self.current / self.total) * 100)
        self.progress_bar.config(text=f"{percentage}%")
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

def simula_scrittura(testo, progress_window):
    mean_speed = 0.2  # velocità media di scrittura
    speed_deviation = 0.1  # deviazione standard della velocità
    error_probability = 0.1  # probabilità di errore per ogni carattere

    chars = list(testo)
    total_chars = len(chars)

    for char in chars:
        # Simula la velocità di scrittura con una distribuzione normale
        pause_interval = random.gauss(mean_speed, speed_deviation)
        time.sleep(max(0, pause_interval))

        # Introduce un errore con la probabilità specificata
        if random.random() < error_probability:
            carattere_errato = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            keyboard.Controller().type(carattere_errato)
            time.sleep(0.5)
            keyboard.Controller().press(keyboard.Key.backspace)
            time.sleep(0.3)
            keyboard.Controller().type(char)
        else:
            keyboard.Controller().type(char)
            progress_window.increment_progress()

    progress_window.on_close()

if __name__ == "__main__":
    testo_da_scrivere = get_user_input()

    total_chars = len(testo_da_scrivere)

    progress_window = ProgressWindow(total_chars)

    print("Lo script inizierà a scrivere tra 3 secondi. Premi Ctrl + C per interrompere.")
    time.sleep(3)

    listener = keyboard.Listener(on_press=lambda k: on_press(k, progress_window),
                                 on_release=lambda k: on_release(k, progress_window, listener))

    threading.Thread(target=simula_scrittura, args=(testo_da_scrivere, progress_window)).start()

    listener.start()
    progress_window.root.mainloop()
    listener.join()
