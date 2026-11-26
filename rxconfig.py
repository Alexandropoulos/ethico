import reflex as rx

config = rx.Config(
    app_name="ethico",
    backend_host="127.0.0.1",
    frontend_port=3000,
    api_url="https://ethico.duckdns.org",
    deploy_url="https://ethico.duckdns.org",
    cors_allowed_origins=["https://ethico.duckdns.org"],
        env_file=".env",
        plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)