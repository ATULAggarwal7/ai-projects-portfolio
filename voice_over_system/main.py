# main.py
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
from tts_engine import combine_audio_chunks, apply_user_dictionary, update_dictionary_entry

OUTPUT_DIR = "samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart CSV → TTS (Row-wise + Manual)")
        self.geometry("1000x750")

        # State
        self.df = None
        self.language = tk.StringVar(value="en")

        # --- UI ---
        frm_top = ttk.Frame(self)
        frm_top.pack(fill=tk.X, padx=8, pady=8)

        btn_load = ttk.Button(frm_top, text="Load CSV", command=self.load_csv)
        btn_load.pack(side=tk.LEFT)

        ttk.Label(frm_top, text="Language:").pack(side=tk.LEFT, padx=(10, 0))
        lang_entry = ttk.Entry(frm_top, textvariable=self.language, width=6)
        lang_entry.pack(side=tk.LEFT)

        btn_process = ttk.Button(frm_top, text="Generate Row-wise Audio", command=self.process_rows)
        btn_process.pack(side=tk.LEFT, padx=(20, 0))

        # Middle: Treeview preview
        self.tree = ttk.Treeview(self, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Manual text input
        frm_manual = ttk.LabelFrame(self, text="Manual Text Input")
        frm_manual.pack(fill=tk.BOTH, padx=8, pady=(0, 8), expand=True)

        self.txt_manual = tk.Text(frm_manual, height=6)
        self.txt_manual.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        frm_params = ttk.Frame(frm_manual)
        frm_params.pack(fill=tk.X, padx=4, pady=4)

        ttk.Label(frm_params, text="Speed").pack(side=tk.LEFT)
        self.speed_manual = tk.DoubleVar(value=1.0)
        ttk.Spinbox(frm_params, from_=0.5, to=2.0, increment=0.1, textvariable=self.speed_manual, width=5).pack(side=tk.LEFT)

        ttk.Label(frm_params, text="Pitch").pack(side=tk.LEFT, padx=(10, 0))
        self.pitch_manual = tk.DoubleVar(value=1.0)
        ttk.Spinbox(frm_params, from_=0.5, to=2.0, increment=0.1, textvariable=self.pitch_manual, width=5).pack(side=tk.LEFT)

        ttk.Label(frm_params, text="Volume(dB)").pack(side=tk.LEFT, padx=(10, 0))
        self.volume_manual = tk.DoubleVar(value=0.0)
        ttk.Spinbox(frm_params, from_=-10, to=10, increment=1, textvariable=self.volume_manual, width=5).pack(side=tk.LEFT)

        btn_manual = ttk.Button(frm_params, text="Generate Speech from Text", command=self.process_manual_text)
        btn_manual.pack(side=tk.LEFT, padx=(10, 0))

        # Log / status
        self.log = tk.Text(self, height=6)
        self.log.pack(fill=tk.X, padx=8, pady=(0, 8))

    def log_msg(self, *parts):
        self.log.insert(tk.END, " ".join(map(str, parts)) + "\n")
        self.log.see(tk.END)

    # --- CSV Handling ---
    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            df = pd.read_csv(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
            return
        self.df = df.fillna("")
        self.refresh_preview()
        self.log_msg("Loaded:", path, "Rows:", len(self.df))

    def refresh_preview(self):
        # clear tree
        for c in self.tree.get_children():
            self.tree.delete(c)
        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        # insert first 50 rows
        for i, row in self.df.head(50).iterrows():
            vals = [str(row[c]) for c in self.df.columns]
            self.tree.insert("", tk.END, values=vals)

    def process_rows(self):
        if self.df is None:
            messagebox.showinfo("No CSV", "Please load a CSV first.")
            return
        threading.Thread(target=self._process_rows_worker, daemon=True).start()

    def _process_rows_worker(self):
        self.log_msg("Starting row-wise generation...")
        for i, row in self.df.iterrows():
            text = str(row.get("text", "")).strip()
            if not text:
                continue

            text = apply_user_dictionary(text)

            # pick per-row params (fallback if missing)
            pitch = float(row.get("pitch", 1.0) or 1.0)
            speed = float(row.get("speed", 1.0) or 1.0)
            volume = float(row.get("volume", 0.0) or 0.0)

            out_file = os.path.join(OUTPUT_DIR, f"row_{i+1}.wav")

            try:
                combine_audio_chunks(
                    text,
                    out_file,
                    language=self.language.get(),
                    pitch=pitch,
                    speed=speed,
                    volume=volume,
                )
                self.log_msg(f"Row {i+1} done → {out_file}")
            except Exception as e:
                self.log_msg(f"Row {i+1} failed:", e)

        self.log_msg("All rows processed.")
        # Ask dictionary corrections in main thread
        self.after(0, self.ask_dictionary_corrections)

    def ask_dictionary_corrections(self):
        want_dic = messagebox.askyesno("Dictionary", "Any pronunciation errors you want to save to dictionary?")
        if want_dic:
            while True:
                wrong = simpledialog.askstring("Wrong word", "Enter wrong word (leave blank to stop):")
                if not wrong:
                    break
                corr = simpledialog.askstring("Correction", f"Enter correction for '{wrong}':")
                if corr:
                    update_dictionary_entry(wrong, corr)
                    self.log_msg(f"Saved dictionary: {wrong} → {corr}")

    # --- Manual Text Handling ---
    def process_manual_text(self):
        text = self.txt_manual.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("No text", "Please enter some text to generate speech.")
            return
        text = apply_user_dictionary(text)
        pitch = self.pitch_manual.get()
        speed = self.speed_manual.get()
        volume = self.volume_manual.get()
        out_file = os.path.join(OUTPUT_DIR, "manual_text.wav")

        threading.Thread(target=self._generate_manual_worker, args=(text, out_file, pitch, speed, volume), daemon=True).start()

    def _generate_manual_worker(self, text, out_file, pitch, speed, volume):
        self.log_msg("Generating manual text audio...")
        try:
            combine_audio_chunks(
                text,
                out_file,
                language=self.language.get(),
                pitch=pitch,
                speed=speed,
                volume=volume,
            )
            self.log_msg("Manual text audio saved →", out_file)
            # Auto-play
            try:
                if os.name == "nt":
                    os.startfile(out_file)
                else:
                    os.system(f'xdg-open "{out_file}"')
            except Exception:
                self.log_msg("Could not auto-play; file at:", out_file)
            # Ask dictionary corrections in main thread
            self.after(0, self.ask_dictionary_corrections)
        except Exception as e:
            self.log_msg("Manual TTS generation failed:", e)


if __name__ == "__main__":
    print("Launching Smart CSV → TTS GUI (Row-wise + Manual)...")
    app = App()
    app.mainloop()
    print("Exited GUI")
