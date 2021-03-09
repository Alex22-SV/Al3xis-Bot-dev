import discord 
from discord.ext import commands 
import datetime
import asyncio
import config, os
import time, random
    
#Bot (our bot)
bot = commands.Bot(command_prefix=['a!', 'A!']) #Set the prefix of the bot and removes the default help command.
bot.remove_command(name='help')


@bot.event
async def on_ready():
    #Message that will be sent when the bot is online.
    print('Bot started succesfully')
    general_channel = bot.get_channel(config.Channels.botChannel)
    await general_channel.send('Hi, I am online again.')
    #Status
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name='a!help for help :p', emoji=None, type=discord.ActivityType.listening))









####################################################################################################
####################################################################################################
##Normal Commands



@bot.command(name='help', aliases=['h'])
async def help(ctx, arg = None):
    if arg == None:
        helpEmbed = discord.Embed(title = 'Help | Prefix: `a!`, `A!`)', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        helpEmbed.add_field(name='Normal commands', value='`help`, `avatar`, `id`, `invite`, `ping`, `suggest`')
        helpEmbed.add_field(name='Moderation commands', value='`ban`, `kick`, `mute`, `pmute`, `purge`, `unban`, `unmute`')
        helpEmbed.add_field(name='Owner commands', value='`save`, `say`')
        await ctx.channel.send(embed=helpEmbed)
        return
    else:
        embed = discord.Embed(title=f'Command: `{arg}` | Aliases: `{getattr(config.AliasesCommands, arg)}`', colour=config.Colors.yellow, timestamp=ctx.message.created_at)
        embed.add_field(name=f'Information', value=getattr(config.InfoCommands, arg), inline=False)
        embed.add_field(name='Usage', value=getattr(config.UsageCommands, arg), inline=False)
        await ctx.send(embed=embed)
        return


        
@bot.command(name='avatar', aliases=['av'])
async def avatar(ctx, member: discord.Member = None): 
    if member == None:
        member = ctx.author
    embed = discord.Embed(title = f'Avatar of user {member}', colour=config.Colors.green, timestamp=ctx.message.created_at)
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)



@bot.command(name='id', aliases=['ID'])
async def id(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    await ctx.send(member.id)



@bot.command(name='invite', aliases=['inv'])
async def invite(ctx):
    embed = discord.Embed(title='Invite the bot to your server!', colour=config.Colors.darkGreen)
    embed.add_field(name='Invite links.', value='[Admin permissions](https://discord.com/oauth2/authorize?client_id=768309916112650321&scope=bot&permissions=8)')
    embed.add_field(name='Join our Discord server!', value='[Al3xis Bot Server](https://discord.gg/AAJPHqNXUy)', inline=False)
    await ctx.send(embed=embed)



@bot.command(name='ping', aliases=['pong', 'latency'])
async def ping (ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    time.sleep(2)
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**Bot's ping:**  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')



suggestion = ''
listSuggestions = ''
@bot.command(name='suggest', aliases=['sug'])
async def suggest(ctx, *, new_suggestion):  
    try:
        global suggestion
        suggestion =  new_suggestion
        description = suggestion 
        msg = await ctx.send('Saving suggestion...')

        time.sleep(2)
        embed = discord.Embed(title=f'New suggestion made by {ctx.author}!', description = f'Suggestion: **{description}** \nUser ID: {ctx.author.id} ', colour=config.Colors.green, timestamp=ctx.message.created_at)
        suggestions_channel = bot.get_channel(config.Channels.suggestionsChannel)
        message = await suggestions_channel.send(embed=embed)
        await message.add_reaction(config.Emojis.ballotBoxWithCheck)
        await message.add_reaction(config.Emojis.x)
        print('New suggestions | ' + suggestion)
        
        await ctx.message.add_reaction(config.Emojis.whiteCheckMark)
        await msg.edit(content=f"**{ctx.author}**, your suggestion **`{suggestion}`** has been submited!")
    except Exception:
        await ctx.send('An error ocurred while running the command.')
        await ctx.message.add_reaction(config.Emojis.noEntry)
        return

@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please add a message to create your suggestion!')




####################################################################################################
####################################################################################################
##Moderation commands


@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided.'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.ban_members:
                    try:
                        time.sleep(0.5)    
                        await ctx.send(f'User {member.mention} was banned | `{reason}`.')
                        await member.send(f'You were banned from {guild.name} | `{reason}`.')
                        await member.ban(reason=reason)
                        print(f'User {ctx.author} banned {member} | {reason}')
                        logEmbed = discord.Embed(title=f'Case: `ban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel=bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)     
                    except Exception:
                        await ctx.send('An error ocurred while runnining the command.')
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    await ctx.send(f"{ctx.author.mention} You don't have permissions to ban **{member}**!")
                    return
            
            else:
                await ctx.send(f'{ctx.author.mention} You are not allowed to ban bots!')
                return
        else: 
            await ctx.send(f"{ctx.author.mention} You are not allowed to ban me!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You can't ban yourself!")
        return
    

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to ban!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='kick', pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    if member != ctx.author:
        if member != ctx.me:
            if not member.bot:
                if not member.guild_permissions.kick_members:
                    try:
                        time.sleep(0.5)
                        await ctx.send(f'User {member.mention} was kicked | `{reason}`.')
                        await member.send(f'You were kicked from {guild.name} | `{reason}`.')
                        await member.kick(reason=reason)
                        print(f'User {ctx.author} kicked {member} in server {guild.name}| {reason}')
                        logEmbed = discord.Embed(title=f'Case: `kick`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                        logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                        logEmbed.add_field(name='User', value=member.mention)
                        logEmbed.add_field(name='Reason', value=reason) 
                        logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                        logChannel = bot.get_channel(config.Channels.logChannel)
                        await logChannel.send(embed=logEmbed)       
                    except Exception:
                        await ctx.send('An error ocurred while runnining the command.') 
                        await ctx.message.add_reaction(config.Emojis.noEntry)
                        return
                else:
                    await ctx.send(f"{ctx.author.mention} You don't have permissions to kick **{member}**!")
                    return
            else:
                await ctx.send(f'{ctx.author.mention} You are not allowed to kick bots!')
                return
        else: 
            await ctx.send(f"{ctx.author.mention} You are not allowed to kick me!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You can't kick yourself!")
        return


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to kick!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention} You don't have permissions to use the `{ctx.command}` command!")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='mute')
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member, duration: int=None, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'
    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.kick_members:
                        if not mutedRole in member.roles:
                            if duration:

                                try:
                                    time.sleep(0.5)
                                    await member.add_roles(mutedRole, reason= reason)
                                    await ctx.send(f'{member.mention} was muted for {duration} seconds | `{reason}`')
                                    await member.send(f'You were muted in {guild.name} for {duration} seconds | `{reason}`')
                                    print(f'User {ctx.author} muted {member} in server {guild.name} for {duration} seconds | {reason}')
                                    logEmbed = discord.Embed(title=f'Case: `mute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                    logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                                    logEmbed.add_field(name='User', value=member.mention)
                                    logEmbed.add_field(name='Reason', value=reason) 
                                    logEmbed.add_field(name='Duration', value=f'{duration} seconds')
                                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                    logChannel=bot.get_channel(config.Channels.logChannel)
                                    await logChannel.send(embed=logEmbed)   

                                    await asyncio.sleep(duration) 
                                    await member.remove_roles(mutedRole)
                                    reason = 'Temporary mute completed!'
                                    await member.send(f'You were unmuted in {guild.name} | `{reason}`')
                                    print(f'User {member} was unmuted in server {guild.name} | {reason}')
                                    logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                                    logEmbed.add_field(name='User', value=member.mention)
                                    logEmbed.add_field(name='Reason', value=reason) 
                                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                                    logChannel=bot.get_channel(config.Channels.logChannel)
                                    await logChannel.send(embed=logEmbed)
                                    return

                                except Exception:
                                    await ctx.send('An error ocurred while running the command.')
                                    await ctx.message.add_reaction(config.Emojis.noEntry)
                                    return
                            else:
                                await ctx.send(f'{ctx.author.mention} Please specify an amount of time or use the `pmute` command')
                        else:
                            await ctx.send(f"**{member}** is already muted!")
                            return
                    else:
                        await ctx.send(f"{ctx.author.mention} You don't have permissions to mute **{member}**!")
                        return
                else:
                    await ctx.send(f'{ctx.author.mention} You are not allowed to mute bots!')
            else:
                await ctx.send(f"{ctx.author.mention} You can't mute me!")
                return
        else:
            await ctx.send(f"{ctx.author.mention} You can't mute yourself!")
            return
    else:   
        await ctx.send("This server doesn't have a muted role. Please create one with the name `Muted`.")
        return     


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to mute!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.UserNotFound):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='pmute', aliases= ['p-mute', 'pm'])
@commands.has_permissions(ban_members=True)
async def pmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    if reason == None:
        reason = 'No reason provided'

    mutedRole = discord.utils.get(guild.roles,name='Muted')
    
    if mutedRole:
        if member != ctx.author:
            if member != ctx.me:
                if not member.bot:
                    if not member.guild_permissions.kick_members:
                        if not mutedRole in member.roles:
                            try:
                                time.sleep(0.5)
                                await member.add_roles(mutedRole, reason= reason)
                                await ctx.send(f'{member.mention} was permanently muted | `{reason}`')
                                await member.send(f'You were permanently muted in {guild.name} | `{reason}`')
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

                            except Exception:
                                await ctx.send('An error ocurred while running the command.')
                                await ctx.message.add_reaction(config.Emojis.noEntry)
                                return

                        else:
                            await ctx.send(f"**{member}** is already muted!")
                            return
                    else:
                        await ctx.send(f"{ctx.author.mention} You don't have permissions to mute **{member}**!")
                        return
                else:
                    await ctx.send(f'{ctx.author.mention} You are not allowed to mute bots!')
            else:
                await ctx.send(f"{ctx.author.mention} You can't mute me!")
                return
        else:
            await ctx.send(f"{ctx.author.mention} You can't mute yourself!")
            return
    else:   
        await ctx.send("This server doesn't have a muted role. Please create one with the name `Muted`.")
        return     


@pmute.error
async def pmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to mute!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.UserNotFound):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='purge', aliases=['clear'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 0):
    guild = ctx.guild
    if amount <= 500:
        if amount >=1:
            await ctx.channel.purge(limit=amount)
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
        await ctx.send('Select an amount of messages that should be purged!')


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to purge messages!')
        return




@bot.command(name='unban') 
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
                    time.sleep(0.5)
                    await ctx.guild.unban(member)
                    await ctx.send(f'User {member.mention} was unbanned | `{reason}`.')
                    await member.send(f'You were unbanned from {guild.name} | `{reason}`.')
                    print(f'User {ctx.author} unbanned {member} from {guild.name} | {reason}')
                    logEmbed = discord.Embed(title=f'Case: `unban`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                    logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                    logEmbed.add_field(name='User', value=member.mention)
                    logEmbed.add_field(name='Reason', value=reason) 
                    logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                    logChannel=bot.get_channel(config.Channels.logChannel)
                    await logChannel.send(embed=logEmbed)     
                except Exception:
                    await ctx.send('An error ocurred while running the command.')
                    await ctx.message.add_reaction(config.Emojis.noEntry)
                    return
            else:
                await ctx.send(f'{ctx.author.mention} You are not allowed to unban bots!')
                return
        else:
            await ctx.send(f"{ctx.author.mention} I'm not banned!")
            return
    else:
        await ctx.send(f"{ctx.author.mention} You are not banned!")
        return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to unban!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return



@bot.command(name='unmute')
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
                            await member.remove_roles(mutedRole)
                            await ctx.send(f'{member.mention} was unmuted | `{reason}`')
                            await member.send(f'You were unmuted in {guild.name} | `{reason}`')
                            print(f'User {ctx.author} unmuted {member} in server {guild.name} | {reason}')
                            logEmbed = discord.Embed(title=f'Case: `unmute`', colour=config.Colors.red, timestamp=ctx.message.created_at)
                            logEmbed.add_field(name='Moderator', value=ctx.author.mention)
                            logEmbed.add_field(name='User', value=member.mention)
                            logEmbed.add_field(name='Reason', value=reason) 
                            logEmbed.set_footer(text=f'Guild: {ctx.guild}')
                            logChannel=bot.get_channel(config.Channels.logChannel)
                            await logChannel.send(embed=logEmbed)     
                        except Exception:
                            await ctx.send('An error ocurred while running the command.')
                            await ctx.message.add_reaction(config.Emojis.noEntry)
                            return
                    else:
                        await ctx.send(f"**{member}** is not muted!")
                        return
                else:
                    await ctx.send(f'{ctx.author.mention} You are not allowed to unmute bots!')
            else:
                await ctx.send(f"{ctx.author.mention} I'm not muted!")
                return
        else:
            await ctx.send(f"{ctx.author.mention} You are not muted!")
            return
    else:
        await ctx.send("This server doesn't have a muted role so nobody is muted.")
        return
 

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an user to unmute!')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} You do not have permissions to use the `{ctx.command}` command!')
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send('I cannot find that user!')
        return




####################################################################################################
####################################################################################################
##Owner commands
savedMessageSave = ''
@bot.command(name='save')
@commands.is_owner()
async def save(ctx,*, saveMsg=None):
    global savedMessageSave
    savedMessageSave = saveMsg
    if saveMsg == None:
        await ctx.send('Please provide a message to save!')
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
        except Exception:
            await ctx.send('An error ocurred while running the command.')
            await ctx.message.add_reaction(config.Emojis.noEntry)
            return



@bot.command(name='say')
@commands.is_owner()
async def say(ctx, *, sayMsg=None):
    randomColors = [config.Colors.red, config.Colors.ligthBlue, config.Colors.green, config.Colors.blue, config.Colors.yellow, config.Colors.orange, config.Colors.purple, config.Colors.darkGreen]
    if sayMsg == None:
        embed = discord.Embed(title='Hi!',description=savedMessageSave, colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    else:
        embed = discord.Embed(title='Hi!',description=sayMsg, colour=random.choice(randomColors))
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    
    

################################
####################################################################################################
####################################################################################################
#Run the bot on the server
bot.run(os.environ['discordToken'])


