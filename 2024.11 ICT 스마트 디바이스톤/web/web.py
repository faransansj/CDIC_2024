from flask import Flask, render_template_string
import os
import threading

app = Flask(__name__)

@app.route('/')
def home():
    # List all images in the 'source' directory
    images = [
        'static/detected_a14.jpg',
        'static/detected_a24.jpg',
        'static/detected_a34.jpg',
        'static/detected_a44.jpg'
    ]

    # Captions for images
    captions = [
        'right',
        'left',
        'frontUp',
        'frontDown'
    ]

    # HTML content with 2x2 image grid, captions, and buttons
    html_content = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>PARKICK</title>
    </head>
    <body>
        <div style="max-width: 1200px; margin: auto; padding: 20px;">
        <div style="display: flex; align-items: center;">
            <img src="static/icon.png" alt="Icon" style="width: 50px; height: 50px; margin-right: 10px;">
            <h1>PARKICK</h1>
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: center;">
            <div style="display: flex; flex-direction: column; align-items: center; margin: 10px;">
                <img src="{{ images[0] }}" alt="Image" style="width: 300px; height: auto;">
                <p>{{ captions[0] }}</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; margin: 10px;">
                <img src="{{ images[1] }}" alt="Image" style="width: 300px; height: auto;">
                <p>{{ captions[1] }}</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; margin: 10px;">
                <img src="{{ images[2] }}" alt="Image" style="width: 300px; height: auto;">
                <p>{{ captions[2] }}</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; margin: 10px;">
                <img src="{{ images[3] }}" alt="Image" style="width: 300px; height: auto;">
                <p>{{ captions[3] }}</p>
            </div>
        </div>
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <button style="padding: 10px 20px; margin: 10px; font-size: 16px;">킥보드 주차하기</button>
            <button style="padding: 10px 20px; margin: 10px; font-size: 16px;">킥보드 대여하기</button>
        </div>
            </div>
    </body>
    </html>
    '''

    return render_template_string(html_content, images=images, captions=captions)

if __name__ == '__main__':
    # Run the Flask app with reloader disabled to avoid threading issues
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
