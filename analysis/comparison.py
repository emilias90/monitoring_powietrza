from api.stations import get_sensors_for_station
from api.sensors import get_sensor_data
import matplotlib.pyplot as plt
from datetime import datetime

def find_sensor_by_param(sensors, param_code):
    for sensor in sensors:
        if sensor["param"]["paramFormula"].upper() == param_code.upper():
            return sensor
    return None

def compare_stations_by_param(param_code, station_ids, station_names=None):
    """
    Porównuje dany parametr (np. PM10) dla wielu stacji i rysuje wykres.
    :param param_code: np. "PM10"
    :param station_ids: lista ID stacji
    :param station_names: opcjonalnie - nazwy miast do wyświetlenia na wykresie
    """
    data_dict = {}

    for i, station_id in enumerate(station_ids):
        sensors = get_sensors_for_station(station_id)
        sensor = find_sensor_by_param(sensors, param_code)

        if not sensor:
            print(f"⚠️ Brak czujnika {param_code} w stacji {station_id}")
            continue

        sensor_data = get_sensor_data(sensor["id"])
        if not sensor_data:
            print(f"⚠️ Brak danych z czujnika {sensor['id']}")
            continue

        values = [
            (item["date"], item["value"])
            for item in sensor_data["values"]
            if item["value"] is not None
        ]

        if station_names and i < len(station_names):
            label = station_names[i]
        else:
            label = f"Stacja {station_id}"

        data_dict[label] = values

    # Rysowanie wykresu
    plt.figure(figsize=(10, 6))
    for label, measurements in data_dict.items():
        dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d, _ in measurements]
        values = [v for _, v in measurements]
        plt.plot(dates, values, label=label)

    plt.title(f"Porównanie parametru {param_code} w różnych lokalizacjach")
    plt.xlabel("Data")
    plt.ylabel(param_code)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
