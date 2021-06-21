const fs = require('fs')
const path = require('path')

const { currentTime } = require('./util')
const Frame = require('./Frame')

class Recording {
  constructor({sourceName = "", iface = null} = {}) {
    this.start = currentTime()
    this.iface = iface
    this.sourceName = sourceName
    this.sourceAddress = ""
    this.universes = []
    this.sequences = 0
    this.frames = {}
  }

  seqToFrame(sequence) {
    const lastFrame = Math.max(...Object.keys(this.frames))

    if(lastFrame > 0 && (lastFrame % 256 > sequence))
      // added sequence number is in the next sequence
      this.sequences++
    
    return this.sequences * 256 + sequence
  }

  /**
   * Add/update a frame
   * @param {Frame} frame Object of type frame
   */
  addFrame(frame) {
    // keep track of universes being recorded
    Object.keys(frame.dmx).forEach(uni => {
      if(this.universes.indexOf(uni) === -1)
        this.universes.push(uni)
    })

    // frame number in frames object
    const frameNumber = this.seqToFrame(frame.sequence)

    if(!this.frames[frameNumber]) {
      // frame hasn't been created yet
      this.frames[frameNumber] = frame
    }
    else {
      // merge the data of the two
      this.frames[frameNumber].dmx = {...this.frames[frameNumber].dmx, ...frame.dmx}
    }
  }

  addPacket(packet) {
    this.sourceName = packet.sourceName
    this.sourceAddress = packet.sourceAddress

    const receivedFrame = new Frame(packet.sequence,packet.universe,this.bufferToObject(packet.payloadAsBuffer))
    this.addFrame(receivedFrame)
  }

  /**
   * Convert buffer into object with value pairs
   * @param {Buffer} buffer
   */
  bufferToObject(buffer) {
    const data = {};
    buffer.forEach((val, ch) => {
      if (val > 0) data[ch + 1] = val;
    });
    return data;
  }

  save(filename = null) {
    if(!filename)
      filename = currentTime() + '.json'

    filename = path.resolve('playback',filename)

    fs.writeFileSync(filename, JSON.stringify(this, null, 2));
  }
}

module.exports = Recording