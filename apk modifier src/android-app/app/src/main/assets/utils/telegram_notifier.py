import requests
import json

class TelegramNotifier:
    """Telegram bot notification handler"""
    
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message):
        """Send a text message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Telegram notification error: {e}")
            return False
    
    def send_file(self, filepath, caption=None):
        """Send a file to Telegram"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            with open(filepath, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': self.chat_id}
                if caption:
                    data['caption'] = caption
                
                response = requests.post(url, data=data, files=files, timeout=300)
                response.raise_for_status()
            
            return True
        except Exception as e:
            print(f"Telegram file send error: {e}")
            return False
