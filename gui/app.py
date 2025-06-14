import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from api.stations import get_all_stations, filter_stations_by_city, get_sensors_for_station
from api.sensors import get_sensor_data
from db.database import (
    create_table,
    create_measurements_table,
    insert_station,
    insert_measurements,
    create_sensors_table,
    insert_sensor
)
from visualization.plotting import plot_measurements, analyze_measurements


class AirQualityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Jakości Powietrza")

        create_table()
        create_measurements_table()
        create_sensors_table()

        self.city_var = tk.StringVar()
        self.station_var = tk.StringVar()
        self.sensor_var = tk.StringVar()
        self.date_from_var = tk.StringVar()
        self.date_to_var = tk.StringVar()

        self.stations = []
        self.sensors = []
        self.sensor_id = None
        self.stats_label = None

        # Statystyki
        self.stats_frame = None
        self.max_label = None
        self.min_label = None
        self.avg_label = None

        self.build_ui()

    def build_ui(self):
        # Miasto
        ttk.Label(self.root, text="Miasto:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.city_var).grid(row=0, column=1, sticky="ew")
        ttk.Button(self.root, text="Pobierz stacje", command=self.load_stations).grid(row=0, column=2, padx=5)

        # Lista stacji
        self.station_box = ttk.Combobox(self.root, textvariable=self.station_var, state="readonly", width=50)
        self.station_box.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        ttk.Button(self.root, text="Pobierz czujniki", command=self.load_sensors).grid(row=1, column=3)

        # Lista czujników
        self.sensor_box = ttk.Combobox(self.root, textvariable=self.sensor_var, state="readonly", width=50)
        self.sensor_box.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)
        ttk.Button(self.root, text="Pobierz dane", command=self.load_measurements).grid(row=2, column=3)

        # Zakres dat
        ttk.Label(self.root, text="Data od:").grid(row=3, column=0, sticky="e", padx=5)
        self.date_from_box = ttk.Combobox(self.root, textvariable=self.date_from_var, state="readonly", width=20)
        self.date_from_box.grid(row=3, column=1, sticky="w")

        ttk.Label(self.root, text="Data do:").grid(row=3, column=2, sticky="e", padx=5)
        self.date_to_box = ttk.Combobox(self.root, textvariable=self.date_to_var, state="readonly", width=20)
        self.date_to_box.grid(row=3, column=3, sticky="w")

        # Wypełnij daty (ostatnie 30 dni)
        from datetime import datetime, timedelta
        today = datetime.today()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        dates.reverse()  # Chronologicznie

        self.date_from_box['values'] = dates
        self.date_to_box['values'] = dates

        # Domyślne zaznaczenia
        self.date_from_var.set(dates[0])
        self.date_to_var.set(dates[-1])

        # Przyciski akcji
        ttk.Button(self.root, text="Wykres", command=self.plot_data).grid(row=4, column=0, pady=10)
        ttk.Button(self.root, text="Wyczyść dane", command=self.clear_data).grid(row=4, column=2)

        # Ramka na statystyki
        self.stats_frame = ttk.LabelFrame(self.root, text="Statystyki pomiarów")
        self.stats_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        self.max_label = ttk.Label(self.stats_frame, text="Maksimum: -")
        self.max_label.grid(row=0, column=0, sticky="w", padx=10)

        self.min_label = ttk.Label(self.stats_frame, text="Minimum: -")
        self.min_label.grid(row=0, column=1, sticky="w", padx=10)

        self.avg_label = ttk.Label(self.stats_frame, text="Średnia: -")
        self.avg_label.grid(row=0, column=2, sticky="w", padx=10)

        self.root.grid_columnconfigure(1, weight=1)

    def load_stations(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Uwaga", "Wprowadź nazwę miasta.")
            return

        all_stations = get_all_stations()
        self.stations = filter_stations_by_city(all_stations, city)

        if not self.stations:
            messagebox.showinfo("Brak wyników", f"Brak stacji w mieście: {city}")
            return

        self.station_box['values'] = [f"{s['stationName']} (ID: {s['id']})" for s in self.stations]
        for s in self.stations:
            insert_station(s)
        self.station_box.current(0)

    def load_sensors(self):
        if not self.station_box.get():
            messagebox.showwarning("Uwaga", "Najpierw wybierz stację.")
            return

        index = self.station_box.current()
        station = self.stations[index]
        self.sensors = get_sensors_for_station(station['id'])

        if not self.sensors:
            messagebox.showinfo("Brak czujników", "Brak czujników dla tej stacji.")
            return

        self.sensor_box['values'] = [f"{s['param']['paramName']} ({s['param']['paramFormula']}) - ID: {s['id']}" for s in self.sensors]
        for s in self.sensors:
            insert_sensor(s)
        self.sensor_box.current(0)

    def load_measurements(self):
        if not self.sensor_box.get():
            messagebox.showwarning("Uwaga", "Najpierw wybierz czujnik.")
            return

        index = self.sensor_box.current()
        sensor = self.sensors[index]
        self.sensor_id = sensor['id']
        data = get_sensor_data(self.sensor_id)
        self.param_name = sensor['param']['paramName']

        if not data or 'values' not in data:
            messagebox.showinfo("Brak danych", "Brak danych pomiarowych dla tego czujnika.")
            return

        param_key = data.get('key', '')
        insert_measurements(self.sensor_id, param_key, data['values'])

        self.raw_values = [
            (item['date'], item['value'])
            for item in data['values']
            if item['value'] is not None
        ]
        # Wyciągnięcie listy dostępnych dat
        all_dates = sorted({item['date'][:10] for item in data['values'] if item['value'] is not None})
        if not all_dates:
            messagebox.showinfo("Brak danych", "Brak wartości do analizy.")
            return

        # Ustaw dostępne daty w dropdownach
        self.date_from_box['values'] = all_dates
        self.date_to_box['values'] = all_dates

        if not self.date_from_var.get():
            self.date_from_var.set(all_dates[0])
        if not self.date_to_var.get():
            self.date_to_var.set(all_dates[-1])

        date_range = self.get_valid_date_range()
        if not date_range:
            return
        date_from, date_to = date_range

        values = [
            (item['date'], item['value'])
            for item in data['values']
            if item['value'] is not None and date_from <= datetime.strptime(item['date'][:10], "%Y-%m-%d") <= date_to
        ]

        if not values:
            messagebox.showinfo("Brak danych", "Brak wartości w wybranym zakresie dat.")
            return

        # Min / Max / Średnia
        min_entry = min(values, key=lambda x: x[1])
        max_entry = max(values, key=lambda x: x[1])
        avg_value = round(sum(v[1] for v in values) / len(values), 2)

        date_from_str = date_from.strftime("%Y-%m-%d")
        date_to_str = date_to.strftime("%Y-%m-%d")

        zakres = f"Statystyki pomiarów ({date_from_str} — {date_to_str})"
        self.stats_frame.config(text=zakres)

        self.min_label.config(text=f"Minimum: {min_entry[1]} ({min_entry[0][:16].replace('T', ' ')})")
        self.max_label.config(text=f"Maksimum: {max_entry[1]} ({max_entry[0][:16].replace('T', ' ')})")
        self.avg_label.config(text=f"Średnia: {avg_value:.2f}")

        # Zapisz przefiltrowane dane do atrybutu
        self.filtered_values = values

    def plot_data(self):
        filtered = self.get_filtered_values()
        if not filtered:
            messagebox.showinfo("Brak danych", "Brak danych do wyświetlenia wykresu.")
            return

        # Konwertuj dane do formatu dla plot_measurements
        data_for_plot = [(d, v, None) for d, v in filtered]
        plot_measurements(data_for_plot, self.param_name)


    def clear_data(self):
        self.station_box.set("")
        self.sensor_box.set("")
        self.sensor_id = None
        self.station_var.set("")
        self.sensor_var.set("")
        self.city_var.set("")
        self.date_from_var.set("")
        self.date_to_var.set("")
        if self.stats_frame:
            self.stats_frame.config(text="Statystyki pomiarów")
            self.min_label.config(text="Minimum: -")
            self.max_label.config(text="Maksimum: -")
            self.avg_label.config(text="Średnia: -")
        messagebox.showinfo("Wyczyszczono", "Dane i statystyki zostały wyczyszczone.")

    def get_filtered_values(self):
        if not hasattr(self, 'raw_values'):
            return []

        date_range = self.get_valid_date_range()
        if not date_range:
            return []
        date_from, date_to = date_range

        return [
            (d, v)
            for d, v in self.raw_values
            if date_from <= datetime.strptime(d[:10], "%Y-%m-%d") <= date_to
        ]

    def get_valid_date_range(self):
        """
        Zwraca krotkę (date_from, date_to) jako obiekty datetime,
        lub None jeśli daty są niepoprawne lub w złej kolejności.
        """
        date_from_str = self.date_from_var.get()
        date_to_str = self.date_to_var.get()

        try:
            date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
            date_to = datetime.strptime(date_to_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty.")
            return None

        if date_from > date_to:
            messagebox.showerror("Błąd", "Data OD nie może być późniejsza niż data DO.")
            return None

        return date_from, date_to


if __name__ == "__main__":
    root = tk.Tk()
    app = AirQualityApp(root)
    root.mainloop()