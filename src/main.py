from android.permissions import request_permissions, Permission
import cv2
from jnius import autoclass, PythonJavaClass, java_method
from jnius.jnius import JavaException
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
import numpy as np
import time

Config.set('kivy', 'camera', 'opencv')

request_permissions([
    Permission.CAMERA,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.READ_EXTERNAL_STORAGE
])

Bitmap = autoclass('android.graphics.Bitmap')
Bitmap_Config = autoclass('android.graphics.Bitmap$Config')
ByteBuffer = autoclass('java.nio.ByteBuffer')
FaceMesh = autoclass('com.google.mediapipe.solutions.facemesh.FaceMesh')
FaceMeshOptions = autoclass('com.google.mediapipe.solutions.facemesh.FaceMeshOptions')
FaceMeshResult = autoclass('com.google.mediapipe.solutions.facemesh.FaceMeshResult')

CameraInfo = autoclass('android.hardware.Camera$CameraInfo')
CAMERA_INDEX = {'front': CameraInfo.CAMERA_FACING_FRONT, 'back': CameraInfo.CAMERA_FACING_BACK}
Builder.load_file("myapplayout.kv")

class FaceMeshResultListener(PythonJavaClass):
    __javainterfaces__ = ['com/google/mediapipe/solutioncore/ResultListener']
    __javacontext__ = 'app'  # or 'system'

    @java_method('(Ljava/lang/Object;)V')
    def run(self, result):
        App.get_running_app().camera_widget.on_face_mesh_result(result)

class AndroidCamera(Camera):
    resolution = (640, 480)
    index = CAMERA_INDEX['front']
    counter = 0

    def __init__(self, **kwargs):
        super(AndroidCamera, self).__init__(**kwargs)
        self._camera.start()
        FaceMeshOptionsBuilder = FaceMeshOptions.builder()
        FaceMeshOptionsBuilder.setRunOnGpu(True)
        try:
            self.faceMesh = FaceMesh(App.get_running_app()._activity, FaceMeshOptionsBuilder.build())
        except JavaException:
            # If the GPU is not available, use the CPU.
            FaceMeshOptionsBuilder.setRunOnGpu(False)
            self.faceMesh = FaceMesh(App.get_running_app()._activity, FaceMeshOptionsBuilder.build())

        self.listener = FaceMeshResultListener()
        self.faceMesh.setResultListener(self.listener)
        self.last_landmarks = []

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return

        super(AndroidCamera, self).on_tex(*l)
        frame = self.frame_from_buf()

        # Convert frame (OpenCV BGR numpy) → Bitmap
        self.send_frame_to_facemesh(frame)

        # Draw the last known mesh landmarks (updated in listener)
        frame = self.draw_mesh_overlay(frame)
        self.frame_to_screen(frame)

    def draw_mesh_overlay(self, frame):
        # Ensure frame is contiguous and 3-channel BGR
        if frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        frame = np.ascontiguousarray(frame, dtype=np.uint8)

        # Draw landmarks safely
        for (x, y) in self.last_landmarks:
            x = int(min(max(x, 0), frame.shape[1]-1))
            y = int(min(max(y, 0), frame.shape[0]-1))
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        return frame

    def frame_from_buf(self):
        w, h = self.resolution
        buffer = bytearray(self._camera._buffer)
        frame = np.frombuffer(buffer, dtype=np.uint8).reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)  # YUV2BGR_NV21

        # Rotate to proper orientation
        frame_rotated = np.rot90(frame_bgr, 3)

        # Flip front camera to mirror (optional)
        if (self.index == 1):  # assuming 1 = front camera
            frame_rotated = np.flip(frame_rotated, 1)

        return frame_rotated

    def frame_to_screen(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame_rgb, str(self.counter), (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        self.counter += 1

        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tobytes()

        # Create texture manually if it doesn't exist or has wrong size/format
        if not self.texture or self.texture.size != (frame.shape[1], frame.shape[0]):
            self.texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

    def on_face_mesh_result(self, result):
        if (counter%100==0):
            try:
                if result is None:
                    self.last_landmarks = []
                    return

                faces = result.multiFaceLandmarks()
                if ((faces is None) or (faces.size()==0)):
                    self.last_landmarks = []
                    return

                face_landmarks = faces.get(0).getLandmarkList()
                self.last_landmarks = [
                    (int(l.getX() * self.resolution[0]),
                    int(l.getY() * self.resolution[1]))
                    for l in face_landmarks
                ]

                print(f"Detected {len(self.last_landmarks)} landmarks")  # DEBUG

            except Exception as e:
                print("Error parsing landmarks:", e)

    def send_frame_to_facemesh(self, frame):
        try:
            frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            h, w, _ = frame_rgba.shape

            buf = ByteBuffer.allocateDirect(w * h * 4)
            buf.put(frame_rgba.tobytes())

            bitmap = Bitmap.createBitmap(w, h, Bitmap_Config.ARGB_8888)
            buf.rewind()
            bitmap.copyPixelsFromBuffer(buf)

            timestamp = int(time.time() * 1000)  # milliseconds
            self.faceMesh.send(bitmap, timestamp)
        except Exception as e:
            print("send_frame_to_facemesh error:", e)

class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(orientation="vertical", **kwargs)
        # Add camera widget programmatically
        
        self.camera_widget = AndroidCamera(size_hint=(1.0, 1.0))
        self.add_widget(self.camera_widget)

class MyApp(App):
    
    def build(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self._activity = PythonActivity.mActivity
        except Exception as e:
            print("Not running on Android or failed to get activity:", e)
            self._activity = None

        root = MyLayout()
        self.camera_widget = root.camera_widget  # assign reference for listener access
        
        return root

if __name__ == '__main__':
    MyApp().run()
