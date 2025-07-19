# Smart Waste Sorting System (FARZ)

An intelligent waste classification and sorting system using machine learning, computer vision, and robotic automation. This project automatically identifies different types of waste materials and sorts them into appropriate bins using stepper motors and servo mechanisms.

## 🎯 Overview

This system uses AI-powered image classification to identify waste materials (paper, plastic, metal, glass, cardboard, biodegradable) and automatically sorts them into different compartments using mechanical actuators. The project is designed to run on a Raspberry Pi with various sensors and motors.

## 🔧 Hardware Components

- **Raspberry Pi** (Main controller)
- **Camera Module** (Image capture for classification)
- **Touch Sensor** (User interaction trigger)
- **Ultrasonic Sensor** (Object detection)
- **Stepper Motors** (Rotation mechanism for sorting)
- **Servo Motors** (Gate/door control)
- **LCD Display** (Status and feedback display)
- **LEDs** (Status indicators)

## 🧠 AI/ML Features

### Models Used

- **TensorFlow Lite Model** (`best_float32.tflite`) - Optimized for edge deployment
- **YOLO Model** (`best.pt`) - Object detection and classification
- **Quantized Model** (`quantized_model.tflite`) - Further optimized for performance

**ML Training Repository**: For model training and development details, see [Farz ML Repository](https://github.com/m7amd777/Farz)

### Supported Waste Categories

1. **Paper** (Quadrant 1)
2. **Metal** (Quadrant 2)
3. **Plastic** (Quadrant 3)
4. **Glass**
5. **Cardboard**
6. **Biodegradable**
7. **General/Other** (Quadrant 4)

## 📁 Project Structure

### Main Application Files

- `iquit.py` / `iquit2.py` - Main application with touch sensor integration
- `mlbins_lcd.py` - Version with LCD display support
- `mlbins2.py` - Alternative main application
- `liteAi.py` - Standalone TensorFlow Lite inference

### Hardware Control Modules

- `stepper.py` / `stepper2.py` / `stepperNew.py` - Stepper motor control
- `stepperAI.py` / `stepperAI2.py` - AI-integrated stepper control
- `motor.py` - General motor control functions
- `sensor.py` - Sensor input handling
- `ultrasonic.py` - Ultrasonic sensor for object detection
- `button.py` - Button/touch interface

### Utility Scripts

- `demo_lcd.py` - LCD display demonstration
- `yolocheck.py` - YOLO model testing
- `scripts.py` - General utility scripts
- `check.py` / `checker2.py` / `Checker3.py` - System testing utilities

## 🚀 Getting Started

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt  # Note: Create from farzpackagesvenv.txt

# Required Python packages include:
# - opencv-python
# - tensorflow
# - numpy
# - RPi.GPIO
# - gpiozero
# - pillow
# - ultralytics
```

### Hardware Setup

1. Connect camera module to Raspberry Pi
2. Wire stepper motors to GPIO pins (17, 18, 27, 22)
3. Connect servo motors to designated GPIO pins
4. Set up touch sensor on GPIO pin 12
5. Connect ultrasonic sensor (Trigger: GPIO 19, Echo: GPIO 4)
6. Wire LCD display (if using LCD version)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd farz

# Set up virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Basic Operation

```bash
# Run the main application with touch sensor
python iquit2.py

# Run with LCD display
python mlbins_lcd.py

# Test individual components
python yolocheck.py        # Test YOLO detection
python demo_lcd.py         # Test LCD display
python ultrasonic.py       # Test ultrasonic sensor
```

### How It Works

1. **Detection**: Touch sensor or ultrasonic sensor detects object presence
2. **Capture**: Camera captures image of the waste item
3. **Classification**: AI model processes image and identifies waste type
4. **Sorting**: System calculates appropriate bin quadrant
5. **Mechanical Action**:
   - Stepper motor rotates to correct position
   - Servo motor opens gate/door
   - Item is sorted into appropriate bin
   - System returns to ready state

## 🔧 Configuration

### Motor Calibration

Each waste category has specific rotation durations:

```python
# Duration values for initial rotation (seconds)
duration_values = {
    1: 0.043,  # Paper
    2: 0.0650, # Metal  
    3: 0.08,   # Plastic
    4: 0.0098  # General
}

# Final positioning durations
final_duration_values = {
    1: 0.059,  # Paper
    2: 0.03,   # Metal
    3: 0.018,  # Plastic
    4: 0.088   # General
}
```

### Pin Configuration

```python
# Stepper Motor Pins
out1 = 17
out2 = 18  
out3 = 27
out4 = 22

# Servo Control
servo_pin = 12

# Sensors
touch_pin = 12
ultrasonic_trigger = 19
ultrasonic_echo = 4
```

## 📊 Model Performance

- **Input Size**: 640x640 pixels
- **Confidence Threshold**: 0.3
- **Supported Formats**: JPG, PNG
- **Inference Time**: ~0.2-0.5 seconds on Raspberry Pi

## 🛠️ Development

### Testing Components

```bash
# Test stepper motor
python stepper.py

# Test camera and AI inference  
python liteAi.py

# Check system sensors
python check.py
```

### Adding New Waste Categories

1. Update the `classes` dictionary in prediction functions
2. Add corresponding quadrant mappings
3. Calibrate motor rotation values
4. Update LCD display messages if applicable

## 📋 Troubleshooting

### Common Issues

- **GPIO already in use**: Run `GPIO.cleanup()` or restart the Pi
- **Camera not found**: Check camera module connection and enable camera in raspi-config
- **Import errors**: Ensure all dependencies are installed correctly
- **Motor not moving**: Verify GPIO pin connections and power supply

### Debug Mode

Most scripts include debug functions and verbose output for troubleshooting.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on hardware
5. Submit a pull request

## 🙏 Acknowledgments

- TensorFlow team for TensorFlow Lite
- Ultralytics for YOLO implementation  
- Raspberry Pi Foundation
- Contributors to the RPi.GPIO and gpiozero libraries

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review hardware connections
3. Test individual components
4. Create an issue in the repository

---

**Note**: This system requires proper hardware setup and calibration. Always test individual components before running the full system.
