import discord
from discord.ext import commands

import os

bot = commands.Bot(command_prefix="$")
token = os.environ['DISCORD_BOT_TOKEN']

#if not discord.opus.is_loaded():
    #discord.opus.load_opus("heroku-buildpack-libopus")
    
@bot.event
async def on_ready():
    print('ready')
    if not discord.opus.is_loaded():
        # opus未ロード
        discord.opus.load_opus("heroku-buildpack-libopus")

@bot.command(aliases=["connect","summon"]) #connectやsummonでも呼び出せる
async def join(ctx):
    """Botをボイスチャンネルに入室させます。むんっ"""
    voice_state = ctx.author.voice

    if (not voice_state) or (not voice_state.channel):
        await ctx.send("ほわっ、先にボイスチャンネルに入っている必要があります。")
        return

    channel = voice_state.channel

    await channel.connect()
    print("connected to:",channel.name)


@bot.command(aliases=["disconnect","bye"])
async def leave(ctx):
    """ボイスチャンネルから切断します。ほわぁ…"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("ほわっ、私はこのサーバーのボイスチャンネルに参加していません…")
        return

    await voice_client.disconnect()
    await ctx.send("ボイスチャンネルから切断しました。むんっ")


@bot.command()
async def play(ctx):
    """音声ファイルをアップロードしてメッセージを「$play」にすれば、それを喋ります。むんっ"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("ほわっ、私はこのサーバーのボイスチャンネルに参加していません…")
        return

    if not ctx.message.attachments:
        await ctx.send("ほわっ、音声ファイルが添付されていません…")
        return

    await ctx.message.attachments[0].save("tmp.mp3")

    ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
    voice_client.play(ffmpeg_audio_source)

    await ctx.send("再生しました。むんっ")

bot.run(token)
