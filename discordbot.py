import discord
from discord.ext import commands

import os

bot = commands.Bot(command_prefix="$")
token = os.environ['DISCORD_BOT_TOKEN']

if not discord.opus.is_loaded():
    discord.opus.load_opus("heroku-buildpack-libopus")

@bot.command(aliases=["connect","summon"]) #connect��summon�ł��Ăяo����
async def join(ctx):
    """Bot���{�C�X�`�����l���ɓ��������܂��B"""
    voice_state = ctx.author.voice

    if (not voice_state) or (not voice_state.channel):
        await ctx.send("��Ƀ{�C�X�`�����l���ɓ����Ă���K�v������܂��B")
        return

    channel = voice_state.channel

    await channel.connect()
    print("connected to:",channel.name)


@bot.command(aliases=["disconnect","bye"])
async def leave(ctx):
    """Bot���{�C�X�`�����l������ؒf���܂��B"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("Bot�͂��̃T�[�o�[�̃{�C�X�`�����l���ɎQ�����Ă��܂���B")
        return

    await voice_client.disconnect()
    await ctx.send("�{�C�X�`�����l������ؒf���܂����B")


@bot.command()
async def play(ctx):
    """�w�肳�ꂽ�����t�@�C���𗬂��܂��B"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("Bot�͂��̃T�[�o�[�̃{�C�X�`�����l���ɎQ�����Ă��܂���B")
        return

    if not ctx.message.attachments:
        await ctx.send("�t�@�C�����Y�t����Ă��܂���B")
        return

    await ctx.message.attachments[0].save("tmp.mp3")

    ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
    voice_client.play(ffmpeg_audio_source)

    await ctx.send("�Đ����܂����B")

bot.run(token)
