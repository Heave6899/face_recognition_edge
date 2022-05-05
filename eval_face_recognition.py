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
import argparse
import build_custom_model
import boto3
import botocore
import pickle
import time
import os
import subprocess
input_bucket = "inputvideoscc"
output_bucket = "outputvideoscc"
credentials = {
    "accessKeyId": 'AKIASLJLX3PWWWLBHDGS',
    "secretAccessKey": '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'
}
import ffmpeg

def face_recognition_handler(event, context):
     client = boto3.client('s3',aws_access_key_id=credentials['accessKeyId'], aws_secret_access_key=credentials['secretAccessKey'])
     client.download_file(event['Records'][0]['s3']['bucket']['name'], event['Records'][0]['s3']['object']['key'], '/tmp/' + event['Records'][0]['s3']['object']['key'])
     # parser = argparse.ArgumentParser(description='Evaluate your customized face recognition model')
     # parser.add_argument('--img_path', type=str, default="./data/test_me/val/angelina_jolie/1.png", help='the path of the dataset')
     # args = parser.parse_args()
     # img_path = args.img_path
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

     #extract images from video:
     input = ffmpeg.input('/tmp/'+ event['Records'][0]['s3']['object']['key'])
     ffmpeg.input('/tmp/'+ event['Records'][0]['s3']['object']['key']).filter('scale', 160, -1).output('/tmp/image01.jpg', vframes=1).run()
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


     client_dynamodb = boto3.resource('dynamodb',aws_access_key_id=credentials['accessKeyId'], aws_secret_access_key=credentials['secretAccessKey'], region_name="us-east-1")
     table = client_dynamodb.Table('AcademicData')
     response = table.scan()

     data = response['Items']
     print("this is data: ", data)

     final_result = []
     for each in data:
          if(each.get("id") == result):
               final_result.append(each)


     print("Response from db: ", final_result[0])


     return(final_result[0])