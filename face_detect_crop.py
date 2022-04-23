import cv2
import glob
import os
image_list = []
for filename in glob.glob('d/*'):
# Read the input image
    print(os.path.basename(filename))
    img = cv2.imread(filename)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        faces = img[y:y + h, x:x + w]
        cv2.imshow("face",faces)
        cv2.imwrite('dd/' + os.path.basename(filename), faces)

    # Display the output
    cv2.imshow('img', img)
    cv2.waitKey()
