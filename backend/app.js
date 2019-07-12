const express = require('express')
const app = express()
const port = 3000

let data = [];

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.post('/send', (req, res) => {
    req.
    res.send('Hello World!')
})

app.listen(port, '0.0.0.0', () => console.log(`[WithU] listening on port ${port}!`))

