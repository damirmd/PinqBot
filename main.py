import discord
import requests
import json
from discord.ext import commands
from config import settings
import random
api_key = "46d81b1aedcf0efbffeadb43ef70dea1"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#_____________________________________

bot = commands.Bot(command_prefix = settings['prefix'])

#@bot.command()
#async def помощь(ctx):
#    author = ctx.message.author
#   await ctx.send(f'Список команд:\n!помощь – актуальный список команд\n!кот – случайное фото кота\n!погода – прогноз погоды в выбранном вами городе')

@bot.command()
async def помощь(ctx):
    embed=discord.Embed(title="Помощь", description="Список команд:\n\n!помощь – актуальный список команд\n\n!кот – случайное фото кота\n\n!погода – прогноз погоды в выбранном вами городе", color=0x8f72da)
    await ctx.send(embed=embed)


#---------------------------------------
@bot.command()
async def кот(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') #
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0x8f72da, title = 'Случайное фото кошки')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)




@bot.command()
async def погода(ctx, *, city: str):

        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel

        if x["cod"] != "404":

                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]

                embed = discord.Embed(
                    title=f"Погода в городе {city_name}",
                    color=0x8f72da,
                    timestamp=ctx.message.created_at,
                )
                embed.add_field(
                    name="Общее",
                    value=f"**{weather_description}**",
                    inline=False)
                embed.add_field(
                    name="Температура",
                    value=f"**{current_temperature_celsiuis}°C**",
                    inline=False)
                embed.add_field(
                    name="Влажность воздуха", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(
                    name="Атмосферное давление",
                    value=f"**{current_pressure}hPa**",
                    inline=False)
                embed.set_footer(text=f"Запросил {ctx.author.name}")

                await channel.send(embed=embed)

        else:
                await channel.send(
                    f"Нет результатов по данному городу!")






bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
