
import nextcord
from nextcord.ext import commands
import asyncio

from goldy_func import *
from goldy_utility import *
import utility.msg as msg

from cogs.database import database
from cogs.giphy_cog import api

cog_name = "extra"

class extra(commands.Cog, name="💜Extra"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 2

    @commands.command(description="💖 A cute command.")
    @commands.cooldown(1, 1.8, commands.BucketType.user)
    async def kawaii(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!kawaii"):
                gif_url = await api.gif.random(ctx, self.client, "kawaii cat", (0, 40))

                embed = nextcord.Embed(title="💖 Kawaii!!!", color=settings.Aki_Pink)
                embed.set_image(url=gif_url)
                embed.set_footer(text=msg.footer.giphy)
                await ctx.send(embed=embed)

            else:
                await ctx.send(msg.error.do_not_have_item.format(ctx.author.mention))

def setup(client):
    client.add_cog(extra(client))

#Need Help? Check out this: {youtube playlist}