from textwrap import dedent

import constant
import discord
from discord.ext import commands


class Authorize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if not (reaction.channel_id == constant.CH_AUTHORIZE_ID
                and reaction.message_id == constant.MESSAGE_AUTHORIZE_ID):
            return

        guild = self.bot.get_guild(reaction.guild_id)
        role_members = guild.get_role(constant.ROLE_MEMBERS_ID)
        member = reaction.member

        if not role_members in member.roles:
            ch_introduction = self.bot.get_channel(constant.CH_INTRODUCTION_ID)
            await member.add_roles(role_members)
            await self.bot.get_channel(constant.CH_NOTICE_JOIN_ID).send(dedent(f"""\
                :tada: **Hi {member.mention}, welcome to {guild.name} !**
                Please tells us about yourself! {ch_introduction.mention}
                Ja: よければ自己紹介をお願いします！ {ch_introduction.mention}
                """))


def setup(bot):
    bot.add_cog(Authorize(bot))
