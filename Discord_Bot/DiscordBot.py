import discord
from discord.ext import commands
import json
import random

TOKEN = 'Bot Token goes here'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user} is Ready')


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


async def update_data(users, user):
    if f'{user.id}' not in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['calls'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp
    users[f'{user.id}']['calls'] += 1
    #  print(users[f'{user.id}']['experience'])  # Prints users exp in terminal for debugging


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    calls = users[f'{user.id}']['calls']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 5))

    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has caught coins {calls} times '
                                   f'and caught {experience} coins.\n{user.name} leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandOnCooldown):
        await message.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')
        return error
    else:
        raise error


@bot.command(aliases=['lb'])
async def leaderboard(message, x=5):
    with open('users.json', 'r') as f:
        users = json.load(f)

    users_by_exp = sorted(users.items())
    sorted_exp = []
    for i in users_by_exp:
        user_id = i[0]
        exp = i[1].get('experience')
        calls = i[1].get('calls')
        level = i[1].get('level')
        sorted_exp.append([exp, user_id, calls, level])
    sorted_exp = sorted(sorted_exp, reverse=True)

    index = 1
    em = discord.Embed(title=f'Top {x} Coin Catchers')
    for i in sorted_exp:
        user = await bot.fetch_user(i[1])
        lvl = 'Level: ' + str(i[3])
        exp = 'Coins: ' + str(i[0])
        call_amnt = 'Caught Instances: ' + str(i[2])
        em.add_field(name=f'{index}. {user.name}', value=f'{lvl}\n{exp}\n{call_amnt}', inline=False)
        if index == x:
            break
        else:
            index += 1
    sort_len = len(sorted_exp)
    if sort_len < x:
        if sort_len == 1:
            em.title = f'Top Coin Catcher'
        elif sort_len == 0:
            em.title = f'No users on leaderboard yet.'
        else:
            em.title = f'Top {sort_len} Coin Catchers'
    await message.send(embed=em)


@bot.command(aliases=['s'])
async def stats(message):
    with open('users.json', 'r') as f:
        users = json.load(f)

        user = message.author
        level = users[f'{user.id}']['level']
        coins = users[f'{user.id}']['experience']
        calls = users[f'{user.id}']['calls']

    await message.send(f'{user.mention} has caught coins {calls} times gaining {coins} coins.\n'
                       f'{user.name} is level {level}.')


@bot.command(aliases=['nl'])
async def nextLevel(message):
    with open('users.json', 'r') as f:
        users = json.load(f)
    user = message.author
    experience = users[f'{user.id}']['experience']
    level = users[f'{user.id}']['level']
    level_end = (level+1) ** 5
    exp_needed = level_end - experience
    await message.send(f'{user.mention} needs {exp_needed} more coins to level up!')


@bot.command(aliases=['h'])
async def handicap(message):
    handicaps = ['Only do damage.', 'No cooldowns.', 'No ultimate.', 'Only heal.', 'Can\'t jump.',
                 'Can only move with w.', 'Can only move with s.']
    await message.send(handicaps[random.randint(0, len(handicaps))])


@bot.command(aliases=['f'])
async def flip(message):
    coin = random.randint(0, 1)
    if coin == 0:
        await message.send('You got heads.')
    if coin == 1:
        await message.send('You got tails.')


@bot.command()
async def helpMe(message):
    await message.send('!pick: Pick a random team, open_team, open, tank, damage, support.\n!coin: Catch coins.\
                       \n!stats: Your coin catching stats.\n!leaderboard: View the top coin Catchers.\
                       \n!nextLevel: See how many coins you need to catch for your next level.\n!flip: Flip a coin.\
                       \n!handicap: Get a random handicap.')


@bot.command(aliases=['c'])
@commands.cooldown(3, 30, commands.BucketType.user)
async def coin(message):
    coins = random.randint(0, 100)
    str_coin = ' coins.'
    if coins == 0:
        str_coin = ' coins. Better luck next time.'
    elif 0 < coins <= 10:
        if coins == 1:
            str_coin = ' coin. Better than nothing.'
        else:
            str_coin = ' coins. Better than nothing.'
    elif 10 < coins <= 30:
        str_coin = ' coins. Not bad.'
    elif 30 < coins <= 50:
        str_coin = ' coins. Go but something nice with those.'
    elif 50 < coins:
        str_coin = ' coins. How did you catch all of those?'
    elif coins == 100:
        str_coin = ' coins. Jackpot!'
    await message.send('You caught ' + str(coins) + str_coin)
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, coins)
    await level_up(users, message.author, message)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    return


@bot.command(aliases=['p'])
async def pick(message, arg):
    roll = -1  # Default roll value
    heros = {  # Hero Dictionary
        'Tank': ['D.V.A', 'Doomfist', 'Junker Queen', 'Orisa', 'Reinhardt', 'RoadHog', 'Sigma', 'Winston',
                 'Wrecking Ball', 'Zarya'],
        'Damage': ['Ashe', 'Bastion', 'Cassidy', 'Echo', 'Genji', 'Hanzo', 'Junkrat', 'Mei', 'Pharah', 'Reaper',
                   'Sojourn', 'Soldier 76', 'Sombra', 'Symmetra', 'Torbjörn', 'Tracer', 'Widowmaker'],
        'Support': ['Ana', 'Baptiste', 'Brigitte', 'Kiriko', 'Lucio', 'Mercy', 'Moira', 'Zenyatta']
    }
    hero = 'ERROR'  # Default hero value
    larg = arg.lower()

    if larg == 'open':
        role = random.randint(0, 2)
        if role == 0:  # tank
            roll = random.randint(0, 9)
            hero = heros.get('Tank')[roll]
        elif role == 1:  # damage
            roll = random.randint(0, 16)
            hero = heros.get('Damage')[roll]
        else:  # support
            roll = random.randint(0, 7)
            hero = heros.get('Support')[roll]
        await message.send(hero)
        return

    if larg == 'open_team':
        roles = []
        h_list = []
        for i in range(5):
            roles.append(random.randint(0, 2))
        j = 0
        while j < 5:
            x = roles[j]
            if x == 0:  # tank
                roll = random.randint(0, 9)
                hero = heros.get('Tank')[roll]
            elif x == 1:  # damage
                roll = random.randint(0, 16)
                hero = heros.get('Damage')[roll]
            else:  # support
                roll = random.randint(0, 7)
                hero = heros.get('Support')[roll]
            if hero in h_list:
                j -= 1
            else:
                h_list.append(hero)
            j += 1
        for i in h_list:
            await message.send(i)
        return

    if larg not in [i.lower() for i in heros.keys()] and larg != 'team':
        await message.send('Please use tank, damage, support or team.')

    else:
        if larg == 'team':
            roll1 = random.randint(0, 9)  # tank
            roll2 = 0  # dps 1
            roll3 = 0  # dps 2
            roll4 = 0  # support 1
            roll5 = 0  # support 2
            while roll3 == roll2 and roll == -1:
                roll2 = random.randint(0, 16)
                roll3 = random.randint(0, 16)
                if roll2 != roll3:
                    roll = 1
                    break
            while roll4 == roll5 and roll == 1:
                roll4 = random.randint(0, 7)
                roll5 = random.randint(0, 7)
                if roll4 != roll5:
                    roll = -1
                    break
            hero = heros.get('Tank')[roll1], heros.get('Damage')[roll2], heros.get('Damage')[roll3], \
                   heros.get('Support')[roll4], heros.get('Support')[roll5]
        if larg == 'tank':
            roll = random.randint(0, 9)
            hero = heros.get('Tank')[roll]
        if larg == 'damage':
            roll = random.randint(0, 16)
            hero = heros.get('Damage')[roll]
        if larg == 'support':
            roll = random.randint(0, 7)
            hero = heros.get('Support')[roll]
        if roll == -1 and larg != 'team':
            await message.send('Unexpected error.')
        else:
            if type(hero) == str:
                await message.send(hero)
            else:
                for i in hero:
                    await message.send(i)

bot.run(TOKEN)
