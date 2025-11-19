// APK Modifier Application
let currentJobId = null;
let statusCheckInterval = null;

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const optionsSection = document.getElementById('optionsSection');
const processingSection = document.getElementById('processingSection');
const completeSection = document.getElementById('completeSection');
const errorSection = document.getElementById('errorSection');

const uploadArea = document.getElementById('uploadArea');
const apkFile = document.getElementById('apkFile');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');

const backBtn = document.getElementById('backBtn');
const processBtn = document.getElementById('processBtn');
const downloadBtn = document.getElementById('downloadBtn');
const newModificationBtn = document.getElementById('newModificationBtn');
const retryBtn = document.getElementById('retryBtn');

const libName = document.getElementById('libName');
const customOptions = document.getElementById('customOptions');
const botToken = document.getElementById('botToken');
const chatId = document.getElementById('chatId');
const uploadServer = document.getElementById('uploadServer');

let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => apkFile.click());
    
    // File selection
    apkFile.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        uploadArea.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].name.endsWith('.apk')) {
            selectedFile = files[0];
            displayFileInfo();
        } else {
            showError('Please select a valid APK file');
        }
    });
    
    // Remove file
    removeFile.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        apkFile.value = '';
        fileInfo.style.display = 'none';
        uploadArea.style.display = 'block';
    });
    
    // Navigation
    backBtn.addEventListener('click', () => {
        showSection(uploadSection);
    });
    
    processBtn.addEventListener('click', handleProcess);
    downloadBtn.addEventListener('click', handleDownload);
    newModificationBtn.addEventListener('click', resetApplication);
    retryBtn.addEventListener('click', () => {
        showSection(uploadSection);
    });
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        if (files[0].name.endsWith('.apk')) {
            selectedFile = files[0];
            displayFileInfo();
        } else {
            showError('Please select a valid APK file');
            apkFile.value = '';
        }
    }
}

function displayFileInfo() {
    const sizeMB = (selectedFile.size / (1024 * 1024)).toFixed(2);
    fileName.textContent = selectedFile.name;
    fileSize.textContent = `${sizeMB} MB`;
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
    
    // Show options section after file selection
    setTimeout(() => {
        showSection(optionsSection);
        optionsSection.scrollIntoView({ behavior: 'smooth' });
    }, 500);
}

async function handleProcess() {
    if (!selectedFile) {
        showError('Please select an APK file first');
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    formData.append('apk_file', selectedFile);
    
    // Get selected mode
    const mode = document.querySelector('input[name="mode"]:checked').value;
    formData.append('mode', mode);
    formData.append('lib_name', libName.value || 'libxx.so');
    formData.append('custom_options', customOptions.value || '');
    formData.append('bot_token', botToken.value || '');
    formData.append('chat_id', chatId.value || '');
    formData.append('upload_server', uploadServer.value || '');
    
    // Show processing section
    showSection(processingSection);
    
    // Update processing info
    document.getElementById('modeDisplay').textContent = mode.toUpperCase();
    document.getElementById('startTime').textContent = new Date().toLocaleString();
    
    try {
        // Upload APK
        processBtn.disabled = true;
        processBtn.innerHTML = '<span>⏳ Uploading...</span>';
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            currentJobId = result.job_id;
            document.getElementById('jobId').textContent = currentJobId;
            
            // Start status checking
            startStatusCheck();
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        showError(error.message);
    } finally {
        processBtn.disabled = false;
        processBtn.innerHTML = '<span>🚀 Process APK</span>';
    }
}

function startStatusCheck() {
    // Check status every 3 seconds
    statusCheckInterval = setInterval(checkStatus, 3000);
    checkStatus(); // Check immediately
}

async function checkStatus() {
    if (!currentJobId) return;
    
    try {
        const response = await fetch(`/status/${currentJobId}`);
        const status = await response.json();
        
        if (!response.ok) {
            throw new Error(status.error || 'Failed to get status');
        }
        
        // Update UI
        updateProgress(status);
        
        // Check if completed or failed
        if (status.status === 'completed') {
            clearInterval(statusCheckInterval);
            showComplete(status);
        } else if (status.status === 'failed') {
            clearInterval(statusCheckInterval);
            showError(status.message);
        }
    } catch (error) {
        console.error('Status check error:', error);
    }
}

function updateProgress(status) {
    const progress = status.progress || 0;
    const message = status.message || 'Processing...';
    
    document.getElementById('progressFill').style.width = `${progress}%`;
    document.getElementById('progressText').textContent = `${progress}%`;
    document.getElementById('statusMessage').textContent = message;
}

function showComplete(status) {
    showSection(completeSection);
    
    document.getElementById('originalFileName').textContent = status.filename;
    document.getElementById('modifiedFileName').textContent = status.output_filename || 'modified.apk';
    document.getElementById('completeJobId').textContent = currentJobId;
    
    // Show upload URL if available
    if (status.upload_url) {
        const urlContainer = document.getElementById('uploadUrlContainer');
        const urlLink = document.getElementById('uploadUrl');
        urlContainer.style.display = 'flex';
        urlLink.href = status.upload_url;
        urlLink.textContent = status.upload_url;
    }
}

function handleDownload() {
    if (currentJobId) {
        window.location.href = `/download/${currentJobId}`;
    }
}

function showError(message) {
    showSection(errorSection);
    document.getElementById('errorMessage').textContent = message;
    
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

function showSection(section) {
    // Hide all sections
    [uploadSection, optionsSection, processingSection, completeSection, errorSection].forEach(s => {
        s.style.display = 'none';
    });
    
    // Show target section
    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth' });
}

function resetApplication() {
    // Clear state
    selectedFile = null;
    currentJobId = null;
    apkFile.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
    
    // Reset form
    document.querySelector('input[name="mode"][value="fud"]').checked = true;
    libName.value = 'libxx.so';
    customOptions.value = '';
    
    // Show upload section
    showSection(uploadSection);
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
