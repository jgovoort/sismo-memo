import numpy as np
import matplotlib.pyplot as plt
import obspy
import datetime
import time


def amp_noise_mean_median(root,stt,window_size, startdate, lowpass, highpass) :

    startdate = datetime.datetime.strptime(startdate, '%Y.%m.%d')
    startnumber = 3
    days = 31 - startnumber

    median = []
    mean = []

    for day in range(days) :
        start = time.process_time()
        date = startdate + datetime.timedelta(days = day)
        datetimeStr = date.strftime("%Y.%m.%d.%H.%M.%S.000")
        print(datetimeStr)
        
        signal = obspy.read(root+str(stt)+str(startnumber+day)+'.'+datetimeStr+'.Z.miniseed')
        
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
        
        signal.filter('lowpass', freq=lowpass).filter('highpass', freq=highpass)
        
        trace = signal[0].data
        
        for i in range(int(window)) :

            
            array = np.abs(trace[i*nbrpoints:(i+1)*nbrpoints])
            #print(array)
            mean.append(np.mean(array))
            median.append(np.median(array))
            if i > 0 and day == 0 :
                noise_time.append(noise_time[i-1]+datetime.timedelta(minutes=window_size))
            elif day > 0 :
                base = int(day*window)
                noise_time.append(noise_time[base+i-1]+datetime.timedelta(minutes=window_size))
        end = time.process_time() 
        print('Days '+str(day+startnumber)+' accomplished in '+str(end-start)+' seconds')
    return noise_time, mean, median



def hydronoise_plot(gauging_time, gauging_velos, temp_time, temp,
                   noise_time,noise_median, limit):
    fig = plt.subplots(3, 1, figsize=(15, 15))

    ax1 = plt.subplot(3, 1, 1)


    ax1.set_xlabel('Time') 
    ax1.set_ylabel('Débit (m$^3$/s)', color = 'blue') 
    ax1.plot(gauging_time, gauging_velos, label = 'Débit | Station V550', c='blue')
    ax1.tick_params(axis ='y', labelcolor = 'blue') 

    # Adding Twin Axes

    ax2 = ax1.twinx() 

    ax2.set_ylabel('Temperature (°C)'+24*' ', color = 'red')
    ax2.set_ylim((12,17))
    ax2.set_yticks([12.5,13,13.5,14,14.5,15])
    ax2.plot(temp_time, temp, label = 'Température | Station V299', c='red', linestyle='--')
    ax2.tick_params(axis ='y', labelcolor = 'red') 

    ax3 = plt.subplot(3, 1, 2)

    ax3.set_xlabel('Time') 
    ax3.set_ylabel('Signal amplitude \n Median over a 1 minute moving window') 
    ax3.set_ylim(limit)
    ax3.plot(noise_time,noise_median, label='SS_20739', c='grey')
    ax3.tick_params(axis ='y') 

    ax4 = ax3.twinx() 

    ax4.set_xlabel('Time') 
    ax4.set_ylabel('Débit (m$^3$/s)'+18*' ', color = 'blue')
    ax4.set_ylim((10,100))
    ax4.set_yticks([20,30,40,50,60,70])
    ax4.plot(gauging_time, gauging_velos, label = 'Débit | Station V550', c='blue')
    ax4.tick_params(axis ='y', labelcolor = 'blue') 

    ax5 = plt.subplot(3, 1, 3)

    ax5.set_xlabel('Time') 
    ax5.set_ylabel('Signal amplitude \n Median over a 1 minute moving window') 
    ax5.set_ylim(limit)
    ax5.plot(noise_time,noise_median, label='SS_20739', c='grey')
    ax5.tick_params(axis ='y') 

    ax6 = ax5.twinx() 

    ax6.set_ylabel('Temperature (°C)'+24*' ', color = 'red')
    ax6.set_ylim((12,17))
    ax6.set_yticks([12.5,13,13.5,14,14.5,15])
    ax6.plot(temp_time, temp, label = 'Température | Station V299', c='red', linestyle='--')
    ax6.tick_params(axis ='y', labelcolor = 'red') 