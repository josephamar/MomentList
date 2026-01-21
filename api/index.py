def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": "<h1>🎉 Bravo ! Ton Python fonctionne sur Vercel</h1>"
    }