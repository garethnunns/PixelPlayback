const { Playback } = require('./libs')

const playback = new Playback({
  filename: "playback/1624230670575.json",
  iface: 'en6'
}).on("loaded", () => {
  playback.play()
})