// Import required libraries
const crypto = require('crypto');
const { createCanvas, loadImage } = require('canvas');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');
const express = require('express');
const fileUpload = require('express-fileupload');

const app = express();
app.use(fileUpload());

// Serve HTML page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Image upload endpoint
app.post('/upload', async (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  let uploadedImage = req.files.image;
  const filePath = path.join(__dirname, 'uploads', uploadedImage.name);

  uploadedImage.mv(filePath, async (err) => {
    if (err) return res.status(500).send(err);

    try {
      const imgWithWatermark = await addWatermark(filePath);
      const imgId = uuidv4();
      const imgHash = crypto.createHash('sha256').update(imgWithWatermark).digest('hex');

      // Save watermarked image
      const outputFilePath = path.join(__dirname, 'output', `${imgId}.png`);
      fs.writeFileSync(outputFilePath, imgWithWatermark);

      res.send({
        message: 'Image uploaded successfully',
        imageId: imgId,
        imageHash: imgHash,
        outputPath: outputFilePath
      });
    } catch (error) {
      res.status(500).send('Error processing image.');
    }
  });
});

// Function to add watermark
async function addWatermark(filePath) {
  const img = await loadImage(filePath);
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');

  ctx.drawImage(img, 0, 0);

  // Generate small watermark pattern
  const patternSize = 2;
  const watermarkCanvas = createCanvas(patternSize, patternSize);
  const watermarkCtx = watermarkCanvas.getContext('2d');
  watermarkCtx.fillStyle = 'rgba(255, 255, 255, 0.1)';
  watermarkCtx.fillRect(0, 0, patternSize, patternSize);
  const pattern = ctx.createPattern(watermarkCanvas, 'repeat');

  // Draw the watermark onto the main image
  ctx.fillStyle = pattern;
  ctx.globalAlpha = 0.1; // Very low opacity to make it almost invisible
  ctx.fillRect(img.width - 20, img.height - 20, img.width / 50, img.height / 50);

  return canvas.toBuffer();
}

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});