import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import Modules.scraper as sc
import Modules.greeting as op
import requests
import sys
import threading
import itertools
import re

class DarkThemeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web Scraper GUI")
        self.configure(bg="#23272e")
        self.geometry("950x700")
        self.create_widgets()
        self.apply_dark_theme()
        self.spinner_running = False
        self.spinner_cycle = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    def create_widgets(self):
        self.header = tk.Label(self, text="Web Scraper", font=("Arial", 26, "bold"), bg="#23272e", fg="#f8f8f2")
        self.header.pack(pady=15)

        self.url_label = tk.Label(self, text="Site URL:", bg="#23272e", fg="#f8f8f2", font=("Arial", 13))
        self.url_label.pack(pady=(10,0))
        self.url_entry = tk.Entry(self, width=55, font=("Arial", 13), bg="#282c34", fg="#f8f8f2", insertbackground="#f8f8f2", borderwidth=2, relief="groove")
        self.url_entry.pack(pady=7, ipady=4)
        self.url_entry.bind('<Return>', lambda event: self.scrape())
        self.url_entry.bind('<Control-a>', self.select_all_url_entry)
        self.url_entry.bind('<Control-A>', self.select_all_url_entry)

        self.scrape_btn = tk.Button(self, text="Scrape", command=self.scrape, bg="#44475a", fg="#f8f8f2", activebackground="#6272a4", activeforeground="#f8f8f2", font=("Arial", 13), width=10, height=1)
        self.scrape_btn.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self, width=80, height=18, font=("Consolas", 11), bg="#282c34", fg="#f8f8f2", insertbackground="#f8f8f2", borderwidth=2, relief="groove")
        self.result_text.pack(pady=12)

        self.save_btn = tk.Button(self, text="Save Results", command=self.save_results, bg="#44475a", fg="#f8f8f2", activebackground="#6272a4", activeforeground="#f8f8f2", font=("Arial", 13), width=14, height=1)
        self.save_btn.pack(pady=7)

        self.loading_label = tk.Label(self, text="", bg="#23272e", fg="#f8f8f2", font=("Arial", 14, "italic"))
        self.loading_label.pack(pady=(0, 7))

    def apply_dark_theme(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background="#23272e", foreground="#f8f8f2", fieldbackground="#282c34")
        style.configure('TButton', background="#44475a", foreground="#f8f8f2")
        style.configure('TLabel', background="#23272e", foreground="#f8f8f2")

    def show_loading(self):
        self.spinner_running = True
        self.animate_spinner()

    def hide_loading(self):
        self.spinner_running = False
        self.loading_label.config(text="")
        self.update_idletasks()

    def animate_spinner(self):
        if self.spinner_running:
            spinner_char = next(self.spinner_cycle)
            self.loading_label.config(text=f"Loading... {spinner_char}")
            self.after(100, self.animate_spinner)

    def scrape(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL.")
            return
        # Basic URL validation
        url_pattern = re.compile(r'^(https?://)?([\w.-]+)\.([a-zA-Z]{2,})(/\S*)?$')
        if not url_pattern.match(url):
            messagebox.showwarning("Warning", "Please enter a valid URL (e.g., https://example.com)")
            return
        self.result_text.delete(1.0, tk.END)
        self.show_loading()
        threading.Thread(target=self._scrape_thread, args=(url,), daemon=True).start()

    def _scrape_thread(self, url):
        try:
            result = sc.scrape(url)
            self.after(0, self.display_results, result, url)
        except requests.exceptions.RequestException as err:
            self.after(0, self.display_error, err)

    def display_results(self, result, url):
        self.hide_loading()
        if not result:
            self.result_text.insert(tk.END, "No links found.")
        else:
            for i, link in enumerate(result):
                self.result_text.insert(tk.END, f"{i+1}. {link}\n")
        self.current_result = result
        self.current_url = url

    def display_error(self, err):
        self.hide_loading()
        self.result_text.insert(tk.END, f"Error: {err}")
        self.current_result = None
        self.current_url = None

    def save_results(self):
        if hasattr(self, 'current_result') and self.current_result:
            sc.saving_results(self.current_result, self.current_url)
            messagebox.showinfo("Success", "Results saved.")
        else:
            messagebox.showwarning("Warning", "No results to save.")

    def select_all_url_entry(self, event):
        self.url_entry.select_range(0, tk.END)
        self.url_entry.icursor(tk.END)
        return 'break'

if __name__ == "__main__":
    op.opening()
    app = DarkThemeApp()
    app.mainloop() 