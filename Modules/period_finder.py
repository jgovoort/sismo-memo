import matplotlib.pyplot as plt
import numpy as np
import scipy

from normalize import normalize


def period_temp_discharge_noise(temp, smp_day_temp, gauging_velos, smp_day_discharge, power, smp_noise_noise) :
    #sample_rate = 180
    temp = np.array(temp)
    amp_temp =np.abs(np.fft.rfft(temp, n=temp.size))
    freq_temp = np.fft.rfftfreq(temp.size, d=1/smp_day_temp)
    amp_temp[0] = 0
    idx = amp_temp.argmax()

    amp_temp = normalize(amp_temp)

    gauging_velos = np.array(gauging_velos)
    amp_gauging_velos =np.abs(np.fft.rfft(gauging_velos, n=gauging_velos.size))
    freq_gauging_velos = np.fft.rfftfreq(gauging_velos.size, d=1/smp_day_discharge)
    amp_gauging_velos[0] = 0
    idx = amp_gauging_velos.argmax()

    amp_gauging_velos = normalize(amp_gauging_velos)

    noise = np.array(power)
    amp_noise =np.abs(np.fft.rfft(noise, n=noise.size))
    freq_noise = np.fft.rfftfreq(noise.size, d=1/smp_noise_noise)
    amp_noise[0] = 0
    idx = amp_noise.argmax()

    amp_noise = normalize(amp_noise)

    fig = plt.figure(figsize=(15, 5))
    plt.plot(freq_gauging_velos, amp_gauging_velos, label="Débit | Station V550")
    plt.plot(freq_temp, amp_temp, label="Température | Station V159")
    plt.plot(freq_noise, amp_noise, label='Noise')
    plt.xlim(0,2)
    plt.xlabel('Périodicité (J)')
    plt.legend()
    plt.show()
