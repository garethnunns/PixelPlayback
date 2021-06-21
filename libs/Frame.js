const { currentTime } = require('./util')

class Frame {
  /**
   * Store of received sACN data
   * @param {Number} seq sACN sequence number
   * @param {Number} uni The universe 
   * @param {Object} dmx DMX data for the universe
   */
  constructor(seq, uni=null, dmx=null) {
    this.sequence = seq
    this.time = currentTime()
    this.dmx = {}
    if(uni && dmx)
      this.dmx[uni] = dmx
  }
}

module.exports = Frame