# services/predictor.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
from django.conf import settings  # импортируем настройки проекта

# путь к файлу в корне проекта
data_path = os.path.join(settings.BASE_DIR, "dbkurs.xlsx")
df = None

def load_historical_data():
    global df
    try:
        df = pd.read_excel(data_path, skiprows=3)
        df.columns = [
            'Date', 'USD_buy', 'USD_sell',
            'EUR_buy', 'EUR_sell',
            'RUB_buy', 'RUB_sell'
        ]
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y', dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Date'])
        df = df.groupby('Date').mean().reset_index().sort_values('Date').reset_index(drop=True)
        print(f"[Predictor] Загружено {len(df)} дней исторических данных")
    except Exception as e:
        print(f"[Predictor] Ошибка загрузки файла: {e}")
        df = None

# Загружаем при старте
load_historical_data()

def predict_7_days_from_current(current_rate: float, currency: str = "USD", rate_type: str = "sell", days_back: int = 7):
    global df
    if df is None or len(df) < days_back:
        raise ValueError("Нет исторических данных")

    col = f"{currency}_{rate_type}"
    if col not in df.columns:
        raise ValueError("Неверная валюта или тип")

    # Берём последние N дней из истории, но последнее значение заменяем на ТЕКУЩИЙ курс
    historical = df[col].tail(days_back).copy().values
    historical[-1] = float(current_rate)  # ← вот магия!

    X = np.arange(len(historical)).reshape(-1, 1)
    y = historical
    model = LinearRegression().fit(X, y)

    # Прогноз на 7 дней вперёд
    future_x = np.arange(len(historical), len(historical) + 7).reshape(-1, 1)
    predictions = model.predict(future_x)

    today = datetime.now().date()
    dates = [(today + timedelta(days=i+1)).strftime("%Y-%m-%d") for i in range(7)]

    result = []
    for d, pred in zip(dates, predictions):
        result.append({"date": d, "rate": round(float(pred), 4)})

    return {
        "currency": currency.upper(),
        "type": rate_type,
        "current_rate_used": round(float(current_rate), 4),
        "predictions": result,
        "model": "Линейная регрессия по последним 7 дням + актуальный курс"
    }
