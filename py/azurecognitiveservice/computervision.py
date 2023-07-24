from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os
import time

computer_vision_endpoint=os.environ["COMPUTER_VISION_ENDPOINT"]
computer_vision_key=os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]

client = ComputerVisionClient(
                computer_vision_endpoint, 
                CognitiveServicesCredentials(computer_vision_key)
            )

image_url = "https://cdn.pixabay.com/photo/2016/04/07/19/08/motivational-1314505__340.jpg"

response = client.read(image_url,  raw=True)

def get_coordinates(bounding_box):
    return ((bounding_box[-2], bounding_box[-1]), (bounding_box[-6], bounding_box[-5]))

operation_location = response.headers["Operation-Location"]

operation_id = operation_location.split("/")[-1]

while True:
    result = client.get_read_result(operation_id)
    if result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

if result.status == OperationStatusCodes.succeeded:
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(img)

    for ocr_text in result.analyze_result.read_results:
        for line in ocr_text.lines:
            print(line.text)
            print(line.bounding_box)
            # draw.rectangle(get_coordinates(line.bounding_box), outline='red')

    img.save("image.png")
    