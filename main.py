import os
import argparse
import cv2
from yolo_detector import YOLODetector
from ocr_parser import OCRParser
from aggregator import Aggregator
from comparer import Comparer

IMG_ROOT = "images"

def parse_req_items(args_list):

    req = {}
    i = 0

    while i < len(args_list):

        if not args_list[i].isdigit():

            raise ValueError(f"need quantity at position {i}")

        qty = int(args_list[i])

        i += 1

        item_words = []

        while i < len(args_list) and not args_list[i].isdigit():

            item_words.append(args_list[i])
            i += 1

        item_name = " ".join(item_words).lower().rstrip('s')

        if not item_name:

            raise ValueError(f"no item name found")

        req[item_name] = qty

    return req

def load_images():

    stores = {}

    if not os.path.exists(IMG_ROOT):

        return stores

    for store_name in os.listdir(IMG_ROOT):

        store_path = os.path.join(IMG_ROOT, store_name)

        if not os.path.isdir(store_path):
            continue

        img_files = [os.path.join(store_path, img)
                     for img in os.listdir(store_path)
                     if img.lower().endswith((".jpg", ".jpeg", ".png"))]

        if img_files:

            stores[store_name] = img_files

    return stores

def main():

    parser = argparse.ArgumentParser(description="Grocery price checker")

    parser.add_argument("--items", nargs="+", required=True, help="list of quantity and items")
    args = parser.parse_args()
    
    req_items = parse_req_items(args.items)

    detector = YOLODetector(model_path="yolo12x.pt")
    ocr = OCRParser()

    aggregator = Aggregator()
    comparer = Comparer()
   

    store_imgs = load_images()

    if not store_imgs:

        print("no store images found")
        return

    for store_name, img_list in store_imgs.items():

        for img_path in img_list:

            img = cv2.imread(img_path)

            if img is None:

                continue
                
            prices_with_positions = ocr.extract_prices_with_positions(img)

            detections, _ = detector.detect_items(img)
            
            for det in detections:

                cls_name = det['class']
                bbox = det['bbox']
                
                matching_target = None

                for target_item in req_items.keys():

                    if (target_item in cls_name or 
                        cls_name in target_item or
                        target_item.rstrip('s') == cls_name.rstrip('s')):

                        matching_target = target_item

                        break
                
                if not matching_target:

                    continue
                
                bbox_center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)

                price = ocr.find_closest_price(prices_with_positions, bbox_center)
                
                if price is not None:

                    aggregator.add(store_name, matching_target, price)

    store_data = aggregator.get()

    store, total = comparer.find_cheapest(store_data, req_items)
    
    if store:

        print(f"cheapest store: {store}")
        print(f"total cost: ${total:.2f}")

    else:

        print("no store has all requested items")

if __name__ == "__main__":
    main()
