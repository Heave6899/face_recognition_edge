import boto3
import botocore
import pickle
import time
import os
import subprocess
input_bucket = "inputvideoscc"
output_bucket = "outputvideoscc"
credentials = {
    "accessKeyId": '',
    "secretAccessKey": ''
}

# Function to read the 'encoding' file
def open_encoding(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data

def face_recognition_handler(event, context):
    print(os.getcwd())
    # print(subprocess.check_output(['python', 'eval_face_recognition.py','--img_path','./IMG_20220417_163147.jpg']))
    print('event',event['Records'][0]['s3']['object']['key'], event['Records'][0]['s3']['bucket']['name'])	
    # We have added a 1 second delay so you can see the time remaining in get_remaining_time_in_millis.
    time.sleep(1) 
    print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())
    
    client = boto3.client('s3',aws_access_key_id=credentials['accessKeyId'], aws_secret_access_key=credentials['secretAccessKey'])
    client.download_file(event['Records'][0]['s3']['bucket']['name'], event['Records'][0]['s3']['object']['key'], '/tmp/' + event['Records'][0]['s3']['object']['key'])
    s = subprocess.check_output(['ffprobe', '/tmp/' + event['Records'][0]['s3']['object']['key'] ,'-count_frames', '-show_entries', 'stream=nb_read_frames,avg_frame_rate,r_frame_rate']).decode('utf-8')
    rates = [i.split('=') for i in s.split(  )]
    print(rates)
    duration = int(rates[3][1])/int(rates[2][1].split('/')[0])
    frames = int(rates[3][1])
    print(duration,frames)
    # NOW THE LOGIC FOR EXTRACTING FRAMES
    result = extract_frames(event['Records'][0]['s3']['object']['key'], duration, frames)
    return {'statusCode':200,'videoName':event['Records'][0]['s3']['object']['key'], 'imageResult': result}

def extract_frames(file_name, duration, frames):
    print(file_name, duration, frames)
    print(subprocess.check_output(['ffmpeg','-i', '/tmp/' + file_name,'-r','2','/tmp/out%03d.jpg']))
    result = subprocess.check_output(['python', 'eval_face_recognition.py','--img_path','/tmp/out001.jpg']).decode('utf-8')
    print(result)
    print(subprocess.check_output(['rm','-rf','/tmp/out*']))
    print(subprocess.check_output(['rm','-rf','/tmp/video_*']))
    return result