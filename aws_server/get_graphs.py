import matplotlib.pyplot as plt
import data_obtainer as do


data = do.get_data("fan", ["temp (C)", "hum", "RPM", "time"], "array")
temps = []
RPMs = []
hums = []
times = []
for d in data:
    temps.append(d[0])
    hums.append(d[1])
    RPMs.append(d[2])
    times.append(d[3])
plt.plot(temps, times, 'ro')
plt.savefig('model/temp_time.png')


plt.plot(hums, times, 'ro')
plt.savefig('model/hums_time.png')


plt.plot(RPMs, times, 'ro')
plt.savefig('model/rpm_time.png')
