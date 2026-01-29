import discord
from gtts import gTTS
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from gtts.lang import tts_langs

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()
user_idioma = {}
idiomas_disponiveis = tts_langs()

PRINCIPAIS_IDIOMAS = {
    'pt': 'Português',
    'pt-pt': 'Português - Portugal',
    'en': 'Inglês',
    'es': 'Espanhol',
    'fr': 'Francês',
    'de': 'Alemão',
    'it': 'Italiano',
    'ja': 'Japonês',
    'ru': 'Russo',
    'ko': 'Coreano'
}

class MenuIdiomas(discord.ui.Select):
    def __init__(self):

        opcoes = [
            discord.SelectOption(label=nome, value=codigo, emoji="🗣️")
            for codigo, nome in PRINCIPAIS_IDIOMAS.items()
        ]
        super().__init__(
            placeholder="Escolha seu idioma",
            min_values=1,
            max_values=1,
            options=opcoes,
            custom_id="select_idioma"
        )

    async def callback(self,interaction: discord.Interaction):
        escolha_codigo = self.values[0]
        nome_idioma = PRINCIPAIS_IDIOMAS[escolha_codigo]
        user_idioma[interaction.user.id] = escolha_codigo
        await interaction.response.send_message(
            f"Idioma configurado para  **{nome_idioma}**!",
            ephemeral=True
        )

class IdiomaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MenuIdiomas())

@bot.event
async def on_ready():
    print(f"Logado como {bot.user} - Armed and Ready!")
    await bot.change_presence(activity=discord.Streaming(
        name = "Shikanoko Nokonoko Koshitantan",
        url="https://www.youtube.com/watch?v=bv__9O5CZok"
    ))

@bot.slash_command(name="idioma", description="Escolhe o idioma do bot")
async def idioma(ctx: discord.ApplicationContext):
    await ctx.respond("Selecione seu idioma: ", view=IdiomaView(), ephemeral=True)


@bot.slash_command(name="falar", description="O bot entra na sala e fala o texto")
async def falar(ctx: discord.ApplicationContext, texto:str):
    if not ctx.author.voice:
        await ctx.respond("Precisa estar em um canal de voz!", ephemeral=True)
        return

    username = ctx.author.name
    lang_code = user_idioma.get(ctx.author.id, "pt-br")
    nome_idioma = PRINCIPAIS_IDIOMAS.get(lang_code,"Português")
    await ctx.respond(f"{username} disse em {nome_idioma}: '{texto.title()}'")

    canal_usuario = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await canal_usuario.connect()
    else:
        vc = ctx.voice_client

    try:
        if lang_code == 'pt-pt':
            tts = gTTS(text=texto, lang="pt",tld='pt')
        else:
            tts = gTTS(text=texto, lang=lang_code)
        arquivo_audio = f"temp_{ctx.author.id}.mp3"
        tts.save(arquivo_audio)

        if vc.is_playing():
            vc.stop()
        
        vc.play(discord.FFmpegPCMAudio(arquivo_audio))

        while vc.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        await ctx.followup.send(f"Erro ao gerar áudio: {e}", ephemeral=True)
    finally:
        if os.path.exists(arquivo_audio):
            os.remove(arquivo_audio)
bot.run(token)