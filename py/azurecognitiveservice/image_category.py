from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

computer_vision_endpoint=os.environ["COMPUTER_VISION_ENDPOINT"]
computer_vision_key=os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]



client = ComputerVisionClient(
                            computer_vision_endpoint, 
                            CognitiveServicesCredentials(computer_vision_key)
                        )

image_url = "https://cdn.pixabay.com/photo/2017/07/24/19/57/tiger-2535888__340.jpg"

image_features = ["categories"]

categorize_results = client.analyze_image(image_url , image_features)

if len(categorize_results.categories) == 0:
    print("No categories detected.")
else:
    print("Categories identified from the image: ")
    for category in categorize_results.categories:
        print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))