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
    
    if(filename) {
      this.filename = filename
      this.loadRecording(filename)
    }
  }

  ready(){
    this.emit("ready")
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
    
    for(const uni in frame.dmx) {
      this.servers[uni].send({
        payload: frame.dmx[uni],
        sourceName: "Pixel Playback",
        priority: 100,
      })
    }
  }
}

module.exports = Playback