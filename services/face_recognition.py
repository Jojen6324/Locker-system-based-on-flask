import os
import pickle
import cv2
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognitionService:
    def __init__(self, face_db_path, features_path):
        self.face_db_path = face_db_path
        self.features_path = features_path
        self.mtcnn = MTCNN(keep_all=False)
        self.resnet = InceptionResnetV1(pretrained="vggface2").eval()
        
    def extract_face_embedding(self, image_path):
        image = Image.open(image_path)
        face = self.mtcnn(image)
        if face is None:
            print(f"⚠️ 未检测到人脸: {image_path}")
            return None
        embedding = self.resnet(face.unsqueeze(0))
        return embedding.detach().numpy()
    
    def build_face_database(self):
        face_embeddings = {}
        for filename in os.listdir(self.face_db_path):
            image_path = os.path.join(self.face_db_path, filename)
            token = filename.rsplit(".", 1)[0]
            try:
                embedding = self.extract_face_embedding(image_path)
                if embedding is not None:
                    face_embeddings[token] = embedding
            except Exception as e:
                print(f"处理 {filename} 失败: {e}")
        with open(self.features_path, "wb") as f:
            pickle.dump(face_embeddings, f)
        print(f"训练完成！数据库包含 {len(face_embeddings)} 个 token")
    
    def recognize_face(self, image_path):
        with open(self.features_path, "rb") as f:
            face_embeddings = pickle.load(f)
        input_embedding = self.extract_face_embedding(image_path)
        if input_embedding is None:
            return None
        best_match = None
        best_score = -1
        for token, emb in face_embeddings.items():
            score = cosine_similarity(input_embedding, emb)
            if score > best_score:
                best_match = token
                best_score = score
        if best_score > 0.6:
            print(best_score, best_match)
            return best_match
        else:
            return None
    
    def add_or_update_face(self, image_path):
        token = os.path.basename(image_path).rsplit(".", 1)[0]
        if os.path.exists(self.features_path):
            with open(self.features_path, "rb") as f:
                face_embeddings = pickle.load(f)
        else:
            face_embeddings = {}
        embedding = self.extract_face_embedding(image_path)
        if embedding is None:
            return
        if token in face_embeddings:
            print(f"更新 {token} 的人脸数据")
        else:
            print(f"添加 {token} 到数据库")
        face_embeddings[token] = embedding
        with open(self.features_path, "wb") as f:
            pickle.dump(face_embeddings, f)
        print(f"数据库更新完成！")
    
    def is_frontal_face(self, face_img):
        # Implement frontal face detection 
        # This function was referenced in the original code but not defined
        # A simple implementation could use facial landmarks or pose estimation
        return True  # Placeholder implementation
    
    def detect_and_crop_face(self, image_path, token):
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes, _ = self.mtcnn.detect(img)
            
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.astype(int)
                    expand_ratio = 0.3
                    width, height = x2 - x1, y2 - y1
                    x1, y1 = max(0, x1 - int(width * expand_ratio)), max(0, y1 - int(height * expand_ratio))
                    x2, y2 = min(img.shape[1], x2 + int(width * expand_ratio)), min(img.shape[0], y2 + int(height * expand_ratio))
                    face = img[y1:y2, x1:x2]
                    
                    if self.is_frontal_face(face):
                        cropped_filename = f"{token}.jpeg"
                        cropped_filepath = os.path.join(self.face_db_path, cropped_filename)
                        Image.fromarray(face).convert('RGB').save(cropped_filepath, format='JPEG')
                        self.add_or_update_face(cropped_filepath)
                        return True, cropped_filepath
            
            return False, None
        except Exception as e:
            print(f"Error processing image: {e}")
            return False, None