# Author: David Canillas Racero, @kartojal
#
# Dependencies: 
#   python3
#   beautifulsoup4 (You can install it throught pip )
#   
# Description: 
#   Python script to alarm you with N beeps and an alert window when any milestone reach the
#   desired percentage at Github. Only for Windows for now. Combine with cron/"Schedule Tasks" 
#   or set "while True: + sleep" after Main comentary if you are lazy, to repeat the script as your needs. 
#   Be the first to know the big news!

from bs4 import BeautifulSoup
from time import sleep
import urllib.request as ul
import ctypes
import winsound

# Array of Milestone names, change for the desired milestone name, must be equal at the title of milestone at the Github milestone page
milestonenames = ['Homestead', '1.3.4']
# Array of Percent Alarm(s)
targetpercent = ('85%','90%','95%','100%') # You can setup more alarms in the same list separated by comma, like this ('10%','30%','60%,'80%')

# Milestone full url, you need to put like the example : 'https://github.com/[ACCOUNT]/[REPOSITORY]/milestones'
milestonesurl = 'https://github.com/ethereum/go-ethereum/milestones'

alert = ctypes.windll.user32.MessageBoxW
modal_flag = 0x00001000

nbeeps = 4 # Number of beeps
Freq = 2700 # Set Frequency of Beep To 2700 Hertz
Dur = 400 # Set Duration of Beep To 400 ms == 0,4 second

htmldocument = ul.urlopen(milestonesurl).read()
soup = BeautifulSoup(htmldocument, 'html.parser')
mildivs = soup.find_all('div', class_='table-list-item')

# Main
for mname in milestonenames:
    for div in mildivs:
        wanteddiv = div.find('div', class_='table-list-cell')
        if wanteddiv.find('a', string=mname ):
            milpercent = wanteddiv.find_next_sibling().find('span',class_='progress-percent').contents 
            if milpercent[0] in targetpercent :
                for x in range (0,nbeeps):
                    winsound.Beep(Freq,Dur)
                    sleep(0.01)
                boxmessage = 'The ' + mname + ' milestone is at ' + milpercent[0]
                boxtitle = 'Github Milestone Status'
                alert(None, boxmessage, boxtitle, 0x40 | modal_flag)
