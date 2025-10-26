\# Air Canvas - Hand Tracking Drawing App



Draw in the air using your hand gestures! This Python application uses computer vision to track your hand movements and create drawings in real-time with multiple colors.



!\[Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)

!\[License](https://img.shields.io/badge/license-MIT-green)



\## ✨ Features



\- 🎨 \*\*15 vibrant colors\*\* to choose from + eraser

\- 👆 \*\*Draw with your index finger\*\* - natural and intuitive

\- 🎨 \*\*Color picker mode\*\* - hold a fist to open/close

\- 🖐️ \*\*Toggle drawing\*\* - extend thumb to pause/resume

\- 💾 \*\*Save your artwork\*\* as PNG files

\- 🧹 \*\*Clear canvas\*\* with a single key press

\- 🪞 \*\*Mirror mode\*\* for natural drawing experience

\- 📺 \*\*Full HD\*\* 1920x1080 resolution



\## 🎮 How to Use



\### Drawing Mode (Default)

\- \*\*Point with INDEX FINGER\*\* → Start drawing

\- \*\*Move your finger\*\* → Create lines and shapes

\- The drawing follows your fingertip naturally!



\### Color Picker Mode

1\. \*\*Make a FIST and hold for 0.5 seconds\*\* → Opens color picker at top

2\. \*\*Point at any color\*\* with your index finger → Selects that color

3\. \*\*Make a FIST again and hold\*\* → Closes picker and returns to drawing



\### Toggle Drawing On/Off

\- \*\*Extend THUMB fully and hold for 0.5 seconds\*\* → Toggles drawing mode

\- Useful when you want to move your hand without drawing



\### Keyboard Controls

\- \*\*C\*\* - Clear the canvas

\- \*\*S\*\* - Save your drawing as PNG

\- \*\*Q\*\* - Quit the application



\## 🎨 Available Colors



\*\*Row 1:\*\* Blue, Orange, Green, Spring Green, Cyan, Pink, Magenta, Purple  

\*\*Row 2:\*\* Red, Olive, Teal, Yellow, White, Gray, Black (Eraser)



\## 🚀 Installation



\### Prerequisites



\- \*\*Python 3.8, 3.9, or 3.10\*\* (recommended: 3.9)

\- Webcam

\- Windows/Mac/Linux



\### Step-by-Step Setup



1\. \*\*Clone this repository:\*\*

```bash

git clone https://github.com/yourusername/air-canvas.git

cd air-canvas

```



2\. \*\*Create a virtual environment (recommended):\*\*

```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# Mac/Linux

python3 -m venv venv

source venv/bin/activate

```



3\. \*\*Install required packages:\*\*

```bash

pip install -r requirements.txt

```



4\. \*\*Run the application:\*\*

```bash

python air\_drawing.py

```



\## 📦 Dependencies



\- `opencv-python` - Camera input and image processing

\- `mediapipe` - Hand tracking and landmark detection

\- `numpy` - Array operations



All dependencies are listed in `requirements.txt`



\## 🎯 Tips for Best Results



\- ✅ \*\*Good lighting\*\* - Ensure your hand is well-lit

\- ✅ \*\*Clear background\*\* - Works best against plain backgrounds

\- ✅ \*\*Distance\*\* - Position yourself 1-2 feet from camera

\- ✅ \*\*Steady movements\*\* - Move at moderate speed for smooth lines

\- ✅ \*\*Keep hand visible\*\* - Ensure your full hand is in frame



\## 🛠️ Troubleshooting



\### Camera not opening?

\- Make sure no other application is using your webcam

\- Try changing the camera index in code: `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)`



\### Hand detection not working?

\- Check lighting conditions

\- Ensure good contrast between hand and background

\- Keep your full hand visible in the frame



\### Low FPS or lag?

\- Close other applications

\- Try reducing resolution in the code (change 1920x1080 to 1280x720)



\### Colors not installing correctly?

Make sure you're using Python 3.8-3.10, as MediaPipe has compatibility issues with Python 3.11+



\## 📁 Project Structure



```

air-canvas/

│

├── air\_drawing.py       # Main application

├── requirements.txt     # Python dependencies

├── README.md           # This file

└── drawings/           # Your saved drawings (created automatically)

```



\## 🤝 Contributing



Contributions are welcome! Feel free to:

\- Report bugs

\- Suggest new features

\- Submit pull requests



\## 📄 License



This project is licensed under the MIT License - feel free to use and modify as you wish!



\## 🙏 Acknowledgments



\- Built with \[MediaPipe](https://google.github.io/mediapipe/) by Google

\- Uses \[OpenCV](https://opencv.org/) for computer vision



\## 📧 Contact



Have questions or suggestions? Open an issue on GitHub!



---



\*\*Enjoy drawing in the air! 🎨✨\*\*

