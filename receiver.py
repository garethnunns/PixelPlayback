import sacn
import time
import netifaces

receiver = sacn.sACNreceiver()
# start the receiving thread
receiver.start()

# define a callback function
@receiver.listen_on('universe', universe=1)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
  # print the received info
  print(packet)

# check for availability of universes
@receiver.listen_on('availability')
def callback_available(universe, changed):
  print(f'universe {universe}: {changed}')

receiver.join_multicast(1)

# receive for a bit
time.sleep(5)
receiver.stop()