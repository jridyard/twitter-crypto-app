from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(
    url='https://discord.com/api/webhooks/1008395822532145153/_SqH5_2m4iLNGxpg7yW49Gxph3_pGQ6D6NXscG9r-usGA83_aHhXbZozr_As7X8GmbQZ',
    username="data['CheckoutID']",
    content='Details available via API.',
    timeout=20
)
webhook.execute()