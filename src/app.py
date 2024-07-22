from flask import Flask, render_template, Response, stream_with_context
import json
import time
from tracker import FaceTracker

app = Flask(__name__)
face_tracker = FaceTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(face_tracker.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/coordinate_stream')
def coordinate_stream():
    def generate():
        while True:
            # Get the latest coordinates from your face_tracker
            # This is just an example, you'll need to implement this method
            coords = face_tracker.get_latest_coordinates()
            data = json.dumps(coords)
            yield f"data: {data}\n\n"
            time.sleep(0.1)  # Adjust the delay as needed

    return Response(stream_with_context(generate()),
                    mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)