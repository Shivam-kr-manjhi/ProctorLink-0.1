import cv2
import numpy as np
def count_faces(img_binary):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load an image
    # image_path = 'download.jpeg'  # Replace with your image path
    nparr = np.frombuffer(img_binary, np.uint8)

    # Decode NumPy array into an OpenCV image (cv2.imread style)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # image = cv2.imread(image_path)

    if image is None:
        print("Could not read the image. Please check the file path.")
    else:
        # Convert the image to grayscale (required for face detection)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Print the number of faces detected
        # print(f'Number of faces detected: {len(faces)}')
        return len(faces)

        # # Draw rectangles around the faces
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)


def compare_images(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # Check if images are loaded successfully
    if img1 is None or img2 is None:
        print("Error: Could not read the images.")
        return

    # Compare images
    if img1.shape == img2.shape and (img1 == img2).all():
        print("Images are identical.")
    else:
        print("Images are not identical.")

