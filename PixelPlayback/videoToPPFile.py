import json
import cv2
import colorsys
from PPFile import PPFile, Frame
from util import filePathToFileName

def videoToPPFile(videoFilePath, mappingFilePath):
  videoFileName = filePathToFileName(videoFilePath)

  ppFile = PPFile(videoFileName, "videoToPPFile")

  # load video
  video = cv2.VideoCapture(videoFilePath)

  # get basic props of video
  fps = video.get(cv2.CAP_PROP_FPS)
  duration = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
  width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

  # TODO: check width and height match video and scale pixels

  ppFile.output["file"]["duration"] = int(fps * duration * 1000)
  ppFile.output["video"] = {
    "fps": fps,
    "mapping": mappingFilePath
  }

  mapping = loadMapping(mappingFilePath)

  for f in range(0, duration):
    video.set(cv2.CAP_PROP_POS_FRAMES, f)
    res, vFrame = video.read()

    # create a new frame
    ppFrame = Frame(int(f * 1000/fps))

    # loop through the outputs specified in the mapping
    for output in mapping["outputs"]:
      curUni = output["universe"]
      curCh = output["channel"]

      # loop through the strips in that output
      for strip in output["strips"]:
        startX, startY = strip["start"]
        endX, endY = strip["end"]

        count = strip["count"]

        # loop through the pixels in the strip
        for pixel in range(count):
          # TODO: add pixel averaging
          curX = int(startX + pixel * (endX - startX)/(count - 1)) if count > 1 else startX
          curY = int(startY + pixel * (endY - startY)/(count - 1)) if count > 1 else startY

          # get colours for this pixel
          BGR = list(vFrame[curX,curY])
          RGBHLS = BGRtoRGBHLS(BGR)

          # get the specified fixture
          # TODO: check fixture exists and throw error
          fixture = mapping["fixtures"][strip["fixture"]]

          # work out whether this fixture will split a universe
          if not mapping["file"]["splitUniverses"] and curCh + len(fixture) > 512:
            curUni += 1
            curCh = 1

          # loop through the subpixels in the specified fixture type
          for subpixel in fixture:
            # check this uni exists and if not create it
            if curUni not in ppFrame.dmx:
              ppFrame.dmx[curUni] = {}

            # work out each channel value
            # and make it an integer < 255
            ppFrame.dmx[curUni][curCh] = min(int(subpixel(*RGBHLS)),255)

            # increment the channel
            curCh += 1

            # increment the channel if needed
            if curCh == 513:
              curUni += 1
              curCh = 1

    # add that frame to the file
    ppFile.addFrame(f, ppFrame)

  # and after all that save the file
  ppFile.save()


def loadMapping(mappingFilePath):
  mapping = json.load(open(mappingFilePath))

  # convert pixel types to lamba functions
  for fixture in mapping["fixtures"]:
    mapping["fixtures"][fixture] = [eval("lambda r, g, b, h, l, s : " + ch) for ch in mapping["fixtures"][fixture]]

  return mapping


def BGRtoRGBHLS(colours):
  colours.reverse()
  hls = colorsys.rgb_to_hls(*(col/255 for col in colours))
  return tuple(colours) + tuple(int(col*255) for col in hls)