const { Sender } = require('sacn')
const fs = require('fs')
const { networkInterfaces } = require('os')
const EventEmitter = require("events")

class Playback extends EventEmitter {
  constructor({filename = null, iface = 'lo0'}) {
    super()
    this.servers = {}
    this._universes = []
    this.iface = iface
    this.recording = null
    this.sourceName = "Pixel Playback"
    this.syncUni = 7962
    
    if(filename) {
      this.filename = filename
      this.loadRecording(filename)
    }

    this.syncServer = new Sender({
      universe: this.syncUni,
      reuseAddr: true
    })

    // based on ANSI E1.31 2018
    // ideally this would be handled by the library in future
    this.syncServer.root_fl = 0x7021
    this.syncServer.root_vector = 8
    this.syncServer.frame_fl = 0x7058;// 0x700b
    this.syncServer.frame_vector = 1
    this.syncServer.syncUniverse = this.syncUni

    this.syncServer.socket.on('listening', () => {
      this.syncServer.socket.setMulticastInterface(networkInterfaces()[this.iface][1].address)
    })

    console.log(this.syncServer)
  }

  get universes() {
    return this._universes
  }

  set universes(universes) {
    this._universes = universes

    // create servers for each universe
    universes.forEach(uni => {
      this.servers[uni] = new Sender({
        universe: uni,
        reuseAddr: true
      })

      this.servers[uni].syncUniverse = this.syncUni

      this.servers[uni].socket.on('listening', () => {
        this.servers[uni].socket.setMulticastInterface(networkInterfaces()[this.iface][1].address)
      })
    })
  }

  loadRecording(filename) {
    this.recording = JSON.parse(fs.readFileSync(filename, 'utf8'))
    this.universes = this.recording.universes

    if(this.recording.start > 0) {
      for(const frame in this.recording.frames) {
        this.recording.frames[frame].time -= this.recording.start
      }
    }

    this.recording.start = 0

    for(const frame in this.recording.frames) {
      for(const uni in this.recording.frames[frame].dmx) {
        Object.keys(this.recording.frames[frame].dmx[uni]).map((ch) => {
          this.recording.frames[frame].dmx[uni][ch] /= 2.55 // to do: make it so it send values not percentage
        })
      }
    }

    setImmediate(() => { // to do: work out why this is needed...
      this.emit("loaded")
    })
  }

  play(loop = true) {
    let duration = 0

    for(const frame in this.recording.frames) {
      setTimeout(() => {
        this.send(this.recording.frames[frame])
      }, this.recording.frames[frame].time)

      duration = this.recording.frames[frame].time
    }

    if(loop) {
      setTimeout(() => {
        this.play()
      }, duration)
    }
  }

  send(frame) {
    if(this.recording == null)
      throw new Error("No recording loaded")
    
    let sequence = 0

    for(const uni in frame.dmx) {
      this.servers[uni].send({
        payload: frame.dmx[uni],
        sourceName: this.sourceName,
        priority: 100,
      })

      sequence = this.servers[uni].sequence
    }

    // based on ANSI E1.31 2018
    // ideally this would be handled by the library in future
    let seqUni = new Uint8Array(3)
    seqUni[0] = sequence
    seqUni[1] = this.syncUni >> 8
    seqUni[2] = this.syncUni & 255
    
    this.syncServer.send({
      payload: {},
      sourceName: Buffer.from(seqUni).toString(),
      priority: 100
    })
  }
}

module.exports = Playback