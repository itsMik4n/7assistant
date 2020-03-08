#import modules
import telebot
import re
from datetime import datetime, timedelta

print("Github clone test yay")


def ext(s):
    p = re.compile(r'\d{1,2}\.\d{1,2}\.')
    x = p.search(s)
    if x:
        dat = ''
        datum = x.group()
        s = p.sub('',s)
        s = s.replace(' ','')
        datum = datum.split('.')
        del datum[2]
        for a in datum:
            a = a.replace(' ', '')
            if len(a) == 2:
                dat += a
                continue
            else:
                dat += '0' + a
        try:
            now = datetime.now()
            dat_formatted = datetime.strptime(str(now.year) + dat, '%Y%d%m')
            test = dat_formatted.date() - now.date()
            if test.days <= 7:
                wday = dat_formatted.weekday()
                dat_formatted = weekdays[wday]
                print(weekdays[wday])
        except:
            dat_formatted = False
    else:
        dat_formatted = False
    print(dat_formatted)
    return dat_formatted, s

def tags(s):
    p = re.compile(r'montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag', re.I)
    x = p.search(s)
    if x:
        s = p.sub('',s)
        s = s.replace('  ', ' ')
        tag = x.group()
    else:
        tag = False
    return tag, s

def form(datum):
    datum = str(datum)
    formt = datum[0:2] + '.' + datum[2:4] + '.'
    return formt


#variables
bot = telebot.TeleBot('940159686:AAH2JNssVMyB0Dc0IKV0xxfZ3mA-LPY0kmg')
subs = ['mathe', 'englisch', 'franz', 'psycho', 'deutsch', 'chemie', 'physik', 'geschichte', 'latein']
weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
hu = {} #dictionary von aufgaben, fächer als keys
neu = {} #hilfsdictionary

#message handlers

@bot.message_handler(commands = ['dazu'])
def dazu(message):
    mest = message.text.split(' ', 2)
    del mest[0]
    fach = mest[0]
    if not fach in subs:
        bot.reply_to(message, 'Falsches Eingabeformat')
        return
    text = mest[1]
    del mest
    datum, text = ext(text)
    if datum:
        try:
            neu = {'dead': str(datum.day) + "." + str(datum.month) + ".", 'task': text}
        except:
            neu = {'dead': datum, 'task': text}
        if fach in hu:
            hu[fach].append(neu)
        else:
            hu[fach] = [neu]
    else:
        wt = tags(text)
        if wt[0]:
            neu = {'dead': wt[0], 'task': wt[1]}
            if fach in hu:
                hu[fach].append(neu)
            else:
                hu[fach] = [neu]
        else:
            bot.reply_to(message, 'Falsches Eingabeformat')
        

    @bot.message_handler(commands = ['zeige'])
    def zeige(message):
        chid = message.chat.id
        sticker = 'CAACAgQAAxkBAANmXmN_UmmKIbbRBlguyPCF9UnVXcYAAg0AA8l8pyHy3-tYPCcNPxgE'
        text = ''
        if len(hu) == 0:
            bot.send_sticker(chid, sticker)
            bot.send_message(chid, 'Keine HÜs mehr!')
        else:
            msg ='AUFGABEN\n'
            for x in hu:
                y = hu[x]
                msg += '[' + x + ']\n'
                for z in y:
                    msg += 'bis zum ' + str(z['dead']) + ': ' + z['task'] + '\n'
            bot.send_message(chid, msg)

@bot.message_handler(commands = ['del'])
def dele(message):
    hu.clear()


@bot.message_handler(commands = ['print'])
def pr(message):
    print(hu)

#polling

while True:
    try:
        bot.polling(interval=1)
    except:
        continue
