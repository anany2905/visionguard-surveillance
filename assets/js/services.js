// ===================================
// SERVICES PAGE JAVASCRIPT
// ===================================

// ===== FLASHCARD FLIP ANIMATION =====
document.querySelectorAll('.service-flashcard').forEach(card => {
    card.addEventListener('click', function(e) {
        if (e.target.closest('button')) return;
        this.classList.toggle('flipped');
    });
});

// ===== MODAL FUNCTIONS =====
function openModal(modalType) {
    const modalId = modalType + '-modal';
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalType) {
    const modalId = modalType + '-modal';
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
});

// ===== DRAG AND DROP FOR IMAGE UPLOAD =====
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.target.closest('.upload-area').style.borderColor = 'var(--primary-color)';
    e.target.closest('.upload-area').style.background = 'rgba(99, 102, 241, 0.1)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const uploadArea = e.target.closest('.upload-area');
    uploadArea.style.borderColor = '';
    uploadArea.style.background = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        const previewId = uploadArea.querySelector('input[type="file"]').id.replace('-input', '-preview');
        const preview = document.getElementById(previewId);
        if (preview) {
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }
}

function previewImage(e, type) {
    const file = e.target.files[0];
    const previewId = type + '-preview';
    const preview = document.getElementById(previewId);
    if (file && preview) {
        const reader = new FileReader();
        reader.onload = function(event) {
            preview.src = event.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// ===== ERROR HANDLING HELPER =====
function getBackendErrorHtml(error) {
    const msg = error.message || String(error);
    if (msg.includes('Failed to fetch') || msg.includes('NetworkError') || msg.includes('fetch')) {
        return `
            <div style="background: #fef3c7; color: #92400e; padding: 20px; border-radius: 12px; text-align: center; border-left: 5px solid #f59e0b;">
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 10px;">Cannot Connect to Backend Server</div>
                <div style="font-size: 0.95rem; line-height: 1.6;">
                    The detection server is not running.<br>
                    Please start it with this command:<br>
                    <code style="background: #fff; padding: 6px 12px; border-radius: 6px; display: inline-block; margin-top: 10px; font-family: monospace; color: #1f2937;">
                        python backend/app.py
                    </code>
                </div>
            </div>
        `;
    }
    return `<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">Error: ${msg}</div>`;
}

// ===== FACE DETECTION FUNCTIONS =====

async function startFaceDetection() {
    const video = document.getElementById('face-live-video');
    const resultsBox = document.getElementById('face-results');
    const placeholder = video.parentNode.querySelector('.placeholder-message');
    
    try {
        resultsBox.innerHTML = '<div style="color: #6366f1;"><i class="fas fa-spinner fa-spin"></i> Starting camera...</div>';
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        placeholder.style.display = 'none';
        video.style.display = 'block';
        video.play();
        
        const detectInterval = setInterval(async () => {
            try {
                if (video.videoWidth === 0) return;
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                const imageData = canvas.toDataURL('image/jpeg', 0.8);
                
                const response = await fetch('/api/face_detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageData })
                });
                
                if (response.ok) {
                    const results = await response.json();
                    displayFaceResults(resultsBox, results);
                } else {
                    const errorText = await response.text();
                    resultsBox.innerHTML = `<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">Server error: ${errorText}</div>`;
                }
            } catch (err) {
                resultsBox.innerHTML = getBackendErrorHtml(err);
                clearInterval(detectInterval);
            }
        }, 2000);
        
        video._detectInterval = detectInterval;
        
    } catch (err) {
        resultsBox.innerHTML = `<div style="color: #ef4444;">Error accessing camera: ${err.message}</div>`;
    }
}

async function runFaceDetection() {
    const preview = document.getElementById('face-preview');
    const resultsBox = document.getElementById('face-upload-results');
    
    if (!preview.src || preview.style.display === 'none') {
        resultsBox.innerHTML = '<div style="color: #ef4444;">Please upload an image first</div>';
        return;
    }
    
    try {
        resultsBox.innerHTML = '<div>Loading... <i class="fas fa-spinner fa-spin"></i></div>';
        
        const response = await fetch('/api/face_detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: preview.src })
        });
        
        if (response.ok) {
            const results = await response.json();
            displayFaceResults(resultsBox, results);
        } else {
            const errorText = await response.text();
            resultsBox.innerHTML = `<div style="color: #ef4444;">Detection failed: ${errorText}</div>`;
        }
    } catch (err) {
        resultsBox.innerHTML = getBackendErrorHtml(err);
    }
}

function displayFaceResults(resultsBox, results) {
    if (results.error) {
        resultsBox.innerHTML = `<div style="background: #fee2e2; color: #dc2626; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold;">Error: ${results.error}</div>`;
        return;
    }
    if (!results.detected || !results.faces || results.faces.length === 0) {
        resultsBox.innerHTML = '<div style="background: #fee2e2; color: #dc2626; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold;">No faces detected</div>';
        return;
    }
    
    let html = `<div style="background: #ecfdf5; padding: 25px; border-radius: 12px; border-left: 5px solid #059669; color: #064e3b;">`;
    html += `<div style="font-size: 1.4rem; font-weight: bold; text-align: center; margin-bottom: 15px;">Faces Detected: ${results.faces.length}</div>`;
    
    results.faces.forEach(face => {
        const authColor = face.authorized ? '#059669' : '#dc2626';
        const authText = face.authorized ? 'Authorized' : 'Unknown';
        html += `
            <div style="padding: 15px; background: #d1fae5; border-radius: 8px; margin-bottom: 10px;">
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 8px;">${face.name}</div>
                <div style="font-size: 0.95rem; margin-bottom: 5px;">ID: ${face.id}</div>
                <div style="font-size: 0.95rem; margin-bottom: 5px;">Status: <span style="color: ${authColor}; font-weight: bold;">${authText}</span></div>
                <div style="font-size: 0.9rem;">Confidence: ${(face.confidence * 100).toFixed(1)}%</div>
            </div>
        `;
    });
    
    html += `</div>`;
    resultsBox.innerHTML = html;
}

// ===== PPE DETECTION FUNCTIONS =====

async function startPPEDetection() {
    const video = document.getElementById('ppe-live-video');
    const resultsBox = document.getElementById('ppe-results');
    const placeholder = video.parentNode.querySelector('.placeholder-message');
    
    try {
        resultsBox.innerHTML = '<div style="color: #6366f1;"><i class="fas fa-spinner fa-spin"></i> Starting camera...</div>';
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        placeholder.style.display = 'none';
        video.style.display = 'block';
        video.play();
        
        const detectInterval = setInterval(async () => {
            try {
                if (video.videoWidth === 0) return;
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                const imageData = canvas.toDataURL('image/jpeg', 0.8);
                
                const response = await fetch('/api/ppe_detect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageData })
                });
                
                if (response.ok) {
                    const results = await response.json();
                    displayPPEResults(resultsBox, results);
                } else {
                    const errorText = await response.text();
                    resultsBox.innerHTML = `<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">Server error: ${errorText}</div>`;
                }
            } catch (err) {
                resultsBox.innerHTML = getBackendErrorHtml(err);
                clearInterval(detectInterval);
            }
        }, 2000);
        
        video._detectInterval = detectInterval;
        
    } catch (err) {
        resultsBox.innerHTML = `<div style="color: #ef4444;">Error accessing camera: ${err.message}</div>`;
    }
}

async function runPPEDetection() {
    const preview = document.getElementById('ppe-preview');
    const resultsBox = document.getElementById('ppe-upload-results');
    
    if (!preview.src || preview.style.display === 'none') {
        resultsBox.innerHTML = '<div style="color: #ef4444;">Please upload an image first</div>';
        return;
    }
    
    try {
        resultsBox.innerHTML = '<div>Loading... <i class="fas fa-spinner fa-spin"></i></div>';
        
        const response = await fetch('/api/ppe_detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: preview.src })
        });
        
        if (response.ok) {
            const results = await response.json();
            displayPPEResults(resultsBox, results);
        } else {
            const errorText = await response.text();
            resultsBox.innerHTML = `<div style="color: #ef4444;">Detection failed: ${errorText}</div>`;
        }
    } catch (err) {
        resultsBox.innerHTML = getBackendErrorHtml(err);
    }
}

function displayPPEResults(resultsBox, results) {
    if (results.error) {
        resultsBox.innerHTML = `<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">Error: ${results.error}</div>`;
        return;
    }
    if (!results.detected || !results.people || results.people.length === 0) {
        resultsBox.innerHTML = '<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">No PPE detected</div>';
        return;
    }
    
    const person = results.people[0];
    const ppe = person.ppe;
    let html = `
        <div style="background: #ecfdf5; padding: 25px; border-radius: 12px; border-left: 5px solid #059669; color: #064e3b;">
            <div style="font-size: 1.4rem; line-height: 2.4; font-weight: 500;">
                <div style="margin-bottom: 8px;"><span style="font-size: 1.6rem; margin-right: 12px;">${ppe.helmet ? '✅' : '❌'}</span>Helmet</div>
                <div style="margin-bottom: 8px;"><span style="font-size: 1.6rem; margin-right: 12px;">${ppe.vest ? '✅' : '❌'}</span>Vest</div>
                <div style="margin-bottom: 8px;"><span style="font-size: 1.6rem; margin-right: 12px;">${ppe.gloves ? '✅' : '❌'}</span>Gloves</div>
                <div style="margin-bottom: 18px;"><span style="font-size: 1.6rem; margin-right: 12px;">${ppe.boots ? '✅' : '❌'}</span>Boots</div>
            </div>
            <div style="padding: 15px; background: #d1fae5; border-radius: 8px; font-weight: bold; text-align: center; font-size: 1.1rem; color: #065f46;">
                Confidence: ${(person.confidence * 100).toFixed(1)}%
            </div>
        </div>
    `;
    resultsBox.innerHTML = html;
}

// ===== BOX COUNTING FUNCTIONS =====

async function startBoxCounting() {
    const video = document.getElementById('box-live-video');
    const resultsBox = document.getElementById('box-results');
    const placeholder = video.parentNode.querySelector('.placeholder-message');
    
    try {
        resultsBox.innerHTML = '<div style="color: #6366f1;"><i class="fas fa-spinner fa-spin"></i> Starting camera...</div>';
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
        video.srcObject = stream;
        placeholder.style.display = 'none';
        video.style.display = 'block';
        video.play();
        
        const detectInterval = setInterval(async () => {
            try {
                if (video.videoWidth === 0) return;
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                const imageData = canvas.toDataURL('image/jpeg', 0.8);
                
                const response = await fetch('/api/box_count', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageData })
                });
                
                if (response.ok) {
                    const results = await response.json();
                    displayBoxResults(resultsBox, results);
                } else {
                    const errorText = await response.text();
                    resultsBox.innerHTML = `<div style="color: #dc2626; padding: 20px; text-align: center; font-weight: bold;">Server error: ${errorText}</div>`;
                }
            } catch (err) {
                resultsBox.innerHTML = getBackendErrorHtml(err);
                clearInterval(detectInterval);
            }
        }, 3000);
        
        video._detectInterval = detectInterval;
    } catch (err) {
        resultsBox.innerHTML = `<div style="color: #dc2626;">Camera error: ${err.message}</div>`;
    }
}

async function runBoxCounting() {
    const preview = document.getElementById('box-preview');
    const resultsBox = document.getElementById('box-upload-results');
    
    if (!preview.src || preview.style.display === 'none') {
        resultsBox.innerHTML = '<div style="color: #dc2626;">Please upload an image first</div>';
        return;
    }
    
    try {
        resultsBox.innerHTML = '<div style="color: #6366f1;"><i class="fas fa-spinner fa-spin"></i> Counting boxes...</div>';
        
        const response = await fetch('/api/box_count', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: preview.src })
        });
        
        if (response.ok) {
            const results = await response.json();
            displayBoxResults(resultsBox, results);
        } else {
            const errorText = await response.text();
            resultsBox.innerHTML = `<div style="color: #dc2626;">Detection failed: ${errorText}</div>`;
        }
    } catch (err) {
        resultsBox.innerHTML = getBackendErrorHtml(err);
    }
}

function displayBoxResults(resultsBox, results) {
    if (results.error) {
        resultsBox.innerHTML = `<div style="background: #fee2e2; color: #dc2626; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold;">Error: ${results.error}</div>`;
        return;
    }
    if (!results.detected) {
        resultsBox.innerHTML = '<div style="background: #fee2e2; color: #dc2626; padding: 20px; border-radius: 12px; text-align: center;">No boxes detected</div>';
        return;
    }
    
    const html = `
        <div style="background: #ecfdf5; padding: 25px; border-radius: 12px; border-left: 5px solid #059669; color: #064e3b;">
            <div style="font-size: 1.6rem; font-weight: bold; text-align: center; margin-bottom: 15px;">
                Boxes Detected: <span style="color: #059669; font-size: 2rem;">${results.count}</span>
            </div>
            <div style="padding: 15px; background: #d1fae5; border-radius: 8px; font-weight: bold; text-align: center; font-size: 1.2rem; color: #065f46;">
                Confidence: ${(results.confidence * 100).toFixed(1)}%
            </div>
        </div>
    `;
    resultsBox.innerHTML = html;
}

// ===== STOP DETECTION =====
function stopDetection() {
    const videos = document.querySelectorAll('video');
    videos.forEach(video => {
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            video.style.display = 'none';
            const placeholder = video.parentNode.querySelector('.placeholder-message');
            if (placeholder) placeholder.style.display = 'block';
        }
        if (video._detectInterval) {
            clearInterval(video._detectInterval);
            video._detectInterval = null;
        }
    });
    
    const modals = document.querySelectorAll('.modal.active');
    modals.forEach(modal => {
        modal.classList.remove('active');
    });
    document.body.style.overflow = 'auto';
}

// ===== PAGE INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const item = this.closest('.faq-item');
            item.classList.toggle('active');
        });
    });
});

