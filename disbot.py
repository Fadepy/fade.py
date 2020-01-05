import discord
from discord.ext import commands 
from discord.ext.commands import Bot
import datetime

Bot = commands.Bot( command_prefix = '.' ) #установили префикс для бота, '.' отвечает за начало команды
Bot.remove_command( 'help' )

#Функция, при коннекте бот пишет 'I am connected and ready to work'.
@Bot.event
async def on_ready():
	print('I am connected and ready to work.')

#Функция, выдает роль при входе на сервер
@Bot.event
async def on_member_join( member ):
	role = discord.utils.get( member.guild.roles, name = 'Все' )
	await member.add_roles(role)

#Команда .help выводит описание всех команд
@Bot.command( pass_contex = True )
async def help( ctx ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Описание команд', colour = discord.Color.green() )
	emb.add_field( name = '.bot', value = 'Бот расскажет о себе' )
	emb.add_field( name = '.hello', value = 'Бот поздоровается с Вами' )
	emb.add_field( name = '.time', value = 'Выводит точное время в милисекундах' )
	emb.add_field( name = '.author', value = 'Показывает авторство бота' )
	emb.add_field( name = '.clear + кол-во сообщений', value = 'Очистка чата (доступ для админов)' )
	emb.add_field( name = '.kick + @Имя пользователя', value = 'Кикает пользователя (доступ для админов)' )
	emb.add_field( name = '.mute + @Имя пользователя', value = 'Выдает мут пользователю (доступ для админов)' )
	emb.add_field( name = '.unmute + @Имя пользователя', value = 'Снимает мут с  пользователя (доступ для админов)' )
	emb.add_field( name = '.ban + @Имя пользователя + причина', value = 'Банит пользователя (доступ для админов)' )
	emb.add_field( name = '.unban + @Имя пользователя', value = 'Разбанивает пользователя (доступ для админов)' )
	await ctx.send( embed = emb)

#Команда .bot выводит наш текст с упоминанием
@Bot.command( pass_contex = True )
async def bot( ctx ):
	author = ctx.message.author
	await ctx.send( f'{ author.mention } Hello! I am a bot for discord. My developer is Fade, him junior Python developer.' )

#Команда .hello бот с нами здоровается
@Bot.command( pass_contex = True )
async def hello( ctx, amount = 1):
	await ctx.channel.purge( limit = 1 )
	author = ctx.message.author
	await ctx.send(	f'{ author.mention } Hello' )

#Команда .clear происходит очистка чата
@Bot.command( pass_contex = True )
@commands.has_permissions( administrator = True )
async def clear( ctx, amount = 10000 ):
	await ctx.channel.purge( limit = amount )
	emb = discord.Embed( title = 'Очистка чата', colour = discord.Color.green() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = 'Чат очищен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Спасибо за использование нашего бота!', value = 'Время {}'.format( datetime.datetime.now() ) )
	await ctx.send( embed = emb)

#Команда .kick кикаем пользователя
@Bot.command( pass_contex = True )
@commands.has_permissions( administrator = True )
async def kick( ctx, member: discord.Member, *, reason = 'Kick from Fade.py' ):
	await ctx.channel.purge( limit = 1 )
	await member.kick( reason = reason )
	emb = discord.Embed( title = 'Информация о кике', colour = discord.Color.red() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = 'Забанен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Время {}'.format( datetime.datetime.now() ), value = 'Пользователь: {}'.format( member.mention ) )
	await ctx.send( embed = emb)

#Команда .ban баним пользователя
@Bot.command( pass_contex = True )
@commands.has_permissions( administrator = True )
async def ban( ctx, member: discord.Member, *, reason = 'Ban from Fade.py' ):
	await ctx.channel.purge( limit = 1 )
	await member.ban( reason = reason )
	emb = discord.Embed( title = 'Информация о бане', colour = discord.Color.red() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = 'Забанен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Время {}'.format( datetime.datetime.now() ), value = 'Пользователь: {}'.format( member.mention ) )
	await ctx.send( embed = emb)

#Команда .unban баним пользователя
@Bot.command( pass_contex = True )
@commands.has_permissions( administrator = True )
async def unban( ctx, *,member ):
	await ctx.channel.purge( limit = 1 )
	banned_users = await ctx.guild.bans()
	for ban_entry in banned_users:
		user = ban_entry.user
		await ctx.guild.unban( user )
		emb = discord.Embed( title = 'Информация о разбане', colour = discord.Color.red() )
		emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
		emb.set_footer( text = 'Разабанен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
		emb.add_field( name = 'Время {}'.format( datetime.datetime.now() ), value = 'Пользователь: {}'.format( user.mention ) )
		await ctx.send( embed = emb)
		return

#Команда .mute мутим пользователя
@Bot.command( pass_contex = True)
@commands.has_permissions( administrator = True )
async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Muted' ) #выдаем роль Muted
	await member.add_roles( mute_role ) #выдаем роль Muted

	role = discord.utils.get( member.guild.roles, name = 'Все' ) #забираем роль Все
	await member.remove_roles(role) #забираем роль Все
	emb = discord.Embed( title = 'Информация о муте', colour = discord.Color.red() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = 'Замучен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Время {}'.format( datetime.datetime.now() ), value = 'Пользователь: {}'.format( member.mention ) )
	await ctx.send( embed = emb)

#Команда .unmute снимает мут с пользователя
@Bot.command( pass_contex = True)
@commands.has_permissions( administrator = True )
async def unmute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )
	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Все' ) #выдаем роль Muted
	await member.add_roles( mute_role ) #выдаем роль Muted

	role = discord.utils.get( member.guild.roles, name = 'Muted' ) #забираем роль Все
	await member.remove_roles(role) #забираем роль Все
	emb = discord.Embed( title = 'Информация о размуте', colour = discord.Color.red() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = 'Разамучен админом: {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Время {}'.format( datetime.datetime.now() ), value = 'Пользователь: {}'.format( member.mention ) )
	await ctx.send( embed = emb)

#Команда .time выводит точное время
@Bot.command( pass_contex = True )
async def time( ctx ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Точное время', colour = discord.Color.green() )
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Спасибо за использование нашего бота!', value = 'Время {}'.format( datetime.datetime.now() ) )
	await ctx.send( embed = emb)

#Команда .author выводит точное время
@Bot.command( pass_contex = True )
async def author( ctx ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Авторство бота', colour = discord.Color.green(), url = 'https://vk.com/demenkoroman')
	emb.set_author( name = Bot.user.name, icon_url = Bot.user.avatar_url )
	emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
	emb.add_field( name = 'Автор is Fade', value = 'Спасибо за использование нашего бота!' )
	await ctx.send( embed = emb)

#подключение бота по токену
token = open( 'token.txt', 'r' ).readline()
Bot.run( token )