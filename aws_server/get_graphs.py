import matplotlib.pyplot as plt
import data_obtainer as do
from datetime import datetime
import time


data = do.get_data("fan", ["temp (C)", "hum", "RPM", "time"], "array")
temps = []
RPMs = []
hums = []
times = []
times2 = []
now = time.time()
c = 0
for d in data:
    ts = d[3]
    if ts > 1618973374:
        ts - 946684800

    if now - ts < 60 * 60 * 12 * 1000:
        temps.append(d[0])
        hums.append(d[1])
        RPMs.append(d[2])
        time = datetime.fromtimestamp(ts) 
        times.append(c)
        times2.append(time)
        c += 1

plt.plot(times, temps, 'ro')
plt.xlabel("time")
plt.ylabel("temperature (C)")
plt.title("Recent temp v. time")
plt.savefig('model/temp_time.png')
plt.clf()


plt.plot(times, hums, 'bo')
plt.xlabel("time")
plt.ylabel("humidity")
plt.title("Recent humidity v. time")
plt.savefig('model/hums_time.png')
plt.clf()


plt.plot(times, RPMs,  'yo')
plt.xlabel("time")
plt.ylabel("RPMs")
plt.title("Recent RPMS v. time")
plt.savefig('model/rpm_time.png')
plt.clf()
