import os
import cv2
import torch
import numpy as np
from django.shortcuts import render
from .forms import UploadFileForm
from PIL import Image

def detect_people(image_path, is_video=False):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    if is_video:
        cap = cv2.VideoCapture(image_path)
        frames = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
        
            results = model(frame)
            result_img = results.render()[0]
            frames.append(result_img)

        cap.release()
        
        output_path = os.path.join('media', 'output_video.gif')
        if frames:
            pil_images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
            pil_images[0].save(output_path, save_all=True, append_images=pil_images[1:], optimize=False, duration=40, loop=0)
    else:
        img = cv2.imread(image_path)
        results = model(img)
        result_img = results.render()[0]
        
        output_path = os.path.join('media', 'output.jpg')
        cv2.imwrite(output_path, result_img)

    return output_path

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_path = os.path.join('media', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            is_video = uploaded_file.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
            output_image_path = detect_people(file_path, is_video)

            return render(request, 'detection/result.html', {'output_image': output_image_path, 'is_video': is_video})
    else:
        form = UploadFileForm()
    return render(request, 'detection/upload.html', {'form': form})
