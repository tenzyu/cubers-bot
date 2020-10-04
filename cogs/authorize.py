from textwrap import dedent

import constant
import discord
from discord.ext import commands


class Authorize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if (reaction.channel_id != constant.CH_AUTHORIZE_ID
                or reaction.message_id != constant.MESSAGE_AUTHORIZE_ID):
            return

        member = reaction.member
        guild = self.bot.get_guild(reaction.guild_id)
        role_authorized = guild.get_role(constant.ROLE_AUTHORIZED_ID)
        role_member = guild.get_role(constant.ROLE_MEMBER_ID)

        channel = self.bot.get_channel(constant.CH_AUTHORIZE_ID)
        message = await channel.fetch_message(constant.MESSAGE_AUTHORIZE_ID)

        if not role_authorized in member.roles:
            ch_introduction = self.bot.get_channel(constant.CH_INTRODUCTION_ID)
            await member.add_roles(role_authorized)
            await member.add_roles(role_member)
            await self.bot.get_channel(constant.CH_NOTICE_JOIN_ID).send(dedent(f"""\
                **Hi {member.mention}, welcome to {guild.name} !**
                Please tells us about yourself! {ch_introduction.mention}
                Ja: よければ自己紹介をお願いします！ {ch_introduction.mention}
                """))
        # await message.remove_reaction(reaction.emoji, member


def setup(bot):
    bot.add_cog(Authorize(bot))
