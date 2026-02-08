from datetime import date, timedelta


def forecast_linear(rows: list[dict], horizon_days: int) -> tuple[list[dict], float]:
    values = [float(r["value"]) for r in rows]
    if len(values) < 2:
        base = values[-1] if values else 0.0
        slope = 0.0
        confidence = 0.4
    else:
        base = values[-1]
        slope = (values[-1] - values[0]) / max(len(values) - 1, 1)
        confidence = 0.68

    start = date.today()
    points = []
    for i in range(1, horizon_days + 1):
        points.append({"date": str(start + timedelta(days=i)), "value": round(base + slope * i, 2)})
    return points, confidence
