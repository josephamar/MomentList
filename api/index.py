def handler(request):
    return (
        "🎉 Bravo ! Ton Python fonctionne sur Vercel",
        200,
        {"Content-Type": "text/plain; charset=utf-8"}
    )