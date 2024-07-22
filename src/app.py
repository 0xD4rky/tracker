from flask import Flask, render_template, Response
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
    
if __name__ == '__main__':
    app.run(debug = True)
    