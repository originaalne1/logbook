import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from log_book import ERROR_LOG_FILE

COLORS = {
    "primary": "#2C3E50",
    "secondary": "#ECF0F1",
    "accent": "#3498DB",
    "success": "#27AE60",
    "danger": "#E74C3C",
    "text": "#2C3E50",
    "white": "#FFFFFF"
}

class LogBookGUI:
    """Kasutajaliidese klass."""
    def __init__(self, root, lb):
        self.root = root
        self.lb = lb
        self.root.title("IT Hoolduspäevik Pro")
        self.root.geometry("1150x700")
        self.root.configure(bg=COLORS["secondary"])

        self.setup_styles()
        self.build_ui()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Accent.TButton", background=COLORS["accent"], foreground=COLORS["white"])
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=COLORS["primary"], foreground="white")

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLORS["primary"], height=80)
        header.pack(fill="x")
        tk.Label(header, text="IT HOOLDUSPÄEVIK", bg=COLORS["primary"], fg="white", font=("Segoe UI", 24, "bold")).pack(pady=15)

        main_frame = tk.Frame(self.root, bg=COLORS["secondary"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. SISESTUSE PANEEL
        input_frame = ttk.LabelFrame(main_frame, text=" ➕ Uus sissekanne ")
        input_frame.pack(fill="x", pady=(0, 15))

        inputs = tk.Frame(input_frame, bg=COLORS["secondary"], pady=5)
        inputs.pack(fill="x", padx=10)

        tk.Label(inputs, text="Pealkiri:", bg=COLORS["secondary"]).grid(row=0, column=0, sticky="w", padx=5)
        self.ent_title = ttk.Entry(inputs, width=25)
        self.ent_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(inputs, text="Kirjeldus:", bg=COLORS["secondary"]).grid(row=0, column=2, sticky="w", padx=5)
        self.ent_desc = ttk.Entry(inputs, width=50)
        self.ent_desc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(inputs, text="LISA KIRJE", style="Accent.TButton", command=self.add_entry).grid(row=0, column=4, padx=15)

        # 2. TABELI PANEEL
        list_frame = ttk.LabelFrame(main_frame, text=" 📋 Tööde nimekiri ")
        list_frame.pack(fill="both", expand=True)

        search_bar = tk.Frame(list_frame, bg=COLORS["secondary"], pady=5)
        search_bar.pack(fill="x", padx=10)
        tk.Label(search_bar, text="🔍 Otsi:", bg=COLORS["secondary"]).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.do_search())
        ttk.Entry(search_bar, textvariable=self.search_var, width=30).pack(side="left", padx=5)

        tree_scroll = tk.Frame(list_frame)
        tree_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("id", "stat", "aeg", "pealkiri", "kirjeldus")
        self.tree = ttk.Treeview(tree_scroll, columns=cols, show="headings")
        self.tree.heading("id", text="ID"); self.tree.column("id", width=0, stretch=False)
        self.tree.heading("stat", text="STAATUS"); self.tree.column("stat", width=100, anchor="center")
        self.tree.heading("aeg", text="AEG"); self.tree.column("aeg", width=180, anchor="center")
        self.tree.heading("pealkiri", text="PEALKIRI"); self.tree.column("pealkiri", width=250)
        self.tree.heading("kirjeldus", text="KIRJELDUS"); self.tree.column("kirjeldus", width=400)

        self.tree.tag_configure("DONE", foreground=COLORS["success"])
        self.tree.tag_configure("OPEN", foreground=COLORS["danger"])

        sb = ttk.Scrollbar(tree_scroll, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        btn_frame = tk.Frame(list_frame, bg=COLORS["secondary"], pady=10)
        btn_frame.pack(fill="x", padx=10)
        ttk.Button(btn_frame, text="✅ STAATUS", command=self.toggle_status).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ KUSTUTA", command=self.delete_entry).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📂 IMPORTI CSV", command=self.import_csv).pack(side="right", padx=5)

    def refresh_table(self, data=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        source = data if data is not None else self.lb.entries
        source = sorted(source, key=lambda x: x.created_at, reverse=True)
        for e in source:
            tag = "DONE" if e.status == "DONE" else "OPEN"
            icon = "✅ DONE" if e.status == "DONE" else "🔥 OPEN"
            self.tree.insert("", "end", values=(e.created_at, icon, e.get_display_time(), e.title, e.description), tags=(tag,))

    def add_entry(self):
        try:
            self.lb.add_entry(self.ent_title.get(), self.ent_desc.get())
            self.refresh_table()
            self.ent_title.delete(0, tk.END); self.ent_desc.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Viga", str(e))

    def do_search(self):
        self.refresh_table(self.lb.search(self.search_var.get()))

    def toggle_status(self):
        sel = self.tree.selection()
        if not sel: return
        item_id = self.tree.item(sel[0])['values'][0]
        self.lb.toggle_status(str(item_id))
        self.do_search()

    def delete_entry(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Kustuta", "Kas oled kindel?"):
            item_id = self.tree.item(sel[0])['values'][0]
            self.lb.remove_entry(str(item_id))
            self.do_search()

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV failid", "*.csv")])
        if path:
            ok, errs = self.lb.import_csv(path)
            self.refresh_table()
            msg = f"Imporditi {ok} kirjet."
            if errs > 0:
                msg += f"\nVigu: {errs}. Vaata: {ERROR_LOG_FILE}"
                messagebox.showwarning("Hoiatus", msg)
            else:
                messagebox.showinfo("Edu", msg)