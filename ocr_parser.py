import easyocr
import re

class OCRParser:

    def __init__(self):

        self.reader = easyocr.Reader(['en'])
    
    def extract_prices_with_positions(self, image):

        results = self.reader.readtext(image, detail=1)
        prices = []
        
        for (bbox, text, confidence) in results:

            price = self.extract_price(text)

            if price is not None:

                x_center = sum(point[0] for point in bbox) / 4
                y_center = sum(point[1] for point in bbox) / 4

                prices.append((price, x_center, y_center))
        
        return prices
    
    def extract_price(self, text):

        price_match = re.search(r'\$?(\d+\.\d{2})', text)

        if price_match:

            return float(price_match.group(1))

        return None
    
    def find_closest_price(self, prices, bbox_center):

        if not prices:

            return None
        
        item_x, item_y = bbox_center
        closest_price = None
        min_distance = float('inf')
        
        for price, price_x, price_y in prices:

            distance = ((price_x - item_x) ** 2 + (price_y - item_y) ** 2) ** 0.5

            if distance < min_distance:

                min_distance = distance
                closest_price = price
        
        return closest_price
