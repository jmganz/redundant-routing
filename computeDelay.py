"""
	Compute delay according to bwm-ng between an active network interface
	going down and another interface picking up the connection
"""
import glob

# Collect the data from the given file

directories = sorted(glob.glob('1*'))

modulus = 7
speedThreshold = 50
pollingResolution = 10

for directory in directories:
  allDelays = []
  positiveDelays = []
  files = sorted(glob.glob(directory + '/clientEdge*.csv'))
  for file in files:
    interface = [None] * modulus
    speed = [None] * modulus
    #print file + '\n'
    with open (file, "r") as data:
      interfaceDown = 0
      trulyDown = 0
      upDelay = 0
      skip = 0
      index = 0
      for line in data:
        if 'down' in line:
          #print line.split('#')[1].split('\n')[0]
          for i in range(0, modulus):
            if interface[i] != 'total' and speed[i] > speedThreshold:
              activeInterface = interface[i]
              #print activeInterface + ' is active with speed ' + str(speed[i]) + ' Mbps'
          interfaceDown = 1
        elif 'back' in line:
          continue
        else:
          data = line.split(';')
          #print index % modulus
          #print data
          #print interface
          interface[index % modulus] = str(data[1])
          speed[index % modulus] = (float(data[2]) * 8.0 / 1000000.0)
          index += 1
          if trulyDown == 0 and interfaceDown == 1:
            #missingInterface = 1
            #for i in range(0, modulus):
            #  #print interface[i]
            #  if interface[i] == activeInterface:
            #    missingInterface = 0
            #if missingInterface == 1:
            if (float(data[2]) * 8.0 / 1000000.0) > 2000:
              trulyDown = 1
              skip = 1
          #if trulyDown == 0 and interfaceDown == 1:
          #  print 'we still see the active interface'
          #if trulyDown == 1:
          #  print line.split('\n')[0]
          if trulyDown == 1 and data[1] == 'total' and (float(data[2]) * 8.0 / 1000000.0) < speedThreshold:
            upDelay += 1
          if trulyDown == 1 and skip == 0 and (float(data[2]) * 8.0 / 1000000.0) > speedThreshold and (float(data[2]) * 8.0 / 1000000.0) < 2000:
            allDelays.append(upDelay)
            if upDelay > 0:
              positiveDelays.append(upDelay)
            #print 'It took the connection ' + str(upDelay) + ' units (~' + str(upDelay * pollingResolution) + ' ms) to recover\n'
            interface = [None] * modulus
            speed = [None] * modulus
            interfaceDown = 0
            trulyDown = 0
            upDelay = 0
            index = 0
            skip = 0
          if data[1] == 'total' and skip == 1:
            skip = 0

  #print allDelays
  print directory
  print 'Average delay: ' + str(sum(allDelays) * pollingResolution / len(allDelays)) + ' ms'
  print 'Without zeros: ' + str(sum(positiveDelays) * pollingResolution / len(positiveDelays)) + ' ms'
  output = open(directory + '/' + directory + '-throughput-delay.log', 'w')
  output.write(directory + '\n')
  output.write('Average delay: ' + str(sum(allDelays) * pollingResolution / len(allDelays)) + ' ms\n')
  output.write('Without zeros: ' + str(sum(positiveDelays) * pollingResolution / len(positiveDelays)) + ' ms')
  output.close()
