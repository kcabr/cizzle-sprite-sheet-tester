# 🎮 Cizzle's Sprite Sheet Tester 🎮

**Bring your sprite sheets to life with this awesome animation tool!**

![Sprite Sheet Animation](https://github.com/user-attachments/assets/39428ea8-0e22-4c88-89f9-f536db639495)

![WhatsApp Image 2025-03-12 at 09 45 49_d7d58f7e](https://github.com/user-attachments/assets/8edf9526-c6c8-4764-a495-6e15bf59619d)

![WhatsApp Image 2025-03-12 at 09 46 41_6a2f2988](https://github.com/user-attachments/assets/a0f90bd1-bbfb-4922-9e1e-4cd73237506b)

![WhatsApp Image 2025-03-12 at 09 48 17_37fdf12a](https://github.com/user-attachments/assets/667f56e5-4fe6-4c95-8748-df694a492dee)


## ✨ What is This?

Ever wondered how game developers turn a grid of images into smooth animations? That's what sprite sheets are all about! This tool lets you:

- 📁 Load any sprite sheet image (PNG, JPG, BMP)
- 📏 Set the dimensions of individual sprites in your sheet
- 🎯 Select specific frames for your animation
- ▶️ Preview animations with adjustable speed and zoom
- 🎛️ Fine-tune your animations with interactive controls

Perfect for game developers, pixel artists, or anyone who wants to play with sprite animations!

## 🚀 Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/cizzle-sprite-sheet-tester.git
cd cizzle-sprite-sheet-tester

# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
env\Scripts\activate
# On macOS/Linux
# source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎮 How to Use

```bash
# Run the application
python -m src.main
```

## 📖 Step-by-Step Guide

1. **Load a Sprite Sheet**:

   - Click "Load Sprite Sheet" and select your image file
   - The tool works best with evenly-spaced sprites in a grid layout

2. **Set Sprite Dimensions**:

   - Use the Width and Height sliders to specify the size of each individual sprite
   - Click "Apply Dimensions" to see your sprite grid

3. **Select Animation Frames**:

   - Click "Select Animation Frames" to open the frame selector
   - Check the boxes for frames you want to include
   - Use "Select All" or "Deselect All" for quick selection
   - The preview shows which frames you've selected
   - Click "Save Selection" when done

4. **Run the Animation**:

   - Click "Run Animation" to see your sprites come to life!
   - A new window will open with your animation playing

5. **Animation Controls**:
   - Left/Right arrows: Navigate between frames
   - Up/Down arrows: Zoom in/out
   - +/- keys: Adjust animation speed
   - ESC: Close the animation and return to the main window

## 🛠️ Adjustable Settings

- **Animation Speed**: Control how fast your animation plays (1-60 FPS)
- **Zoom Level**: Make your sprites bigger or smaller (1-10x)
- **Frame Selection**: Choose any combination of frames for your animation

## 🧩 Project Structure

```
cizzle-sprite-sheet-tester/
│
├── src/               # Source code
│   ├── __init__.py    # Makes src a Python package
│   └── main.py        # Entry point for the application
│
├── tests/             # Test files
│   └── __init__.py    # Makes tests a Python package
│
├── .gitignore         # Specifies files to ignore in version control
├── requirements.txt   # Project dependencies
├── pyproject.toml     # Project metadata and build configuration
└── README.md          # This file
```

## 💡 Tips & Tricks

- **Perfect Loop**: Choose frames that make a smooth loop for continuous animations
- **Multiple Animations**: You can test different animations from the same sprite sheet by selecting different frame sequences
- **Keyboard Shortcuts**: While in the animation window, use keyboard controls for quick adjustments
- **Visual Debugging**: Use this tool to easily spot animation issues in your sprite sheets

## 📝 Requirements

- Python 3.6+
- Pygame
- Tkinter (usually comes with Python)
- Pillow (PIL)

## 🎨 Example Sprite Sheets

Not sure where to start? Try these free sprite sheet resources:

- [OpenGameArt.org](https://opengameart.org/)
- [Itch.io Free Game Assets](https://itch.io/game-assets/free)
- [Kenney's Free Assets](https://kenney.nl/assets)

## 🤝 Contributing

Have ideas for improvements? Contributions are welcome! Feel free to fork this repository and submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by Cizzle
