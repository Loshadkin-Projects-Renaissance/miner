# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import info
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient

from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
vip=[441399484, 55888804]

craftable=['Бутерброд с рыбой','Приготовленное мясо','Печь','Колодец','Хлеб','Удочка','','','','','','','','','','','','']
recipes=['furnance', 'cookedmeat', 'fountain', 'bread', 'fishingrod', 'fishhamburger', 'woodsword', 'farm']

#@bot.message_handler(commands=['updatecraft'])
#def upd(m):
#        if m.from_user.id==441399484:
#            users.update_many({}, {'$set':{'craftable.hoe':0}})
#            print('yes')


#@bot.message_handler(commands=['update'])
#def upd(m):
#        if m.from_user.id==441399484:
#            users.update_many({}, {'$set':{'strenght':0}})
#            users.update_many({}, {'$set':{'squama':0}})
#            print('yes')

def recipetoname(x):
   text='У рецепта нет названия, сообщите об этом разработчику.'
   if x=='furnance':
      text='Печь'
   if x=='cookedmeat':
      text='Приготовленное мясо'
   if x=='fountain':
      text='Колодец'
   if x=='bread':
      text='Хлеб'
   if x=='fishingrod':
      text='Удочка'
   if x=='fishhamburger':
      text='Бутерброд с рыбой'
   if x=='woodsword':
      text='Деревянный меч'
   if x=='farm':
      text='Ферма'
   return text


client1=os.environ['database']
client=MongoClient(client1)
db=client.farmer
users=db.users


@bot.message_handler(commands=['start'])
def start(m):
   if users.find_one({'id':m.from_user.id})==None and m.chat.id==m.from_user.id:
      users.insert_one(createuser(m.from_user.id, m.from_user.first_name))
      kb=types.ReplyKeyboardMarkup()
      kb.add(types.KeyboardButton('👷🏻Добыча'))
      bot.send_message(m.chat.id, '''Здраствуй, ты попал в игру "Survival simulator"!
*Предыстория:*
На земле появился вирус, превращающий людей в зомби, передающийся через укус. В скором времени почти всё
население земли было заражено, и оставшимся в живых ничего не оставалось, кроме переселения на необитаемые острова.
Так как все, кого вы знали, были заражены, вы в одиночку построили плот, взяли минимум необходимых вещей, и отправились в плавание.
Через 3 дня плавания, в 5 часов утра, вы увидели берег какого-то острова. Первым делом, после высадки, вы решили, что нужно построить дом.
Для этого нужно дерево. Чтобы начать добывать его, нажмите кнопку "👷Добыча", а затем - кнопку "🌲Лес".''', parse_mode='markdown', reply_markup=kb)


 
@bot.message_handler(commands=['inventory'])
def inventory(m):
   x=users.find_one({'id':m.from_user.id})
   if x!=None:
      text=''
      if x['coal']>0:
         text+='Уголь: '+str(x['coal'])+'\n'
      if x['iron']>0:
         text+='Железо: '+str(x['iron'])+'\n'
      if x['gold']>0:
         text+='Золото: '+str(x['gold'])+'\n'
      if x['diamond']>0:
         text+='Алмазы: '+str(x['diamond'])+'\n'
      if x['wood']>0:
         text+='Дерево: '+str(x['wood'])+'\n'
      if x['rock']>0:
         text+='Камень: '+str(x['rock'])+'\n'
      if x['money']>0:
         text+='Деньги: '+str(x['money'])+'\n'
      if x['sand']>0:
         text+='Песок: '+str(x['sand'])+'\n'
      if x['salt']>0:
         text+='Соль: '+str(x['salt'])+'\n'
      if x['ruby']>0:
         text+='Рубины: '+str(x['ruby'])+'\n'
      if x['iridium']>0:
         text+='Иридий: '+str(x['iridium'])+'\n'
      if x['shugar']>0:
         text+='Сахар: '+str(x['shugar'])+'\n'
      if x['mushroom']>0:
         text+='Грибы: '+str(x['mushroom'])+'\n'
      if x['meat']>0:
         text+='Мясо: '+str(x['meat'])+'\n'
      if x['fish']>0:
         text+='Рыба: '+str(x['fish'])+'\n'
      if x['egg']>0:
         text+='Яйца: '+str(x['egg'])+'\n'
      if x['water']>0:
         text+='Вода: '+str(x['water'])+'\n'
      if x['squama']>0:
         text+='Чешуя: '+str(x['squama'])+'\n'
      if x['craftable']['cookedmeat']>0:
         text+='Приготовленное мясо: '+str(x['craftable']['cookedmeat'])+'\n'
      if x['craftable']['woodsword']>0:
         text+='Деревянный меч: '+str(x['craftable']['woodsword'])+'\n'
      if text=='':
         text='Инвентарь пуст!'
      bot.send_message(m.chat.id, text)
      
   
def recipetocraft(x):
   text='Рецепта нет! Обратитесь к разработчику.'
   if x=='furnance':
      text='*Печь:* 100 (Камень), 10 (Дерево), 30 (Голод) (/furnance).\n'
   if x=='cookedmeat':
      text='*Приготовленное мясо:* 1 (Мясо), 1 (Уголь) (/meat).\n'
   if x=='fountain':
      text='*Колодец:* 150 (Камень), 20 (Дерево), 1 (Ведро) (/fountain).\n'
   if x=='bread':
      text='*Хлеб:* 10 (Пшено) (/bread).\n'
   if x=='fishingrod':
      text='*Удочка:* 40 (Дерево), 10 (Нитки) (/rod).\n'
   if x=='fishhamburger':
      text='*Бутерброд с рыбой:* 15 (Рыба), 10 (Хлеб) (/fishburger).\n'
   if x=='woodsword':
      text='*Деревянный меч:* 40 (Дерево) (/woodsword).\n'
   if x=='farm':
      text='*Ферма:* 600 (Дерево), 250 (Камень), 20 (Вода), 1 (Мотыга), 70 (Голод), 30 (Минут) (/farm).\n'
   return text
   
@bot.message_handler(commands=['furnance'])
def furnance(m):
   x=users.find_one({'id':m.from_user.id})
   if 'furnance' in x['recipes']:
    if x['craftable']['furnance']<=0:
      if x['rock']>=100 and x['wood']>=10 and x['hunger']>=30:
         users.update_one({'id':m.from_user.id}, {'$inc':{'rock':-100}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'wood':-10}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'hunger':-30}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'craftable.furnance':1}})
         bot.send_message(m.chat.id, 'Вы успешно скрафтили Печь!')
      else:
         bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
    else:
      bot.send_message(m.chat.id, 'У вас уже есть Печь!')
   else:
      bot.send_message(m.chat.id, 'У вас нет этого рецепта!')
      
@bot.message_handler(commands=['meat'])
def meat(m):
   x=users.find_one({'id':m.from_user.id})
   if 'cookedmeat' in x['recipes']:
    if x['craftable']['furnance']>=1:
      if x['meat']>=1 and x['coal']>=1:
         users.update_one({'id':m.from_user.id}, {'$inc':{'coal':-1}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'meat':-1}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'craftable.cookedmeat':1}})
         bot.send_message(m.chat.id, 'Вы успешно скрафтили Приготовленное мясо!')
      else:
         bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
    else:
      bot.send_message(m.chat.id, 'Для крафта вам нужно: Печь.')
   else:
      bot.send_message(m.chat.id, 'У вас нет этого рецепта!')   
      
@bot.message_handler(commands=['farm'])
def meat(m):
   x=users.find_one({'id':m.from_user.id})
   if 'farm' in x['recipes']:
      if x['wood']>=600 and x['stone']>=250 and x['water']>=20 and x['craftable']['hoe']>=1 and x['hunger']>=70:
         users.update_one({'id':m.from_user.id}, {'$inc':{'stone':-250}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'wood':-600}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'hunger':-70}})
         users.update_one({'id':m.from_user.id}, {'$inc':{'craftable.hoe':-1}})
         users.update_one({'id':m.from_user.id}, {'$push':{'buildings':'farm'}})
         bot.send_message(m.chat.id, 'Вы успешно построили Ферму!')
      else:
         bot.send_message(m.chat.id, 'Недостаточно ресурсов!')
   else:
      bot.send_message(m.chat.id, 'У вас нет этого рецепта!')   
   
@bot.message_handler(commands=['help'])
def help(m):
   bot.send_message(m.chat.id, '*Что обозначают значки ⚪️,🔵,🔴,🔶 около добытых ресурсов?*\n'+
                    'Обозначают они редкость материалов:\n'+
                    '⚪️ - обычные;\n'+
                    '🔵 - редкие;\n'+
                    '🔴 - эпические;\n'+
                    '🔶 - легендарные.', parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def text(m):
   if m.from_user.id==m.chat.id:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
      if x['tutorial']==1:
         if m.text=='👷🏻Добыча':
            kb=types.ReplyKeyboardMarkup()
            kb.add(types.KeyboardButton('🌲Лес'))
            bot.send_message(m.chat.id, 'Куда вы хотите направиться?', reply_markup=kb)
         elif m.text=='🌲Лес' and x['tforest']==0:
            users.update_one({'id':m.from_user.id}, {'$set':{'tforest':1}})
            bot.send_message(m.chat.id, 'Вы отправились в лес. Вернётесь через минуту (Минута вашего времени = 15 минут жизни на острове).')
            t=threading.Timer(60, tforest, args=[m.from_user.id])
            t.start()
         elif m.text=='🔨Постройка':
            kb=types.ReplyKeyboardMarkup()
            kb.add(types.KeyboardButton('⛺️Дом'))
            bot.send_message(m.chat.id, 'Что вы хотите построить?', reply_markup=kb)
         elif m.text=='⛺️Дом' and x['thouse']==0:
            users.update_one({'id':m.from_user.id}, {'$set':{'thouse':1}})
            bot.send_message(m.chat.id, 'Вы отправились строить дом. Вернётесь через 2 минуты.')
            users.update_one({'id':m.from_user.id}, {'$set':{'wood':0}})
            t=threading.Timer(120, thouse, args=[m.from_user.id])
            t.start()
      else:
         if m.text=='Обо мне':
            bot.send_message(m.chat.id, 'Привет, '+x['name']+'!\n'+
                             'Голод: '+str(x['hunger'])+'/'+str(x['maxhunger'])+'🍗\n'+
                             'Уровень: '+str(x['level'])+'\n'+
                             'Опыт: '+str(x['exp'])+'\n'+
                             'Инвентарь: /inventory')
            
         elif m.text=='Добыча':
            kb=types.ReplyKeyboardMarkup()
            kb.add(types.KeyboardButton('🌲Лес'))
            kb.add(types.KeyboardButton('🕳Пещера'))
            kb.add(types.KeyboardButton('🐖Охота'))
            kb.add(types.KeyboardButton('↩️Назад'))
            bot.send_message(m.chat.id, 'Куда хотите отправиться?', reply_markup=kb)
            
         elif m.text=='Дом':
            kb=types.ReplyKeyboardMarkup()
            kb.add(types.KeyboardButton('⚒Крафт'))
            kb.add(types.KeyboardButton('↩️Назад'))
            bot.send_message(m.chat.id, 'Дома вы можете крафтить полезные вещи и строить дополнительные строения.', reply_markup=kb)
            
         elif m.text=='⚒Крафт':
            x=users.find_one({'id':m.from_user.id})
            text='Список того, что вы можете скрафтить:\n'
            for ids in x['recipes']:
               text+=recipetocraft(ids)
            if text=='Список того, что вы можете скрафтить:\n':
               text='У вас пока что нет рецептов. Получить их можно, добывая ресурсы в любой локации.'
            bot.send_message(m.chat.id, text, parse_mode='markdown')
            
         elif m.text=='🌲Лес':
          x=users.find_one({'id':m.from_user.id})
          if x['farming']==0:
            users.update_one({'id':m.from_user.id}, {'$set':{'farming':1}})
            bot.send_message(m.chat.id, 'Вы отправились в лес. Вернётесь через 5 минут.')
            t=threading.Timer(300, forest, args=[m.from_user.id])
            t.start()
          else:
            bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')
            
         elif m.text=='🕳Пещера':
          x=users.find_one({'id':m.from_user.id})
          if x['farming']==0:
            users.update_one({'id':m.from_user.id}, {'$set':{'farming':1}})
            bot.send_message(m.chat.id, 'Вы отправились в пещеру. Вернётесь через 5 минут.')
            t=threading.Timer(300, cave, args=[m.from_user.id])
            t.start()
          else:
            bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')
            
         elif m.text=='🐖Охота':
          x=users.find_one({'id':m.from_user.id})
          if x['farming']==0:
            users.update_one({'id':m.from_user.id}, {'$set':{'farming':1}})
            bot.send_message(m.chat.id, 'Вы отправились на охоту. Вернётесь через 5 минут.')
            t=threading.Timer(300, hunt, args=[m.from_user.id])
            t.start()
          else:
            bot.send_message(m.chat.id, 'Вы уже заняты добычей ресурсов, попробуйте позже.')
        
         elif m.text.lower()=='тест':
            if m.from_user.id==441399484:
                bot.send_message(m.chat.id, 'Вы отправились в пещеру. Вернётесь через 3 секунды.')
                users.update_one({'id':m.from_user.id}, {'$set':{'farming':1}})
                t=threading.Timer(3, cave, args=[m.from_user.id])
                t.start()
                        
         
         elif m.text=='↩️Назад':
            kb=types.ReplyKeyboardMarkup()
            kb.add('Добыча')
            kb.add('Дом')
            kb.add('Обо мне')
            bot.send_message(m.chat.id, 'Добро пожаловать домой!', reply_markup=kb)
            
               
            
def forest(id):
   woodtexts=['Вы вернулись из леса. В этот раз удалось добыть:\n']
   wood=random.randint(1,100)
   rock=random.randint(1,100)
   meat=random.randint(1,100)
   gwood=0
   grock=0
   gmeat=0
   if wood<=75:
      wood=1
      gwood=random.randint(4, 15)
   else:
      wood=0
   if rock<=15:
      rock=1
      grock=random.randint(1,8)
   else:
      rock=0
   if meat<=15:
      meat=1
      gmeat=random.randint(1,3)
   else:
      meat=0
   recources=''  
   text=random.choice(woodtexts)
   if wood==1:
      recources+='⚪️Дерево: '+str(gwood)+'\n'
   if rock==1:
      recources+='🔵Камень: '+str(grock)+'\n'
   if meat==1:
      recources+='🔵Мясо: '+str(gmeat)+'\n'
   
   grecipe=random.randint(1,100)
   if grecipe<=15:
      x=users.find_one({'id':id})
      recipe=random.choice(recipes)
      if len(x['recipes'])<len(recipes):
         while recipe in x['recipes']:
            recipe=random.choice(recipes)
         users.update_one({'id':id}, {'$push':{'recipes':recipe}})
         recources+='🔴Рецепт: '+recipetoname(recipe)
      
   text=random.choice(woodtexts)
   if wood==0 and rock==0 and meat==0 and grecipe>15:
      text='В этот раз ничего добыть не удалось. Зато вы прогулялись по лесу и хорошо отдохнули!'
    
   users.update_one({'id':id}, {'$inc':{'wood':gwood}})
   users.update_one({'id':id}, {'$inc':{'meat':gmeat}})
   users.update_one({'id':id}, {'$inc':{'rock':grock}})
   users.update_one({'id':id}, {'$set':{'farming':0}})
   try:
      bot.send_message(id, text+recources)
   except:
      pass
   
   
def hunt(id):
   hunttexts=['Вы вернулись с охоты. В этот раз удалось добыть:\n']
   meat=random.randint(1,100)
   eggs=random.randint(1,100)
   mushroom=random.randint(1,100)
   fish=random.randint(1,100)
   gmeat=0
   geggs=0
   gfish=0
   gmushroom=0

   if meat<=60:
      meat=1
      gmeat=random.randint(3,8)
   else:
      meat=0
      
   if eggs<=25:
      eggs=1
      geggs=random.randint(1,4)
   else:
      eggs=0
      
   if mushroom<=1:
      mushroom=1
      gmushroom=1
   else:
      mushroom=0
      
   if fish<=40:
      fish=1
      gfish=random.randint(2,6)
   else:
      fish=0
      
   recources=''  
   text=random.choice(hunttexts)
   if meat==1:
      recources+='⚪️Мясо: '+str(gmeat)+'\n'
   if fish==1:
      recources+='⚪️Рыба: '+str(gfish)+'\n'
   if eggs==1:
      recources+='🔵Яйца: '+str(geggs)+'\n'
   if mushroom==1:
      recources+='🔶Грибы: '+str(gmushroom)+'\n'
      
   grecipe=random.randint(1,100)
   if grecipe<=15:
      x=users.find_one({'id':id})
      recipe=random.choice(recipes)
      if len(x['recipes'])<len(recipes):
         while recipe in x['recipes']:
            recipe=random.choice(recipes)
         users.update_one({'id':id}, {'$push':{'recipes':recipe}})
         recources+='🔴Рецепт: '+recipetoname(recipe)
      
   text=random.choice(hunttexts)
   if meat==0 and fish==0 and eggs==0 and mushroom==0 and grecipe>15:
      text='В этот раз никого поймать не удалось - добыча была слишком быстрой.'
      
   users.update_one({'id':id}, {'$inc':{'meat':gmeat}})
   users.update_one({'id':id}, {'$inc':{'fish':gfish}})
   users.update_one({'id':id}, {'$inc':{'egg':geggs}})
   users.update_one({'id':id}, {'$inc':{'mushroom':gmushroom}})
   users.update_one({'id':id}, {'$set':{'farming':0}})
   try:
      bot.send_message(id, text+recources)
   except:
      pass
   
   
   
def cave(id):
   cavetexts=['Вы вернулись из пещеры. В этот раз удалось добыть:\n']
   iron=random.randint(1,100)
   gold=random.randint(1,100)
   diamond=random.randint(1,1000)
   ruby=random.randint(1,1000)
   rock=random.randint(1,100)
   coal=random.randint(1,100)
   giron=0
   grock=0
   ggold=0
   gdiamond=0
   gcoal=0
   gruby=0
   x=users.find_one({'id':id})
   
   if iron<=20:
      iron=1
      giron=random.randint(2, 10)
   else:
      iron=0
      
   if rock<=75:
      rock=1
      grock=random.randint(5,14)
   else:
      rock=0
      
   if gold<=5:
      gold=1
      ggold=random.randint(1,5)
   else:
      gold=0
      
   if diamond<=2:
      diamond=1
      gdiamond=random.randint(1,3)
   else:
      diamond=0
      
   if coal<=40:
      coal=1
      gcoal=random.randint(1,15)
   else:
      coal=0
      
   if ruby<=1:
      ruby=1
      gruby=random.randint(1,3)
   else:
      ruby=0
      
   recources=''  
   text=random.choice(cavetexts)
   if rock==1:
      recources+='⚪️Камень: '+str(grock)+'\n'
   if coal==1:
      recources+='⚪️Уголь: '+str(gcoal)+'\n'
   if iron==1:
      recources+='🔵Железо: '+str(giron)+'\n'
   if gold==1:
      recources+='🔴Золото: '+str(ggold)+'\n'
   if diamond==1:
      recources+='🔶Алмазы: '+str(gdiamond)+'\n'
   if ruby==1:
      recources+='🔶Рубины: '+str(gruby)+'\n'
      
   grecipe=random.randint(1,100)
   if grecipe<=15:
      recipe=random.choice(recipes)
      if len(x['recipes'])<len(recipes):
         while recipe in x['recipes']:
            recipe=random.choice(recipes)
         users.update_one({'id':id}, {'$push':{'recipes':recipe}})
         recources+='🔴Рецепт: '+recipetoname(recipe)
      else:
         grecipe=100
      
   text=random.choice(cavetexts)
   if rock==0 and iron==0 and coal==0 and gold==0 and diamond==0 and ruby==0 and grecipe>15:
      text='В этот раз ничего добыть не удалось - пещера оказалось слишком опасной, и вы решили не рисковать.'
    
   users.update_one({'id':id}, {'$inc':{'rock':grock}})
   users.update_one({'id':id}, {'$inc':{'coal':gcoal}})
   users.update_one({'id':id}, {'$inc':{'iron':giron}})
   users.update_one({'id':id}, {'$inc':{'gold':ggold}})
   users.update_one({'id':id}, {'$inc':{'diamond':gdiamond}})
   users.update_one({'id':id}, {'$inc':{'ruby':gruby}})
   users.update_one({'id':id}, {'$set':{'farming':0}})
   try:
      bot.send_message(id, text+recources)
   except:
      pass
   
   mobs=['Червя-камнееда']
   text=''
   enemy=random.randint(1,100)
   recources=''
   if enemy<=20:
      mob=random.choice(mobs)
      text='По пути назад вы встретили '+mob+'!\n.............\n'
      y=random.randint(1,100)
      if 'woodsword' in x['craftable']:
         x['strenght']+=8
      if y-x['strenght']<=1:
         gleither=0
         if mob=='Червя-камнееда':
            leither=random.randint(1,100)
            if leither<=50:
               gleither=random.randint(1,5)
               recources+='⚪️Чешуя: '+str(gleither)+'\n'
         text2='Вы оказались сильнее, и убили врага. Полученные ресурсы:\n'+recources
         users.update_one({'id':id}, {'$inc':{'squama':gleither}})
      else:
         text2='Враг был силён, и вам пришлось отступить.'
      bot.send_message(id, text+text2)
            
      
def tforest(id):
   kb=types.ReplyKeyboardMarkup()
   kb.add(types.KeyboardButton('🔨Постройка'))
   users.update_one({'id':id}, {'$set':{'wood':1000}})
   try:
      bot.send_message(id, 'Прошло пол часа. С помощью топора, который вы взяли с собой в путь, вы добыли 1000 ед. дерева -'+
   ' Этого должно хватить на постройку дома. Чтобы начать постройку, нажмите кнопку "🔨Постройка", и выберите пункт "⛺️Дом".', reply_markup=kb)
   except:
      pass


def thouse(id):
   kb=types.ReplyKeyboardMarkup()
   kb.add('Добыча')
   kb.add('Дом')
   kb.add('Обо мне')
   try:
      bot.send_message(id, 'Поздравляю! Вы построили себе дом! Здесь вы сможете спастись от дикой природы и от холода.'+
                    ' Дальше выживать придётся самостоятельно. Но осторожнее: добывая ресурсы, вы можете встретить других игроков, и если'+
                    ' они будут сильнее вас - добычу придётся отдать.', reply_markup=kb)
   except:
      pass
   users.update_one({'id':id}, {'$set':{'tutorial':0}})
                    
                   
              
         
 
def createuser(id, name):
   return{'id':id,
          'name':name,
          'strenght':0,
          'coal':0,
          'iron':0,
          'gold':0,
          'diamond':0,
          'wood':0,
          'rock':0,
          'money':0,
          'sand':0,
          'salt':0,
          'ruby':0,
          'shugar':0,
          'mushroom':0,
          'meat':0,
          'fish':0,
          'egg':0,
          'water':0,
          'iridium':0,
          'hunger':100,
          'maxhunger':100,
          'buildings':[],
          'farm':None,
          'animals':[],
          'exp':0,
          'level':1,
          'tutorial':1,
          'tforest':0,
          'thouse':0,
          'building':0,
          'farming':0,
          'recipes':[],
          'craftable':{'furnance':0,
                       'cookedmeat':0,
                       'fountain':0,
                       'bread':0,
                       'fishingrod':0,
                       'fishhamburger':0,
                       'woodsword':0,
                       'hoe':0
          },
          'squama':0
         }

if True:
 try:
   print('7777')
   x=users.find({})
   for ids in x:
      try:
         bot.send_message(ids['id'], 'Бот был перезагружен! Если вы в этот момент добывали ресурсы, придется начать сначала. Приношу свои извенения за это.')
      except:
         pass
   users.update_many({}, {'$set':{'farming':0}})
   users.update_many({}, {'$set':{'building':0}})
   bot.polling(none_stop=True,timeout=600)
 except (requests.ReadTimeout):
        print('!!! READTIME OUT !!!')           
        bot.stop_polling()
        time.sleep(1)
        check = True
        while check==True:
          try:
            bot.polling(none_stop=True,timeout=1)
            print('checkkk')
            check = False
          except (requests.exceptions.ConnectionError):
            time.sleep(1)
   
   
        

   
#if __name__ == '__main__':
 # bot.polling(none_stop=True)

#while True:
#    try:
  #      bot.polling()
 #   except:
  #      pass
#    time.sleep(1)
       
