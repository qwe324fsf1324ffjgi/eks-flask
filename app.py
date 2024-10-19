from flask import Flask, render_template, Response
import cv2
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained MobileNetSSD model and the class names
net = cv2.dnn.readNetFromCaffe('model/deploy.prototxt', 'model/mobilenet_iter_73000.caffemodel')

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle",
           "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse",
           "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Video stream generator function
def gen_frames():
    cap = cv2.VideoCapture(0)  # Use your webcam
    while True:
        success, frame = cap.read()  # Read the frame from the camera
        if not success:
            break

        # Convert the frame to blob for the model
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        (h, w) = frame.shape[:2]

        # Loop through the detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:  # Confidence threshold
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box and label on the frame
                label = f"{CLASSES[idx]}: {confidence * 100:.2f}%"
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define a route to the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
