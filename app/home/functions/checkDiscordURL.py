def checkDiscordURL(url):
    if 'discord' not in url:
        return {
            'error_message': "Not a discord URL"
        }

    channel_id = url.split('/')[-1]

    if len(channel_id) != 19 or channel_id.isdigit() == False:
        return {
            'error_message': "Invalid Discord Channel URL"
        }

    return {
        'channel_url': url,
        'channel_id': channel_id
    }