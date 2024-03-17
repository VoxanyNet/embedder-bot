import discord 

class Sex(discord.Bot):
    async def on_ready(self):
        member_count = 0
        guild_count = 0
        for guild in self.guilds:
            guild_count += 1
            member_count += guild.member_count
        
        print(member_count)
        print(guild_count)
        


bot = Sex()

bot.run("MTE3NjMzNjE2MTgxNjQ2MTM3Mg.GxIGBY.tPdvxIFIFVoygDr-lxCTOwlOfYf-UOJDjoB1h4")

