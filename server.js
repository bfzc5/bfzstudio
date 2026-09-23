const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();

app.use(express.json());

// Serve static frontend files from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint triggered from your website dashboard
app.post('/api/trigger-copy', (req, res) => {
    const { assetId } = req.body;

    if (!assetId) {
        return res.status(400).json({ error: "Missing asset identifier." });
    }

    console.log(`[+] Initializing pipeline for asset: ${assetId}`);

    // Execute the Python backend extraction script
    exec(`python3 core_extractor.py --id ${assetId}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`[-] Execution error: ${error.message}`);
            return res.status(500).json({ status: "failed", error: error.message });
        }
        
        return res.status(200).json({ 
            status: "success", 
            message: "Asset processed and webhook notification dispatched.",
            output: stdout.trim()
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`NexusStudio backend operational on port ${PORT}`);
});
