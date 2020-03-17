import telebot
import matplotlib.pyplot as plt
import random
import re
from numpy import sin,cos,linspace

weini = telebot.TeleBot('928189418:AAH6SZbYLU5p7J12VhhfimKGvQZO080n0ek')

triggered = ['robert', 'weini', 'weinhandl']
ideen = []
chid = '-1001256312641'

##def weinhandler(message):
##    text = message.text
##    
##

rwfct = ''

def fctval(string):
    print('Extracting function value request...')
    global rwfct
    p = re.compile(r'f\(\d+\.?\d*')
    m = p.search(string)
    if m:
        if rwfct:
            x = m.group()
            x = x.replace('f(','')
            x = x.replace(')','')
            x = int(x)
            y = eval(rwfct)
            rwmsg = 'Der gesuchte Wert von f(x) ist: ' + str(y)
            weini.send_message(chid, rwmsg)
            return True
        else:
            weini.send_message(chid, 'Auf Mahara ist keine Funktion zu finden!')
            return True
    else:
        return None

def extract_fct(string):
    print('-'*20)
    print('Exctrating function from', string,'...')
    global rwfct
    p = re.compile(r'f\(x\)=[x\d.\+\*\-/\^()coisn]+', re.I)
    m = p.search(string)
    if m:
        fct = m.group()
        print(fct)
        a = 'cosin'
        wfct = ['sin', 'cos']
        ##search for cosin indicators
        if any(i in fct for i in a):
            print('Found function containing cosin indicators...')
            ##found cos or sin
            if any(i in fct for i in wfct):
                print('Cos or Sin found!')
                fct = fct.replace('f(x)=', '')
                fct = fct.replace(' ','')
                fct = fct.replace('^','**')
                print('Extracted', fct, 'sucessfully')
                print('-'*20)
                rwfct = fct
                return fct
            ##foung cosin, but no cos or sin
            else:
                print('ERROR: No cos or sin found!')
                print('-'*20)
                return none
        #found no cos or sin
        else:
            print('Found no cosin indicators...')
            fct = fct.replace('f(x)=', '')
            fct = fct.replace(' ','')
            fct = fct.replace('^','**')
            print('Extracted', fct, 'sucessfully')
            print('-'*20)
            rwfct = fct
            return fct
    ##found no function
    else:
        print('Extraction failed, found no satisfying pattern!')
        print('-'*20)
        return None

def plot_fct(term):
    print('-'*20)
    print('Plotting function', term)
    yvals = []
    x = linspace(-10,10,200)
    lab = 'f(x)=' + term
    print(lab)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(x,eval(term),'g')
    plt.title(lab)
    plt.savefig('plot.png')
    print('Exported plot sucessfully!')
    with open('plot.png', 'rb') as image:
          weini.send_photo(chid, image)
          print('Sent plot sucessfully!')
          print('-'*20)
