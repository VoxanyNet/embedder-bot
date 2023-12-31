import discord

@discord.commands.application_command(description="Ping the bot")
async def ping(ctx: discord.ApplicationContext):

    await ctx.respond("Pong!")