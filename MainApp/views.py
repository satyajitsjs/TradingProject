from django.shortcuts import render
import pandas as pd
import json
from django.http import JsonResponse, HttpResponse
from .forms import UploadFileForm
from .models import Candle
from django.views.decorators.csrf import csrf_exempt
import asyncio

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            timeframe = form.cleaned_data['timeframe']
            candles = process_csv(file)
            converted_candles = asyncio.run(convert_timeframe(candles, timeframe))
            json_file_path = save_to_json(converted_candles)
            response = HttpResponse(json_file_path, content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="converted_candles.json"'
            return response
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def process_csv(file):
    df = pd.read_csv(file)
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

def save_to_json(candles):
    file_path = 'converted_candles.json'
    with open(file_path, 'w') as json_file:
        json.dump(candles, json_file)
    return file_path
