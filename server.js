const express = require('express');
const m3u8 = require('m3u8');
const fetch = require('node-fetch');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

app.post('/stream', async (req, res) => {
  const m3u8Url = req.body.m3u8_url;

  try {
    const response = await fetch(m3u8Url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const m3u8Content = await response.text();

    const playlist = m3u8.parse(m3u8Content);

    res.writeHead(200, {
      'Content-Type': 'application/x-mpegURL'
    });

    for (const segment of playlist.segments) {
      res.write(`${segment.uri}\n`);
    }

    res.end();

  } catch (error) {
    console.error(error);
    res.status(500).send(`Error: ${error.message}`);
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
