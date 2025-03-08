from flask import Blueprint, request, jsonify, current_app
import os
from services.face_recognition import FaceRecognitionService
from utils.responses import msgErr, msgSuccess

face_bp = Blueprint('face', __name__)

@face_bp.route('/recognizeFace', methods=['POST'])
def recognize_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "temp", "temp_uploaded.jpg")
    image_file.save(image_path)
    
    face_service = FaceRecognitionService(
        face_bp.config['FACE_DB_PATH'],
        face_bp.config['FEATURES_PATH']
    )
    match_token = face_service.recognize_face(image_path)
    
    if match_token:
        return jsonify(msgSuccess("匹配成功"))
    return jsonify(msgErr("请重试"))

@face_bp.route('/uploadFace', methods=['POST'])
def upload_face():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    
    token = request.headers.get('token')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    
    temp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "temp", f"{token}_temp.jpg")
    image.save(temp_file_path)
    
    face_service = FaceRecognitionService(
        face_bp.config['FACE_DB_PATH'],
        face_bp.config['FEATURES_PATH']
    )
    success, face_path = face_service.detect_and_crop_face(temp_file_path, token)
    
    if success:
        return jsonify(msgSuccess('上传成功')), 200
    else:
        return jsonify(msgErr('未检测到正脸')), 400