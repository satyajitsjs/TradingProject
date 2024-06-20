from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import UploadFileForm
import pandas as pd
import json
import asyncio
from io import BytesIO

# Define the Candle class
class Candle:
    def __init__(self, id, open, high, low, close, date):
        self.id = id
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            timeframe = form.cleaned_data['timeframe']
            candles = process_csv(file)
            converted_candles = asyncio.run(convert_timeframe(candles, timeframe))
            response = create_json_response(converted_candles)
            return response
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def process_csv(file):
    df = pd.read_csv(file, delimiter=',')  # Ensure it reads the .txt file as CSV
    candles = []
    for index, row in df.iterrows():
        candle = Candle(
            id=index,
            open=row['OPEN'],
            high=row['HIGH'],
            low=row['LOW'],
            close=row['CLOSE'],
            date=f"{row['DATE']} {row['TIME']}"
        )
        candles.append(candle)
    return candles

async def convert_timeframe(candles, timeframe):
    converted_candles = []
    for i in range(0, len(candles), timeframe):
        batch = candles[i:i+timeframe]
        if not batch:
            continue
        open_price = batch[0].open
        high_price = max(c.high for c in batch)
        low_price = min(c.low for c in batch)
        close_price = batch[-1].close
        date = batch[0].date
        converted_candles.append({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'date': date
        })
        await asyncio.sleep(0)  # Simulate async operation
    return converted_candles

def create_json_response(candles):
    json_data = json.dumps(candles, indent=4)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="converted_candles.json"'
    return response
