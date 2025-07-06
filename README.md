# LED Matrix Web Controller

A Flask-based web application for controlling RGB LED matrix displays on Raspberry Pi. This project provides an intuitive web interface to display text, images, animations, and dynamically generated graphs on LED matrix panels.

## What It Does

This application transforms your Raspberry Pi into a versatile LED matrix display controller that can:

- **Display Rich Text**: Show scrolling text messages with HTML styling support, including custom colors and bold formatting
- **Show Images**: Display static images (JPG, PNG) that are automatically resized to fit your LED matrix
- **Play Animations**: Show animated GIFs with proper frame sequencing
- **Generate Graphs**: Create and display bar charts from JSON data using matplotlib
- **Queue Management**: Handle multiple display requests through a background queue system

## How It Works

### Architecture

The application is built with a modular Flask architecture that separates concerns across different components:

#### Web Interface (`app/web/`)
- **Flask Routes**: Handle HTTP requests for text, image, and graph submissions
- **HTML Template**: Provides a clean, responsive web interface using Tailwind CSS
- **File Upload**: Securely handles image uploads with validation and unique naming

#### Display Engine (`app/display/`)
- **LED Display**: Manages the RGB matrix hardware interface using the `rpi-rgb-led-matrix` library
- **Rich Text Rendering**: Supports styled text with colors and bold formatting
- **Image Processing**: Handles image resizing and format conversion for LED display
- **Animation Support**: Processes GIF files frame by frame for smooth animations

#### Queue Management (`app/queue_manager/`)
- **Background Worker**: Runs in a separate thread to process display requests
- **Queue System**: Manages the order of display requests to prevent conflicts
- **Automatic Cleanup**: Removes temporary files after display completion

#### Utilities (`app/utils/`)
- **HTML Parser**: Converts HTML-styled text into rich text objects with color and formatting
- **Privilege Management**: Safely drops root privileges after hardware initialization
- **File Handling**: Manages file extensions and validation

### Display Process

1. **Web Request**: Users submit content through the web interface
2. **Content Processing**: 
   - Text is parsed for HTML styling and converted to rich text objects
   - Images are validated, saved temporarily, and added to the queue
   - Graph data is processed with matplotlib to generate PNG images
3. **Queue Management**: Content is added to a thread-safe queue for sequential processing
4. **Hardware Display**: The LED display worker processes queue items:
   - Text scrolls across the matrix with proper timing
   - Images are shown for a fixed duration
   - Animations play through all frames
5. **Cleanup**: Temporary files are automatically removed after display

### Technical Features

- **Hardware Configuration**: Supports various LED matrix configurations (32x64, chained panels, different GPIO mappings)
- **Font Management**: Uses bitmap fonts for crisp text rendering at low resolutions
- **Color Support**: Full RGB color support for text and graphics
- **Performance Optimization**: Configurable refresh rates and GPIO timing for smooth display
- **Thread Safety**: Proper synchronization between web requests and display operations
- **Error Handling**: Graceful error handling with user feedback through the web interface

### Supported Content Types

- **Styled Text**: HTML with `<span style="color: #ff0000;">` and `<b>` tags
- **Static Images**: JPEG and PNG files (automatically resized)
- **Animated GIFs**: Multi-frame animations
- **Bar Charts**: Generated from JSON data with matplotlib

## Installation

### Prerequisites
- Raspberry Pi (3B+ or newer recommended)
- RGB LED Matrix panel
- Python 3.7 or higher

### Setup

1. **Clone the repository:**
   ```bash
   git clone --recurse-submodules https://github.com/Lalith-Shravan/led-matrix-web.git
   cd led-matrix-web
   ```

2. **Set up a Python virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install required Python libraries:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the `rpi-rgb-led-matrix` library:**
   ```bash
   cd lib/rpi-rgb-led-matrix
   sudo apt update && sudo apt install python3-dev cython3 -y
   make build-python
   make install-python
   ```

5. **Return to the project root directory:**
   ```bash
   cd ../../
   ```

### Configuration

Before running the application, you may need to adjust some parameters in the `run.py` file to match your specific setup:

1. **LEDDisplay Parameters**:
   - The `LEDDisplay` class in `run.py` is initialized with several parameters, such as `led_slowdown_gpio`, `led_gpio_mapping`, `limit_refresh_rate_hz`, and `led_chain`.
   - These parameters should be updated to match your LED matrix hardware configuration. Refer to the [rpi-rgb-led-matrix documentation](https://github.com/hzeller/rpi-rgb-led-matrix) for details on these options.

2. **User Privileges**:
   - The `drop_privileges` function in `run.py` is used to drop root privileges after initializing the hardware.
   - Update the username parameter (currently set to `"pi"`) to your own username to ensure proper permissions.

Example snippet from `run.py`:
```python
# Adjust these parameters to match your setup
led_slowdown_gpio=4,
led_gpio_mapping="adafruit-hat",
limit_refresh_rate_hz=120,
led_chain=2

# Change this to your own username
 drop_privileges("your-username")
```

The application runs as a web server accessible from any device on the network, making it easy to control your LED display remotely from phones, tablets, or computers.

### Additional Resources

For more detailed documentation, troubleshooting, and advanced configuration options for the LED matrix hardware, refer to the [rpi-rgb-led-matrix library](https://github.com/hzeller/rpi-rgb-led-matrix) by hzeller. This library provides comprehensive information on:

- Supported hardware and wiring instructions
- Advanced display configurations
- Performance tuning and optimization
- Common issues and their solutions

This resource is invaluable for understanding the capabilities and limitations of the LED matrix hardware and ensuring smooth operation.
