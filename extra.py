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

    @commands.command(description="🍜 Command for them anime weebs.")
    @commands.cooldown(1, 1.8, commands.BucketType.user)
    async def weeb(self, ctx, page_choice:int=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!weeb"):
                gifs_list = await api.gif.all(ctx, self.client, "anime", 50)
                BUTTONS = ["◀️", "▶️"]
                weeb_embed_dict = {}
                page_count = 1
                weeb_bt_current_page = 1
                weeb_embed_dict[1] = {}
                message = None

                #Create pages accoring to the amount of items.
                for gif in gifs_list:
                    new_embed = await weeb.create(gif)
                    weeb_embed_dict[page_count] = {}
                    weeb_embed_dict[page_count]["embed_obj"] = new_embed
                    page_count += 1

                weeb_embed_dict["max_pages"] = (page_count - 1)

                #Apply footer to all pages.
                for page in weeb_embed_dict:
                    if not page == "max_pages":
                        embed = weeb_embed_dict[int(page)]["embed_obj"]
                        max_pages = weeb_embed_dict["max_pages"]
                        embed.set_footer(text=f"[PAGE {page}/{max_pages}] " + msg.footer.type_2)
                
                #Start of Command
                if not page_choice == None:
                    try:
                        message = await ctx.send(embed=weeb_embed_dict[page_choice]["embed_obj"])
                        weeb_bt_current_page = page_choice
                    except KeyError:
                        await ctx.send(msg.shop.page_out_of_range.format(ctx.author.mention))
                else:
                    message = await ctx.send(embed=weeb_embed_dict[1]["embed_obj"])
                
                if not message == None: #Start reactions.
                    #Add reactions.
                    for button in BUTTONS:
                        await message.add_reaction(button)

                    #Wait for user inputs.
                    while True:
                        try:
                            reaction, user = await goldy_cache.client.wait_for('reaction_add', timeout=360)
                            if not user == goldy_cache.client.user: #Ignores reactions from itself.
                                if user == ctx.author: #Only change page if author is reacting.
                                    if reaction.message == message:
                                        if reaction.emoji == BUTTONS[0]: #Backwards button.
                                            if not weeb_bt_current_page <= 1: #Stops page num from going under 1.
                                                weeb_bt_current_page -= 1
                                                await weeb.change(message, page=weeb_bt_current_page, weeb_embed_dict=weeb_embed_dict)
                                                await message.remove_reaction(reaction.emoji, user)
                                            else:
                                                await message.remove_reaction(reaction.emoji, user)

                                        if reaction.emoji == BUTTONS[1]: #Forwards button.
                                            if not weeb_bt_current_page >= weeb_embed_dict["max_pages"]:
                                                weeb_bt_current_page += 1 #Stops page num from going over max amount.
                                                await weeb.change(message, page=weeb_bt_current_page, weeb_embed_dict=weeb_embed_dict)
                                                await message.remove_reaction(reaction.emoji, user)
                                            else:
                                                await message.remove_reaction(reaction.emoji, user)

                        except asyncio.TimeoutError:
                            #Clear reactions first.
                            for button in BUTTONS:
                                await message.clear_reaction(button)

                            break #Stop loop
            else:
                await ctx.send(msg.error.do_not_have_item.format(ctx.author.mention))

    @weeb.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await cmds.cooldown.msg_send(ctx, error)
        if isinstance(error, (commands.MemberNotFound, commands.ExpectedClosingQuoteError)):
            await ctx.send(msg.error.member_not_found.format(ctx.author.mention))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.weeb")

class weeb():
    @staticmethod
    async def get_gif(ctx, gifs_list, page): #Grabs the correct number of items to view in page. (Used to only grab a certain amount of items for the shop page)
        return gifs_list[page]

    @staticmethod
    async def change(msg_obj, page, weeb_embed_dict): #Method that changes the shop command page.
        await msg_obj.edit(embed=weeb_embed_dict[page]["embed_obj"])

    @staticmethod
    async def create(gif_url):
        embed=nextcord.Embed(title="**🍜 __Random Anime Gifs__**", 
        description=f"Idk why I made this knowing what images show up on Giphy but here you go.", 
        color=settings.PURPLE)
        embed.set_image(url=gif_url)
        return embed

def setup(client):
    client.add_cog(extra(client))

#Need Help? Check out this: {youtube playlist}