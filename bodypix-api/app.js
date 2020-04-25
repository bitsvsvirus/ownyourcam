const tf = require('@tensorflow/tfjs-node');
const bodyPix = require('@tensorflow-models/body-pix');
const fs = require('fs').promises;
const http = require('http');
(async () => {
    const net = await bodyPix.load({
        architecture: 'MobileNetV1',
        outputStride: 16,
        multiplier: 0.75,
        quantBytes: 2,
    });
    const server = http.createServer();
    server.on('request', async (req, res) => {
        var chunks = [];
        req.on('data', (chunk) => {
            chunks.push(chunk);
        });
        req.on('end', async () => {
            // Write image to localfile (for debug purpose)
            await fs.writeFile('image.jpg', Buffer.concat(chunks));
            const image = tf.node.decodeImage(Buffer.concat(chunks));
            segmentation = await net.segmentPerson(image, {
                internalResolution: "medium",
                segmentationThreshold: 0.7,
                maxDetections: 5,
                scoreThreshold: 0.3,
                nmsRadius: 20,
            });
            res.writeHead(200, {'Content-Type': 'application/octet-stream'});
            res.write(Buffer.from(segmentation.data));
            res.end();
            tf.dispose(image);
        });
    });
    server.listen(9000);
})();
