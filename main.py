import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    responses = {
        "imperator": "Did someone mentioned me, The Imperator?",
        "Imperator": "Did someone mentioned me, The Imperator?",
        "cerydra": "Who are you mention my name with no respect?"
    }

    for keyword, response in responses.items():
        if keyword in content:
            await message.channel.send(response)
            break

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channes, name='general')
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

@bot.command(name='ping')
async def ping(ctx):
    """"Check if the bot is responsibe"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)} ms')

@bot.command(name='hello')
async def hello(ctx):
    """"Say hello to the user"""
    await ctx.send(f'Silence, {ctx.author.mention}! Who are you dare to disrespect me, The Imperator?')

@bot.command(name='roll')
async def roll(ctx, sides: int = 6):
    """Roll a dice with specified sides (default: 6)"""
    if sides < 2:
        await ctx.send("Dice must have at least 2 sides!")
        return
    
    result = random.randint(1, sides)
    await ctx.send(f'You rolled a {result} on a {sides}-sided dice!')

@bot.command(name='choose')
async def choose(ctx, *choices):
    """Choose randomly between given options"""
    if len(choices) < 2:
        await ctx.send("Please provide at least 2 choices! Usage: `!choose option1 option2 option3`")
        return
    
    choice = random.choice(choices)
    await ctx.send(f'I Choose: **{choice}**')

@bot.command(name='nuclear')
async def generate_code(ctx):
    """Generate a random 6-digit code"""
    code = random.randint(100000, 999999)
    await ctx.send(f'Try this nuclear code: **{code}**')

@bot.command(name='math')
async def math_quiz(ctx):
    """Take a quick math quiz"""
    operations = ['+', '-', '*']
    operation = random.choice(operations)
    
    if operation == '*':
        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
    else:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
    
    if operation == '+':
        answer = num1 + num2
        op_name = "addition"
    elif operation == '-':
        answer = num1 - num2
        op_name = "subtraction"
    else:  # multiplication
        answer = num1 * num2
        op_name = "multiplication"
    
    embed = discord.Embed(
        title="🧮 Math Quiz",
        description=f"Solve this {op_name} problem:\n\n**{num1} {operation} {num2} = ?**\n\nYou have 15 seconds!",
        color=0x9b59b6
    )
    await ctx.send(embed=embed)
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', timeout=15.0, check=check)
        user_answer = int(msg.content)
        
        if user_answer == answer:
            embed = discord.Embed(
                title="✅ Correct!",
                description=f"Great job! **{num1} {operation} {num2} = {answer}**",
                color=0x00ff00
            )
        else:
            embed = discord.Embed(
                title="❌ Wrong Answer",
                description=f"The correct answer was **{answer}**\nYour answer: {user_answer}",
                color=0xff0000
            )
        await ctx.send(embed=embed)
        
    except ValueError:
        await ctx.send("❌ Please enter a valid number!")
    except TimeoutError:
        embed = discord.Embed(
            title="⏰ Time's Up!",
            description=f"The correct answer was **{answer}**",
            color=0xff6b6b
        )
        await ctx.send(embed=embed)

@bot.command(name='serverinfo')
async def server_info(ctx):
    """Display server information"""
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Server Info", color=0x00ff00)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await ctx.send(embed=embed)

##@bot.command(name='userinfo')
#async def user_info(ctx, member: discord.Member = None):
#    """Display user information"""
#    if member is None:
#        member = ctx.author 

@bot.command(name='call')
async def user_info(ctx, member: discord.Member = None):
    """Call user"""
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f"{member.display_name}'s Info", color=0x0099ff)
    embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)

    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument! Use `!help {ctx.command}` for more info.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument! Please check your input and try again.")
    else:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    bot.run('MTM5NjUwMTM5NjI0MDYwMTI5MA.GwGsoq.j2aV_QVj9DtfSgdljmvGvnmBVyo1TggYEo-zk0')