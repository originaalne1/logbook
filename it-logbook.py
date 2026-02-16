import json
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# --- KONFIGURATSIOON ---
DATA_JSON = "logbook.json"
ERROR_LOG_FILE = "import_errors.log"

# Värvid ja stiilid
COLORS = {
    "primary": "#2C3E50",  # Tumesinine päis
    "secondary": "#ECF0F1",  # Hele taust
    "accent": "#3498DB",  # Sinine nupp
    "success": "#27AE60",  # Roheline (Done)
    "danger": "#E74C3C",  # Punane (Open/Delete)
    "text": "#2C3E50",  # Tume tekst
    "white": "#FFFFFF"
}


# ==========================================
# 1. ANDMEMUDEL: Logikirje
# ==========================================
class LogEntry:
    VALID_STATUSES = ["OPEN", "DONE"]

    def __init__(self, title, description, status="OPEN", created_at=None):
        if not title or len(str(title).strip()) < 4:
            raise ValueError("Pealkiri peab olema vähemalt 4 tähemärki.")
        if not description or len(str(description).strip()) < 10:
            raise ValueError("Kirjeldus peab olema vähemalt 10 tähemärki.")

        status = str(status).upper().strip()
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Lubamatu staatus: {status}")

        self.title = title.strip()
        self.description = description.strip()
        self.status = status

        if created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            success = False
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(str(created_at).strip(), fmt)
                    self.created_at = dt.strftime("%Y-%m-%d %H:%M:%S")
                    success = True
                    break
                except ValueError:
                    continue
            if not success:
                raise ValueError(f"Vigane kuupäev: {created_at}")

    def get_display_time(self):
        dt = datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d.%m.%Y %H:%M")

    def to_dict(self):
        return {
            "created_at": self.created_at,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }


# ==========================================
# 2. LOGIRAAMAT (Loogika)
# ==========================================
class LogBook:
    def __init__(self):
        self.entries = []
        self.load_json()

    def add_entry(self, title, description, status="OPEN", created_at=None):
        entry = LogEntry(title, description, status, created_at)
        self.entries.append(entry)
        self.save_json()
        return entry

    def remove_entry(self, created_at_id):
        self.entries = [e for e in self.entries if e.created_at != created_at_id]
        self.save_json()

    def toggle_status(self, created_at_id):
        for e in self.entries:
            if e.created_at == created_at_id:
                e.status = "DONE" if e.status == "OPEN" else "OPEN"
                self.save_json()
                return True
        return False

    def search(self, phrase):
        phrase = phrase.lower()
        return [e for e in self.entries if phrase in e.title.lower() or phrase in e.description.lower()]

    def save_json(self):
        data = [e.to_dict() for e in self.entries]
        with open(DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_json(self):
        if not os.path.exists(DATA_JSON): return
        try:
            with open(DATA_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.entries = []
                for d in data:
                    try:
                        self.entries.append(LogEntry(**d))
                    except:
                        continue
        except:
            pass

    def import_csv(self, filepath):
        if not os.path.exists(filepath): return "Fail puudub."
        valid_count = 0
        errors = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2048)
                f.seek(0)
                dialect = csv.Sniffer().sniff(content, delimiters=',;')
                reader = csv.reader(f, dialect)
                for row in reader:
                    if not row or len(row) < 2: continue
                    try:
                        c_at = row[0] if len(row) > 0 else None
                        tit = row[1] if len(row) > 1 else ""
                        desc = row[2] if len(row) > 2 else ""
                        stat = row[3] if len(row) > 3 else "OPEN"
                        self.add_entry(tit, desc, stat, c_at)
                        valid_count += 1
                    except Exception as e:
                        errors.append(f"Rida {row} -> {e}")
            if errors:
                with open(ERROR_LOG_FILE, "a", encoding="utf-8") as ef:
                    ef.write(f"\n--- Import {datetime.now()} ---\n")
                    for err in errors: ef.write(err + "\n")
            return valid_count, len(errors)
        except Exception as e:
            return str(e), 0


# ==========================================
# 3. ILUS GUI (Tkinter)
# ==========================================
class LogBookGUI:
    def __init__(self, root, lb):
        self.root = root
        self.lb = lb
        self.root.title("IT Hoolduspäevik Pro")
        self.root.geometry("1100x700")
        self.root.configure(bg=COLORS["secondary"])

        self.setup_styles()
        self.build_ui()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Üldine nupp
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=6,
                        background=COLORS["white"],
                        foreground=COLORS["text"])
        style.map("TButton", background=[("active", COLORS["accent"])], foreground=[("active", COLORS["white"])])

        # Accent nupp (Lisa)
        style.configure("Accent.TButton", background=COLORS["accent"], foreground=COLORS["white"])
        style.map("Accent.TButton", background=[("active", "#2980B9")])

        # Treeview (Tabel)
        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        foreground=COLORS["text"],
                        rowheight=30,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 11, "bold"),
                        background=COLORS["primary"],
                        foreground="white")

        # LabelFrame
        style.configure("TLabelframe", background=COLORS["secondary"])
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background=COLORS["secondary"],
                        foreground=COLORS["primary"])

    def build_ui(self):
        # --- PÄIS ---
        header = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header.pack(fill="x")
        tk.Label(header, text="IT HOOLDUSPÄEVIK", bg=COLORS["primary"], fg="white", font=("Segoe UI", 24, "bold")).pack(
            pady=15)

        # --- PEAMINE KONTEINER ---
        main_frame = tk.Frame(self.root, bg=COLORS["secondary"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. SISESTUSE PANEEL
        input_frame = ttk.LabelFrame(main_frame, text=" ➕ Uus sissekanne ")
        input_frame.pack(fill="x", pady=(0, 15))

        inputs = tk.Frame(input_frame, bg=COLORS["secondary"], pady=5)
        inputs.pack(fill="x", padx=10)

        tk.Label(inputs, text="Pealkiri:", bg=COLORS["secondary"], font=("Segoe UI", 10)).grid(row=0, column=0,
                                                                                               sticky="w", padx=5)
        self.ent_title = ttk.Entry(inputs, width=25, font=("Segoe UI", 10))
        self.ent_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(inputs, text="Kirjeldus:", bg=COLORS["secondary"], font=("Segoe UI", 10)).grid(row=0, column=2,
                                                                                                sticky="w", padx=5)
        self.ent_desc = ttk.Entry(inputs, width=50, font=("Segoe UI", 10))
        self.ent_desc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(inputs, text="LISA KIRJE", style="Accent.TButton", command=self.add_entry).grid(row=0, column=4,
                                                                                                   padx=15)

        # 2. FILTRI JA TABELI PANEEL
        list_frame = ttk.LabelFrame(main_frame, text=" 📋 Tööde nimekiri ")
        list_frame.pack(fill="both", expand=True)

        # Otsinguriba
        search_bar = tk.Frame(list_frame, bg=COLORS["secondary"], pady=5)
        search_bar.pack(fill="x", padx=10)

        tk.Label(search_bar, text="🔍 Otsi (pealkiri/kirjeldus):", bg=COLORS["secondary"]).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.do_search())
        ttk.Entry(search_bar, textvariable=self.search_var, width=30).pack(side="left", padx=5)

        # Tabel
        tree_scroll = tk.Frame(list_frame)
        tree_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("id", "stat", "aeg", "pealkiri", "kirjeldus")
        self.tree = ttk.Treeview(tree_scroll, columns=cols, show="headings")

        self.tree.heading("id", text="ID");
        self.tree.column("id", width=0, stretch=False)
        self.tree.heading("stat", text="STAATUS");
        self.tree.column("stat", width=100, anchor="center")
        self.tree.heading("aeg", text="AEG");
        self.tree.column("aeg", width=140, anchor="center")
        self.tree.heading("pealkiri", text="PEALKIRI");
        self.tree.column("pealkiri", width=250)
        self.tree.heading("kirjeldus", text="KIRJELDUS");
        self.tree.column("kirjeldus", width=400)

        # Värvilised tagid
        self.tree.tag_configure("DONE", foreground=COLORS["success"])  # Roheline tekst
        self.tree.tag_configure("OPEN", foreground=COLORS["danger"])  # Punane tekst

        sb = ttk.Scrollbar(tree_scroll, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # 3. NUPUD ALL
        btn_frame = tk.Frame(list_frame, bg=COLORS["secondary"], pady=10)
        btn_frame.pack(fill="x", padx=10)

        ttk.Button(btn_frame, text="✅ MÄRGI TEHTUKS / AVA", command=self.toggle_status).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ KUSTUTA", command=self.delete_entry).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="📂 IMPORTI CSV", command=self.import_csv).pack(side="right", padx=5)

    def refresh_table(self, data=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        source = data if data is not None else self.lb.entries
        # Sorteerime nii, et uusimad on eespool
        source = sorted(source, key=lambda x: x.created_at, reverse=True)

        for e in source:
            tag = "DONE" if e.status == "DONE" else "OPEN"
            icon = "✅ DONE" if e.status == "DONE" else "🔥 OPEN"
            self.tree.insert("", "end", values=(e.created_at, icon, e.get_display_time(), e.title, e.description),
                             tags=(tag,))

    def add_entry(self):
        try:
            self.lb.add_entry(self.ent_title.get(), self.ent_desc.get())
            self.refresh_table()
            self.ent_title.delete(0, tk.END)
            self.ent_desc.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Viga andmetes", str(e))

    def do_search(self):
        self.refresh_table(self.lb.search(self.search_var.get()))

    def toggle_status(self):
        sel = self.tree.selection()
        if not sel: return
        item_id = self.tree.item(sel[0])['values'][0]
        self.lb.toggle_status(str(item_id))
        self.do_search()  # Säilitame filtri

    def delete_entry(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Kustutamine", "Oled kindel, et soovid selle kirje jäädavalt kustutada?"):
            item_id = self.tree.item(sel[0])['values'][0]
            self.lb.remove_entry(str(item_id))
            self.do_search()

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV failid", "*.csv")])
        if path:
            ok, errs = self.lb.import_csv(path)
            self.refresh_table()
            msg = f"Imporditi edukalt {ok} kirjet."
            if errs > 0:
                msg += f"\n\n⚠️ Tähelepanu: {errs} rida oli vigased!\nVaata faili: {ERROR_LOG_FILE}"
                messagebox.showwarning("Import lõpetatud vigadega", msg)
            else:
                messagebox.showinfo("Import edukas", msg)


# ==========================================
# 4. PAREMDATUD CLI (Ikka olemas!)
# ==========================================
def run_cli(lb):
    while True:
        print("\n" + "=" * 50)
        print("   IT HOOLDUSPÄEVIK - CLI")
        print("=" * 50)
        print(f" Kirjeid andmebaasis: {len(lb.entries)}")
        print("-" * 50)
        print(" [1] Lisa uus töö")
        print(" [2] Kuva kõik tööd")
        print(" [3] Otsi (filtreeri fraasi järgi)")
        print(" [4] Muuda staatust")
        print(" [5] Kustuta")
        print(" [6] Importi CSV-st")
        print(" [0] Välju")

        c = input("\nValik > ").strip()

        if c == "1":
            try:
                lb.add_entry(input("Pealkiri: "), input("Kirjeldus: ")); print(">> OK!")
            except ValueError as e:
                print(f"!! {e}")
        elif c == "2":
            print(f"{'AEG':<20} | {'STAATUS':<6} | {'PEALKIRI'}")
            print("-" * 60)
            for e in lb.entries: print(f"{e.get_display_time():<20} | {e.status:<7} | {e.title}")
        elif c == "3":
            res = lb.search(input("Otsingusõna: "))
            for e in res: print(f"{e.get_display_time()} | {e.status} | {e.title}")
        elif c == "4":
            for i, e in enumerate(lb.entries): print(f"{i + 1}. {e.title} ({e.status})")
            try:
                idx = int(input("Nr: ")) - 1
                if 0 <= idx < len(lb.entries):
                    lb.toggle_status(lb.entries[idx].created_at);
                    print(">> Muudetud!")
            except:
                pass
        elif c == "5":
            try:
                idx = int(input("Kustuta nr: ")) - 1
                if 0 <= idx < len(lb.entries): lb.remove_entry(lb.entries[idx].created_at); print(">> Kustutatud!")
            except:
                pass
        elif c == "6":
            ok, err = lb.import_csv(input("Faili tee: "))
            print(f">> Imporditi {ok}, vigu {err}")
        elif c == "0":
            break


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    lb = LogBook()

    print("Käivitan IT Hoolduspäeviku...")
    print("1 - Konsoolirakendus (CLI)")
    print("2 - Graafiline liides (GUI) - SOOVITATAV")

    m = input("Valik (vaikimisi 2): ").strip()

    if m == "1":
        run_cli(lb)
    else:
        root = tk.Tk()
        app = LogBookGUI(root, lb)
        root.mainloop()