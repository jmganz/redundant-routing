"""
	Plot Network Throughput on Each Interface as Recorded by bwm-ng
"""
import re
import sys
import glob
import math
import numpy
from array import array
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Collect the data from the given file

files = sorted(glob.glob('*.csv'))

for file in files:
  date = "-".join(file.split("-")[2:]).split(".")[0]
  with open (file, "r") as data:
    dataPoints = []
    timestamp = []
    interfaceField = []
    interfaceActivity = [[],[]]
    MbitOut = []
    MbitIn = []
    traffic = []
    packetsOut = []
    packetsIn = []
    errorsIn = []
    errorsOut = []
    ifaces = []
    for line in data:
      if "timestamp" in line or "down" in line or "back" in line:
        interfaceActivity[0].append(len(dataPoints))
        interfaceActivity[1].append(line[1:].split('at')[0])
      else:
        dataPoints.append(line.split(";"))
    for i in range(len(dataPoints)):
      timestamp.append(dataPoints[i][0])
      interfaceField.append(dataPoints[i][1])
      MbitOut.append(float(dataPoints[i][2]) * 8.0 / 1000000.0)
      MbitIn.append(float(dataPoints[i][3]) * 8.0 / 1000000.0)
      traffic.append(float((float(dataPoints[i][2])) * 8.0 / 1000000.0) + ((float(dataPoints[i][3])) * 8.0 / 1000000.0))
      packetsOut.append(float(dataPoints[i][7]))
      packetsIn.append(float(dataPoints[i][8]))
      errorsIn.append(int(dataPoints[i][14]))
      errorsOut.append(int(dataPoints[i][15]))
    for i in range(len(set(interfaceField))):
      ifaces.append(interfaceField[i])

  avgTimestamp = [[] for _ in xrange(len(ifaces))]
  avgMbitOut = [[] for _ in xrange(len(ifaces))]
  avgMbitIn = [[] for _ in xrange(len(ifaces))]
  avgTraffic = [[] for _ in xrange(len(ifaces))]
  avgPacketsOut = [[] for _ in xrange(len(ifaces))]
  avgPacketsIn = [[] for _ in xrange(len(ifaces))]
  # Average the data over 10 samples
  skip = 0
  for i in range(len(dataPoints) - (10 * len(ifaces))):
    if skip:
      skip -= 1
      continue
    for j in range(10 * len(ifaces)):
      if timestamp[i] != timestamp[i+j]:
        j -= 1
        break
    sumMbitOut = [[] for _ in xrange(len(ifaces))]
    sumMbitIn = [[] for _ in xrange(len(ifaces))]
    sumTraffic = [[] for _ in xrange(len(ifaces))]
    sumPacketsOut = [[] for _ in xrange(len(ifaces))]
    sumPacketsIn = [[] for _ in xrange(len(ifaces))]
    for k in range(j + 1):
      whichIface = k % len(ifaces)
      sumMbitOut[whichIface].append(MbitOut[i+k])
      sumMbitIn[whichIface].append(MbitIn[i+k])
      sumTraffic[whichIface].append(traffic[i+k])
      sumPacketsOut[whichIface].append(packetsOut[i+k])
      sumPacketsIn[whichIface].append(packetsIn[i+k])
    for m in range(len(ifaces)):
      if (len(sumMbitOut[m]) > 0):
        avgTimestamp[m].append(timestamp[i])
        avgMbitOut[m].append(sum(sumMbitOut[m]) / len(sumMbitOut[m]))
        avgMbitIn[m].append(sum(sumMbitIn[m]) / len(sumMbitIn[m]))
        avgTraffic[m].append(sum(sumTraffic[m]) / len(sumTraffic[m]))
        avgPacketsOut[m].append(sum(sumPacketsOut[m]) / len(sumPacketsOut[m]))
        avgPacketsIn[m].append(sum(sumPacketsIn[m]) / len(sumPacketsIn[m]))
    skip = j

  for index in range(len(interfaceActivity[0])):
    interfaceActivity[0][index] = (interfaceActivity[0][index] / (10 * len(ifaces)))

  color = ['b', 'r', 'g', 'm', 'k', 'c', 'y']

  plt.figure(num=None, figsize=(16, 12), dpi=90, facecolor='w', edgecolor='k')
  ax = plt.subplot(111)
  graphTraffic = []
  upperLimit = -20
  for index in range(len(ifaces)):
    if ('total' == ifaces[index]) or ('lo' == ifaces[index]):
      continue
    graphTraffic.append(mlines.Line2D(range(len(avgTimestamp[index])), avgTraffic[index], color=color[index], label=ifaces[index]))
    ax.add_line(mlines.Line2D(range(len(avgTimestamp[index])), avgTraffic[index], color=color[index], label=ifaces[index]))

    avgTraffic[index].sort(reverse=True)
    for i in range(len(avgTraffic[index])):
      if avgTraffic[index][i] < 2 * avgTraffic[index][i+5]:
        goodMax = avgTraffic[index][i] # eliminate outliers
        break
    if upperLimit < goodMax:
      upperLimit = goodMax
  plt.legend(handles=graphTraffic, loc=2)

  plt.xlim([-20, max([len(avgTimestamp[i]) for i in range(len(avgTimestamp))]) + 20])
  plt.ylim([-5, upperLimit + 20])
  position = upperLimit / 5
  for i in range(len(interfaceActivity[0])):
    position += upperLimit / 10
    plt.axvline(interfaceActivity[0][i])
    ax.annotate(interfaceActivity[1][i], xy=(0, 0), xytext=((interfaceActivity[0][i] + 5), position))

  plt.xlabel('Time (s)')
  plt.ylabel('Throughput (Mbps)')
  plt.title('Throughput On ' + str(file.split("-")[0]) + ' During File Transfer')

  saveLocation = 'plots/' + file.split("-")[0] + '-' + date + '.pdf'
  saveLocation2 = "png/" + file.split("-")[0] + '-' + date + '.png'
  plt.savefig(saveLocation, bbox_inches='tight')
  plt.savefig(saveLocation2, bbox_inches='tight')
  plt.close()
