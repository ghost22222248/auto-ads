import asyncio
import os
from telethon import TelegramClient, events
from datetime import datetime
import time
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
import random
import requests
import json

############################### Bot ############################################
server = 'https://telegram-lottery-default-rtdb.firebaseio.com/'

TOKEN='1785407247:AAEArN7KPU8a4Z2Gb5-NzlL08aqkVrfTiK8'


def start_message(name):
    return 'Hi {}.\nWelcome to Eta Eta! A classic game that offers 50/50 chance of winning.'.format(name)


def start(update, context):

     update.message.reply_text('yeah')

def start2(update, context):
    current_balance = 1000
    bet_size=50
    user_choice = ''
    drawn_choice = ''
    print(update.message.chat_id)
    r = requests.get(server+'users/'+str(update.message.chat_id)+'.json')
    r2=requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json')
    print(r2.json())
    if (str(requests.get(server+'users/'+str(update.message.chat_id)+'.json').json())=='None'):
        print('registering')
        requests.put(server + 'users/' + str(update.message.chat_id) + '.json',json={'chat_id':update.message.chat_id,'current_balance':1000,'bet_size':50})
    else:
        print('recovering')
        current_balance=int(requests.get(server + 'users/' + str(update.message.chat_id) + '/current_balance.json').json())
        bet_size=int(requests.get(server + 'users/' + str(update.message.chat_id) + '/bet_size.json').json())

    print(r.json())
    update.message.reply_text(start_message(update.message.chat.first_name))
    update.message.reply_text(main_menu_message(drawn_choice, bet_size, current_balance),
                              reply_markup=main_menu_keyboard())


def conv(inp):
    if (inp == 'heads'):
        return 1
    if (inp == 'tails'):
        return 0
    if (inp == 'cbs'):
        return 2
    if (inp == 'back'):
        return 4
    if (inp == 'deposit'):
        return 5
    if (inp == 'withdraw'):
        return 6


def setwinprob(prob):
     ch=random.randint(1, 100)
     if(ch<=prob): return 1
     else: return 0

def altch(drawn_choice):
    if(drawn_choice=='heads'): return 'tails'
    else: return 'heads'

def All_queries_handler(update, context):



    query = update.callback_query
    query.answer()
    current_balance=int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json()))
    bet_size=int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/bet_size.json').json()))
    print(int(str(requests.get(server + 'users/' + str(query.message.chat_id) + '/current_balance.json').json())))
    user_choice = ''
    drawn_choice = ''
    #cn = random.randint(0, 1)
    cn=setwinprob(40)
    # print('result: '+str(cn) +query.data+ ' '+altch(query.data))
    if(query.data!=''):
     print(query.data)
    if (cn == 0):
        drawn_choice = altch(query.data)
    else:
        drawn_choice = query.data

    #  query.message.reply_text(text=main_menu_message(drawn_choice,bet_size,current_balance),reply_markup=main_menu_keyboard())
    # print(query.data+'\n')
    if(query.data=='deposit_choice_keyboard'):

       query.edit_message_text('Choose amount in Birr: ', reply_markup=deposit_choice_keyboard())

    if(query.data=='withdraw_choice_keyboard'):
       query.edit_message_text('Choose amount in Birr: ', reply_markup=withdraw_choice_keyboard())

    if(query.data=='deposit_method_keyboard'):
       print('deposit')
       query.edit_message_text('Choose deposit method: ', reply_markup=deposit_choice_keyboard())

    if(query.data=='withdraw_method_keyboard'):
       query.edit_message_text('Choose withdraw method: ', reply_markup=withdraw_method_keyboard())


    if (query.data == 'back'): #back button
        query.edit_message_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                reply_markup=main_menu_keyboard())




    if (query.data == 'cbs'): # change bet size
            query.edit_message_text('Choose bet size in coins', reply_markup=bet_choice_keyboard())
            print('change-bet-size')
    if (conv(query.data) == 1 or conv(query.data) == 0): # head or tail
        print('heads or tails')
        if (current_balance < bet_size):  # low balance
                query.edit_message_text('You don\'t have enough balance.', reply_markup=balance_low_keyboard())
        else: # enough balance
                #if (conv(query.data) == cn):  # won
            if(cn==1):
                    print('won')
                    current_balance += bet_size
                    #requests.put(server + 'users/' + str(query.message.chat_id) + '/current_balance.json',current_balance)
                    requests.put(server + 'users/' + str(query.message.chat_id) + '.json',json={'chat_id':query.message.chat_id,'current_balance':current_balance,'bet_size':bet_size})
                    query.edit_message_text(won_message(drawn_choice, bet_size, current_balance))
                    query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                             reply_markup=main_menu_keyboard())
            else:  # lost
                    print('lost')
                    current_balance -= bet_size
                    #requests.put(server + 'users/' + str(query.message.chat_id) + '/current_balance.json',current_balance)
                    requests.put(server + 'users/' + str(query.message.chat_id) + '.json',json={'chat_id':query.message.chat_id,'current_balance':current_balance,'bet_size':bet_size})

                    query.edit_message_text(lost_message(drawn_choice, bet_size, current_balance))
                    query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                             reply_markup=main_menu_keyboard())

    else:
     if (query.data[0] == 'b'):  #change bet size


        bet_size = int(query.data[1:len(query.data)])
        #requests.put(server + 'users/' + str(query.message.chat_id) + '/bet_size.json',int(query.data))
        requests.put(server + 'users/' + str(query.message.chat_id) + '.json',json={'chat_id':query.message.chat_id,'current_balance':current_balance,'bet_size':bet_size})

        query.edit_message_text('Bet size is changed to ' + query.data[1:len(query.data)] + ' coins.')
        query.message.reply_text(text=main_menu_message(drawn_choice, bet_size, current_balance),
                                 reply_markup=main_menu_keyboard())

def bet_choice_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('50', callback_data='b50'),
            InlineKeyboardButton('100', callback_data='b100'),
            InlineKeyboardButton('300', callback_data='b200'),
            InlineKeyboardButton('500', callback_data='b500')
        ],

        [
            InlineKeyboardButton('1000', callback_data='b1000'),
            InlineKeyboardButton('2000', callback_data='b2000'),
            InlineKeyboardButton('3000', callback_data='b3000'),
            InlineKeyboardButton('5000', callback_data='b5000')
        ],

        [
            InlineKeyboardButton('10000', callback_data='b10000'),
            InlineKeyboardButton('20000', callback_data='b20000'),
            InlineKeyboardButton('30000', callback_data='b30000'),
            InlineKeyboardButton('50000', callback_data='b50000')
        ],
        [
            InlineKeyboardButton('Go back', callback_data='back')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)

def deposit_choice_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('10', callback_data='d10'),
            InlineKeyboardButton('20', callback_data='d20'),
            InlineKeyboardButton('30', callback_data='d30'),
            InlineKeyboardButton('50', callback_data='d50')
        ],

        [
            InlineKeyboardButton('100', callback_data='d100'),
            InlineKeyboardButton('200', callback_data='d200'),
            InlineKeyboardButton('300', callback_data='d300'),
            InlineKeyboardButton('500', callback_data='d500')
        ],

        [
            InlineKeyboardButton('1000', callback_data='d1000'),
            InlineKeyboardButton('2000', callback_data='d2000'),
            InlineKeyboardButton('3000', callback_data='d3000'),
            InlineKeyboardButton('5000', callback_data='d5000')
        ],
        [
            InlineKeyboardButton('Go back', callback_data='back_dm')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)

def withdraw_choice_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('10', callback_data='w10'),
            InlineKeyboardButton('20', callback_data='w20'),
            InlineKeyboardButton('30', callback_data='w30'),
            InlineKeyboardButton('50', callback_data='w50')
        ],

        [
            InlineKeyboardButton('100', callback_data='w100'),
            InlineKeyboardButton('200', callback_data='w200'),
            InlineKeyboardButton('300', callback_data='w300'),
            InlineKeyboardButton('500', callback_data='w500')
        ],

        [
            InlineKeyboardButton('1000', callback_data='w1000'),
            InlineKeyboardButton('2000', callback_data='w2000'),
            InlineKeyboardButton('3000', callback_data='w3000'),
            InlineKeyboardButton('5000', callback_data='w5000')
        ],
        [
            InlineKeyboardButton('Go back', callback_data='back_wm')
        ],

    ]
    return InlineKeyboardMarkup(keyboard)


def keyboards():
    keyboard = [
        [
            KeyboardButton('Play', callback_data='play')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def deposit_method_keyboard():
    keyboard = [

            InlineKeyboardButton('CBE birr', callback_data='cbebirr_d'),


            InlineKeyboardButton('Mobile Airtime', callback_data='airtime_d'),


            InlineKeyboardButton('Go Back', callback_data='back'),

    ]
    return InlineKeyboardMarkup(keyboard)

def withdraw_method_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('CBE birr', callback_data='cbebirr_w')
        ],
        [
            InlineKeyboardButton('Mobile Airtime', callback_data='airtime_w')
        ],
        [
            InlineKeyboardButton('Go Back', callback_data='back')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def deposit_button():
    keyboard = [
        [
            KeyboardButton('CBE birr', callback_data='cbebirr_dc')
        ],
        [
            KeyboardButton('Mobile Airtime', callback_data='airtime_dc')
        ],
        [
            KeyboardButton('Go Back', callback_data='back')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def withdraw_button():
    keyboard = [
        [
            KeyboardButton('CBE birr', callback_data='cbebirr_wc')
        ],
        [
            KeyboardButton('Mobile Airtime', callback_data='airtime_wc')
        ],
        [
            KeyboardButton('Go Back', callback_data='back')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Heads', callback_data='heads'),
            InlineKeyboardButton('Tails', callback_data='tails')
        ],
        [
            InlineKeyboardButton('Deposit', callback_data='deposit_method_keyboard'),
            InlineKeyboardButton('Withdraw', callback_data='withdraw_method_keyboard')
        ],
        [InlineKeyboardButton('Change bet size', callback_data='cbs')],
    ]
    return InlineKeyboardMarkup(keyboard)


def balance_low_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Deposit', callback_data='deposit'),
            InlineKeyboardButton('Change Bet size', callback_data='cbs')
        ],
        [InlineKeyboardButton('Go back', callback_data='back')],
    ]
    return InlineKeyboardMarkup(keyboard)


def won_message(drawn_choice, bet_size, current_balance):

    return '*\n*\nCongratulations!! You have won ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(current_balance) + ' coins.\n*\n*'


def lost_message(drawn_choice, bet_size, current_balance):

    return '*\n*\nOops... you have lost ' + str(
        bet_size) + ' coins. Coin landed on ' + drawn_choice + '. Your balance is ' + str(current_balance) + ' coins.\n*\n*'


def main_menu_message(drawn_choice, bet_size, current_balance):
    return 'Heads or Tails?   Bet size: ' + str(bet_size) + ' coins\n\n(1 Birr = 100 coins)\n\nCurrent balance: ' + str(
        current_balance) + ' coins or '+str(
        current_balance/100)+' Birr'


def main():
    TOKEN='1785407247:AAEArN7KPU8a4Z2Gb5-NzlL08aqkVrfTiK8'
    #PORT=process.env.PORT
    
    updater = Updater('1785407247:AAEArN7KPU8a4Z2Gb5-NzlL08aqkVrfTiK8', use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(All_queries_handler))

    #updater.start_polling()
    
    PORT=int(os.environ.get("PORT",8443))
    #PORT=8443
    print("EXEC 7")
    print("port "+str(PORT))
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url='https://tele2442.herokuapp.com/' + TOKEN)
    #updater.idle()
    #updater.bot.setWebhook('https://tele2442.herokuapp.com/' + TOKEN)
    print("done")


main()


session_name = "session_name"
api_id = '14940426'
api_hash = 'a5e6221082b82f157025f48cc78692e2'

f=open("last.txt","r")
st=float(f.read())
f.close()


async def main2():
    #st = 1658651373.806289
    ind=0
    ind2=0
    async with TelegramClient(session_name, api_id, api_hash) as client:
      TOKEN='1785407247:AAEArN7KPU8a4Z2Gb5-NzlL08aqkVrfTiK8'
      while(1==1):
       dt = datetime.now().timestamp()
       if dt-st>1000:

        #requests.get('https://tele2442.herokuapp.com/' + TOKEN)
        message2 = 'Worrying does not take away tommorow\'s problems. It takes away today\'s peace.\n\nhttps://t.me/lifeisgreatt'
        message3 = 'When you have to make a hard decision,\njust flip a coin.\nBecause when that coin is in the air, you suddenly know what you\'re hopping for.\n\nhttps://t.me/lifeisgreatt'
        message = 'Increase youtube subscribers, views, likes, comments and watch-hours.\n\nAre you struggling to get youtube subscribers?\nMaybe you are posting great content but need a little push to make your youtube channel bigger.\n\nWe can get you real youtube subscribers and increase your video views, likes and comments.\n\nContact us: @Ghost_advertisement\n\n\nየዩቲዩብ ተመዝጋቢዎችን ለማግኘት እየታገልክ ነው?\nምናልባት አሪፍ ይዘት እየለጠፍክ ነው ነገር ግን የዩቲዩብ ቻናልህን ትልቅ ለማድረግ ትንሽ ግፊት ያስፈልግሃል።\n\nእውነተኛ የዩቲዩብ ተመዝጋቢዎችን ልናገኝህ እና የቪዲዮ እይታህን፣ መውደዶችህን እና አስተያየቶችህን ማሳደግ እንችላለን።\n\n  ያግኙን: @Ghost_advertisement' 
        message1 = 'Welcome to Eta Eta. It is a simple game of heads and tails. If the coin flips to your choice, you win twice your bet. You can bet real money.\n\nIt offers 50/50 chance. Try your luck.\n\nhttps://t.me/etaeta24bot\n\nወደ እታ እታ እንኳን በደህና መጡ። እሱ ቀላል የጭንቅላቶች እና የጅራት ጨዋታ ነው። \n\nሳንቲሙ ወደ ምርጫዎ ከተገለበጠ ውርርድዎን በእጥፍ ያሸንፋሉ። እውነተኛ ገንዘብ ለውርርድ ይችላሉ። ዕድልዎን ይሞክሩ።\n\nhttps://t.me/etaeta24bot'
        message_pr = 'https://youtu.be/uSI7hjBaycc'
        message_pr2 = '📔 ማንበብ እና ማወቅ ሙሉ ሰው ያደርጋል ይህንን post የምታዩት 97% እነኚህን እንስሳቶች አታውቋቸውም👇👇 በአለማችን ላይ ያሉ አስደናቂ እውነታዎችን ለማወቅ ይህንን video በመንካት የምታገኙትን የ YouTube channel በመንካት subscribe አድርጉ እንዲሁም የ ደውል 🛎 ምልክቷን ተጫኑ \n👇👇👇👇👇👇👇👇👇👇👇👇👇\n\nhttps://youtu.be/APZqjfObWok'
        messages = [message, message1,message_pr2]
        if(ind == 1): 
          ind=2
        else: 
          ind=2
        #await client.send_message('me', messages[ind])
        try:
         await client.send_message('Hwgsguaihwuwiwibot', '/start')
        except Exception as e:
            print('Ex Error '+str(e))         
        try:    
         await client.send_message('etaeta24bot', '/start')
        except Exception as e:
            print('Ex Error '+str(e))  
        try:
         await client.send_message('ethio_free_promotion', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))  
        #await client.send_message('UnlimitedAdvertisement_Free', messages[ind])
        #await client.send_message('AllPromotionsGroup', messages[ind])
        try:
         await client.send_message('backourmoney', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))  
        try:
         await client.send_message('free_cross_promotions', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))  
        try:
         await client.send_message('free_promotion_site', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))  
        try:
         await client.send_message('Amazingfam07', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))  
        
        try:
         await client.send_message('advertisehereforfree', messages[ind])
        except Exception as e:
            print('Ex Error '+str(e))          
        
        #requests.get('https://tele2442.herokuapp.com/' + TOKEN)
        f=open("last_60.txt")
        if(datetime.now().timestamp()-int(f.read())>3600):
           if(ind2 == 1): 
            ind2=0
           else: 
            ind2=1
           try:
             await client.send_message('zionhotsale', messages[ind])
           except Exception as e:
             print('Ex Error '+str(e)) 
        f.close() 
        
        f=open("count.txt","r")
        count = int(f.read())
        f.close()
        
        
        
        f=open("count.txt","w")
        f.write(str(count+1))
        f.close()
        try:
         await client.send_message('me', 'Advertised '+ str(count+1) +' times.')
        except Exception as e:
            print('Ex Error '+str(e))  

        f=open("last.txt","w")
        f.write(str(dt))
        f.close()
       else:
         print("Not yet")
       time.sleep(1000)
    



        #await client.run_until_disconnected()



# Otherwise
#asyncio.run(main2())
def main():
    print('hey')
    sleep(2)
 





