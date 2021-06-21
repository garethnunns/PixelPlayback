const { Receiver } = require('sacn')
const { networkInterfaces } = require('os')

const { Recording } = require('./libs')

const sACN = new Receiver({
  universes: Array.from(Array(44), (e,i)=>i+1), // to do: add options
  iface: networkInterfaces()['en6'][1].address, // to do add selector
  //iface: '127.0.0.1',
  reuseAddr: true
})

var record = new Recording({iface : sACN.iface})

sACN.on('packet', (packet) => {
  console.log(`ello ${packet.sequence}`)
  record.addPacket(packet)
})

sACN.on('PacketCorruption', (err) => {
  // trigged if a corrupted packet is received
})

sACN.on('PacketOutOfOrder', (err) => {
  // trigged if a packet is recieved out of order
})

sACN.on('error', (err) => {
  // trigged if there is an internal error (e.g. the supplied `iface` does not exist)
  console.log('ah....',err)
})

setInterval(() => {
  sACN.close()
  console.log(record)
  record.save()
},10000)