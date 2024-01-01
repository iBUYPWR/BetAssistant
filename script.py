from urllib.request import urlopen,Request
import urllib
import json
from cairosvg import svg2png
import time
import socket
import os
import re
import timeit
import gc
from threading import Thread
import ex
import config
import bs4 as bs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import warnings
try:
    os.mkdir('/tmp/'+"dumlog")
except:
    pass

warnings.filterwarnings("ignore", category=DeprecationWarning)

while True:
    start = timeit.default_timer()
    gc.collect()
    drive = webdriver.PhantomJS(service_args=['--load-images=no','--disk-cache=false'])


    def scan(url):
        drive.implicitly_wait(20)
        drive.get(url)
        ansis = bs.BeautifulSoup(str(drive.page_source),'html.parser')
        return ansis
    
    #paged source
    soup=scan("https://www.hltv.org/matches")
    drive.close()
    drive.quit()

    #teamlivescores
    livescores = []
    supa = soup.find_all('div',attrs={'class' : 'scores'})
    x=0
    for val in supa:
        livescores.append([])
        scfix = val.find_all('td',attrs={'class' : 'mapscore'})
        for m in scfix: 
            livescores[x].append(m.find('span').string)
        x+=1

            
    #teamnames
    teamnames = []
    #live matches
    supa = soup.find_all('div',attrs={'class' : 'matchTeamName'})
    #Non-Live matches
    supa2 = soup.find_all('td',attrs={'class' : 'team-cell'})
    for val in supa: 
        teamnames.append(val.string)
    for val in supa2:
        teamnames.append(val.find('div',attrs={'class':'team'}).string)

    #teamlogos
    teamlogos = []
    supa = soup.find_all('img',attrs={'class' : 'matchTeamLogo'})
    supk = soup.find_all('img',attrs={'class' : 'night-only'})
    supar = set(supa) - set(supk)
    cairoc = 0
    for val in supar:
            if cairoc > 20 :
                break
            value = val.get('src')
            print(value)
            req = Request(value)
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0')
            resp = urlopen(req)
            #check if match is TBD
            if '/' in teamnames[cairoc]:
                teamlogos.append('')
            #if PNG
            elif resp.info().get_content_type()=="image/png":
                teamlogos.append(value)
            #if SVG
            else:
                svg2png(bytestring=resp.read(),write_to='/tmp/'+'/dumlog/'+str(cairoc)+'.png')
                config.thrust('/tmp/'+'/dumlog/'+str(cairoc)+'.png',config.ids['dumlog'][cairoc])
                teamlogos.append("https://drive.google.com/uc?id="+config.ids['dumlog'][cairoc])
            cairoc +=1
            


    #tourneynames
    tournames = []
    supa = soup.find_all('img',attrs={'class' : 'matchEventLogo'})
    for val in supa:
        value = val.get('alt')
        tournames.append(value)


    #tourneyimages
    tourimg = []
    supa = soup.find_all('img',attrs={'class' : 'matchEventLogo'})
    for val in supa:
        #only add if they were not in featured tours box
        if val.parent.get('class') == None or not 'guide-event' in val.parent.get('class'):
            value = val.get('src')
            tourimg.append(value)
        

    #matchlinks
    guplink = []
    supa = soup.find_all('div',attrs={'class' : 'liveMatch'})
    supaalt = soup.find_all('div',attrs={'class' : 'upcomingMatch'})
    x=0
    for val in supa:
        if x > 10:
            break
        value = val.find_all('a')[0].get('href')
        guplink.append("https://www.hltv.org"+value)
        x+=1
    for val in supaalt:
        value = val.find_all('a')[0].get('href')
        guplink.append("https://www.hltv.org"+value)


    try:    
        bloglib=json.loads(config.grust(config.ids['main']['bloglib']).decode('utf8').replace("'", '"'))
    except:
        bloglib={}
    bloglib['teamnames']=[]
    data = {}
    x=0
    while x < 10:
        data[x]={}
        bloglib['teamnames'].append({})
        bloglib['teamnames'][x]=[]
        data[x]['info']=[]
        data[x]['info'].append({
            'tourimage':tourimg[x],
            'team1':teamnames[x*2],
            'team1logo':teamlogos[x*2],
            'team2':teamnames[x*2+1],
            'team2logo':teamlogos[x*2+1],
            })
        bloglib['teamnames'][x].append(teamnames[x*2])
        bloglib['teamnames'][x].append(teamnames[x*2+1])
        x+=1

    if not 'betodds' in bloglib:
        bloglib['betodds']=[]
    def betClarifier(entry):
        if not entry.find("thunder")==-1:
            return "thunderpick"
        if not entry.find("loot")==-1:
            return "lootbet"
        if not entry.find("egb")==-1:
            return "egb"
        if not entry.find("cyber")==-1:
            return "cyberbet"
        if not entry.find("glhf")==-1:
            return "glfh"
        if not entry.find("1xbet")==-1:
            return "1xbet"
        if not entry.find("omg")==-1:
            return "omgbet"
        if not entry.find("unikrn")==-1:
            return "unikrn"
        if not entry.find("pinnacle")==-1:
            return "pinnacle"
        if not entry.find("vulkan")==-1:
            return "vulkanbet"
        if not entry.find("365")==-1:
            return "bet365"
        if not entry.find("betwin")==-1:
            return "betwin"
        if not entry.find("buff")==-1:
            return "buff"
        if not entry.find("ggbet")==-1:
            return "ggbet"
        if not entry.find("betway")==-1:
            return "betway"
        else:
            return "null";
        

    del soup

    for n in range(10):
        drive = webdriver.PhantomJS(service_args=['--load-images=no','--disk-cache=false'])
        print(gc.get_count())
        dum = scan(guplink[n])
        #matchinfo
        tourpar = dum.find_all('div',attrs={'class' : 'event'})
        tourch = tourpar[0].find('a').string
        team1roph = []
        team2roph = []
        pph = dum.find_all('img',attrs={'class' : 'player-photo'})
        ppn1=[]
        ppn2=[]
        maph1 = dum.find_all('div',attrs={'class' : 'map-name-holder'})
        maps=[]
        #maps
        for x in maph1:
            maps.append(x.find('div',attrs={'class' : 'mapname'}).string)
        #teamrosters
        for x in pph[0:5]:
            if x.get('alt')=="TBD":
                team1roph.append("blank")
                ppn1.append('TBD')
            elif x.get('src')=='https://static.hltv.org/images/playerprofile/blankplayer.svg':
                team1roph.append("blank")
                ppn1.append(x.get('alt').split("'")[1])
            else:
                team1roph.append(x.get('src'))
                ppn1.append(x.get('alt').split("'")[1])
        #for unqualified matched like godsent/astralis who lack second participant
        if len(pph)>5:
            for x in pph[5:11]:
                if x.get('alt')=="TBD":
                    team2roph.append("blank")
                    ppn2.append('TBD')
                elif x.get('src')=='https://static.hltv.org/images/playerprofile/blankplayer.svg':
                    team2roph.append("blank")
                    ppn2.append(x.get('alt').split("'")[1])
                else:
                    team2roph.append(x.get('src'))
                    ppn2.append(x.get('alt').split("'")[1])
        team1KD = []
        team2KD = []
        team1N = []
        team2N = []
        try:
            data1 = json.loads(dum.find('div',attrs={'class' : 'lineups-compare-container'}).get('data-team1-players-data'))
            data2 = json.loads(dum.find('div',attrs={'class' : 'lineups-compare-container'}).get('data-team2-players-data'))
            #check if that instance exists in any(for sorting)
            for f in range(5):
                for i in data1.keys() :
                    if ppn1[f]==data1[i]['nickname']:
                        team1KD.append(float(data1[i]['rating']))
                        team1N.append(data1[i]['nickname'])
            for f in range(5):
                for i in data2.keys() :
                    if ppn2[f]==data2[i]['nickname']:
                        team2KD.append(float(data2[i]['rating']))
                        team2N.append(data2[i]['nickname'])
        except:pass
        data[n]['info'].append({
            'tourname' : tourch,
            'maps' :maps,
            'team1roph':team1roph,
            't1players':team1KD,
            't1names':team1N,
            'team2roph':team2roph,
            't2players':team2KD,
            't2names':team2N
            })

        #mapAnalysis
        maflinks = []
        data[n]['info'].append([])
        #first team
        data[n]['info'][2].append({})
        #second team
        data[n]['info'][2].append({})
        for mp in range(2):
            data[n]['info'][2][mp]['percent']=[]
            data[n]['info'][2][mp]['times']=[]
            data[n]['info'][2][mp]['keys']=[]
        links = dum.find_all('div',attrs={'class' : 'map-stats-infobox-winpercentage'})
        times =dum.find_all('div',attrs={'class' : 'map-stats-infobox-maps-played'})
        count=0
        for val in links:
            if dum.find_all('div',attrs={'class' : 'not-picked'}) != []:
                maflinks.append(val.find('a').get('href'))
                #team1
                if count==0 or count%2==0:
                    data[n]['info'][2][0]['percent'].append(val.find('a').string)
                #team2
                else:
                    data[n]['info'][2][1]['percent'].append(val.find('a').string)
            else:
                #team1
                if count==0 or count%2==0:
                    data[n]['info'][2][0]['percent'].append(val.find('a').string)
                #team2
                else:
                    data[n]['info'][2][1]['percent'].append(val.find('a').string)
            count+=1
        count=0
        for val in times:
            #team1
            if count==0 or count%2==0:
                data[n]['info'][2][0]['times'].append(val.string)
            #team2
            else:
                data[n]['info'][2][1]['times'].append(val.string)
            count+=1
        
        count=0
        for val in maflinks:
            mapage = scan('https://hltv.org'+val)
            columns = mapage.find('table',attrs={'stats-table'}).find_all('td')
            #if any data
            for x in range(1,int(len(columns)/5+1)):
                if x>5:
                    break
                #for only selection of colomn 3 and 5
                #if the link is for team 1 or 2
                if count==0 or count%2==0:
                    data[n]['info'][2][0]['keys'].append([columns[x*5-3].find('a').find('span').string,columns[x*5-1].string])
                else:
                    data[n]['info'][2][1]['keys'].append([columns[x*5-3].find('a').find('span').string,columns[x*5-1].string])
            count+=1
        
        #betodds
        oc1 = dum.find_all('tr',attrs={'class' : 'provider'})
        oc2 = dum.find_all('tr',attrs={'class' : 'hidden'})
        oddcell= set(oc1) - set(oc2)
        data[n]['betodds']={}
        if len(bloglib['betodds']) < 10:
            bloglib['betodds'].append({})
        for val in oddcell:
            las = val.find_all('td',attrs={'class': 'odds-cell'})
            img = val.find('img').get('src')
            provider = betClarifier(img)
            for mn in las:
                value = mn.find('a').string
                parentbet = mn.parent.get('class')
                if not value == "-" and not provider == "null":
                    try:
                        if 'provider' in parentbet:
                            if provider in data[n]['betodds']:
                                data[n]['betodds'][provider].append(float(value))
                            else:
                                data[n]['betodds'][provider]=[]
                                data[n]['betodds'][provider].append(float(value))                               
                        if 'provider' in parentbet:
                            #if instance is available, length is less than 20 and teams did match(game didnt finish)
                            if provider in bloglib['betodds'][n] and len(bloglib['betodds'][n][provider]) < 20 and bloglib['teamnames'][n][0]==data[n]['info'][0]['team1'] and bloglib['teamnames'][n][1]==data[n]['info'][0]['team2']:
                                bloglib['betodds'][n][provider].append(float(value))
                            #no instance, make one
                            elif not provider in bloglib['betodds'][n]:
                                bloglib['betodds'][n][provider]=[]
                                bloglib['betodds'][n][provider].append(float(value))
                            #there is instance, but filled and 0 space, so delete oldest
                            elif not len(bloglib['betodds'][n][provider]) < 20:
                                del bloglib['betodds'][n][provider][0]
                                bloglib['betodds'][n][provider].append(float(value))
                            #teams didnt match, game was finished probs
                            elif not bloglib['teamnames'][n][0]==data[n]['info'][0]['team1'] or not bloglib['teamnames'][n][1]==data[n]['info'][0]['team2']:
                                del bloglib['teamnames'][n]
                                del bloglib['betodds'][n]
                                break
                    except Exception as e:
                        pass
        drive.close()
        drive.quit()
    for f in range(10):
        try:
            data[f]['livescores']=[]
            data[f]['livescores'].append({
                'live':'true',
                'scores':livescores[f]
                })
        except:
            data[f]['livescores'].append({
                'live':'false'
                })
        
    #betoddds = list(filter(("-").__ne__, betodds))
    """
    m=0
    while m < 10:
        data[m]['betodds']={}
        try:
            his = len(data[m]['betodds'])
        except:
            for f in betodds:
                data[int(f.split('.')[0])]['betodds'][f.split('.')[1]]=[]
                
        m+=1
        """
    with open('/tmp/'+'bloglib.json', 'w') as outfile:
        json.dump(bloglib, outfile)
    config.thrust('/tmp/'+'bloglib.json',config.ids['main']['bloglib'])
    #print(data)
    ex.march(data)
    config.thrust('/tmp/'+'data.json',config.ids['main']['data'])
    #Your statements here
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    del(start)
    del(stop)

