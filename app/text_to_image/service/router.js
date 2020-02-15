const express = require('express');

const textToImage = require('text-to-image');

var router = express.Router()

router.post('/text-to-image', (req, res) => {
    let data = req.body;

    let text = data['text'];
    let options = data['options'];

    textToImage.generate(text, options)
        .then(dataURI => {
            res.json({
                status: 'success',
                message: 'successfully generate image',
                dataURI: dataURI,
                date: new Date()
            });
        })
        .catch(error => {
            res.json({
                status: 'fail',
                message: 'fail to generate image',
                errorMessage: error,
                date: new Date()
            });
        });
});

module.exports = router;
