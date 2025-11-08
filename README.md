
# 🖐️ Hand Gesture Controlled Virtual Mouse

This project enables control of the mouse using **hand gestures** through a webcam. It uses **MediaPipe** for hand tracking, **OpenCV** for video capture and display, and **PyAutoGUI** and **Pynput** to perform mouse actions such as movement, clicks, scrolls, drag, and screenshots.

---

## 📹 Features

* 🖱️ **Mouse Movement** – Move cursor with index finger.
* 👆 **Left Click** – Gesture-based detection.
* 👉 **Right Click** – Alternate finger gesture.
* 🖱️🖱️ **Double Click** – Custom pose-based detection.
* 📸 **Screenshot** – Open hand followed by fist gesture.
* 🔃 **Scroll Up/Down** – Controlled via specific finger angles.
* ✋ **Drag Mode** – Thumb and index finger close together initiates drag.

---

## 🛠️ Technologies Used

* **Python 3**
* **OpenCV**
* **MediaPipe**
* **PyAutoGUI**
* **Pynput**
* **NumPy**

---

## 📂 Project Structure

```
virtual-mouse/
│
├── virtual_mouse.py           # Main Python script
├── README.md                  # Project documentation
├── screenshots/               # Saved screenshots will be stored here
```

---

## 💻 Requirements

* Python 3.7+
* Webcam (Built-in or USB)
* Libraries:

  * `opencv-python`
  * `mediapipe`
  * `pyautogui`
  * `pynput`
  * `numpy`

### ✅ Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui pynput numpy
```

---

## ▶️ How to Run

```bash
python virtual_mouse.py
```

* Press **`q`** to quit the application.
* Make sure your **webcam is active** and **hand is visible in frame**.

---

## 🧠 Gesture Overview

| Gesture                          | Action                |
| -------------------------------- | --------------------- |
| Index finger open                | Move Mouse            |
| Thumb + Index angle              | Left Click            |
| Middle finger folded             | Right Click           |
| Three fingers folded + thumb out | Double Click (Custom) |
| Thumb + Index very close         | Drag                  |
| All fingers stretched            | Hand Open             |
| All fingers closed (after open)  | Take Screenshot       |
| Fingers straight (index/middle)  | Scroll Up             |
| All fingers bent                 | Scroll Down           |

---

## 💾 Screenshot Saving

* Screenshots are saved automatically on gesture detection.
* Default directory:

  ```
  C:\Users\Arun E\OneDrive\Desktop\virtulmouse screenshoot
  ```

---

## 🧪 Troubleshooting

* Make sure your hand is well-lit and clearly visible to the webcam.
* Use gestures in front of the webcam steadily.
* If mouse movement is jerky, adjust the `smoothening` factor in code.
* Ensure your screen resolution is detected correctly using `pyautogui.size()`.

---


## 🙌 Acknowledgements

* [MediaPipe by Google](https://mediapipe.dev/)
* [OpenCV](https://opencv.org/)
* [PyAutoGUI](https://pyautogui.readthedocs.io/)
* [Pynput](https://pynput.readthedocs.io/en/latest/)
