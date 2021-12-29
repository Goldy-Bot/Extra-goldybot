import datetime
import nextcord
from nextcord.ext import commands
import asyncio

from src.goldy_func import *
from src.goldy_utility import *
import src.utility.msg as msg

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

    @kawaii.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.kawaii")

    @commands.command(description="💕 Feel in the need to hug somebody, we got you.")
    @commands.cooldown(1, 2.8, commands.BucketType.user)
    async def hug(self, ctx, member: nextcord.Member=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!hug"):
                if not member == None:
                    gif_url = await api.gif.random(ctx, self.client, "hug anime", (3, 20))

                    embed = nextcord.Embed(title="**💕 *__{}__* hugged *__{}__!***".format(ctx.author.name, member.name), color=settings.AKI_PINK)
                    embed.set_image(url=gif_url)
                    embed.set_footer(text=msg.footer.giphy)
                    await ctx.send(embed=embed)
                    return True

                else:
                    await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!hug {member}"))
                    return False
            else:
                await ctx.send(msg.error.do_not_have_item.format(ctx.author.mention))
                
    @hug.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.hug")

    @commands.command(description="😊 Idk, it shows gifs of anime characters blushing I guess?")
    @commands.cooldown(1, 1.8, commands.BucketType.user)
    async def blush(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!blush"):
                gif_url = await api.gif.random(ctx, self.client, "anime blush", (0, 30))

                embed = nextcord.Embed(title=f"😊 __{ctx.author.name}'s__ blushing!", color=settings.AKI_RED)
                embed.set_image(url=gif_url)
                embed.set_footer(text=msg.footer.giphy)
                await ctx.send(embed=embed)

            else:
                await ctx.send(msg.error.do_not_have_item.format(ctx.author.mention))

    @blush.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.blush")

def setup(client):
    client.add_cog(extra(client))

#Need Help? Check out this: {youtube playlist}