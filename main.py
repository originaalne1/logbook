import tkinter as tk
from log_book import LogBook
from log_book_gui import LogBookGUI

def run_cli(lb):
    """Käsurea liides (CLI)."""
    while True:
        print("\n" + "=" * 50)
        print("   IT HOOLDUSPÄEVIK - CLI")
        print("=" * 50)
        print(f" Kirjeid: {len(lb.entries)}")
        print("-" * 50)
        print(" [1] Lisa uus töö")
        print(" [2] Kuva kõik (koos sekunditega)")
        print(" [3] Otsi")
        print(" [4] Muuda staatust")
        print(" [5] Kustuta")
        print(" [0] Välju")

        c = input("\nValik > ").strip()

        if c == "1":
            try:
                lb.add_entry(input("Pealkiri: "), input("Kirjeldus: "))
                print(">> Lisatud!")
            except ValueError as e:
                print(f"!! {e}")
        elif c == "2":
            print(f"{'AEG (sekunditega)':<22} | {'STAATUS':<6} | {'PEALKIRI'}")
            print("-" * 70)
            for e in lb.entries:
                print(f"{e.get_display_time():<22} | {e.status:<7} | {e.title}")
        elif c == "3":
            res = lb.search(input("Otsingusõna: "))
            for e in res:
                print(f"{e.get_display_time()} | {e.status} | {e.title}")
        elif c == "4":
            for i, e in enumerate(lb.entries):
                print(f"{i + 1}. {e.title} ({e.status})")
            try:
                idx = int(input("Järjekorra number: ")) - 1
                if 0 <= idx < len(lb.entries):
                    lb.toggle_status(lb.entries[idx].created_at)
                    print(">> Muudetud!")
            except:
                print("!! Vigane valik")
        elif c == "5":
            try:
                idx = int(input("Kustuta number: ")) - 1
                if 0 <= idx < len(lb.entries):
                    lb.remove_entry(lb.entries[idx].created_at)
                    print(">> Kustutatud!")
            except:
                print("!! Vigane valik")
        elif c == "0":
            break

if __name__ == "__main__":
    lb = LogBook()

    print("Käivitan IT Hoolduspäeviku...")
    print("1 - Konsool (CLI)")
    print("2 - Graafiline liides (GUI) [Vaikimisi]")

    m = input("Valik: ").strip()

    if m == "1":
        run_cli(lb)
    else:
        root = tk.Tk()
        app = LogBookGUI(root, lb)
        root.mainloop()