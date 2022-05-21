# face_recognition_edge

This system uses Raspberry Pi 3B+ and AWS Lambda, EC2, SQS, ECR and DynamoDB as its core components.

### Steps to reproduce the project:

1.First setup Raspberry Pi, which includes installing OS and flashing it into a disk and attaching the disk to the hardware.
2.Boot into Pi, copy the file provided in the mainProject folder, server.py, run the python script using Thonny to simultaneously get console output in a good UI.
3.Before running the server.py script, setup the internal services required to process the image end-to-end, this includes setting up an AWS S3 bucket, 3 AWS SQS queues(1,2,3).
4.Create 3 AWS Lambda functions such that 1st function will contain the code, firstLambda.py, 2nd function will be deployed with the help of a dockerFile provided, the docker file required eval_face_recognition.py and other related files. The 3rd function will contain the code, thirdLambda.py.
5.For the secondLambda function, first build the docker image using DockerFile, then push this docker image to a private ECR repository. Use this pushed image to launch a AWS Lambda function and deploy it as a cloud image.
6.Connect all the components using appropriate URLs.
7.Once done, all steps above, we are ready to test live images, just run the script server.py on Raspberry Pi and check the response latency.
