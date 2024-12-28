import time
import cv2 as cv

def initializeWebcam() -> object:
    cam = cv.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cam.isOpened():
        print("Error: Could not open webcam.")
        exit()
    
    return (cam)
    
def takePicture(cam: object, filename: str) -> None:
    # Capture a frame
    ret, frame = cam.read()

    # If frame is captured successfully, save it
    if not ret:
        print("Error: Failed to capture frame.")

    cv.imwrite(filename, frame)
    print(f"Image captured and saved as {filename}")


def captureSeries(cam: object, album_path: str, photos: int, delay: int) -> None:
    for i in range(0, photos):
        image_num: int = f"{i + 1:03d}"
        filename = f"{album_path}image{image_num}.jpg"
        print(filename)
        takePicture(cam, filename)
        time.sleep(delay)

def closeCam(cam: object) -> None:
    cam.release()

def main() -> None:
    cam = initializeWebcam()
    album_path = "tests/pictures/"
    photos = 3
    delay = 1

    # takePicture(cam, "tests/pictures/test.jpg")

    captureSeries(cam, album_path, photos, delay)
    closeCam(cam)

if __name__ == '__main__':
    main()
