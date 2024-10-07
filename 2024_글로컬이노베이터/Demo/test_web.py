from flask import Flask, request, render_template_string, send_file, jsonify
import hashlib
import uuid
import cv2
import numpy as np
from PIL import Image
import io
import os
import threading
import time

app = Flask(__name__)

# HTML 템플릿 정의
template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Image Upload and Watermark</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container mt-5">
      <h1 class="text-center">Upload an Image with Watermark</h1>
      <div class="card p-4">
        <form method="POST" action="/upload" enctype="multipart/form-data" id="uploadForm">
          <div class="form-group">
            <input type="file" name="file" class="form-control-file" id="fileInput" required>
          </div>
          <div class="form-group">
            <label for="watermarkText">Watermark Text (Optional):</label>
            <input type="text" name="watermarkText" class="form-control" id="watermarkText">
          </div>
          <button type="submit" class="btn btn-primary btn-block">Upload</button>
        </form>
      </div>
      <div id="preview" class="mt-4 text-center" style="display: none;">
        <h3>Image Preview</h3>
        <img id="imagePreview" src="" class="img-fluid" alt="Image Preview">
      </div>
      <div id="progress" class="mt-4 text-center" style="display: none;">
        <h3>Processing Image...</h3>
        <div class="progress">
          <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%;" id="progressBar"></div>
        </div>
      </div>
      <div id="result" class="mt-4 text-center" style="display: none;">
        <h3>Image Processed</h3>
        <p><strong>Image ID:</strong> <span id="imageId"></span></p>
        <p><strong>Image Hash:</strong> <span id="imageHash"></span></p>
      </div>
    </div>
    <script>
      document.getElementById('fileInput').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
            document.getElementById('preview').style.display = 'block';
            document.getElementById('imagePreview').src = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      });

      document.getElementById('uploadForm').addEventListener('submit', function(event) {
        event.preventDefault();
        document.getElementById('progress').style.display = 'block';
        let progress = 0;
        const progressBar = document.getElementById('progressBar');
        const interval = setInterval(() => {
          progress += 10;
          if (progress >= 100) {
            progress = 100;
            progressBar.classList.remove('progress-bar-animated');
            progressBar.classList.add('bg-success');
            clearInterval(interval);
          }
          progressBar.style.width = progress + '%';
        }, 500);

        const formData = new FormData(document.getElementById('uploadForm'));
        fetch('/upload', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          document.getElementById('progress').style.display = 'none';
          document.getElementById('result').style.display = 'block';
          document.getElementById('imageId').innerText = data.image_id;
          document.getElementById('imageHash').innerText = data.image_hash;
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    </script>
  </body>
</html>
'''

# 이미지 업로드 및 워터마크 기능 구현
def upload_image(file_path, watermark_text=None):
    if not file_path:
        return None, None, None

    # 이미지 열기
    img = Image.open(file_path)
    
    # 이미지 ID 및 해시 생성
    img_id = str(uuid.uuid4())
    img_hash = hashlib.sha256(img.tobytes()).hexdigest()

    # 해시 값을 워터마크로 삽입하기 위한 작업
    img_with_watermark = add_watermark(img, watermark_text if watermark_text else img_hash)
    
    return img_with_watermark, img_id, img_hash


def add_watermark(img, text):
    # OpenCV로 이미지 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # 워터마크 추가 - 더 복잡한 패턴 생성
    watermark = np.zeros((cv_img.shape[0] // 10, cv_img.shape[1] // 10, 3), dtype=np.uint8)
    cv2.circle(watermark, (watermark.shape[1] // 2, watermark.shape[0] // 2), min(watermark.shape[0], watermark.shape[1]) // 4, (255, 255, 255), -1)
    cv2.line(watermark, (0, 0), (watermark.shape[1], watermark.shape[0]), (255, 255, 255), 1)
    cv2.line(watermark, (0, watermark.shape[0]), (watermark.shape[1], 0), (255, 255, 255), 1)

    # 워터마크를 이미지의 특정 위치에 투명하게 삽입
    x_offset = cv_img.shape[1] - watermark.shape[1] - 10
    y_offset = cv_img.shape[0] - watermark.shape[0] - 10
    alpha = 0.1  # 워터마크의 투명도 (사람의 눈에 보이지 않게 매우 낮게 설정)
    for c in range(0, 3):
        cv_img[y_offset:y_offset+watermark.shape[0], x_offset:x_offset+watermark.shape[1], c] = (
            (1 - alpha) * cv_img[y_offset:y_offset+watermark.shape[0], x_offset:x_offset+watermark.shape[1], c] +
            alpha * watermark[:, :, c]
        )

    # 텍스트 워터마크 추가 (옵션)
    if text:
        font_scale = 1
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (cv_img.shape[1] - text_size[0]) // 2
        text_y = cv_img.shape[0] - 20
        cv2.putText(cv_img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)

    # 다시 PIL 이미지로 변환
    img_with_watermark = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    return img_with_watermark


@app.route('/')
def index():
    return render_template_string(template)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    watermark_text = request.form.get('watermarkText')

    # 파일을 임시로 저장하고 처리
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    img_with_watermark, img_id, img_hash = upload_image(file_path, watermark_text)
    if img_with_watermark is None:
        return 'Error processing image', 500

    # 이미지 저장
    output_buffer = io.BytesIO()
    img_with_watermark.save(output_buffer, format='PNG')
    output_buffer.seek(0)

    # 파일 삭제 (임시 파일 정리)
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e.strerror}")

    response = send_file(output_buffer, mimetype='image/png')
    response.headers['image-id'] = img_id
    response.headers['image-hash'] = img_hash
    response.headers['X-Image-ID'] = img_id
    response.headers['X-Image-Hash'] = img_hash
    response.headers['Content-Type'] = 'application/json'
    return jsonify({'image_id': img_id, 'image_hash': img_hash})


@app.after_request
def after_request(response):
    if 'X-Image-ID' in response.headers and 'X-Image-Hash' in response.headers:
        response.direct_passthrough = False
        script = f'''
        <script>
          document.getElementById('progressBar').style.width = '100%';
          document.getElementById('progressBar').classList.remove('progress-bar-animated');
          document.getElementById('progressBar').classList.add('bg-success');
          document.getElementById('progress').style.display = 'none';
          document.getElementById('result').style.display = 'block';
          document.getElementById('imageId').innerText = '{response.headers.get('X-Image-ID')}';
          document.getElementById('imageHash').innerText = '{response.headers.get('X-Image-Hash')}';
        </script>
        '''
        response.set_data(response.get_data() + script.encode('utf-8'))
        response.mimetype = "text/html"
    return response


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, host='0.0.0.0', port=5000)