from ultralytics import YOLO
import cv2

class YOLODetector:

    def __init__(self, model_path=r"C:\Users\jjtwt\Downloads\CSC245_final_project\yolo12x.pt"):

  
        self.model = YOLO(model_path, verbose = False)

    def detect_items(self, img):

        if isinstance(img, str):

            img = cv2.imread(img)

        results = self.model.predict(img, conf=0.75)

        det = []

        for r in results:

            for box in r.boxes:

                cls_id = int(box.cls[0])

                cls_name = self.model.model.names.get(cls_id, "unknown").lower()

                xyxy = box.xyxy[0].cpu().numpy().astype(int)

                det.append({
                    "class": cls_name,
                    "bbox": xyxy
                })

        return det, img
