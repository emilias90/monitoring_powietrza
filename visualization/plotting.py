import matplotlib.pyplot as plt
from datetime import datetime

def plot_measurements(measurements, param_name):
    """
    Tworzy wykres wartości pomiarów, zaznaczając wartości minimalne i maksymalne.
    """
    if not measurements:
        return

    dates = []
    values = []

    for date_str, value, _ in measurements:
        if value is None:
            continue

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        dates.append(date)
        values.append(value)

    if not dates:
        return

    min_val = min(values)
    max_val = max(values)
    min_idx = values.index(min_val)
    max_idx = values.index(max_val)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', linestyle='-', color='blue', label=param_name)
    plt.scatter(dates[min_idx], min_val, color='green', label=f'Min: {min_val} ({dates[min_idx].strftime("%Y-%m-%d %H:%M")})')
    plt.scatter(dates[max_idx], max_val, color='red', label=f'Max: {max_val} ({dates[max_idx].strftime("%Y-%m-%d %H:%M")})')
    plt.title(f"Wykres: {param_name}")
    plt.xlabel("Data")
    plt.ylabel("Wartość")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def analyze_measurements(measurements):
    values = [(m[0], m[1]) for m in measurements if m[1] is not None]
    if not values:
        return None

    sorted_vals = sorted(values, key=lambda x: x[1])
    min_val, min_date = sorted_vals[0][1], sorted_vals[0][0]
    max_val, max_date = sorted_vals[-1][1], sorted_vals[-1][0]
    avg_val = sum(v[1] for v in values) / len(values)

    return {
        "min": (min_val, min_date),
        "max": (max_val, max_date),
        "avg": avg_val,
        "count": len(values),
        "start": values[0][0],
        "end": values[-1][0]
    }
