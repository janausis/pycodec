# THIS IS IN GERMAN, I WILL PROBABLY NOT CREATE AN ENGLISH VERSION OF THE PROMPTS


import discord
from discord.ext import commands
from dotenv import load_dotenv

token = "" # YOUR DISCORD BOT TOKEN HERE

helpText = ("```Global:\n"
            "    !start                  Starte eine private Konversation mit dem Bot\n"
            "    !hilfe                  Öffnet dieses Fenster\n\n\n"

            "Nur in deinen DMs:\n"
            "    !encode  <text:max:155> Verschlüssele eine Nachricht und merke dir deinen Seed\n"
            "                            Wenn !setseed gesetzt wurde, wird dieser seed verwendet\n"
            "    !decode  <seed> <text>  Entschlüssele eine Nachricht. Du benötigst den passenden Seed\n"
            "                            Seed kann weggelassen werden, wenn mit !setseed ein default seed gesetzt wurde\n"
            "    !addseed <seed> <name>  Speichere einen Seed. Sie sind nur für dich sichtbar\n"
            "    !delseed <seed>         Lösche einen Seed aus deiner persönlichen Liste\n"
            "    !clearseeds             Lösche alle deine Seeds aus deiner persönlichen Liste\n"
            "    !seed    (länge 8-256)  Generiere einen neuen Seed, gibt Kontrolle über Länge des Seeds. Default: 32 \n"
            "    !seeds                  Liste alle deine persönlichen Seeds auf\n"
            "    !setseed <name>         Setze einen standard seed, der immer bei En- und Decoding prozessen verwendet wird\n"
            "```")

secText = ("``` Level |  Seed length  |  letterlength  \n"
           "  1    |       16      |       8       \n"
           "  2    |       32      |       8       \n"
           "  3    |       16      |       10       *default\n"
           "  4    |       32      |       10      \n"
           "  5    |       32      |       15      ```\n")

load_dotenv()
TOKEN = token
GUILD = "Test Server"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.send(
        f'Hi {member.name}, willkommen auf dem Server!')


@bot.command(name='start', help='starts the dm chat')
async def start_dms(ctx):
    await ctx.message.author.create_dm()
    await ctx.send("DM Chat gestartet!")
    await ctx.message.author.send(
        f'```Hi {str(ctx.message.author).split("#")[0]}, was kann ich für dich tun?```\n\n{helpText}')


@bot.command(name='test', help="TEST!")
async def test(ctx):
    await ctx.send(
        f'```Hi {str(ctx.message.author).split("#")[0]}, du bist im Channel: {str(ctx.message.channel).split("#")[0]}!```')


@bot.command(name='encode', help="verschlüsseln eines Textes")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        if not args:
            await ctx.send("```Kein Text gegeben. Syntax: !encode <str>```")
        elif args:
            if len(" ".join(args)) > 155:
                argLen = len(' '.join(args))
                await ctx.message.author.send(
                    f"```css\n[Der Text darf maximal 155 Zeichen lang sein (Deiner war: {argLen}), aufgrund Limitierungen von Discord!]\n```")
                return
            from langNew import encodePrep
            from databases import hasDefault
            DefSeed = hasDefault(ctx.message.author)
            seed, out = encodePrep(" ".join(args), DefSeed)
            await ctx.message.author.send(f'```\n{out}```\n```\n Seed: {seed}\n```')

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='decode', help="entschlüsseln eines Textes")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        if not args:
            await ctx.send("```Kein Text gegeben. Syntax: !decode <seed> <text>```")
        elif len(args) == 1:
            from databases import hasDefault
            DefSeed = hasDefault(ctx.message.author)

            from langNew import decodePrep
            text = decodePrep(str("".join(args)), str(DefSeed))

            if text == "" or text.isspace() or text is None:
                text = "Es konnte nichts entschlüsselt werden! Falscher Seed?"

            await ctx.message.author.send(f"```\n{text}\n```")

        elif len(args) > 1:
            from langNew import decodePrep
            text = decodePrep("".join(args[1:]), str(args[0]))
            if text == "" or text.isspace() or text is None:
                text = "Es konnte nichts entschlüsselt werden! Falscher Seed?"

            await ctx.message.author.send(f"```\n{text}\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='seeds', help="lists all you quick seeds")
async def test(ctx):
    if str(ctx.message.channel.type) == 'private':
        from databases import listSeeds
        await ctx.message.author.send(f"```\n{listSeeds(ctx.message.author)}\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='addseed', help="add to your quick seeds")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        if not args:
            await ctx.send("```Keine Argumente gegeben. Syntax: !addseed <seed> <name>```")
        elif len(args) == 1:
            await ctx.send("```Seed oder Name fehlt! Syntax: !addseed <seed> <name>```")
        elif len(args) > 1:
            from databases import newseed
            result = newseed(ctx.message.author, str(args[0]), str(args[1]))
            await ctx.message.author.send(f"```\n{result}\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='delseed', help="remove from your quick seeds")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        if not args:
            await ctx.send("```Keine Argumente gegeben. Syntax: !delseed <name>```")
        elif len(args) == 1:
            from databases import getSeed
            seed = getSeed(ctx.message.author, args[0])
            if seed is None:
                await ctx.send("```Diesen Seednamen gibt es nicht!```")
                return
            botmessage = await ctx.channel.send(f'```css\n[Möchtest du wirklich den Seed: {seed} löschen?]\n```')
            await botmessage.add_reaction('\N{WHITE HEAVY CHECK MARK}')
            await botmessage.add_reaction('\N{CROSS MARK}')

            def checkUp(reaction, user):
                return user == ctx.author and (str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}' or str(
                    reaction.emoji) == '\N{CROSS MARK}')

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checkUp)
            except:
                await botmessage.delete()
            else:
                if str(reaction.emoji) == '\N{CROSS MARK}':
                    await botmessage.delete()
                    await ctx.message.author.send(f"```\nAbgebrochen!\n```")
                else:
                    await botmessage.delete()
                    from databases import removeseed
                    result = removeseed(ctx.message.author, str(args[0])).lower()
                    if result == "succes":
                        await ctx.message.author.send(f"```\nErfolgreich entfernt!\n```")
                    elif result == "error":
                        await ctx.message.author.send(f"```\nEs ist ein Fehler aufgetreten!\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='setseed', help="set standard seed to use, no argument to deactivate")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        if not args:
            from databases import delStandard
            result = delStandard(ctx.message.author).lower()
            if result == "succes":
                await ctx.message.author.send(f"```\nErfolgreich entfernt!\n```")
            if result == "error":
                await ctx.message.author.send(f"```\nEs ist ein Fehler aufgetreten!\n```")
        elif len(args) == 1:
            from databases import addStandard
            result = addStandard(ctx.message.author, str(args[0])).lower()
            if result == "succes":
                await ctx.message.author.send(f"```\nErfolgreich hinzugefügt!\n```")
            if result == "error":
                await ctx.message.author.send(f"```\nEs ist ein Fehler aufgetreten!\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='clearseeds', help="remove all your quick seeds")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':
        botmessage = await ctx.channel.send(u'```css\n[Möchtest du wirklich alle deine Seeds löschen?]\n```')
        await botmessage.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await botmessage.add_reaction('\N{CROSS MARK}')

        def checkUp(reaction, user):
            return user == ctx.author and (
                        str(reaction.emoji) == '\N{WHITE HEAVY CHECK MARK}' or str(reaction.emoji) == '\N{CROSS MARK}')

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checkUp)
        except:
            await botmessage.delete()
        else:
            if str(reaction.emoji) == '\N{CROSS MARK}':
                await botmessage.delete()
                await ctx.message.author.send(f"```\nAbgebrochen!\n```")
            else:
                await botmessage.delete()
                from databases import removeallseeds
                result = removeallseeds(ctx.message.author).lower()
                if result == "succes":
                    await ctx.message.author.send(f"```\nErfolgreich entfernt!\n```")
                elif result == "error":
                    await ctx.message.author.send(f"```\nEs ist ein Fehler aufgetreten!\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")

@bot.command(name='seed', help="generate a custom seed, length 8-256")
async def test(ctx, *args):
    if str(ctx.message.channel.type) == 'private':

        if not args:
            from langNew import OnlyGenerateSeed
            seed = OnlyGenerateSeed(32)
            await ctx.message.author.send(f"```{seed}```")
        elif args:
            try:
                laenge = int(args[0])
            except:
                await ctx.message.author.send(f"```css\n[Die Länge muss eine Zahl ohne Komma sein!]\n```")
                return
            if laenge in range(8, 256):
                from langNew import OnlyGenerateSeed
                laenge = int((laenge // 2) * 2)
                seed = OnlyGenerateSeed(laenge)
                await ctx.message.author.send(f"```{seed}```")
            elif laenge not in range(8, 256):
                await ctx.message.author.send("```css\n[Länge muss zwischen 8 und 255 liegen]\n```")

    else:
        await ctx.send("```Dieser Command funktioniert nur in DMs! !start um einen DM-Verlauf zu beginnen.```")


@bot.command(name='hilfe', help="Hilfe zu commands!")
async def test(ctx):
    await ctx.send(helpText)


bot.run(TOKEN)
