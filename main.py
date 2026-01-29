import discord
from gtts import gTTS
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logado como {bot.user} - Armed and Ready!")


@bot.slash_command(name="falar", description="O bot entra na sala e fala o texto")
async def falar(ctx: discord.ApplicationContext, texto:str):
    if not ctx.author.voice:
        await ctx.respond("Precisa estar em um canal de voz!")
        return

    await ctx.respond(f"Falando {texto}")

    canal_usuario = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await canal_usuario.connect()
    else:
        vc = ctx.voice_client

    tts = gTTS(text=texto, lang="pt")
    arquivo_audio = "temp_audio.mp3"
    tts.save(arquivo_audio)

    if vc.is_playing():
        vc.stop()
    
    vc.play(discord.FFmpegPCMAudio(arquivo_audio))

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()

    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)
bot.run(token)