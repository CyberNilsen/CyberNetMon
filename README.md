# 🛡️ CyberNetMon

**Real-time Network Connection Monitor with Threat Detection**

CyberNetMon is a professional network monitoring application that provides real-time surveillance of your system's network connections with built-in threat detection and geolocation mapping.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Features

### 🔍 Real-time Network Monitoring
- **Live Connection Tracking**: Monitor all active TCP/UDP connections in real-time
- **Process Identification**: See which applications are making network connections
- **Connection Status**: Track connection states (ESTABLISHED, LISTENING, etc.)
- **Local & Remote Address Mapping**: Full visibility of source and destination endpoints

### 🌍 Geographic Intelligence
- **IP Geolocation**: Automatic location detection for remote connections
- **Country Flags**: Visual country identification with emoji flags
- **ISP Information**: Organization and service provider details
- **Local Network Detection**: Smart filtering of private/local connections

### ⚠️ Threat Detection
- **Suspicious Connection Alerts**: Automated flagging of potentially harmful connections
- **Geographic Risk Assessment**: Highlight connections from high-risk countries
- **Port Analysis**: Detection of connections on suspicious ports
- **Process Monitoring**: Alert on potentially malicious processes

### 📊 Analytics & Statistics
- **Connection Statistics**: Real-time counts of TCP/UDP, established connections
- **Unique IP Tracking**: Monitor distinct remote addresses
- **Country Distribution**: Geographic spread of your connections
- **Historical Data**: Connection history and trends

### 💻 Modern GUI Interface
- **Dark Theme**: Professional cybersecurity-inspired interface
- **Real-time Updates**: Live data refresh with customizable intervals
- **Interactive Controls**: Start/stop monitoring, manual refresh, data export
- **Status Indicators**: Visual monitoring state and connection health
- **Responsive Design**: Scalable interface for different screen sizes

### 📁 Data Export
- **JSON Export**: Structured data export for analysis
- **CSV Support**: Spreadsheet-compatible format
- **Timestamped Reports**: Automatic filename generation with timestamps
- **Complete Data**: Include process info, geolocation, and threat assessment

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package installer)
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CyberNetMon.git
   cd CyberNetMon
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run CyberNetMon**
   ```bash
   python gui.py
   ```

### Dependencies
```
psutil>=5.8.0
requests>=2.25.0
tkinter (included with Python)
```

## 🎯 Usage

### Basic Operation

1. **Launch Application**
   ```bash
   python gui.py
   ```

2. **Start Monitoring**
   - Click "START MONITORING" to begin real-time surveillance
   - The status indicator will show "ACTIVE" when monitoring is running
   - Connection data will populate automatically

3. **View Connections**
   - Monitor live connections in the main table
   - Color coding indicates threat levels:
     - 🟢 Green: Normal connections
     - 🟡 Yellow: Potentially suspicious
     - 🔴 Red: High-risk connections

4. **Export Data**
   - Click "EXPORT" to save current connection data
   - Choose JSON or CSV format
   - Files are automatically timestamped

### Advanced Features

#### Manual Refresh
Click "REFRESH" to manually update connection data without starting continuous monitoring.

#### Clear Display
Use "CLEAR" to reset the display and statistics while keeping monitoring active.

#### Connection Analysis
- **Process Column**: Shows which application initiated the connection
- **Location Column**: Displays city and country of remote endpoint
- **Status Column**: Current connection state
- **Protocol Column**: TCP or UDP connection type

## 🛡️ Security Considerations

### Administrator Privileges
For complete functionality on Windows, run as Administrator:
```bash
# Windows (Run as Administrator)
python gui.py

# Linux/macOS (with sudo if needed)
sudo python gui.py
```

### Privacy
- **Local Processing**: All analysis is performed locally
- **API Usage**: Geolocation uses ipapi.co (respects rate limits)
- **No Data Collection**: CyberNetMon doesn't send your data anywhere
- **Export Control**: You control all data export and storage

### Network Security
- CyberNetMon monitors **outbound** connections from your system
- It does **not** perform network scanning or intrusion detection
- Use responsibly and in compliance with local laws and policies

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.12+, or Linux (any recent distribution)
- **Python**: 3.7 or higher
- **RAM**: 256 MB available memory
- **Storage**: 50 MB free space

### Recommended Requirements
- **OS**: Windows 10+, macOS 11+, or Ubuntu 20.04+
- **Python**: 3.9 or higher
- **RAM**: 512 MB available memory
- **Network**: Internet connection for geolocation services

## 🤝 Contributing

We welcome contributions to CyberNetMon! Here's how you can help:

### Bug Reports
- Use GitHub Issues to report bugs
- Include system information and error messages
- Provide steps to reproduce the issue

### Feature Requests
- Suggest new features via GitHub Issues
- Describe the use case and expected behavior
- Consider the security implications

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/CyberNetMon.git
cd CyberNetMon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

**⚠️ Disclaimer**: CyberNetMon is intended for legitimate network monitoring and security purposes. Users are responsible for ensuring compliance with local laws and regulations. The developers are not responsible for misuse of this software.
