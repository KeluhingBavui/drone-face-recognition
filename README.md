# Face Recognition and Tracking Using Tello Drone

This is a simple implementation of face recognition on Tello drone's camera based on HAAR Cascade using Python and openCV.

## How to start

To initialize the drone and get it running, simply clone the repository and download the requirements in your environment.

```bash
pip install -r requirements.txt
```

Then, connect to your drone's wifi and run:
```bash
python FaceTracking.py
```

The drone should take off after running the file and initialize a window on your computer that show's the camera feed.

## For testing purposes
- To test the drone connection from the code, run
```bash
python basicMovements.py
```
- To test just the facial recognition features on your webcam, run
```bash
python FaceRecognition.py
```