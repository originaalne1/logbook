from datetime import datetime

class LogEntry:
    """Klass, mis esindab ühte hoolduspäeviku kirjet."""
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

        # Kuupäeva töötlemine ja sekunite lisamine
        if created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            success = False
            # Proovime erinevaid sisendvorminguid, kuid salvestame alati sekunditega
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
        """Tagastab kuupäeva koos sekunditega kasutajale kuvamiseks."""
        dt = datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d.%m.%Y %H:%M:%S")

    def to_dict(self):
        """Teisendab kirje sõnastikuks JSON-i salvestamiseks."""
        return {
            "created_at": self.created_at,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }