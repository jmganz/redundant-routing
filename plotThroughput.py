"""
	Plot Network Throughput on Each Interface as Recorded by bwm-ng
"""
import os
import re
import sys
import glob
import math
import numpy
import random
from array import array
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Collect the data from the given file

if not os.path.exists('plots'):
  os.makedirs('plots')
if not os.path.exists('png'):
  os.makedirs('png')

files = sorted(glob.glob('15 - Identical QoS Redo/clientEdge*.csv'))

for file in files:
  print file
  date = "-".join(file.split("-")[3:]).split(".")[0]
  with open (file, "r") as data:
    dataPoints = []
    interfaceActivity = [[],[]]
    interfaceField = []
    ifaces = []
    for line in data:
      if "timestamp" in line or "down" in line or "back" in line or "#" in line:
        interfaceActivity[0].append(int(line[1:].split('at')[1]))
        interfaceActivity[1].append(line[1:].split('at')[0])
      else:
        dataPoints.append(line.split(';'))
    for i in range(len(dataPoints)):
      if len(dataPoints[i]) < 2:
        print "Error: " + str(dataPoints[i])
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
    print str(dataPoints[0][1]) + ' and ' + str(ifaces[0])
    while index < (len(dataPoints) - drift):
      adjustedIndex = index + drift
      whichInterface = adjustedIndex % len(ifaces)
      while (dataPoints[adjustedIndex][1] != ifaces[whichInterface]):
        #print str(dataPoints[adjustedIndex][1]) + ' != ' + str(ifaces[whichInterface]) + ' at ' + str(adjustedIndex)
        if (int(dataPoints[adjustedIndex][0]) > int(dataPoints[0][0]) + 400) and (int(dataPoints[adjustedIndex][0]) < int(dataPoints[0][0]) + 450):
          print str(ifaces[whichInterface]) + ': nothing'
        timestamp[whichInterface].append(dataPoints[adjustedIndex][0])
        MbitOut[whichInterface].append(0)
        MbitIn[whichInterface].append(0)
        traffic[whichInterface].append(0)
        packetsOut[whichInterface].append(0)
        packetsIn[whichInterface].append(0)
        errorsIn[whichInterface].append(0)
        errorsOut[whichInterface].append(0)
        drift += 1
        whichInterface = (index + drift) % len(ifaces)
      timestamp[whichInterface].append(dataPoints[adjustedIndex][0])
      #if (float(dataPoints[adjustedIndex][2]) * 8.0 / 1000000.0) < 0.001:
      #  MbitOut[whichInterface].append(-3 - 3 * whichInterface)
      #else:
      if (int(dataPoints[adjustedIndex][0]) > int(dataPoints[0][0]) + 400) and (int(dataPoints[adjustedIndex][0]) < int(dataPoints[0][0]) + 450):
        print str(ifaces[whichInterface]) + ': ' + str(float(dataPoints[adjustedIndex][2]) * 8.0 / 1000000.0) + ' Mbps'
      MbitOut[whichInterface].append(float(dataPoints[adjustedIndex][2]) * 8.0 / 1000000.0)
      MbitIn[whichInterface].append(float(dataPoints[adjustedIndex][3]) * 8.0 / 1000000.0)
      traffic[whichInterface].append(float((float(dataPoints[adjustedIndex][2])) * 8.0 / 1000000.0) + ((float(dataPoints[adjustedIndex - 1][3])) * 8.0 / 1000000.0))
      packetsOut[whichInterface].append(float(dataPoints[adjustedIndex][7]))
      packetsIn[whichInterface].append(float(dataPoints[adjustedIndex][8]))
      errorsIn[whichInterface].append(int(dataPoints[adjustedIndex][14]))
      errorsOut[whichInterface].append(int(dataPoints[adjustedIndex][15]))
      index += 1
    print 'drift = ' + str(drift)
    while (ifaces[0] != interfaceField[0]):
      ifaces = ifaces[1:] + ifaces[:1]
  iperfTransfer = []
  with open (glob.glob(file.split("/")[0] + '/iperf3-client-log-' + date[:-2] + '*.log')[0], "r") as iperf:
    for line in iperf:
      if 'sender' in line or 'receiver' in line:
        avgSpeed = line.split('bits/sec')[0].split(' ')
        avgSpeed = float(avgSpeed[len(avgSpeed) - 2])
        break
      elif 'Bytes' in line:
        speed = line.split('bits/sec')[0].split(' ')
        speed = float(speed[len(speed) - 2])
        if speed > 250:
          speed = 0
        iperfTransfer.append(speed)
    

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
    for j in range(10 * len(ifaces)):
      if timestamp[0][i] != timestamp[0][i+j]:
        j -= 1
        break
    sumMbitOut = [[] for _ in xrange(len(ifaces))]
    sumMbitIn = [[] for _ in xrange(len(ifaces))]
    sumTraffic = [[] for _ in xrange(len(ifaces))]
    sumPacketsOut = [[] for _ in xrange(len(ifaces))]
    sumPacketsIn = [[] for _ in xrange(len(ifaces))]
    for k in range(j + 1):
      whichIface = (i + k) % len(ifaces)
      sumMbitOut[whichIface].append(MbitOut[whichIface][i+k])
      sumMbitIn[whichIface].append(MbitIn[whichIface][i+k])
      sumTraffic[whichIface].append(traffic[whichIface][i+k])
      sumPacketsOut[whichIface].append(packetsOut[whichIface][i+k])
      sumPacketsIn[whichIface].append(packetsIn[whichIface][i+k])
    for m in range(len(ifaces)):
      if (len(sumMbitOut[m]) > 0):
        avgTimestamp[m].append(timestamp[m][i])
        avgMbitOut[m].append(sum(sumMbitOut[m]) / len(sumMbitOut[m]))
        avgMbitIn[m].append(sum(sumMbitIn[m]) / len(sumMbitIn[m]))
        avgTraffic[m].append(sum(sumTraffic[m]) / len(sumTraffic[m]))
        avgPacketsOut[m].append(sum(sumPacketsOut[m]) / len(sumPacketsOut[m]))
        avgPacketsIn[m].append(sum(sumPacketsIn[m]) / len(sumPacketsIn[m]))
    skip = j

  color = ['r', 'g', 'b', 'm', 'c', 'k', 'y']

  # This code looks odd
  # We'll shuffle the ifaces until they're sorted
  # There are usually less than 10
  # so statistically, it shouldn't take too many attempts
  # even though the shuffle is random
  # but if the shuffle is random, we mix up all the associated data!
  # that's why we use variable r: it forces the exact same shuffle
  # for all lists, keeping the association for all ifaces

  for i in range(len(ifaces)):
    print ifaces[i] + ': ' + str(min(MbitOut[i])) + ', ' + str(max(MbitOut[i])) + ', ' + str(sum(MbitOut[i])/len(MbitOut[i]))

  while (ifaces != sorted(ifaces)):
    #for i in range(len(ifaces)):
    #  print str(ifaces[i]) + ': ' + str(min(MbitOut[i])) + ', ' + str(max(MbitOut[i])) + ', ' + str(sum(MbitOut[i])/len(MbitOut[i]))
    r = random.random()
    for variable in [ifaces, timestamp, MbitOut, traffic, packetsOut, packetsIn, errorsIn, errorsOut, avgTimestamp, avgMbitOut, avgMbitIn, avgTraffic, avgPacketsOut, avgPacketsIn, sumMbitOut, sumMbitIn, sumTraffic, sumPacketsOut, sumPacketsIn]:
      random.shuffle(variable, lambda: r)

  plt.figure(num=None, figsize=(16, 12), dpi=90, facecolor='w', edgecolor='k')
  ax = plt.subplot(111)
  graphTraffic = []
  upperLimit = -20
  pixelSize = 15
  transparency = 0.50
  iperfStart = int(avgTimestamp[0][0]) + 20
  graphTraffic.append(mlines.Line2D(range(iperfStart, iperfStart + len(iperfTransfer)), iperfTransfer, color='k', label='instantaneous throughput'))
  ax.add_line(mlines.Line2D(range(iperfStart, iperfStart + len(iperfTransfer)), iperfTransfer, color='k', label='instantaneous throughput'))
  graphTraffic.append(plt.axhline(y=avgSpeed, color='b', ls='dashed', label='average throughput'))

  for index in range(len(ifaces)):
    if ('total' == ifaces[index]) or ('lo' == ifaces[index]):
      continue
    #graphTraffic.append(mlines.Line2D(avgTimestamp[index], avgMbitOut[index], color=color[index], label=ifaces[index]))
    #ax.add_line(mlines.Line2D(avgTimestamp[index], avgMbitOut[index], color=color[index], label=ifaces[index]))
    #graphTraffic.append(ax.scatter(avgTimestamp[index], avgMbitOut[index], s=20, color=color[index], alpha=0.8, lw=0, label=ifaces[index]))



    #print ifaces[index] + ': ' + str(max(MbitOut[index]))
    #if (max(MbitOut[index]) < 5.0):
    #  print str(ifaces[index]) + ': ' + str(MbitOut[index])
    #  continue # don't bother graphing interfaces that have very little activity



    #print sorted(MbitOut[index])
    graphTraffic.append(ax.scatter(timestamp[index], MbitOut[index], s=pixelSize, color=color[index], alpha=transparency, lw=0, label=ifaces[index]))
    #pixelSize -= 4
    #transparency -= 0.15
    avgMbitOut[index].sort(reverse=True)
    goodMax = 0
    #for i in range(len(avgMbitOut[index])):
    #  if avgMbitOut[index][i] <= 2 * avgMbitOut[index][i+5]:
    #    goodMax = avgMbitOut[index][i] # eliminate outliers
    #    break
    if upperLimit < goodMax:
      upperLimit = goodMax
  upperLimit = 600 # ensure that all graphs are the same height
  moveLegend = 0 # useful for my first set of data
  if (moveLegend):
    legend = plt.legend(handles=graphTraffic, loc='lower right')
    plt.draw()
    legendBox = legend.legendPatch.get_bbox().inverse_transformed(ax.transAxes)
    legendBox.set_points([[legendBox.x0 + 1.15, legendBox.y0 + 0.20], [legendBox.x1 + 1.15, legendBox.y1 + 0.20]])
    legend.set_bbox_to_anchor(legendBox)
  else:
    legend = plt.legend(handles=graphTraffic, loc='upper left')
  plt.xlim([(int(timestamp[1][0]) - 20), (int(timestamp[1][len(timestamp[1]) - 1]) + 20)])
  #plt.ylim([-5, upperLimit + 20])
  plt.ylim([-20, upperLimit])
  position = upperLimit / 5
  for i in range(len(interfaceActivity[0])):
    # plot vertical lines indicating interface activity
    position += upperLimit / 10
    plt.axvline(interfaceActivity[0][i])
    if (i > 0) and (interfaceActivity[0][i] - interfaceActivity[0][i - 1] > 100):
      shift = -61
    else:
      shift = 2
    ax.annotate(interfaceActivity[1][i], xy=(interfaceActivity[0][i], 0), xytext=((interfaceActivity[0][i] + shift), position))

  plt.ticklabel_format(style='plain', axis='x', useOffset=True)
  plt.xlabel('Time (s)')
  plt.ylabel('Throughput (Mbps)')
  plt.title('Throughput On ' + str(file.split("-")[0]) + ' During File Transfer')
  saveLocation = file.split("/")[0] + '/plots/' + file.split("/")[1].split("-")[0] + '-' + date + '.pdf'
  saveLocation2 = file.split("/")[0] + "/png/" + file.split("/")[1].split("-")[0] + '-' + date + '.png'
  plt.savefig(saveLocation, bbox_inches='tight')
  plt.savefig(saveLocation2, bbox_inches='tight')
  plt.close()
