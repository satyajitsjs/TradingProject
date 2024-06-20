from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseNotFound
from .forms import UploadFileForm
from .tasks import process_csv_file
from celery.result import AsyncResult
import os
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            timeframe = form.cleaned_data['timeframe']
            task = process_csv_file.delay(file.read().decode('utf-8'), timeframe)
            return JsonResponse({'task_id': task.id})
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def result(request, task_id):
    json_file_path = os.path.join(settings.MEDIA_ROOT, 'converted_data.json')
    if not os.path.exists(json_file_path):
        return HttpResponseNotFound('File not found')

    return render(request, 'result.html', {'task_id': task_id})

def task_status(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        json_file_path = result.result
        json_file_url = os.path.join(settings.MEDIA_URL, os.path.basename(json_file_path))
        return JsonResponse({'status': 'SUCCESS', 'url': json_file_url})
    else:
        return JsonResponse({'status': 'PENDING'})
