import sacn
import time
import netifaces

UNIVERSES = 44

IFACE = 'en6' # lo0 en6
FPS = 25

netifaces.ifaddresses(IFACE)
IP = netifaces.ifaddresses(IFACE)[netifaces.AF_INET][0]['addr']

CID = [ord(char) for char in "gareth nunns"]  + [int(char) for char in IP.split(".")] # generate CID based on IP

# define sender with attributes
sender = sacn.sACNsender(IP, 5568, 'GN ' + IP, tuple(CID), FPS)

# start the sending thread
sender.start()

for uni in range(1,UNIVERSES+1):
  # start sending data to universe
  sender.activate_output(uni)

  # set multicast to True
  sender[uni].multicast = True

  # sender[uni].destination = "169.254.90.4"  # or provide unicast information

  sender[uni].dmx_data = (1, 2, 3, 4, 5, 6, 7)  # some test DMX data

 # send the data for a bit
time.sleep(3)

# stop the sender
sender.stop()