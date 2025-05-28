const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const axios = require('axios');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors());
app.use(express.json());

wss.on('connection', (ws) => {
  console.log('🔌 WebSocket client connected');

  ws.on('message', async (message) => {
    const query = message.toString();
    console.log("📨 Received query:", query);

    try {
      const response = await axios.post('http://127.0.0.1:8000/ask', {
        query: query
      });

      const answer = response.data.answer;
      // Send JSON string to client
      ws.send(JSON.stringify({ answer }));
    } catch (error) {
      console.error("❌ Error calling Python RAG API:", error.message);
      ws.send(JSON.stringify({ answer: "Error fetching answer from RAG engine." }));
    }
  });

  ws.on('close', () => {
    console.log("❌ WebSocket client disconnected");
  });
});

app.get('/', (req, res) => {
  res.send("RAG Node WebSocket Server is running!");
});

server.listen(3001, () => {
  console.log("🚀 Node.js WebSocket server running on http://localhost:3001");
});
