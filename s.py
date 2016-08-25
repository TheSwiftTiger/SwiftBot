import discord
from discord.ext import commands
import asyncio
import sys
import logging
import os.path
import hashlib
import math
import numpy as np
import string
import time
import praw
import random
import datetime
import io
from contextlib import redirect_stdout

client = discord.Client()

user_agent = ("Swifty")

redditing = False

is_animating = False

sys.setrecursionlimit(120)

gameoflife = False

empty = ' '
cell = '▓'

line_template = [empty for x in range(10)]
nboard_template = [0 for x in range(10)]

board = []
n_board = []

for x in range(10):
    exec('locals()["line{}"] = [{}]'.format(x, line_template))
    exec('locals()["nline{}"] = [{}]'.format(x, nboard_template))

for x in range(10):
    exec('line{} = line{}[0]'.format(x, x))
    exec('nline{} = nline{}[0]'.format(x, x))

for x in range(10):
    exec('board.append(line{})'.format(x))
    exec('n_board.append(nline{})'.format(x))


@client.event
async def on_ready():
    cooldown = {}

    x = [x for x in client.get_all_channels()]

    for i in x:
        cooldown[str(i)] = 0

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global cooldown
    global is_animating
    global n_board
    global empty
    global cell


@client.event
async def on_message(message):
    global cooldown
    global is_animating
    global gameoflife
    global board
    global n_board
    global empty
    global cell
    for key, value in cooldown.items():
        if value > 0:
            cooldown[key] -= 1

    authorized = ['TheSwiftTiger#8711', 'Zatherz#8995']

    memes = {'feelsbadman': 'http://i.imgur.com/ajRCCHa.png',
             'dat boi': 'http://i.imgur.com/qA6vnL8.png',
             'triggered': 'http://i.imgur.com/fC51q72.png',
             'troll': 'http://i.imgur.com/Gw4ipWB.png',
             'no': 'http://i.imgur.com/pyBR4Qb.png',
             'harambe': 'http://i.imgur.com/cvzfmHs.png',
             'that\'s pretty good': 'http://i.imgur.com/JL51XgL.png',
             'john cena': 'https://www.youtube.com/watch?v=enMReCEcHiM',
             'rip': 'http://i.imgur.com/g0eQChZ.png'

             }

    presets = {
               'glider': ['a2', 'b3', 'c3', 'c2', 'c1'],
               'line': ['e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9'],
               'tnt': ['c2', 'c3', 'd2', 'd4', 'e3', 'e5', 'f4', 'f5', 'f6', 'g5'],
               'spaceship': ['c2', 'c3', 'c4', 'c5', 'd1', 'd5', 'e5', 'f1', 'f4']
               }

    if message.content.startswith('<> help') and not is_animating and not gameoflife:
        await client.send_message(message.channel, """Here is a list of commands I can do (all starting with <>): ```eval: Syntax: eval ``math`` Description: returns the value of a Python math statement
8ball: Syntax: 8ball <question> Description: A magic 8 ball for all your Helix fossil needs
reddit: Syntax: reddit *subreddit* *post number* Description: Fetches a reddit post from the desired subreddit
meme: Syntax: meme *meme* Description: all your meme needs
memes: Syntax: memes Description: lists all memes
say: Syntax: say *text* Description: The bot says something
anim: Syntax: anim*loops* *animation* Description: It's complicated. Ask TheSwiftTiger for more info`
rps: Syntax: rps *move* ```""")

    elif message.content.startswith('<> close') and str(message.author).strip() in authorized and not is_animating and not gameoflife:
        sys.exit()

    elif message.content.startswith('<> close') and str(message.author).strip() not in authorized and not is_animating and not gameoflife:
        await client.send_message(message.channel, "Nope.")

    elif cooldown[str(message.channel)] > 0 and message.content.startswith('<>') and not is_animating and not gameoflife:
        await client.send_message(message.channel, "Cooldown Messages: {}".format(cooldown[str(message.channel)] // 2 + 1))

    elif message.content.startswith('<> eval') and not is_animating and not gameoflife:
        sep = '`'
        try:
            if '`' not in message.content:
                raise Exception("Put these: '`' around your eval code")
            elif '__' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'sys' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'exit' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'discord' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'message' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'client' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'user' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'time' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'authorized' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'globals' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'os' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'import' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif '<>' in message.content.split(sep, 1)[-1].replace('`', ''):
                raise Exception("You might be trying to break the system, please don't")
            elif 'eval' in message.content.split(sep, 1)[-1].replace('`', ''):
                raise Exception("You might be trying to break the system, please don't")
            elif 'chr' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'exec' in message.content:
                raise Exception("You might be trying to break the system, please don't")
            elif 'locals' in message.content:
                raise Exception("You might be trying to break the system, please don't")

            if 'print' in message.content:
                with io.StringIO() as buf, redirect_stdout(buf):
                    msg = eval(message.content.split(sep, 1)[-1].replace('`', ''))
                    output = buf.getvalue()
                if '<>' in output:
                    raise Exception("You might be trying to break the system, please don't")
                await client.send_message(message.channel, output)
                cooldown[str(message.channel)] = 4
            else:
                msg = message.content.split(sep, 1)[-1].replace('`', '')
                msg = eval(message.content.split(sep, 1)[-1].replace('`', ''))
                if (len(str(msg))) > 200:
                    await client.send_message(message.channel, 'Too many characters. ({})'.format(len(str(msg))))
                else:
                    await client.send_message(message.channel, msg)
                    cooldown[str(message.channel)] = 4
        except Exception as e:
            await client.send_message(message.channel, 'Could not compute, error: ```{}```'.format(e))

    elif message.content.startswith('<> exec') and str(message.author).strip() in authorized and not is_animating and not gameoflife:
        sep = '```'
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                msg = exec(message.content.split(sep, 1)[-1].replace('`', ''))
                if msg is None:
                    pass
                else:
                    output = buf.getvalue()
                    await client.send_message(message.channel, output)
        except Exception as e:
            await client.send_message(message.channel, 'Could not compute, error: ```{}```'.format(e))

    elif message.content.startswith("<> exec") and str(message.author).strip() not in authorized and not is_animating and not gameoflife:
        await client.send_message(message.channel, "You are not authorized to use exec.")

    elif message.content.startswith('<> 8ball') and not is_animating and not gameoflife:
        choice = random.randrange(0, 3)
        if choice == 0:
            no = ['Nope', 'Not really', "I don't think so", 'Naaaah', 'Bite my shiny metal ass. No.']
            await client.send_message(message.channel, random.choice(no))
        elif choice == 1:
            maybe = ['Maybe', 'Might be', "I'm very very slightly feeling it", 'Try again later']
            await client.send_message(message.channel, random.choice(maybe))
        elif choice == 2:
            yes = ['Yep', 'Yes', 'Affirmative', "I'm feeling it", 'I think']
            await client.send_message(message.channel, random.choice(yes))
        cooldown[str(message.channel)] = 4

    elif message.content.startswith('<> reddit') and not is_animating and not gameoflife:
        noload = False
        nsfw = False
        sep = 'reddit'
        sep2 = '-'
        progress = 0
        if '-noload' in message.content:
            message.content.replace('-noload', '')
            noload = True
        if '-nsfw' in message.content:
            message.content.replace('-nsfw', '')
            nsfw = True
        sr = message.content.split(sep, 1)[-1].strip()
        idx = sr.split(' ', 1)[-1].strip()
        sr = sr.split(' ', 1)[0].strip()

        if sr is None:
            pass
        if idx is None:
            pass
        else:
            cooldown[str(message.channel)] = 6
            r = praw.Reddit(user_agent=user_agent)
            subreddit = r.get_subreddit(sr)
            submission = []
            if noload:
                for x in subreddit.get_hot():
                    submission.append(x)
            else:
                bar = await client.send_message(message.channel, "Loading... [{}{}]".format(progress * '▓', (27 - progress) * '░'))
                for x in subreddit.get_hot():
                    progress += 1
                    submission.append(x)
                    await client.edit_message(bar, "Loading... [{}{}]".format('▓' * progress, '░' * (27 - progress)))
                    if progress % 6 == 0 or progress % 7 == 0 or progress % 8 == 0 or progress % 9 == 0:
                        time.sleep(1)
                await client.edit_message(bar, "Loaded")
            submission = submission[int(idx) - 1]
            if submission.over_18 and not nsfw:
                await client.send_message(message.channel, 'Contains NSFW content.')
            else:
                try:
                    await client.send_message(message.channel, "Title: {}".format(submission.title))
                    time.sleep(0.5)
                    await client.send_message(message.channel, "Author: {}".format(submission.author))
                    time.sleep(0.5)
                    await client.send_message(message.channel, "Text: ```{}```".format(submission.selftext))
                    time.sleep(0.5)
                    await client.send_message(message.channel, "Score: {}".format(submission.score))
                    time.sleep(0.5)
                    await client.send_message(message.channel, "URL: <{}>".format(submission.url))
                except:
                    await client.send_message(message.channel, "Was not able to send post, either too big or an internal error.")

    elif message.content.startswith('<> memes') and not is_animating and not gameoflife:
        x = str([x for x in memes.keys()])
        await client.send_message(message.channel, x.replace('[', '').replace(']', '').replace("'", ''))

    elif message.content.startswith('<> meme') and not is_animating and not gameoflife:
        sep = 'meme'
        meme = message.content.split(sep, 1)[-1].strip()
        cooldown[str(message.channel)] = 5
        try:
            await client.send_message(message.channel, memes[meme])
        except:
            await client.send_message(message.channel, "No such meme exists")

    elif message.content.startswith('<> say') and not is_animating and not gameoflife:
        sep = 'say'
        say = message.content.split(sep, 1)[-1].strip()
        if '<>' in say:
            await client.send_message(message.channel, "You cannot make the bot do commands.")
        else:
            await client.send_message(message.channel, say)

    elif message.content.startswith('<> animadv') and not is_animating and not gameoflife:
        sep = 'animadv'
        progress = 0
        anim = message.content.split(sep, 1)[-1]
        try:
            loops = int(anim[0])
            anim = anim[1:]
        except ValueError:
            loops = 1
        if loops > 5:
            await client.send_message(message.channel, 'Too many loops')
        elif len(message.content.split()) > 20:
            await client.send_message(message.channel, 'Too many frames')
        else:
            cooldown[str(message.channel)] = 8
            anim = anim.split('//')
            anim.pop(0)
            is_animating = True
            if loops == 1 and len(anim) <= 9:
                msg = await client.send_message(message.channel, anim[0])
                for i in anim:
                    await client.edit_message(msg, i)
                    time.sleep(0.1)
            else:
                loopview = loops
                msg = await client.send_message(message.channel, '{} {:>32}{}{}] {} loops'.format(anim[0], '[', '▓', len(anim) * '░', loopview))
                is_animating = True
                for x in range(loops):
                    for i in anim:
                        progress += 1
                        await client.edit_message(msg, "{} {:>32}{}{}] {} loops".format(i, '[', progress * '▓', (len(anim) - progress) * '░', loopview))
                        time.sleep(1)
                    loopview -= 1
                    if loops == 1:
                        for i in anim:
                            progress += 1
                            await client.edit_message(msg, "{} {:>32}{}{}] {} loop".format(i, '[', progress * '▓', (len(anim) - progress) * '░', loopview))
                            time.sleep(1)
                    progress = 0
            loopview = 0
            await client.edit_message(msg, 'Animation Finished')
            is_animating = False

    elif message.content.startswith('<> anim') and not is_animating and not gameoflife:
        sep = 'anim'
        progress = 0
        anim = message.content.split(sep, 1)[-1]
        try:
            loops = int(anim[0])
            anim = anim[1:]
        except ValueError:
            loops = 1
        if loops > 5:
            await client.send_message(message.channel, 'Too many loops')
        elif len(message.content.split()) > 20:
            await client.send_message(message.channel, 'Too many frames')
        else:
            cooldown[str(message.channel)] = 8
            anim = anim.split(' ')
            anim.pop(0)
            is_animating = True
            if loops == 1 and len(anim) <= 9:
                msg = await client.send_message(message.channel, anim[0])
                for i in anim:
                    await client.edit_message(msg, i)
                    time.sleep(0.1)
            else:
                loopview = loops
                msg = await client.send_message(message.channel, '{} {:>32}{}{}] {} loops'.format(anim[0], '[', '▓', len(anim) * '░', loopview))
                is_animating = True
                for x in range(loops):
                    for i in anim:
                        progress += 1
                        await client.edit_message(msg, "{} {:>32}{}{}] {} loops".format(i, '[', progress * '▓', (len(anim) - progress) * '░', loopview))
                        time.sleep(1)
                    loopview -= 1
                    if loops == 1:
                        for i in anim:
                            progress += 1
                            await client.edit_message(msg, "{} {:>32}{}{}] {} loop".format(i, '[', progress * '▓', (len(anim) - progress) * '░', loopview))
                            time.sleep(1)
                    progress = 0
            loopview = 0
            await client.edit_message(msg, 'Animation Finished')
            is_animating = False

    elif message.content.startswith('<> rps') and not is_animating and not gameoflife:
        sep = 'rps'
        choices = ['rock', 'paper', 'scissors']
        move = message.content.split(sep, 1)[-1]
        move = move[1:]
        choice = random.choice(choices)
        if move not in choices:
            await client.send_message(message.channel, "I don't know what you're getting at here, but '{}' is not a move.".format(move))
        else:
            cooldown[str(message.channel)] = 5
            await client.send_message(message.channel, "You chose: {}\nI chose: {}".format(move, choice))
            tmp1 = choices.index(move) + 1
            tmp2 = choices.index(choice) + 1
            tmp3 = tmp2 - tmp1
            tmp4 = tmp3 % 3
            if tmp4 == 2:
                await client.send_message(message.channel, "You won")
            elif tmp4 == 1:
                await client.send_message(message.channel, "I won")
            else:
                await client.send_message(message.channel, "It was a tie")

    elif message.content.startswith('<> channels') and str(message.author) in authorized:
        for i in list(string.ascii_lowercase):
            await client.create_channel(message.server, i + "channel")
            await client.send_message(message.channel, "Creating channel...")

    elif message.content.startswith('<> bypass') and str(message.author) in authorized:
        cooldown[str(message.channel)] = 0

    elif message.content.startswith('<> gameoflifepresets'):
        listofpresets = ''
        for key, value in presets.items():
            listofpresets = listofpresets + '{}: {}\n'.format(key, value).replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        await client.send_message(message.channel, listofpresets)

    elif message.content.startswith('<> gameoflife') and not gameoflife and not is_animating:
        sep = 'gameoflife'

        chosen = message.content.split(sep, 1)[-1]
        try:
            frames = int(chosen.split(' ', 1)[0])
            chosen = chosen[2:].strip()
        except:
            await client.send_message(message.channel, "Specify number of frames after '<> gameoflife' (cannot be more than 25). \nDefaulted to 5.")
            frames = 5

        if frames > 25 and str(message.author) not in authorized:
            await client.send_message(message.channel, "Too many frames")
        else:
            gameoflife = True
            cooldown[str(message.channel)] = 6

            frame = 0

            def resetNBoard():
                global n_board
                for index in range(len(n_board)):
                    for index2 in range(len(n_board[index])):
                        n_board[index][index2] = 0

            xlist = []
            ylist = []

            for i in chosen:
                if i != ' ':
                    try:
                        ylist.append(string.ascii_lowercase.index(i[0]))
                    except:
                        try:
                            xlist.append(int(i))
                        except:
                            await client.send_message(message.channel, 'Incorrect Formatting')
                else:
                    pass
            for x, y in zip(xlist, ylist):
                board[y][x] = cell
            formatted = '```fix\n'

            for i in board:
                formatted = formatted + ''.join(i) + '\n'

            msg = await client.send_message(message.channel, '---\n' + formatted + '\n```')

            while frame < frames:
                resetNBoard()
                for c_y, lst in enumerate(board):
                    for c_x, state in enumerate(lst):
                        for q in [board[c_y-1] if c_y-1 > -1 else board[len(board)-1], board[c_y], board[c_y+1] if c_y+1 < len(board) else board[0]]:
                            for n in [q[c_x-1] if c_x-1 > -1 else q[len(q)-1], q[c_x], q[c_x+1] if c_x+1 < len(q) else q[0]]:
                                if n == '▓':
                                    n_board[c_y][c_x] += 1
                        if board[c_y][c_x] == '▓':
                            n_board[c_y][c_x] -= 1

                for c_y, lst in enumerate(board):
                    for c_x, state in enumerate(lst):
                        if n_board[c_y][c_x] < 2 and board[c_y][c_x] == '▓':
                            board[c_y][c_x] = ' '
                        elif n_board[c_y][c_x] > 3 and board[c_y][c_x] == '▓':
                            board[c_y][c_x] = ' '
                        elif n_board[c_y][c_x] == 3 and board[c_y][c_x] == ' ':
                            board[c_y][c_x] = '▓'
                        else:
                            pass
                formatted = '```fix\n'

                for i in board:
                    formatted = formatted + ''.join(i) + '\n'

                await client.edit_message(msg, '---\n{}\n```\n```fix\n{}{}\n``` {}/{}'.format(formatted, '▓' * frame, ' ' * (frames - frame), frame, frames))

                frame += 1
                time.sleep(1)
            empty = ' '
            cell = '▓'
            line_template = [empty for x in range(10)]
            nboard_template = [0 for x in range(10)]
            board = []
            for x in range(10):
                exec('locals()["line{}"] = [{}]'.format(x, line_template))
            for x in range(10):
                exec('line{} = line{}[0]'.format(x, x))
            for x in range(10):
                exec('board.append(line{})'.format(x))
            await client.delete_message(msg)
            gameoflife = False
