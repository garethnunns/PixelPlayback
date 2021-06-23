{
  "version": 0.1,
  "file": {
    "name": "Example Mapping",
    "created": 123456789,
    "splitUniverses": true
  },
  "canvas": {
    "width": 44,
    "height": 48
  },
  "fixtures": {
    "BRGW": [
      "b",
      "r",
      "g",
      "l"
    ],
    "red": [
      "r",
      "0",
      "0",
      "l"
    ],
    "green": [
      "0",
      "g",
      "0",
      "l"
    ],
    "blue": [
      "0",
      "0",
      "b",
      "l"
    ]
  },
  "outputs": [
    {
      "universe": 3,
      "channel": 5,
      "strips": [
        {
          "start": [0,0],
          "end": [47,0],
          "count": 48,
          "size": 1,
          "fixture": "red"
        },
        {
          "start": [47,1],
          "end": [0,1],
          "count": 48,
          "size": 1,
          "fixture": "green"
        },
        {
          "start": [0,2],
          "end": [47,2],
          "count": 48,
          "size": 1,
          "fixture": "blue"
        },
        {
          "start": [47,3],
          "end": [0,3],
          "count": 48,
          "size": 1,
          "fixture": "BRGW"
        }
      ]
    },
    {
      "universe": 60,
      "channel": 1,
      "strips": [
        {
          "start": [0,20],
          "end": [0,20],
          "count": 1,
          "size": 1,
          "fixture": "red"
        }
      ]
    }
  ]
}