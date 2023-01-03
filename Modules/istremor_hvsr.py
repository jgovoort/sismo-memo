import matplotlib.pyplot as plt
import numpy as np
import numpy_indexed as npi
from matplotlib.patches import Ellipse, Circle
import datetime

def amp_stat(miniplotamp) :
    
    #computation of the MIN, MAX, MEAN of the amplitude for each frequency
    
    miniplotMIN = np.amin(np.array(miniplotamp), axis = 0)
    miniplotMAX = np.amax(np.array(miniplotamp), axis = 0)
    miniplotMEAN = np.mean(np.array(miniplotamp), axis = 0)
    
    return miniplotMIN, miniplotMAX, miniplotMEAN 

def hvsr_TimePlot(miniplotfrq,miniplotamp, ylimmin = None, ylimmax = None) :

    miniplotMIN, miniplotMAX, miniplotMEAN = amp_stat(miniplotamp)
               
    plt.plot(miniplotfrq[0], miniplotMEAN, c='red', label='Mean')
    plt.plot(miniplotfrq[0], miniplotMIN,c='grey', linestyle='--', label='Max')
    plt.plot(miniplotfrq[0], miniplotMAX,c='grey', linestyle='--', label='Min')
    plt.xscale('log')
    if ylimmin != None and ylimmax != None :
        plt.ylim(ylimmin,ylimmax)
    plt.xlabel('Frequency f0 (Hz)')
    plt.ylabel('H/V amplitude')
    plt.legend()
    plt.show()
    
def hv_cycle(miniplotfrq,miniplotamp,miniplottimestart,nbrdays,namestt=None,lowfrq = None,highfrq = None,startnbrdays=None) :
    
    '''
    miniplotfrq : list or array containing the frequencies --> 2 dimensional array/list : n * m
    miniplotamp : list or array containing the amplitude corresponding to the frequencies array --> 2 dimensional array/list : n * m
    miniplottimestart : list or array containing the time --> 1 dimensional array/list : n
    nbrday : integer that corresponds to the number of days that must be analysed
       <OPTIONAL> startnbrdays : interger corresponding to the number of the starting day. if None == 0

    <OPTIONAL> lowfrq : The lowest frequency that must be computed. if None == min(minplotfrq)
    <OPTIONAL> highfrq : The highest frequency that must be computed. if None == max(minplotfrq)

    Julien Govoorts
    julien.govoorts@ulb.be

    '''
    if namestt == None :
        namestt= 'N/A'
    if lowfrq == None :
        lowfrq = np.min(np.array(miniplotfrq[0]))
    if highfrq == None :
        highfrq = np.max(np.array(miniplotfrq[0]))
    if startnbrdays == None :
        startnbrdays = 0
    
    miniplothour = []
    for elem in miniplottimestart :
        miniplothour.append(float(elem.hour)+float(elem.minute)/60) #append the hour of miniplottimestart
    
    miniplotMIN, miniplotMAX, miniplotMEAN = amp_stat(miniplotamp)
    
    nbrsteps = miniplothour.index(0,1,len(miniplothour))
    
    # Determined the index of the lowest and highest frequency
    idxlowfrq = np.argmin(np.abs(np.array(miniplotfrq[0])- lowfrq))
    idxhighfrq = np.argmin(np.abs(np.array(miniplotfrq[0])- highfrq))

    frqLowHigh = miniplotfrq[0][idxlowfrq:idxhighfrq+1]
    AmpLowHigh = []

    for elem in miniplotamp :
        AmpLowHigh.append(elem[idxlowfrq:idxhighfrq+1])
    AmpLowHigh = np.array(AmpLowHigh)

    maxAmpEvol = np.max(AmpLowHigh, axis = 1)
    idxAmpEvol = np.argmax(AmpLowHigh, axis = 1)

    F1Evol = []
    F0Evol = []
    minAmpEvol = []
    i = 0
    for idx in idxAmpEvol :
        F0Evol.append(frqLowHigh[idx])

        minAmpEvol.append(np.min(AmpLowHigh[i][idx:]))
        idxF1 = np.argmin(AmpLowHigh[i][idx:]) + idx
        #print(idxF1)
        F1Evol.append(frqLowHigh[idxF1])
        i += 1
    AmpF0F1Evol = maxAmpEvol/minAmpEvol
    F1F0EVol = np.array(F1Evol)/np.array(F0Evol)

    PosMeanMax = [np.mean(F0Evol),np.mean(maxAmpEvol)]
    PosMedianMax = [np.median(F0Evol),np.median(maxAmpEvol)]
    StdMax = [np.std(F0Evol,dtype=np.float64),np.std(maxAmpEvol,dtype=np.float64)] 

    col = list(range(0,len(miniplottimestart)))

    maxAmp = np.max(miniplotMEAN)+.5 #Valeur maximale où on rajoute .5 pour faire un beau plot

    #### Computing the MEAN, MEDIAN AND INTEGER BETWEEN LOWEST FRQ AND HIGHEST FRQ ####

    IntF = []
    HOURAMPMEDIAN = []
    HOURAMPMEAN = []

    rgdays = nbrdays - startnbrdays

    for day in range(rgdays) :
        for t in range(nbrsteps):
            t += day*nbrsteps #give the array position
            HVHOUR = np.array(miniplotamp[t][idxlowfrq:idxhighfrq+1])  #Clipping the array according to lowfrq and highfrq
            FRQHOUR = np.array(miniplotfrq[t][idxlowfrq:idxhighfrq+1]) #Clipping the array according to lowfrq and highfrq
            HOURAMPMEDIAN.append(np.median(HVHOUR)) #Mediane du signal entre lowfrq et highfrq
            HOURAMPMEAN.append(np.mean(HVHOUR))     #Moyenne du signal entre lowfrq et highfrq   
            #calcule l'intégrale trapèze entre 2 points de fréquence
            tmpIntF = 0
            for AF in range(len(HVHOUR)-1) :
                tmpIntF += (HVHOUR[AF]+HVHOUR[AF+1])/(FRQHOUR[AF+1]-FRQHOUR[AF])
            IntF.append(tmpIntF)



    #### PLOTTING THE RESULTS ####        


    fig = plt.figure(figsize=(17, 20))

    ax1 = plt.subplot2grid((5,3), (0,0), colspan=3)
    ax1.set_ylabel('HV maximum amplitude')
    ax1.set_xlabel('Time')
    ax1.plot(miniplottimestart, maxAmpEvol, label='Amplitude at F0')
    ax1.plot(miniplottimestart, minAmpEvol, label='Amplitude at F1')
    #ax1.plot(miniplottimestart, AmpF0F1Evol, label='Amplitude F0/F1')
    ax1.legend()
    ax1.set_title('Station '+str(namestt)+' : Maximum amplitude and frequency evolution between '
                  +str(lowfrq)+'Hz and '+ str(highfrq)+ 'Hz', fontsize=16)

    ax2 = plt.subplot2grid((5,3), (1,0), colspan=3)
    ax2.set_ylabel('HV maximum frequency (Hz)')
    ax2.set_xlabel('Time')
    ax2.plot(miniplottimestart, F0Evol, label='F0')
    ax2.plot(miniplottimestart, F1Evol, label='F1')
    ax2.plot(miniplottimestart, F1F0EVol, label='F1/F0')
    ax2.legend()

    ax2b = plt.subplot2grid((5,3), (2,0), colspan=3)
    ax2b.set_ylabel('Mean and median \n HV amplitude in dt')
    ax2b.set_xlabel('Time')
    ax2b.plot(miniplottimestart, HOURAMPMEDIAN, label="Median")
    ax2b.plot(miniplottimestart, HOURAMPMEAN,linestyle='--', label='Mean')
    ax2b.legend()

    ax3 = plt.subplot2grid((5,3), (3,2), colspan=1, rowspan=2)
    ax3.set_ylabel('HV maximum amplitude')
    ax3.set_xlabel('HV maximum frequency (Hz)')
    synth = ax3.scatter(F0Evol,maxAmpEvol, c=col)
    ax3.scatter(PosMeanMax[0],PosMeanMax[1],c='red',marker='x')
    ax3.scatter(PosMedianMax[0],PosMedianMax[1],c='black',marker='x')
    ax3.add_artist(Ellipse((PosMeanMax[0],PosMeanMax[1]), StdMax[0], StdMax[1],fill=False,linestyle='--'))

    cbar = fig.colorbar(synth, ax=ax3, label='Time', ticks=[np.min(col), np.max(col)/2, np.max(col)], orientation='horizontal')
    
    cbarstart = str(miniplottimestart[0].day)+' '+str(miniplottimestart[0].month)+' '+str(miniplottimestart[0].year)
    cbarmid = str(miniplottimestart[int(len(col)/2)].day)+' '+str(miniplottimestart[int(len(col)/2)].month)+' '+str(miniplottimestart[int(len(col)/2)].year)
    cbarend = str(miniplottimestart[len(col)-1].day)+' '+str(miniplottimestart[len(col)-1].month)+' '+str(miniplottimestart[len(col)-1].year)
    cbar.ax.set_xticklabels([cbarstart, cbarmid, cbarend])
    ax4 = plt.subplot2grid((5,3), (3,0), colspan=1, rowspan=2)
    ax4.set_xscale('log')
    ax4.plot(miniplotfrq[0],miniplotMEAN, c='red', label='Mean')
    ax4.plot(miniplotfrq[0], miniplotMIN,c='grey', linestyle='--', label='Max')
    ax4.plot(miniplotfrq[0], miniplotMAX,c='grey', linestyle='--', label='Min')
    ax4.plot([lowfrq,lowfrq],[0,maxAmp], label = 'Lowest value analysed')
    ax4.plot([highfrq,highfrq],[0,maxAmp], label = 'Highest value analysed')
    ax4.set_ylim(0,maxAmp)
    ax4.set_xlabel('Frequency f0 (Hz)')
    ax4.set_ylabel('H/V amplitude')
    ax4.legend(loc="upper left", mode="expand", ncol=2)

    ax5 = plt.subplot2grid((5,3), (3,1), colspan=1, rowspan=1)
    ax5.set_ylabel('HV maximum amplitude')
    ax5.set_xlabel('Hours in a day')
    #synth = ax5.scatter(F0Evol,maxAmpEvol, c=miniplothour, cmap='seismic')
    #synth5 = ax5.scatter(miniplothour,maxAmpEvol, c=F0Evol, cmap='seismic')

    groups, Ampmeans = npi.group_by(miniplothour).mean(maxAmpEvol)
    groups, Ampmedian = npi.group_by(miniplothour).median(maxAmpEvol)
    groups, Ampstds = npi.group_by(miniplothour).std(maxAmpEvol)
    groups, Ampmin = npi.group_by(miniplothour).min(maxAmpEvol)
    groups, Ampmax = npi.group_by(miniplothour).max(maxAmpEvol)

    ax5.plot(groups, Ampmedian, c='red', label='Median')
    ax5.plot(groups, Ampmeans, c='orange', linestyle = '--',label='Mean')
    ax5.fill_between(groups, Ampmeans+Ampstds,Ampmeans-Ampstds,alpha=0.2,color='orange', label='Standard deviation')
    #ax5.fill_between(groups, Ampmin,Ampmax,edgecolor='black', facecolor = 'None',linestyle='--', label='Min-Max')
    ax5.plot(groups, Ampmin, c='grey',linestyle='--',label='Min-Max')
    ax5.plot(groups, Ampmax, c='grey',linestyle='--')
    #ax5.errorbar(groups,Ampmeans,yerr=Ampstds,linestyle='--',c='orange', ecolor= 'grey', capsize=2, capthick=2, label='Mean with STD')
    #ax5.errorbar(groups,Frqmeans,yerr=Ampstds,linestyle='-',c='blue', ecolor= 'grey', capsize=2, capthick=2, label='STD')
    ax5.legend(loc="lower left", mode="expand", ncol=2)

    ax6 = plt.subplot2grid((5,3), (4,1), colspan=1, rowspan=1)

    groups, Frqmeans = npi.group_by(miniplothour).mean(F0Evol)
    groups, Frqmedian = npi.group_by(miniplothour).median(F0Evol)
    groups, Frqmin = npi.group_by(miniplothour).min(F0Evol)
    groups, Frqmax = npi.group_by(miniplothour).max(F0Evol)
    groups, Frqstd = npi.group_by(miniplothour).std(F0Evol)


    ax6.plot(groups, Frqmedian, c='red', label='Median')
    ax6.plot(groups, Frqmeans, c='orange', linestyle = '--',label='Mean')
    ax6.fill_between(groups, Frqmeans+Frqstd,Frqmeans-Frqstd,alpha=0.2,color='orange', label='Standard deviation')
    ax6.plot(groups, Frqmin, c='grey',linestyle='--',label='Min-Max')
    ax6.plot(groups, Frqmax, c='grey',linestyle='--')

    ax6.set_ylabel('Frequency f0 (Hz)')
    ax6.set_xlabel('Hours in a day')
    ax6.legend(loc="lower left", mode="expand", ncol=2)

    plt.show()