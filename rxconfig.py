import reflex as rx

config = rx.Config(
    app_name="ethico",
    show_built_with_reflex=False,
    env_file=".env",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)