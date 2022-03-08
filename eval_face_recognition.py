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


labels_dir = "./checkpoint/labels.json"
model_path = "./checkpoint/model_vggface2_best.pth"
# img_path = './data/test_me/val/kaiqi/1.png'
# img_path = "./data/real_images/train/kaiqi/IMG_7989.png"
img_path = './data/real_images/val/kaiqi/IMG_7996.png'
# img_path = './data/real_images/val/neha/2022-03-05-121938_4.png'
# img_path = './data/real_images/val/yitao/IMG_7984.png'


# read labels
with open(labels_dir) as f:
     labels = json.load(f)
print(f"labels: {labels}")


device = torch.device('cpu')
model = build_custom_model.build_model(len(labels)).to(device)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
model.eval()
print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")

img = Image.open(img_path)
img_tensor = transforms.ToTensor()(img).unsqueeze_(0).to(device)

outputs = model(img_tensor)
_, predicted = torch.max(outputs.data, 1)
result = labels[np.array(predicted.cpu())[0]]
# print(predicted.data, result)

img_name = img_path.split("/")[-1]
img_and_result = f"({img_name}, {result})"
print(f"Image and its recognition result is: {img_and_result}")



