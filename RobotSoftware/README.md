# Robot Software

Control software for the camp robot, used in the **Edge Detection** project track to run the method on a live video stream. The system uses a **client/server architecture** over **TCP/JSON** (control commands) and **UDP** (webcam stream).

> [!NOTE]
> The control center loads a PyTorch CNN whose model path is hardcoded to a Windows path — update it before use. Settings are read from [`system/settings.json`](./system/settings.json).

## 📁 Structure

### `system/` — robot control system
| File | Purpose |
|---|---|
| `controlCenter.py` | tkinter GUI control center: receives JPEG frames over UDP, sends commands over TCP, runs a CNN for arrow-direction classification |
| `robot_client.py` | Client running on the robot |
| `control.py` | Sends motor/servo/buzzer/dot-matrix commands as JSON over TCP |
| `UDPwebcam.py` | Streams webcam JPEG frames over UDP |
| `motor.py`, `servo.py`, `sensor.py`, `buzzer.py`, `dot_matrix.py`, `speech.py` | Hardware peripheral drivers |
| `settings.json`, `songs.json`, `dot_matricies.json`, `speech.txt` | Configuration and assets |

### `UDP_chat/` — minimal UDP example
A small client/server chat pair (`client.py`, `server.py`) illustrating UDP communication.

### `video/` — video and webcam experiments
Standalone scripts for camera capture, video stabilization, `cv2.goodFeaturesToTrack`, PIL/UDP frame transfer, servo control, and Flask-based streaming, plus sample `.avi` clips used during development.

## ▶️ Running

Start the control center on the operator's machine and the client on the robot:

```bash
python system/controlCenter.py   # operator GUI
python system/robot_client.py    # on the robot
```
