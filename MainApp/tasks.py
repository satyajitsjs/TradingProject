from celery import shared_task
import csv
import json
from datetime import datetime, timedelta
from django.conf import settings
import os

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@shared_task(bind=True)  # Retry up to 3 times with a delay of 10 seconds
def process_csv_file(self, file_content, timeframe):
    try:
        reader = csv.DictReader(file_content.splitlines())
        candles = []

        for row in reader:
            candle = {
                'id': row['BANKNIFTY'],
                'open': float(row['OPEN']),
                'high': float(row['HIGH']),
                'low': float(row['LOW']),
                'close': float(row['CLOSE']),
                'date': datetime.strptime(row['DATE'] + row['TIME'], '%Y%m%d%H:%M'),
            }
            candles.append(candle)

        # Convert candles to given timeframe
        converted_candles = []
        current_candle = None
        for candle in candles:
            if current_candle is None:
                current_candle = candle
            elif candle['date'] - current_candle['date'] >= timedelta(minutes=timeframe):
                # Append converted candle
                converted_candles.append({
                    'id': current_candle['id'],
                    'open': current_candle['open'],
                    'high': max([c['high'] for c in candles if current_candle['date'] <= c['date'] <= candle['date']]),
                    'low': min([c['low'] for c in candles if current_candle['date'] <= c['date'] <= candle['date']]),
                    'close': candle['close'],
                    'date': current_candle['date'],
                })
                current_candle = None

        # Save converted data to JSON file
        json_file_path = os.path.join(settings.MEDIA_ROOT, 'converted_data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(converted_candles, json_file, cls=CustomJSONEncoder)  # Use custom JSON encoder

        return json_file_path
    except Exception as exc:
        # Retry the task in case of exceptions
        raise self.retry(exc=exc)
