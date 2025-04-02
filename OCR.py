import cv2  # process those images
import pytesseract  # no dyslexia anymore
import re  # Kakyoin can't comprehent stopped time - if you dont get it, dont sweat it
import Bilanzklassen # don't forget the class file :3

# this was fun, so I did it myself, no cheating this time (stack overflow is fair game) :O
class Bilanz_OCR:
    def __init__(self, image_path):
        self.image_path = image_path
        self.bilanz = Bilanzklassen.Bilanz()
    
    def preprocess_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)  # greyscale cause less information flooding
        _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # >150=white, <=150=black, true binary makes OCR smoother, thresh
        cv2.imwrite("processed_image.png", thresh)  # for testing
        return thresh
    
    def extract_text(self):
        processed_img = self.preprocess_image()

        custom_config = "--oem 3 "  # LSTM OCR Engine mit semi-automatischem Layout-Parsing (schlechter
        text = pytesseract.image_to_string(processed_img, lang="deu",config=custom_config)  # <- dark magic
        return text
    
    def get_clean_number(self,x: str)->float:
        is_german = False

        for i in range(len(x)-1, 0, -1):
            if x[i] == ",":
                is_german = True
                break
            elif x[i] == ".":
                break

        if is_german:
            x_clean = x.replace(".", "").replace(",", ".")
            return float(x_clean)
        else:
            return float(x.replace(",", ""))
        
    def parse_text(self, text):
        active_category= ''
        for line in text.split("\n"):
            scan_category = re.findall(r"Anlagevermögen|Umlaufvermögen|Eigenkapital|Langfristiges Fremdkapital|Kurzfristiges Fremdkapital", line)  # don't ask me if there are easier ways, stack overflow gave me this
            if scan_category:
                active_category = scan_category[0]
                continue

            scan_money = re.findall(r"\s+(\d*[.,]*\d*[.,]*\d*[.,]*\d*[.,]*\d*[.,]*\d*[.,]*\d+[.,]\d+)", line)  # don't ask me if there are easier ways, stack overflow gave me this
            print(scan_money)
            if scan_money:
                if type(self.bilanz.aktiva[active_category]) == dict:
                    self.bilanz.aktiva[active_category] = 0
                self.bilanz.aktiva[active_category] += self.get_clean_number(scan_money[0])
                continue
             
    def computer_use_reading_comprehention(self):
        text = self.extract_text()
        self.parse_text(text)
        print(text)  # for testing
        self.bilanz.show()

if __name__ == "__main__":
    ocr = Bilanz_OCR("bilanz_scan.png")
    ocr.computer_use_reading_comprehention()