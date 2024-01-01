import matplotlib.pyplot as plt
import numpy as np
import json
import socket
from urllib.request import urlopen,Request
import urllib
import os
import config
def march(write):
    try:
        os.mkdir('/tmp/'+"overall")
    except:
        pass
    try:
        os.mkdir('/tmp/'+"specif")
    except:
        pass

    try:
        datum = json.loads(config.grust(config.ids['main']['bloglib']).decode('utf8').replace("'", '"'))
    except Exception as e:
        print(str(e))
        datum = {}

    for c in range(10):
        names = []
        teamnames= []
        fir = []
        sec = []
        lj = 0
        teamnames.append(datum['teamnames'][c])
        for x in datum['betodds'][c]:
            if lj == 5:
                break
            names.append(x)
            fir.append(datum['betodds'][c][x][-2:][0])
            sec.append(datum['betodds'][c][x][-2:][1])
            lj +=1

        plt.clf()
        plt.cla()
        plt.close()
        x = np.arange(len(names)) 
        width = 0.35 

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, fir, width, label=teamnames[0][0])
        rects2 = ax.bar(x + width/2, sec, width, label=teamnames[0][1])

        ax.set_ylabel('Odds')
        ax.set_title('Overall Odds')
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')


        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        write[c]['plot']={}
        write[c]['plot']['overall']="http://drive.google.com/uc?id="+config.ids['overall'][c]
        plt.savefig('/tmp'+'/overall/'+str(c))
        config.thrust('/tmp'+'/overall/'+str(c)+'.png',config.ids['overall'][c])



    for l in range(10):
        try:
            os.mkdir("/tmp/specif/"+str(l))
        except:
            pass
        tmpt1=[]
        tmpt2=[]
        write[l]['plot']['specif']={}
        teamnames= []
        lj = 0
        teamnames.append(datum['teamnames'][l])
        for x in datum['betodds'][l]:
            if lj == 5:
                break
            jj = str(lj)
            name=x
            num=[]
            for exs in range(int(len(datum['betodds'][l][x])/2)):
                num.append(exs)
            tmpt1=datum['betodds'][l][x][::2]
            tmpt2=datum['betodds'][l][x][1::2]
            write[l]['plot']['specif'][jj]=[]
            plt.clf()
            plt.cla()
            plt.close()
            plt.plot(num,tmpt1,num,tmpt2)
            plt.legend((teamnames[0][0],teamnames[0][1]))
            plt.title(name)
            write[l]['plot']['specif'][jj].append(name)
            write[l]['plot']['specif'][jj].append("http://drive.google.com/uc?id="+config.ids['specif'][l][lj])
            plt.savefig('/tmp'+'/specif/'+str(l)+'/'+str(lj))
            config.thrust('/tmp'+'/specif/'+str(l)+'/'+str(lj)+'.png',config.ids['specif'][l][lj])
            lj +=1
            
    
        with open('/tmp/'+'data.json', 'w') as outfile:
            json.dump(write, outfile)
        
