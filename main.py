import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from conversion import convertToFloat


class DolbyAudioDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("Dolby Audio Decoder")
        self.root.geometry("500x400")
        self.results = {}
        self.file_path = None
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File selector frame
        file_frame = ttk.LabelFrame(main_frame, text="Select file", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        self.file_path = tk.StringVar()
        ttk.Label(file_frame, text="Welect WAV file:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        file_entry_frame = ttk.Frame(file_frame)
        file_entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        file_entry_frame.columnconfigure(0, weight=1)

        ttk.Entry(file_entry_frame, textvariable=self.file_path, state="readonly", width=50).grid(row=0, column=0,
                                                                                                  sticky=(tk.W, tk.E),
                                                                                                  padx=(0, 10))
        ttk.Button(file_entry_frame, text="Browse", command=self.browse_file).grid(row=0, column=1)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Process Button
        self.process_btn = ttk.Button(buttons_frame, text="Process Audio", command=self.process_audio, state="disabled")
        self.process_btn.grid(row=0, column=0, padx=(0, 5))

        # Test Button
        self.test_btn = ttk.Button(buttons_frame, text="Test filtration", state="disabled")
        self.test_btn.grid(row=0, column=1, padx=(5, 0))

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        # Results text widget with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.results_text = tk.Text(text_frame, height=15, width=60, state="disabled")
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select WAV Audio File",
                                               filetypes=[("WAV files", "*.wav")],
                                               initialdir=".")
        if file_path:
            self.file_path.set(file_path)
            self.process_btn.config(state="normal")
            self.test_btn.config(state="normal")
            self.clear_results()

    def clear_results(self):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.configure(state="disabled")

    def add_result_text(self, text):
        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.config(state="disabled")
        self.results_text.see(tk.END)

    def process_audio(self):
        try:
            file_path = self.file_path.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a WAV file.")
                return

            self.clear_results()
            self.add_result_text("Processing audio...")
            self.add_result_text(f"File path: {file_path}")
            self.add_result_text("-" * 50)

        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = DolbyAudioDecoder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
