#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 15:11:53 2021

@author: dylanorrell


"""
############ IMPORTS ############

import discord
import asyncio
import nest_asyncio
nest_asyncio.apply()
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient

############ MONGODB CONNECTION ############

cluster = MongoClient("URL")
print(cluster)
db = cluster['']
collection = db['']

############ DISCORD SETUP ############

#doesn't require a command, so use empty string here
bot = commands.Bot(command_prefix='!')
client=discord.Client()

@bot.event
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot))
    
############ DISCORD COMMAND ############

@bot.command()
async def whitelist (ctx):
    await ctx.message.add_reaction('✅')
    user = ctx.author
    role = user.top_role
    displayname = ctx.author.display_name
    print(user)
    print(role)
    await ctx.message.author.send (f'Hey {displayname}! Your highest role is {role}')
    await ctx.message.author.send ('What address would you like to whitelist?')
    #response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
    def check(msg):
        return msg.content.startswith('0x')
    try:
        response = await bot.wait_for('message', check=check, timeout=15)
        addy = response.content
        print (user, role, addy)
        myquery = { "_id": str(user) }
        if (collection.count_documents(myquery) == 0):
                  post = {"_id": str(user), "role": str(role), "address" : str(addy)}
                  collection.insert_one(post)
                  await response.add_reaction('✅')
                  await ctx.message.author.send (f'🤘❤️ LFG! {addy} is whitelisted! 👀 Stay up to date on project news over at <#847109630030250026>')
        else:
            await response.add_reaction('❌')
            await ctx.message.author.send (f'😎 You have already submitted an addrress to be whitelisted.')

    except asyncio.TimeoutError:
        await ctx.message.author.send('😢 Your whitelist request has timed out. 🚀 Please try the !whitelist command again in <#879734307768389642>')

    return(role)

bot.run('TOKEN')