from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import base64
import os

def home(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        image_url = request.POST.get('image')

        if image_url:
            response = requests.get(image_url)
            image_bytes = BytesIO(response.content)

            demo_image = Image.open(image_bytes).convert('RGBA')

            img_width, img_height = demo_image.size

            draw_image = ImageDraw.Draw(demo_image)
            text_image = f'{data}'

            font_size = 250 
            font_file_name = 'ProtestGuerrilla-Regular.ttf'
            font_directory = 'fonts'  
            font_path = os.path.join(os.path.dirname(__file__), font_directory, font_file_name)

            try:
                font_image = ImageFont.truetype(font_path, font_size)
            except IOError:
                font_image = ImageFont.load_default()
                print("filenotfound")

            bbox = draw_image.textbbox((0, 0), text_image, font=font_image)
            text_width = bbox[2] - bbox[0]  
            text_height = bbox[3] - bbox[1]  

            x = (img_width - text_width) / 2
            y = (img_height - text_height) / 2

            draw_image.text((x, y), text_image, font=font_image, fill=(255, 255, 255, 128))

            demo_image = demo_image.convert('RGB')  
            image_bytes = BytesIO()
            demo_image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)  
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

            return render(request, "index.html", {
                'data': data,
                'img': image_base64
            })
    
    return render(request, "index.html")