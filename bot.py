import discord
from discord.ext import commands 
import datetime
import asyncio
import config, os
import time, random, math
    
#Bot (our bot)
intents=discord.Intents.default()
intents.members=True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('a!', 'A!'), intents=intents) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')


@bot.event
async def on_ready():
    #Message that will be sent when the bot is online.
    print('Bot started succesfully')
    general_channel = bot.get_channel(config.Channels.botChannel)
    await general_channel.send('Hi, I am online again.')
    #Status
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        embed = discord.Embed(description='**Error!** I cannot find that user.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.ChannelNotFound):
        embed = discord.Embed(description='**Error!** I cannot find that channel.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.BotMissingPermissions) or isinstance(error, commands.errors.CommandNotFound) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.CommandInvokeError):
        pass  
    else:
        embed = discord.Embed(description='**Error!** '+str(error), colour=config.Colors.red)
        await ctx.send(embed=embed)

@bot.event
async def on_command(ctx):
    try:
        channel = bot.get_channel(config.Channels.logCommandsChannel)
        embed = discord.Embed(description=f'{ctx.guild.name} - {ctx.author} | {ctx.message.clean_content}', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)
    except Exception:
        pass 

@bot.event
async def on_message(message):
    if message.content == '<@!768309916112650321>':
        titleMsg = f'Information about Al3xis'
        descriptionMsg = f'''
        Hello, I'm Al3xis, a Discord bot developed by Alex22#7756.
        If you want my list of commands, use the command `a!help`.
        If you have any questions related to the bot you can [join my support server](https://discord.com/invite/AAJPHqNXUy).
        Have you found a bug? You can report it using the command `a!report`
        Do you have any suggestion? use the command `a!suggest`
        '''
        infoEmbed = discord.Embed(title=titleMsg, description=descriptionMsg, colour=config.Colors.blue)
        await message.reply(embed=infoEmbed, mention_author=False)
    if message.guild == bot.get_guild(793987455149408309):
        for word in config.BadWords:
            if word in message.content.lower():
                embed = discord.Embed(description=f"{config.Emojis.noEntry} {message.author.mention} your message includes words that are not allowed here. {config.Emojis.noEntry}", colour=config.Colors.red)
                await message.delete()
                botMsg = await message.channel.send(embed=embed)
                logEmbed = discord.Embed(title=f'Message in #{message.channel} was deleted.', description=f'{message.content}\n __**Reason**: Message includes words that are not allowed here.__', colour=config.Colors.red, timestamp=message.created_at)
                logEmbed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
                logChannel = bot.get_channel(config.Channels.logChannel)
                await logChannel.send(embed=logEmbed)
                await asyncio.sleep(4)
                await botMsg.delete()

    if isinstance(message.channel, discord.channel.DMChannel):
        if not message.author.bot:                
            channel = bot.get_channel(config.Channels.DMsChannel)
            embed = discord.Embed(title=f'{message.author.name} sent a DM!', description=message.content, colour=config.Colors.orange, timestamp=message.created_at)
            embed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
            await channel.send(embed=embed)
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.guild == bot.get_guild(793987455149408309):
        if not message.author.bot:
            logEmbed = discord.Embed(title=f'Message in #{message.channel} was deleted.', description=f'{message.content}', colour=config.Colors.red, timestamp=message.created_at)
            logEmbed.set_footer(text=message.author.id, icon_url=message.author.avatar_url)
            logChannel = bot.get_channel(config.Channels.logChannel)
            await logChannel.send(embed=logEmbed)

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(config.Channels.joinsleavesChannel)
    embed = discord.Embed(title='Al3xis was added to a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {guild.member_count}', colour=config.Colors.green)
    embed.set_footer(text=f'{len(bot.guilds)} guilds now', icon_url=guild.icon_url)
    await channel.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(config.Channels.joinsleavesChannel)
    embed = discord.Embed(title='Al3xis was removed from a guild.', description=f'Guild name: {guild.name} \n Guild ID: {guild.id} \n Member count: {guild.member_count}', colour=config.Colors.green)
    embed.set_footer(text=f'{len(bot.guilds)} guilds now', icon_url=guild.icon_url)
    await channel.send(embed=embed)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{len(bot.guilds)} servers | a!help', emoji=None, type=discord.ActivityType.listening))

@bot.event
async def on_member_join(member):
    if member.guild == bot.get_guild(793987455149408309):
        memberRole = discord.utils.get(member.guild.roles, id=829793629236494417)
        await member.add_roles(memberRole, reason='Member Join Event')
        chatChannel = bot.get_channel(config.Channels.chatChannel)
        randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen, config.Colors.gray]
        embed = discord.Embed(description=f'Welcome {member.mention} to the **Alex\'s bots** server!', colour=random.choice(randomColors))
        await chatChannel.send(embed=embed)
        return
    else:
        return

@bot.event
async def on_member_remove(member):
    if member.guild == bot.get_guild(793987455149408309):
        chatChannel = bot.get_channel(config.Channels.chatChannel)
        randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen, config.Colors.gray]
        embed = discord.Embed(description=f'{member.mention} left the server.', colour=random.choice(randomColors))
        await chatChannel.send(embed=embed)
        return
    else:
        return

####################################################################################################
####################################################################################################
##Info Commands

@bot.command(name='about', aliases=['info'])
async def about(ctx):
    embedI = discord.Embed(title=f'Information about Al3xis#4614', colour=config.Colors.blue, timestamp=ctx.message.created_at)
    embedI.add_field(name='Owner', value='`Alex22#7756`')
    embedI.add_field(name='Current Version', value='__[v1.3.8](https://github.com/Alex0622/Al3xis-Bot-dev/releases/tag/v1.3.8)__')
    embedI.add_field(name='Guilds', value=f'`{len(bot.guilds)}`')
    embedI.add_field(name='Prefix', value='`a!`, `A!`')
    embedI.add_field(name='Developed since', value='`21/10/2020`')
    embedI.add_field(name='Developed with', value='`Python`')
    embedI.add_field(name='Useful links', value='[GitHub](https://github.com/Alex0622/Al3xis-Bot-dev/) | [Top.gg](https://top.gg/bot/768309916112650321) | [Discord Bot List](https://discord.ly/al3xis)')
    embedI.add_field(name='Latest updates', value="Removed 'lock' and 'unlock' commands, added 'vote' and 'say' commands, updated 'announce' and 'nick' commands and more.", inline=False)
    embedI.set_thumbnail(url=ctx.me.avatar_url)
    embedI.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embedI, mention_author=False)


@bot.command(name='help', aliases=['h'])
async def help(ctx, arg = None):
    if arg == None:
        helpEmbed = discord.Embed(title = 'Help | Prefix: `a!`, `A!`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        helpEmbed.add_field(name='Info', value='`about`, `help`, `invite`, `ping`, `report`, `source`, `suggest`, `vote`')
        helpEmbed.add_field(name='Utility', value='`announce`, `avatar`, `id`, `membercount`, `nick`, `reminder`, `say`, `servericon`, `userinfo`')
        helpEmbed.add_field(name='Math', value='`calc`, `mathrandom`, `mathsq`, `mathsqrt`')
        helpEmbed.add_field(name='Moderation', value='`ban`, `kick`, `mute`, `pmute`, `purge`, `unban`, `unmute`')
        helpEmbed.add_field(name='Owner', value='`DM`, `embed`, `save`, `updatesuggestion`')
        helpEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=helpEmbed, mention_author=False)
        return
    if str(arg).lower() == 'info':
        titleEmbed = 'Info commands'
        descEmbed = f'''
        `about` - {config.InfoCommands.about}
        `help` - {config.InfoCommands.help}
        `invite` - {config.InfoCommands.invite}
        `ping` - {config.InfoCommands.ping}
        `report` - {config.InfoCommands.report}
        `source` - {config.InfoCommands.source}
        `suggest` - {config.InfoCommands.suggest}
        `vote` - {config.InfoCommands.vote}'''
        infoEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        infoEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=infoEmbed, mention_author=False)
        return
    if str(arg).lower() == 'utility':
        titleEmbed = 'Utility commands'
        descEmbed = f'''
        `announce` - {config.InfoCommands.announce}
        `avatar` - {config.InfoCommands.avatar}
        `id` - {config.InfoCommands.id}
        `membercount` - {config.InfoCommands.membercount}
        `nick` - {config.InfoCommands.nick}
        `reminder` - {config.InfoCommands.reminder}
        `say` - {config.InfoCommands.say}
        `servericon` - {config.InfoCommands.servericon}
        `userinfo`- {config.InfoCommands.userinfo}'''
        utilityEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        utilityEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=utilityEmbed, mention_author=False)
        return
    if str(arg).lower() == 'math':
        titleEmbed = 'Math commands'
        descEmbed = f'''
        `calc` - {config.InfoCommands.calc}
        `mathrandom` - {config.InfoCommands.mathrandom}
        `mathsq` - {config.InfoCommands.mathsq}
        `mathsqrt` - {config.InfoCommands.mathsqrt}'''
        mathEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        mathEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=mathEmbed, mention_author=False)
        return
    if str(arg).lower() == 'moderation':
        titleEmbed = 'Moderation commands'
        descEmbed = f'''
        `ban` - {config.InfoCommands.ban}
        `kick`- {config.InfoCommands.kick}
        `mute` - {config.InfoCommands.mute}
        `pmute` - {config.InfoCommands.pmute}
        `purge` - {config.InfoCommands.purge}
        `unban` - {config.InfoCommands.unban}
        `unmute` - {config.InfoCommands.unmute}'''
        moderationEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        moderationEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=moderationEmbed, mention_author=False)
        return
    if str(arg).lower() == 'owner':
        titleEmbed = 'Owner commands'
        descEmbed = f'''
        `DM` - {config.InfoCommands.DM}
        `embed` - {config.InfoCommands.embed}
        `save` - {config.InfoCommands.save}
        `updatesuggestion` -{config.InfoCommands.updatesuggestion}'''
        ownerEmbed = discord.Embed(title=titleEmbed, description=descEmbed, colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        ownerEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=ownerEmbed, mention_author=False)
        return
    else:
        arg = str(arg).lower()
        embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{getattr(config.AliasesCommands, arg)}`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
        embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
        embed.add_field(name='Required permissions', value='`'+getattr(config.RequiredPermissions, arg)+'`', inline=False)
        embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
        return
        

@bot.command(name='invite', aliases=['inv'])
async def invite(ctx):
    embed = discord.Embed(title='Links', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
    embed.add_field(name='Join our Discord server!', value="[Alex's bots](https://discord.gg/AAJPHqNXUy)", inline=False)
    embed.add_field(name='Invite the bot to your server', value='[Admin permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=8) \n[Required permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=134556758)')
    embed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name='ping', aliases=['pong', 'latency'])
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.reply("Pong!", mention_author=False)
    time.sleep(2)
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**Bot's ping:**  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.command(name='report')
async def report(ctx, *, msg=None):
    if msg != None:
        try:
            botMsg = await ctx.reply(f'Saving report {config.Emojis.loading}', mention_author=False)
            await asyncio.sleep(2)
            embed = discord.Embed(title=f'Report made by {ctx.author.name}', description=msg, colour=config.Colors.purple, timestamp=ctx.message.created_at)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            print(f'{ctx.author} reported: {msg}')
            channel = bot.get_channel(config.Channels.reportsChannel)
            await channel.send(content='',embed=embed)
            
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await botMsg.edit(content='Thanks for your report!, and Admin will review your report as soon as possible.')
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await botMsg.edit(content='', embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return
    else:
        embed = discord.Embed(description="Please provide a description for your report.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='source')
async def source(ctx):
    embed = discord.Embed(title=f"{ctx.me.name}'s source", description='Hi!, you can find my source code [here](https://github.com/Alex0622/Al3xis-Bot-dev/).', colour=config.Colors.yellow)
    await ctx.reply(embed=embed, mention_author=False)


suggestion = ''
listSuggestions = ''
@bot.command(name='suggest', aliases=['sug'])
async def suggest(ctx, *, new_suggestion=None):
    if new_suggestion == None:
        embed = discord.Embed(description='Please add a suggestion in your message.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        global suggestion
        suggestion =  new_suggestion
        description = suggestion 
        msg = await ctx.reply('Saving suggestion...', mention_author=False)
        time.sleep(2)
        embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description=description, colour=config.Colors.green, timestamp=ctx.message.created_at)
        embed.set_footer(text=ctx.author.id)
        suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
        message = await suggestions_channel.send(f'Status: **Pending** {config.Emojis.loading}', embed=embed)
        await message.add_reaction(config.Emojis.ballotBoxWithCheck)
        await message.add_reaction(config.Emojis.x)
        print('New suggestion: ' + suggestion)      
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await msg.edit(content=f'Thanks for your suggestion: {suggestion}', allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await msg.edit(content='', embed=errorEmbed)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return


@bot.command(name='vote')
async def vote(ctx):
    voteEmbed = discord.Embed(description='''Hi, you can vote me on the following websites:
    1. [Top.gg](https://top.gg/bot/768309916112650321)
    2. [Discord Bot List](https://discordbotlist.com/bots/al3xis)
    3. [Discord Boats](https://discord.boats/bot/768309916112650321)
     ''', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
    voteEmbed.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=voteEmbed, mention_author=False)

####################################################################################################
####################################################################################################
##Utility Commands

@bot.command(name='announce', aliases=['announcement', 'ann'])
@commands.guild_only()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_messages=True)
async def announce(ctx, channel : discord.TextChannel=None, *, announceMsg=None):
    if not channel:
        embed = discord.Embed(description='Please provide a Discord channel for the announcement!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if not announceMsg:
        embed = discord.Embed(description='Please provide the text for the announcement!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        def check(reaction, user):
            return user.id == ctx.author.id and reaction.message.id == botMsg.id
        botMsg = await ctx.send('Do you want to send this message in an embed?')
        await botMsg.add_reaction(config.Emojis.whiteCheckMark)
        await botMsg.add_reaction(config.Emojis.x)
        react, user = await bot.wait_for('reaction_add', check=check, timeout=120)
        if str(react) == config.Emojis.whiteCheckMark:
            try:
                await botMsg.clear_reactions()
            except Exception:
                pass
            randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
            AnnounceEmbed = discord.Embed(description=announceMsg, colour=random.choice(randomColors))
            await channel.send(embed=AnnounceEmbed)
            await botMsg.edit(content='Announcement sent sucessfully.')
            return

        if str(react) == config.Emojis.x:
            try:
                await botMsg.clear_reactions()
            except Exception:
                pass
            await channel.send(announceMsg)
            await botMsg.edit(content='Announcement sent sucessfully.')
            return 
    except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return

@announce.error
async def announce_error(ctx, error):
    if isinstance(error,commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** Only administrators of this server can use that command!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE MESSAGES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='avatar', aliases=['av'])
@commands.guild_only()
async def avatar(ctx, *, member: discord.Member = None):
    if member == None:
        member = ctx.author
    user = await bot.fetch_user(member.id)
    embed = discord.Embed(title = f'Avatar of user {user}', colour=config.Colors.green, timestamp=ctx.message.created_at)
    embed.set_image(url='{}'.format(user.avatar_url))
    await ctx.send(embed=embed)


@bot.command(name='id', aliases=['ID'])
@commands.guild_only()
async def id(ctx, *, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await ctx.reply(member.id, mention_author=False)


@bot.command(name='membercount')
@commands.guild_only()
async def membercount(ctx):
    embed = discord.Embed(description=f'There are **{ctx.guild.member_count} members** in this server.', colour=config.Colors.lightBlue)
    await ctx.reply(embed=embed, mention_author=False)


@bot.command(name='nick', aliases=['setnick'])
@commands.guild_only()
@commands.has_permissions(change_nickname=True)
@commands.bot_has_permissions(manage_nicknames=True)
async def nick(ctx, *, new_nick=None):
    embed = discord.Embed(description=f'Updating nick {config.Emojis.loading}', colour=config.Colors.gray)
    if new_nick:
        botmsg = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        if ctx.author.top_role.position >= ctx.guild.me.top_role.position:
            embed = discord.Embed(description="I cannot change your nickname because you have the same role as me or your top role is above mine.", colour=config.Colors.red)
            await botmsg.edit(embed=embed)
            return   
        else:         
            if str(new_nick).lower() == 'reset':
                if ctx.author.nick == None:
                    embedDesc = "You don't have a nickname!"
                    color = config.Colors.red
                else:
                    await ctx.author.edit(nick=ctx.author.name)
                    embedDesc = f"{config.Emojis.whiteCheckMark} I've removed your nickname."
                    color = config.Colors.green
                embed2 = discord.Embed(description=embedDesc, colour=color)
                await botmsg.edit(embed=embed2)
                return
            if new_nick == ctx.author.nick:
                embed3 = discord.Embed(description="You already have that nickname, please select a different one!", colour=config.Colors.red)
                await botmsg.edit(embed=embed3)
                return
            else:
                await ctx.author.edit(nick=new_nick)
                embed4 = discord.Embed(description=f'{config.Emojis.whiteCheckMark} Your new nickname is: {new_nick}', colour=config.Colors.green)
                await botmsg.edit(embed=embed4)
                return
    else:
        if ctx.author.nick == None:
            desc = 'You don\'t have a current nickname.'
            color = config.Colors.red
        else:
            desc = f'Your current nick is: {ctx.author.nick}'
            color = config.Colors.orange
        embed = discord.Embed(description=desc, colour=color)
        await ctx.channel.send(embed=embed)
        return  

@nick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `CHANGE NICKNAME` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE NICKNAMES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

    
@bot.command(name='reminder', aliases=['remind'])
async def reminder(ctx, time=None, *, msg=None):
    if time != None:
        if msg != None:
            await asyncio.sleep(0.5)
            seconds = 0
            if time.lower().endswith("d"):
                seconds += int(time[:-1]) * 60 * 60 * 24
                counter = f"{seconds // 60 // 60 // 24} days"
            elif time.lower().endswith("h"):
                seconds += int(time[:-1]) * 60 * 60
                counter = f"{seconds // 60 // 60} hours"
            elif time.lower().endswith("m"):
                seconds += int(time[:-1]) * 60
                counter = f"{seconds // 60} minutes"
            elif time.lower().endswith("s"):
                seconds += int(time[:-1])
                counter = f"{seconds} seconds"
            else:
                embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                await ctx.send(embed=embed)
                return  

            await ctx.reply(f"I've set a reminder of {counter}: {msg}", mention_author=False, allowed_mentions=discord.AllowedMentions.none())
            await asyncio.sleep(seconds)
            await ctx.reply(f'Hey! {msg}', mention_author=True, allowed_mentions=discord.AllowedMentions.none())
        else: 
            embed = discord.Embed(description="Please provide a message for your reminder.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="Please provide a period of time for your reminder.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@reminder.error
async def reminder_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        if str('Unknown message') in str(error):
            await ctx.send(f"Hey {ctx.author.mention} please don't delete your message when using `{ctx.prefix}{ctx.command}`")
            return
        if str('ValueError') in str(error): 
            embed = discord.Embed(description=f'**Error!** Your message does not include a valid duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 


@bot.command(name='say')
@commands.guild_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def say(ctx, *, sayMsg=None):
    if not sayMsg:
        embed = discord.Embed(description='Please provide a message!', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:
        try:
           await ctx.message.delete()
        except Exception:
           pass
        await ctx.send(sayMsg, allowed_mentions=discord.AllowedMentions.none())
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return


@bot.command(name='servericon')
@commands.guild_only()
async def servericon(ctx):
    embed = discord.Embed(title = f'Icon of {ctx.guild}', colour=config.Colors.green, timestamp=ctx.message.created_at)
    embed.set_image(url='{}'.format(ctx.guild.icon_url))
    await ctx.send(embed=embed)


@bot.command(name='userinfo', aliases=['user', 'ui'])
@commands.guild_only()
async def userinfo(ctx, *, member: discord.Member=None):
    if member is None:
        member = ctx.author
    try:
        mentions = []
        for role in member.roles:
            if role.name != "@everyone":
                mentions.append(role.mention)
        roleS = ", ".join(mentions)

        if roleS == '':
            ROLES = f'No roles to show here {config.Emojis.eyes}'
        else:
            ROLES = roleS

        if member.bot:
            isBotMsg = 'Yes'
        else:
            isBotMsg = 'No'

        userinfoEmbed = discord.Embed(title=str(member), description=f'__**Information about**__ {member.mention} \n**User ID**: {member.id} \n**Created at** {member.created_at.strftime("%A %d %B %Y, %H:%M")} \n**Joined at** {member.joined_at.strftime("%A %d %B %Y, %H:%M")} \n **Bot?**: {isBotMsg}', colour=config.Colors.darkGreen, timestamp=ctx.message.created_at)
        userinfoEmbed.set_thumbnail(url=member.avatar_url)
        userinfoEmbed.add_field(name='**Roles**', value=ROLES)
        await ctx.reply(embed=userinfoEmbed, mention_author=False)
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return

####################################################################################################
####################################################################################################
#Math commands

def add(x:float, y:float):
    return x + y
def sub(x:float, y:float):
    return x - y
def mult(x:float, y:float):
    return x * y
def div(x:float, y:float):
    return x / y
def rando(x:int, y:int):
    return random.randint(x, y)
def sqrt(x:float):
    return math.sqrt(x)
def sq(x:float):
    return x * x

@bot.command(name='calc', aliases=['calculator'])
async def calc(ctx, x:float=None, arg=None, y:float=None):
    if arg != None:
        if x != None:
            if y != None:
                if arg == '+':
                    result = add(x, y)
                    await ctx.reply(result, mention_author=False)
                    return
                if arg == '-':
                    result = sub(x, y)
                    await ctx.reply(result, mention_author=False)
                    return
                if arg == '*':
                    result = mult(x, y)
                    await ctx.reply(result, mention_author=False)
                    return
                if arg == '/':
                    result = div(x, y)
                    await ctx.reply(result, mention_author=False)
                    return
                else:
                    embed = discord.Embed(description=f'"{arg}" is not a valid option!', colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return   
            else:
                embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
                await ctx.send(embed=embed)
                return    
        else:
            embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return      
    else:
        embed = discord.Embed(description=f'Please provide a math argument (+ - * /)', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 

@calc.error
async def calc_error(ctx, error):
    if str(error) == 'Command raised an exception: ZeroDivisionError: float division by zero':
        await ctx.reply('Math ERROR.', mention_author=False)
        return
    if str('Converting to "float"') in str(error):
        embed = discord.Embed(description=f'Please provide a valid math equation. \nNote: Rememeber to add spaces between arguments. (e.g. `a!calc 1 + 1`)', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 


@bot.command(name='mathrandom')
async def mathrandom(ctx, x:int=None, y:float=None):
    if x != None:
        if y != None:
            result = rando(x, y)
            await ctx.reply(result, mention_author=False)
        else:
            embed = discord.Embed(description='You are missing the argument "y".', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return    
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 

@mathrandom.error
async def mathrandom_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(description='The order of your values must be from lowest to highest. \n Note: Only use numbers.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  


@bot.command(name='mathsq')
async def mathsq(ctx, x:float=None):
    if x != None:      
        result = sq(x)
        await ctx.reply(result, mention_author=False)
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  


@bot.command(name='mathsqrt')
async def mathsqrt(ctx, x:float=None):
    if x != None:          
        result = sqrt(x)
        await ctx.reply(result, mention_author=False)
    else:
        embed = discord.Embed(description='You are missing the argument "x".', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return  


####################################################################################################
####################################################################################################
##Moderation commands

@bot.command(name='ban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member.top_role > ctx.me.top_role:
        embed = discord.Embed(description="I cannot ban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return   
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)    
                        await ctx.send(f'**{member}** was banned | `{reason}`')
                        try:
                            await member.send(f'You were banned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.ban(reason=f'{ctx.author}: {reason}')
                        print(f'User {ctx.author} banned {member} | {reason}')
                        logEmbed = discord.Embed(title=f'Case: `ban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception as e:
                        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                        await ctx.reply(embed=errorEmbed, mention_author=False)
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to ban that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't ban me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't ban yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to ban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='kick', pass_context=True)
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member.top_role > ctx.me.top_role:
        embed = discord.Embed(description="I cannot kick that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)
                        await ctx.send(f'**{member}** was kicked | `{reason}`')
                        try:
                            await member.send(f'You were kicked from server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.kick(reason=f'{ctx.author}: {reason}')
                        print(f'User {ctx.author} kicked {member} in server {guild.name}| {reason}')
                        logEmbed = discord.Embed(title=f'Case: `kick`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel = bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)       
                    except Exception as e:
                        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                        await ctx.reply(embed=errorEmbed, mention_author=False)
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to kick that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't kick me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't kick yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to kick.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='mute')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member, duration=None, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member.top_role > ctx.me.top_role:
        embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if not mutedRole in member.roles:
                            if duration:
                                time.sleep(0.5)
                                seconds = 0
                                if duration.lower().endswith("d"):
                                    seconds += int(duration[:-1]) * 60 * 60 * 24
                                    counter = f"{seconds // 60 // 60 // 24} days"
                                elif duration.lower().endswith("h"):
                                    seconds += int(duration[:-1]) * 60 * 60
                                    counter = f"{seconds // 60 // 60} hours"
                                elif duration.lower().endswith("m"):
                                    seconds += int(duration[:-1]) * 60
                                    counter = f"{seconds // 60} minutes"
                                elif duration.lower().endswith("s"):
                                    seconds += int(duration[:-1])
                                    counter = f"{seconds} seconds"
                                else:
                                    embed = discord.Embed(description=f'**Error!** "{time}" is not a valid duration.', colour=config.Colors.red)
                                    await ctx.send(embed=embed)
                                    return 
                                
                                await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                await ctx.send(f'**{member}** was muted for {counter} | `{reason}`')
                                try:                    
                                    await member.send(f'You were muted in server: **{guild.name}** for {counter} | `{reason}`')
                                except Exception:
                                    pass
                                print(f'User {ctx.author} muted {member} in server {guild.name} for {counter} | {reason}')
                                logEmbed = discord.Embed(title=f'Case: `mute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                                logEmbed.add_field(name='User', value=member.mention)   
                                logEmbed.add_field(name='Reason', value=reason) 
                                logEmbed.add_field(name='Duration', value=counter)
                                logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                logChannel=bot.get_channel(config.Channels.logChannel)
                                await logChannel.send(embed=logEmbed)   

                                await asyncio.sleep(seconds) 
                                await member.remove_roles(mutedRole, reason='Temporary mute completed!')
                                reason = 'Temporary mute completed!'
                                try:
                                    await member.send(f'You were unmuted in server: **{guild.name}** | `{reason}`')
                                except Exception:
                                    pass
                                print(f'User {member} was unmuted in server {guild.name} | {reason}')
                                logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                logEmbed.add_field(name='User', value=member.mention)
                                logEmbed.add_field(name='Reason', value=reason) 
                                logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                logChannel=bot.get_channel(config.Channels.logChannel)
                                await logChannel.send(embed=logEmbed)
                                return
                            else:
                                embed = discord.Embed(description='Please specify an amount of time to mute that member.', colour=config.Colors.red)
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(description=f'**{member}** is already muted.', colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return
                    else:
                        embed = discord.Embed(description="**Error!** You don't have permissions to mute that member.", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="You can't mute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:   
        embed = discord.Embed(description='**Error!** This server does not have a Muted role. Please make one named `Muted`.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return 

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.CommandInvokeError):
        if str('ValueError') in str(error): 
            embed = discord.Embed(description=f'**Error!** Your message does not include a valid duration.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return 


@bot.command(name='pmute', aliases= ['pm'])
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def pmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member.top_role > ctx.me.top_role:
        embed = discord.Embed(description="I cannot mute that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.ban_members:
                        if not mutedRole in member.roles:
                            try:
                                time.sleep(0.5)
                                await member.add_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                                await ctx.send(f'**{member}** was permanently muted | `{reason}`')
                                try:
                                    await member.send(f'You were permanently muted in server: **{guild.name}** | `{reason}`')
                                except Exception:
                                    pass
                                print(f'User {ctx.author} permanently muted {member} in server {guild.name} | {reason}')
                                logEmbed = discord.Embed(title=f'Case: `mute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                                logEmbed.add_field(name='User', value=member.mention)
                                logEmbed.add_field(name='Reason', value=reason) 
                                logEmbed.add_field(name='Duration', value=f'Permanently')
                                logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                logChannel=bot.get_channel(config.Channels.logChannel)
                                await logChannel.send(embed=logEmbed)  
                                return

                            except Exception as e:
                                errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                                await ctx.reply(embed=errorEmbed, mention_author=False)
                                await ctx.message.add_reaction(config.Emojis.noEntry)
                                return

                        else:
                            embed = discord.Embed(description=f'**{member}** is already muted.', colour=config.Colors.red)
                            await ctx.send(embed=embed)
                            return 
                    else:
                        embed = discord.Embed(description=f"**Error!** You don't have permissions to mute that member!", colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="You can't mute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't mute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:   
        embed = discord.Embed(description='**Error!** This server does not have a Muted role. Please make one named `Muted`.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return   

@pmute.error
async def pmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to mute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='purge', aliases=['clear'])
@commands.guild_only()
@commands.bot_has_permissions(manage_messages=True)
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 0):
    guild = ctx.guild
    if amount <= 500:
        if amount >=1:
            await ctx.channel.purge(limit=amount)
            e = discord.Embed(description=f'Deleted {amount} messages {config.Emojis.loading}', colour=config.Colors.red)
            botMsg = await ctx.send(embed=e)
            await asyncio.sleep(5)
            await botMsg.delete()
            logEmbed = discord.Embed(title=f'Case: `purge`', colour=config.Colors.orange, timestamp=ctx.message.created_at)
            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
            logEmbed.add_field(name='Channel', value=ctx.message.channel.mention)
            logEmbed.add_field(name='Deleted messages', value=f'{amount} message(s).')
            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
            logChannel=bot.get_channel(config.Channels.logChannel)
            await logChannel.send(embed=logEmbed)
            print(f'{ctx.message.author} deleted {amount} messages using the purge command in server {guild.name}.')
    if amount > 500:
        await ctx.send(f'You can only purge **500** messages at a time and you tried to delete **{amount}**.')
        print(f'{ctx.message.author} tried to delete {amount} messages with the purge command in server {guild.name}.')
        return
    if amount == 0:
        embed = discord.Embed(description='Select an amount of messages to purge.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `MANAGE MESSAGES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `MANAGE MESSAGES` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='softban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def softban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member.top_role > ctx.me.top_role:
        embed = discord.Embed(description="I cannot softban that user because they have the same role as me or their top role is above mine.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)
                        await ctx.send(f'**{member}** was softbanned | `{reason}`')
                        try:
                            await member.send(f'You were softbanned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        await member.ban(reason=f'{ctx.author}: {reason}', delete_message_days=5)
                        await member.unban(reason=f'{ctx.author}: softban')
                        print(f'User {ctx.author} softbanned {member} in server {guild.name}| {reason}')
                        logEmbed = discord.Embed(title=f'Case: `softban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel = bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)       
                    except Exception as e:
                        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                        await ctx.reply(embed=errorEmbed, mention_author=False)
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    embed = discord.Embed(description="**Error!** You don't have permissions to softban that member.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else: 
            embed = discord.Embed(description="You can't softban me.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You can't softban yourself.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@softban.error
async def softban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to softban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='unban')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, UserID: int, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    member = await bot.fetch_user(UserID)
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                try:
                    await ctx.guild.fetch_ban(discord.Object(id=member.id))
                    try:
                        time.sleep(0.5)
                        await ctx.guild.unban(member, reason=f'{ctx.author}: {reason}')
                        await ctx.send(f'**{member}** was unbanned | `{reason}`')
                        try:
                            await member.send(f'You were unbanned in server: **{guild.name}** | `{reason}`')
                        except Exception:
                            pass
                        print(f'User {ctx.author} unbanned {member} from {guild.name} | {reason}')
                        logEmbed = discord.Embed(title=f'Case: `unban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception as e:
                        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                        await ctx.reply(embed=errorEmbed, mention_author=False)
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                except discord.NotFound:
                    embed = discord.Embed(description='That user is not banned here.', colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return     
            else:
                embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="I'm not banned...", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description="You are not banned here...", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to unban.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='unmute')
@commands.guild_only()
@commands.bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if mutedRole in member.roles:
                        try:
                            time.sleep(0.5)
                            await member.remove_roles(mutedRole, reason=f'{ctx.author}: {reason}')
                            await ctx.send(f'**{member}** was unmuted | `{reason}`')
                            try:
                                await member.send(f'You were unmuted in server: **{guild.name}** | `{reason}`')
                            except Exception:
                                pass
                            print(f'User {ctx.author} unmuted {member} in server {guild.name} | {reason}')
                            logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                            logEmbed.add_field(name='User', value=member.mention)
                            logEmbed.add_field(name='Reason', value=reason) 
                            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                            logChannel=bot.get_channel(config.Channels.logChannel)
                            await logChannel.send(embed=logEmbed)     
                        except Exception as e:
                            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                            await ctx.reply(embed=errorEmbed, mention_author=False)
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            return
                    else:
                        embed = discord.Embed(description=f'**{member}** is not muted.', colour=config.Colors.red)
                        await ctx.send(embed=embed)
                        return 
                else:
                    embed = discord.Embed(description="I can't interact with bots.", colour=config.Colors.red)
                    await ctx.send(embed=embed)
                    return
            else: 
                embed = discord.Embed(description="You can't unmute me.", colour=config.Colors.red)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(description="You can't unmute yourself.", colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        await ctx.send("I can't find any muted role here. Guess nobody is muted.")
        return

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(description='Please specify a member to unmute.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.errors.MissingPermissions):
        embed = discord.Embed(description='**Error!** You need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description='**Error!** I need the permission `BAN MEMBERS` to run this command.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return

####################################################################################################
####################################################################################################
##Owner commands

@bot.command(name='DM', aliases=['dm', 'msg'])
@commands.guild_only()
@commands.is_owner()
async def DM(ctx, member: discord.Member=None, *, msg=None):
    if member != None:
        if msg != None:
            botMsg = await ctx.send(f'DMing user {config.Emojis.loading}')
            await asyncio.sleep(2)
            embed = discord.Embed(description=msg, colour=config.Colors.orange)
            embed.set_footer(text=f'Sent by {ctx.author}', icon_url=ctx.author.avatar_url)
            try:
                await member.send(embed=embed)
                logEmbed = discord.Embed(title=f'{ctx.author.name} has sent a DM to {member.name}', description=msg, colour=config.Colors.orange, timestamp=ctx.message.created_at)
                logEmbed.set_footer(text=member, icon_url=member.avatar_url)
                DMs_channel = bot.get_channel(config.Channels.DMsChannel)
                await DMs_channel.send(embed=logEmbed)
                await botMsg.edit(content=f'DM sent successfully! {config.Emojis.whiteCheckMark}')
            except Exception as e:
                errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
                await ctx.reply(embed=errorEmbed, mention_author=False)
                await ctx.message.add_reaction(config.Emojis.noEntry)
                return
        
        else:
            embed = discord.Embed(description='Please provide a description for your embed.', colour=config.Colors.red)
            await ctx.send(embed=embed)
            return
    else:
        embed = discord.Embed(description='Please specify a member to DM.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return


@bot.command(name='embed')
@commands.guild_only()
@commands.is_owner()
async def embed(ctx, *, embedMsg=None):
    randomColors = [config.Colors.red, config.Colors.lightBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
    if embedMsg == None:
        embed = discord.Embed(description=savedMessageSave, colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    else:
        embed = discord.Embed(description=embedMsg  , colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return


savedMessageSave = ''
@bot.command(name='save')
@commands.guild_only()
@commands.is_owner()
async def save(ctx,*, saveMsg=None):
    global savedMessageSave
    savedMessageSave = saveMsg
    if saveMsg == None:
        embed = discord.Embed(description='Please provide a description for your embed.', colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    else:
        try:
            firstMessage = await ctx.send('Saving message...')
            await ctx.message.delete()
            time.sleep(3)
            embed = discord.Embed(title=f'{ctx.author} saved a new message.', description=savedMessageSave, colour=config.Colors.green, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Guild: {ctx.guild}')
            savedMessagesChannel = bot.get_channel(config.Channels.ownerChannel)
            await savedMessagesChannel.send(embed=embed)
            print(f'New message saved sent by {ctx.author} | {savedMessageSave}')
            await firstMessage.edit(content=f'**{ctx.author}** Your message has been saved!')
        except Exception as e:
            errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
            await ctx.reply(embed=errorEmbed, mention_author=False)
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return


@bot.command(name='us', aliases=['updatesuggestion'])
@commands.guild_only()
@commands.is_owner()
async def us(ctx, msgID:int=None, type=None, *, reason=None):
    if msgID == None:
        embed = discord.Embed(description="Please provide the message ID.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if type == None:
        embed = discord.Embed(description="Please provide if the suggestion should be approved `(a)` or denied `(d)`.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    if reason == None:
        embed = discord.Embed(description="You need to provide a reason.", colour=config.Colors.red)
        await ctx.send(embed=embed)
        return
    try:    
        if str(type).lower() == 'accept':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Accepted** {config.Emojis.whiteCheckMark} | Reason: {reason}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.clear_reaction(emoji1)
            await msg.clear_reaction(emoji2)
            botMsg = await ctx.reply(f'{config.Emojis.whiteCheckMark} Suggestion was successfully accepted.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
            return
        if str(type).lower() == 'deny':
            Suggestionschannel = await bot.fetch_channel(config.Channels.suggestionsChannel)
            msg = await Suggestionschannel.fetch_message(msgID)
            await msg.edit(content=f'Status: **Denied** {config.Emojis.noEntry} | Reason: {reason}')
            emoji1 = config.Emojis.ballotBoxWithCheck
            emoji2 = config.Emojis.x
            await msg.clear_reaction(emoji1)
            await msg.clear_reaction(emoji2)
            botMsg = await ctx.reply(f'{config.Emojis.whiteCheckMark} Suggestion was successfully denied.', mention_author=False)
            await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
            await asyncio.sleep(5)
            await botMsg.delete()
            return
    except Exception as e:
        errorEmbed= discord.Embed(description=f'An error occurred while running that command: {e}', colour=config.Colors.red)
        await ctx.reply(embed=errorEmbed, mention_author=False)
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return
    
  
################################
####################################################################################################
####################################################################################################
#Run the bot on Discord.
bot.run(os.environ['discordToken'])


