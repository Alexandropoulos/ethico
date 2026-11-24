import reflex as rx

config = rx.Config(
    app_name="ethico",
    api_url="http://4.223.154.216",
    env_file=".env",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)