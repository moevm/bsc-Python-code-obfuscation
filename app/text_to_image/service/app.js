const express = require('express');

const router = require('./router');

var app = express();

app.use(express.json());

app.use('/api', router);

app.listen(process.env.PORT || 8080);
