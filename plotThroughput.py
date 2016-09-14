"""
	Plot Network Throughput on Each Interface as Recorded by bwm-ng
"""
import re
import sys
import glob
import math
import numpy
from array import array
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
    MbitOut = []
    MbitIn = []
    packetsOut = []
    packetsIn = []
    errorsIn = []
    errorsOut = []
    ifaces = []
    for line in data:
      if "timestamp" in line or line[0] == '#':
        pass
      else:
        dataPoints.append(line.split(";"))
    for i in range(len(dataPoints)):
      timestamp.append(dataPoints[i][0])
      interfaceField.append(dataPoints[i][1])
      MbitOut.append(float(dataPoints[i][2]) * 8.0 / 1000000.0)
      MbitIn.append(float(dataPoints[i][3]) * 8.0 / 1000000.0)
      packetsOut.append(float(dataPoints[i][7]))
      packetsIn.append(float(dataPoints[i][8]))
      errorsIn.append(int(dataPoints[i][14]))
      errorsOut.append(int(dataPoints[i][15]))
    for i in range(len(set(interfaceField))):
      ifaces.append(interfaceField[i])

  avgTimestamp = [[] for _ in xrange(len(ifaces))]
  avgMbitOut = [[] for _ in xrange(len(ifaces))]
  avgMbitIn = [[] for _ in xrange(len(ifaces))]
  avgPacketsOut = [[] for _ in xrange(len(ifaces))]
  avgPacketsIn = [[] for _ in xrange(len(ifaces))]
  # Average the data over 10 samples
  skip = 0
  for i in range(len(dataPoints) - (10 * len(ifaces))):
    if skip:
      skip -= 1
      continue
    #print range(10 * len(ifaces))
    for j in range(10 * len(ifaces)):
      if timestamp[i] != timestamp[i+j]:
        #print "mismatch!: " + str(timestamp[i]) + " and " + str(timestamp[i+j])
        j -= 1
        break
    #print "matching: " + str(timestamp[i]) + " and " + str(timestamp[i+j])
    sumMbitOut = [[] for _ in xrange(len(ifaces))]
    sumMbitIn = [[] for _ in xrange(len(ifaces))]
    sumPacketsOut = [[] for _ in xrange(len(ifaces))]
    sumPacketsIn = [[] for _ in xrange(len(ifaces))]
    for k in range(j + 1):
      #print (i+k+1)
      whichIface = k % len(ifaces)
      sumMbitOut[whichIface].append(MbitOut[i+k])
      sumMbitIn[whichIface].append(MbitIn[i+k])
      sumPacketsOut[whichIface].append(packetsOut[i+k])
      sumPacketsIn[whichIface].append(packetsIn[i+k])
    #print sumMbitOut
    #print sumMbitIn
    #print sumPacketsOut
    #print sumPacketsIn
    for m in range(len(ifaces)):
      if (len(sumMbitOut[m]) > 0):
        avgTimestamp[m].append(timestamp[i])
        avgMbitOut[m].append(sum(sumMbitOut[m]) / len(sumMbitOut[m]))
        avgMbitIn[m].append(sum(sumMbitIn[m]) / len(sumMbitIn[m]))
        avgPacketsOut[m].append(sum(sumPacketsOut[m]) / len(sumPacketsOut[m]))
        avgPacketsIn[m].append(sum(sumPacketsIn[m]) / len(sumPacketsIn[m]))
      #else:
      #  print "No data!"
    #print "done!"
    skip = j

  for index in range(len(ifaces)):
    #print "Mbps In for " + ifaces[index] + ":"
    #print avgMbitIn[index]
    #print " "
    plt.figure(num=None, figsize=(16, 12), dpi=90, facecolor='w', edgecolor='k')

    ax = plt.subplot(111)
    graphMbitOut = ax.scatter(range(len(avgTimestamp[index])), avgMbitOut[index], s=20, c='b', alpha=0.8, lw=0, label='Traffic Out')
    graphMbitIn = ax.scatter(range(len(avgTimestamp[index])), avgMbitIn[index], s=20, c='r', alpha=0.8, lw=0, label='Traffic In')
    #graphPacketsOut = ax.scatter(range(len(dataPoints) / len(ifaces)), packetsOut[index::len(ifaces)], s=20, c='g', alpha=0.8, lw=0, label='Packets Out Per Second')
    #graphPacketsIn = ax.scatter(range(len(dataPoints) / len(ifaces)), packetsIn[index::len(ifaces)], s=20, c='m', alpha=0.8, lw=0, label='Packets In Per Second')

    ax.legend(handles=[graphMbitOut, graphMbitIn], loc=2)

    plt.xlim([-20, len(avgTimestamp[index]) + 20])
    plt.ylim([-5, max(max(avgMbitOut[index]), max(avgMbitIn[index])) + 20])

    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (Mbps)')
    if ('total' == ifaces[index]):
      plt.title('Throughput During File Transfer On All Interfaces')
    else:
      plt.title('Throughput During File Transfer On ' + ifaces[index])

    saveLocation = 'plots/' + date + '-graph-' + ifaces[index] + '.pdf'
    saveLocation2 = "png/" + date + '-graph-' + ifaces[index] + '.png'
    plt.savefig(saveLocation, bbox_inches='tight')
    plt.savefig(saveLocation2, bbox_inches='tight')
    #plt.show()
    plt.close()
