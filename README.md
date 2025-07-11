<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python Badge" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-green?logo=python&logoColor=white" alt="Tkinter Badge" />
</p>

<h1 align="center">🖼️ BMP File Viewer</h1>
<p align="center">
  <b>A Python Tkinter GUI to view and analyze BMP images with interactive scaling, brightness, and channel controls</b>
</p>

---

## 🚀 Features

- **Open & Display BMP Images:**  
  Supports 1, 4, 8, and 24 bits per pixel (BPP) BMP files with automatic header validation.
- **Image Metadata Display:**  
  Instantly view original file size, image dimensions, and BPP.
- **Interactive Scaling:**  
  Zoom in/out and see real-time changes to display size.
- **Brightness Adjustment:**  
  Fine-tune image brightness with a slider.
- **Channel Toggle:**  
  Toggle the visibility of Red, Green, and Blue channels independently for detailed analysis.
- **Efficient Pixel Parsing:**  
  Custom handlers for 1, 4, 8, and 24-bit images with color tables and index mapping.

## 🛠️ How It Works

### 1. **File Handling & Validation**
- Prompts user to select a `.bmp` file.
- Validates BMP header (`'BM'`, size ≥ 54 bytes).

### 2. **Metadata Extraction**
- Reads:
  - File size
  - Image width/height
  - Bits Per Pixel (BPP)
- Displays metadata to user.

### 3. **Pixel Data Parsing**
- **1-bit, 4-bit, 8-bit BMP**:  
  Uses color tables and bitwise operations to parse indexed pixel data.
- **24-bit BMP**:  
  Direct extraction of RGB pixel data.
- Data stored in a NumPy array for processing.

### 4. **Image Processing**
- **Scaling**:  
  Initial scale to fit canvas, adjustable by user.
- **Brightness**:  
  Applies multiplicative adjustment to all pixels.
- **Channel Masking**:  
  Red, green, blue can be toggled independently.

### 5. **Rendering**
- Tkinter’s `PhotoImage` renders the processed image onto the canvas.
- UI updates in real time as user interacts with controls.

---

## 📦 Installation

> **Requires Python 3.x**

```bash
pip install numpy
```
No external image libraries required—everything is handled via pure Python and Tkinter.
# ▶️ Usage

```bash
python BMP_viewer.py
```
- 1.Click Open BMP File to select an image.

- 2.Use the sliders to adjust scale and brightness.

- 3.Toggle the Red, Green, and Blue channels as needed.

- 4.View metadata and display info live as you interact.
#🧑‍💻 Code Architecture
<details> <summary><strong>Class: <code>BMPViewerApp</code></strong> (click to expand)</summary>

    open_file(): File dialog, loads and validates BMP data.

    validate_bmp(): Checks for valid BMP headers.

    parse_bmp(): Extracts metadata and triggers display.

    display_image(): Routes to parsing based on BPP.

    parse_1bit/4bit/8bit/24bit(): Specialized functions for each BMP type.

    update_image(): Handles scaling, brightness, channel toggling, and rendering.

    toggle_red/green/blue(): Channel visibility toggles.

</details>

#📝 Example Supported BMP Types

    1-bit: Black & white

    4-bit: 16-color indexed

    8-bit: 256-color indexed

    24-bit: True color (RGB)

# 👨‍💻 Author

Utsav Patel

Email:usp@sfu.ca

Simon Fraser University
# License

This project is open for educational and demonstration purposes. Attribution is appreciated!
<p align="center"> <b>🌟 If you like this project, please star the repo! 🌟</b> </p> 
