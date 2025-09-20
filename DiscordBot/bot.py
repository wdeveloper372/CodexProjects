import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello World!")
           


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run("MTM3MTM5MDUyNzAzNTE1MDQxNw.GCBZGm.jhN_ZAWvUdCfl0gA2XPeMeQVBnFoPnAbrO9C1w")