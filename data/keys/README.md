# HOW TO USE
Update this thing, I got rid of all dependencies. Also change it to use filename.key and be
able to launch anything. Default to moogle.

This folder normally contains "5" necessary files (actually only 3 of those are necessary atm):
admin.key, chocobo.key, lamia.key, moogle.key and whitemage.key

- admin.key contains the id of the administrator of the bot.
  Only used to fetch the admin to DM him in some specific commands.

- chocobo.key, lamia.key, moogle.key and whitemage.key contain token ids of the bot to launch.
  This is so the admin can choose which one to launch the script with.
  Currently, only whitemage + any of the other 3 is necessary, and only if you launch said bot.
  Chocobo, Lamia and Moogle have the exact same code. The launch script defaults to Moogle.

Extra keys:
- chamo_server.key: custom welcome message for the Chamo server (gets ignored if it doesn't exist)
