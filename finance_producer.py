import time
import json
from pathlib import Path
import pandas as pd
from kafka import KafkaProducer

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

DATA_DIR = Path("data")
csv_files = DATA_DIR.glob("*.csv")  # find all CSV files in folder

for file in csv_files:
    symbol = file.stem  # get filename without .csv
    df = pd.read_csv(file, skiprows=[1])

    for _, row in df.iterrows():  # _ means we ignore index
        event = {
            "symbol": symbol,
            "date": str(row["Date"]),  # 2023-01-03
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"])
        }

        # Send the event to Kafka
        producer.send('finance', value=event)
        producer.flush()

        print(f'Sent: {event}')
        time.sleep(2)  # simulate real-time
