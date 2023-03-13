import numpy as np
import matplotlib.pyplot as plt
import obspy
import datetime
import time
import math
import os, sys

def amp_noise_mean_median(root,stt,window_size, startdate, days, lowpass, highpass) :
    fileroot= os.listdir(root)
    
    startdate = datetime.datetime.strptime(startdate, '%Y.%m.%d')
    #startnumber = 3
    #days = 31 - startnumber

    median = []
    mean = []

    theta = []
    
    for day in range(days) :
        start = time.process_time()
        date = startdate + datetime.timedelta(days = day)
        datetimeStr = date.strftime("%Y.%m.%d.%H.%M.%S.000")
        print(datetimeStr)
        
        for file in fileroot :
            if file.startswith(stt) and file.endswith(datetimeStr+'.E.miniseed') :
                signalE = obspy.read(root+file)
            elif file.startswith(stt) and file.endswith(datetimeStr+'.N.miniseed') :
                signalN  = obspy.read(root+file)
            elif file.startswith(stt) and file.endswith(datetimeStr+'.Z.miniseed') :
                signal = obspy.read(root+file) 
        
        
        
        
        #signal = obspy.read(root+str(stt)+str(startnumber+day)+'.'+datetimeStr+'.Z.miniseed')
        #signalE = obspy.read(root+str(stt)+str(startnumber+day)+'.'+datetimeStr+'.E.miniseed')
        #signalN = obspy.read(root+str(stt)+str(startnumber+day)+'.'+datetimeStr+'.N.miniseed')
        
        if day == 0 :
            starttime = signal[0].stats.starttime
            endtime = signal[0].stats.endtime
            datetimestarttime = datetime.datetime.strptime(str(starttime), 
                                                           '%Y-%m-%dT%H:%M:%S.000000Z')
            noise_time = [datetimestarttime]
            t0 = starttime+(window_size*60)
            t1 = t0+(window_size*60)
        
            nbrpoints = signal.copy()
            nbrpoints = nbrpoints[0].trim(starttime=t0, endtime=t1)
            nbrpoints = len(nbrpoints)
            
        window = 24*60/window_size
        
        if lowpass > 0 and highpass > 0 :
            signal.filter('lowpass', freq=lowpass).filter('highpass', freq=highpass)
            signalE.filter('lowpass', freq=lowpass).filter('highpass', freq=highpass)
            signalN.filter('lowpass', freq=lowpass).filter('highpass', freq=highpass)
            
        trace = signal[0].data
        traceE = signalE[0].data
        traceN = signalN[0].data
        
        
        
        for i in range(int(window)) :

            
            array = np.abs(trace[i*nbrpoints:(i+1)*nbrpoints])
            arrayE = np.abs(traceE[i*nbrpoints:(i+1)*nbrpoints])
            arrayN = np.abs(traceN[i*nbrpoints:(i+1)*nbrpoints])
            
            #print(array)
            mean.append([np.mean(array),np.mean(arrayE), np.mean(arrayN)])
            
            medE = np.median(arrayE)
            medN = np.median(arrayN)
            
            median.append([np.median(array),medE,medN])
            
            theta.append(math.atan(medE/medN)*(360/math.pi))
            
            if i > 0 and day == 0 :
                noise_time.append(noise_time[i-1]+datetime.timedelta(minutes=window_size))   
            elif day > 0 :
                base = int(day*window)
                noise_time.append(noise_time[base+i-1]+datetime.timedelta(minutes=window_size))
                
        end = time.process_time() 
        print('Days '+str(date)+' accomplished in '+str(end-start)+' seconds')
        
        medianall = np.median(np.array(median), axis=1)
        meanall = np.mean(np.array(mean), axis=1)
        
        
    return noise_time, mean, median, meanall, medianall, theta



def hydronoise_plot(gauging_time, gauging_velos, temp_time, temp,
                   noise_time,noise_median, limit = None, label_noise = 'PPSD', Yax_noise = 'PPSD', 
                    label_gauging = 'Discharge', label_temp = 'Temperature', Title = 'PPSD, discharge, temperature'):
    if limit == None :
        limit = (np.min(noise_median)-2,np.max(noise_median)+2)

    fig = plt.subplots(3, 1, figsize=(15, 15))

    ax1 = plt.subplot(3, 1, 1)


    ax1.set_xlabel('Time') 
    ax1.set_ylabel('Débit (m$^3$/s)', color = 'blue') 
    ax1.plot(gauging_time, gauging_velos, label = label_gauging, c='blue')
    ax1.tick_params(axis ='y', labelcolor = 'blue') 

    # Adding Twin Axes

    ax2 = ax1.twinx() 
    
    mintemp = int(np.min(temp))
    maxtemp = int(np.max(temp))
    dtemp = maxtemp - mintemp
    Ltemp = [mintemp, mintemp+(dtemp/3), mintemp+(2*dtemp/3), maxtemp]
    ax2.set_ylabel('Temperature (°C)'+24*' ', color = 'red')
    ax2.set_ylim((mintemp-0.5,maxtemp+dtemp))
    ax2.set_yticks(Ltemp)
    ax2.plot(temp_time, temp, label = label_temp, c='red', linestyle='--')
    ax2.tick_params(axis ='y', labelcolor = 'red') 

    ax3 = plt.subplot(3, 1, 2)
    
    ax3.set_xlabel('Time') 
    ax3.set_ylabel(Yax_noise) 
    ax3.set_ylim(limit)
    ax3.plot(noise_time,noise_median, label=label_noise, c='grey')
    ax3.tick_params(axis ='y') 

    ax4 = ax3.twinx() 

    ax4.set_xlabel('Time') 
    ax4.set_ylabel('Débit (m$^3$/s)'+18*' ', color = 'blue')
    ax4.set_ylim((10,100))
    ax4.set_yticks([20,30,40,50,60,70])
    ax4.plot(gauging_time, gauging_velos, c='blue')
    ax4.tick_params(axis ='y', labelcolor = 'blue') 

    ax5 = plt.subplot(3, 1, 3)

    ax5.set_xlabel('Time') 
    ax5.set_ylabel(Yax_noise) 
    ax5.set_ylim(limit)
    ax5.plot(noise_time,noise_median, c='grey')
    ax5.tick_params(axis ='y') 

    ax6 = ax5.twinx() 
    

    ax6.set_ylabel('Temperature (°C)'+24*' ', color = 'red')
    ax6.set_ylim((mintemp-0.5,maxtemp+dtemp))
    ax6.set_yticks(Ltemp)
    ax6.plot(temp_time, temp, c='red', linestyle='--')
    ax6.tick_params(axis ='y', labelcolor = 'red') 
    
    plt.figlegend()
    plt.suptitle(Title)