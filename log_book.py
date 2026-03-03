import json
import os
import csv
from datetime import datetime
from log_entry import LogEntry

DATA_JSON = "logbook.json"
ERROR_LOG_FILE = "import_errors.log"

class LogBook:
    """Logiraamatu haldusloogika: lisamine, kustutamine, otsimine ja failihaldus."""
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
        if not os.path.exists(filepath): return "Fail puudub.", 0
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