from contextlib import nullcontext
from urllib import response
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from models.inception_resnet_v1 import InceptionResnetV1
from urllib.request import urlopen
from PIL import Image
import json
import numpy as np
import build_custom_model
import pickle 
import time
import os 
import base64
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
# from boto3.dynamodb.conditions import Key

credentials = {
    "accessKeyId": 'AKIASLJLX3PWWWLBHDGS',
    "secretAccessKey": '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'
}

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def face_recognition_handler(event, context):
     print('this is even: ', event)
     labels_dir = "./checkpoint/labels.json"
     model_path = "./checkpoint/model_vggface2_best.pth"

     
     # read labels
     with open(labels_dir) as f:
          labels = json.load(f)
     print(f"labels: {labels}")


     device = torch.device('cpu')
     model = build_custom_model.build_model(len(labels)).to(device)
     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
     model.eval()
     print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")

     #extract image from url:
     # print(event)
     image = json.loads(event.get("Records")[0].get('body'))['responsePayload']['encoded']
     name = json.loads(event.get("Records")[0].get('body'))['responsePayload']['name']

     fh = open("/tmp/image01.jpg", "wb+")
     fh.write(base64.b64decode(image))
     fh.close()

     img_path = '/tmp/image01.jpg'
     img = Image.open(img_path)
     img_tensor = transforms.ToTensor()(img).unsqueeze_(0).to(device)
     outputs = model(img_tensor)
     _, predicted = torch.max(outputs.data, 1)
     result = labels[np.array(predicted.cpu())[0]]
     # print(predicted.data, result)
     os.system('rm -rf /tmp/image*')

     img_name = img_path.split("/")[-1]
     img_and_result = f"({img_name}, {result})"

     print(f"Image and its recognition result is: {img_and_result}")

     if result == 'vansh_patel':
          result = 2
     elif result == 'hameeda':
          result = 3
     else:
          result = 1

     sqs_client = boto3.client("sqs", region_name="us-east-1")
     
     # client_dynamodb = boto3.resource('dynamodb',aws_access_key_id=credentials['accessKeyId'], aws_secret_access_key=credentials['secretAccessKey'], region_name="us-east-1")
     # table = client_dynamodb.Table('AcademicData')
     # response = table.query(KeyConditionExpression=Key(result))

     # data = response['Items']
     # print("this is data: ", data)

     # final_result = []
     # for each in data:
     #      if(each.get("id") == result):
     #           final_result.append(each)


     # print("Response from db: ", final_result[0])

     try:
        response = sqs_client.send_message(QueueUrl="https://sqs.us-east-1.amazonaws.com/161689885677/sqs-2",
                                           MessageAttributes={},
          MessageBody=json.dumps({'final_result': result, 'name': name}, default=default)
     )
     except ClientError as e:
          print(e)

     return {'final_result': result, 'name': name}