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

#files = sorted(glob.glob('*.csv'))
files = ['clientEdge-throughput-09-20-16_02:16.csv']

for file in files:
  date = "-".join(file.split("-")[2:]).split(".")[0]
  with open (file, "r") as data:
    dataPoints = []
    interfaceActivity = [[],[]]
    interfaceField = []
    ifaces = []
    for line in data:
      if "timestamp" in line or "down" in line or "back" in line:
        interfaceActivity[0].append(len(dataPoints))
        interfaceActivity[1].append(line[1:].split('at')[0])
      else:
        dataPoints.append(line.split(';'))
    for i in range(len(dataPoints)):
      interfaceField.append(dataPoints[i][1])
    for i in range(len(set(interfaceField))):
      ifaces.append(interfaceField[i])
    timestamp = [[] for _ in xrange(len(ifaces))]
    MbitOut = [[] for _ in xrange(len(ifaces))]
    MbitIn = [[] for _ in xrange(len(ifaces))]
    traffic = [[] for _ in xrange(len(ifaces))]
    packetsOut = [[] for _ in xrange(len(ifaces))]
    packetsIn = [[] for _ in xrange(len(ifaces))]
    errorsIn = [[] for _ in xrange(len(ifaces))]
    errorsOut = [[] for _ in xrange(len(ifaces))]
    drift = 0
    index = 0
    #shift = 0
    while index < (len(dataPoints) - drift):
      adjustedIndex = index + drift
      whichInterface = adjustedIndex % len(ifaces)
      while (dataPoints[adjustedIndex][1] != ifaces[whichInterface]):
        #print 'mismatch! (' + dataPoints[adjustedIndex][1] + ' != ' + ifaces[whichInterface] + ') adding entry'
        #whichInterface = (whichInterface - 1) % len(ifaces)
        #datalist = [dataPoints[i][0], ifaces[whichInterface], '0.00', '0.00', '0.00', '0', '0', '0.00', '0.00', '0.00', '0', '0', '0.00', '0.00', '0', '0\n']
        #print datalist
        #print 'storing values in ' + ifaces[whichInterface]
        timestamp[whichInterface].append(dataPoints[i][0])
        MbitOut[whichInterface].append(0)
        MbitIn[whichInterface].append(0)
        traffic[whichInterface].append(0)
        packetsOut[whichInterface].append(0)
        packetsIn[whichInterface].append(0)
        errorsIn[whichInterface].append(0)
        errorsOut[whichInterface].append(0)
        #ifaces = ifaces[1:] + ifaces[:1] # SHIFT DATA
        #print 'now we have ' + ifaces[whichInterface]
        #shift = 1
        #whichInterface = i % len(ifaces)
        drift = drift + 1
        #ifaces = ifaces[1:] + ifaces[:1] # SHIFT DATA
        whichInterface = (index + drift) % len(ifaces)
      #print 'done'
      #if shift:
      #  whichInterface = (index + drift) % len(ifaces)
      #  whichInterface = i % len(ifaces)
      #  ifaces = ifaces[1:] + ifaces[:1] # SHIFT DATA
      #  shift = 0
      #print dataPoints[i]
      #print 'storing values in ' + ifaces[whichInterface]
      timestamp[whichInterface].append(dataPoints[adjustedIndex][0])
      MbitOut[whichInterface].append(float(dataPoints[adjustedIndex][2]) * 8.0 / 1000000.0)
      MbitIn[whichInterface].append(float(dataPoints[adjustedIndex][3]) * 8.0 / 1000000.0)
      traffic[whichInterface].append(float((float(dataPoints[adjustedIndex][2])) * 8.0 / 1000000.0) + ((float(dataPoints[adjustedIndex - 1][3])) * 8.0 / 1000000.0))
      packetsOut[whichInterface].append(float(dataPoints[adjustedIndex][7]))
      packetsIn[whichInterface].append(float(dataPoints[adjustedIndex][8]))
      errorsIn[whichInterface].append(int(dataPoints[adjustedIndex][14]))
      errorsOut[whichInterface].append(int(dataPoints[adjustedIndex][15]))
      index = index + 1

  '''
    PROGRAM MUST DETECT WHEN INTERFACES GO DOWN
    THIS IS WHAT CAUSES GRAPHS TO BE INACCURATE
  '''
  while (ifaces[0] != interfaceField[0]):
    ifaces = ifaces[1:] + ifaces[:1]
  for i in range(len(ifaces)):
    print ifaces[i] + ':\n\n' + '\n'.join([str(trafficElement) for trafficElement in MbitOut[i]]) + '\n\n'

  avgTimestamp = [[] for _ in xrange(len(ifaces))]
  avgMbitOut = [[] for _ in xrange(len(ifaces))]
  avgMbitIn = [[] for _ in xrange(len(ifaces))]
  avgTraffic = [[] for _ in xrange(len(ifaces))]
  avgPacketsOut = [[] for _ in xrange(len(ifaces))]
  avgPacketsIn = [[] for _ in xrange(len(ifaces))]
  # Average the data over 10 samples
  skip = 0
  limit = len(timestamp[0])
  for index in range(len(ifaces)):
    limit = min(limit, len(timestamp[index]))
  for i in range(limit - (10 * len(ifaces))):
    if skip:
      skip -= 1
      continue
    #print range(10 * len(ifaces))
    for j in range(10 * len(ifaces)):
      #print str(j) + ' and ' + str(i+j)
      if timestamp[0][i] != timestamp[0][i+j]:
        j -= 1
        break
    #print 'done'
    sumMbitOut = [[] for _ in xrange(len(ifaces))]
    sumMbitIn = [[] for _ in xrange(len(ifaces))]
    sumTraffic = [[] for _ in xrange(len(ifaces))]
    sumPacketsOut = [[] for _ in xrange(len(ifaces))]
    sumPacketsIn = [[] for _ in xrange(len(ifaces))]
    #print 'j is ' + str(range(j + 1))
    #print len(MbitOut[i % len(ifaces)])
    for k in range(j + 1):
      #print 'k is ' + str(k)
      whichIface = (i + k) % len(ifaces)
      #print (i + k)
      #print interfaceField[i+k] + ': ' + str(MbitOut[i+k])
      sumMbitOut[whichIface].append(MbitOut[whichIface][i+k])
      sumMbitIn[whichIface].append(MbitIn[whichIface][i+k])
      sumTraffic[whichIface].append(traffic[whichIface][i+k])
      sumPacketsOut[whichIface].append(packetsOut[whichIface][i+k])
      sumPacketsIn[whichIface].append(packetsIn[whichIface][i+k])
    #for p in range(len(ifaces)):
    #  print ifaces[p] + ': ' + str(sumMbitOut[p])
    for m in range(len(ifaces)):
      #print ifaces[m] + ': ' + str(sumMbitOut[m])
      if (len(sumMbitOut[m]) > 0):
        #print 
        avgTimestamp[m].append(timestamp[m][i])
        avgMbitOut[m].append(sum(sumMbitOut[m]) / len(sumMbitOut[m]))
        avgMbitIn[m].append(sum(sumMbitIn[m]) / len(sumMbitIn[m]))
        avgTraffic[m].append(sum(sumTraffic[m]) / len(sumTraffic[m]))
        avgPacketsOut[m].append(sum(sumPacketsOut[m]) / len(sumPacketsOut[m]))
        avgPacketsIn[m].append(sum(sumPacketsIn[m]) / len(sumPacketsIn[m]))
    skip = j

  #for m in range(len(ifaces)):
  #  print ifaces[m] + ': ' + str(avgMbitOut[m])

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
    graphTraffic.append(mlines.Line2D(range(len(avgTimestamp[index])), avgMbitOut[index], color=color[index], label=ifaces[index]))
    ax.add_line(mlines.Line2D(range(len(avgTimestamp[index])), avgMbitOut[index], color=color[index], label=ifaces[index]))

    avgMbitOut[index].sort(reverse=True)
    goodMax = 0
    #print len(avgMbitOut[index])
    for i in range(len(avgMbitOut[index])):
      if avgMbitOut[index][i] <= 2 * avgMbitOut[index][i+5]:
        goodMax = avgMbitOut[index][i] # eliminate outliers
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
  #plt.title('Throughput On ' + str(file.split("-")[0]) + ' During File Transfer')
  plt.title('Throughput On test During File Transfer')

  #saveLocation = 'plots/' + file.split("-")[0] + '-' + date + '.pdf'
  #saveLocation2 = "png/" + file.split("-")[0] + '-' + date + '.png'
  saveLocation = 'plots/' + file + '.pdf'
  saveLocation2 = "png/" + file + '.png'
  plt.savefig(saveLocation, bbox_inches='tight')
  plt.savefig(saveLocation2, bbox_inches='tight')
  plt.close()
