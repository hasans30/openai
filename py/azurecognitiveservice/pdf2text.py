import time
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

computer_vision_endpoint=os.environ["COMPUTER_VISION_ENDPOINT"]
computer_vision_key=os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]

client = ComputerVisionClient(
                      computer_vision_endpoint, 
                      CognitiveServicesCredentials(computer_vision_key)
                    )


def pdf_to_text():
  filepath = open('printed_pdf.pdf','rb')

  response = client.read_in_stream(filepath, raw=True)

  filepath.close()

  operation_location = response.headers["Operation-Location"]
  operation_id = operation_location.split("/")[-1]

  while True:
    result = client.get_read_result(operation_id)
    if result.status.lower () not in ['notstarted', 'running']:
      break
    time.sleep(10)
  return result

result = pdf_to_text()

if result.status == OperationStatusCodes.succeeded:
  for readResult in result.analyze_result.read_results:
    for line in readResult.lines:
      print(line.text)
      print(line.bounding_box)