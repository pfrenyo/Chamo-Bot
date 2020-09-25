This folder will contain several data files created by your Bot after it launched and worked for a bit.

For now, it will mainly contain:
- whitemage.json, containing data on which guilds (servers) whitemage knows (and doesn't have to introduce herself to)
- rssmanager.json, containing data on RSS Manager's different RSS feeds, data to be collected, channels to provide data to, etc.

If one wishes, feel free to create the following files (these will not be created by the bot):
- welcome.json, a flat JSON file for custom welcome messages for new users on specific servers of your choice with:
    key = server (guild) ID from discord
    value = custom welcome message string that needs a single "{}" (without quotation marks)
            present anywhere in there, which will be replaced by the new user's name.
