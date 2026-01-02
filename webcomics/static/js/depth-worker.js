
// Web Worker for Client-Side Depth Generation
// Moves heavy AI processing off the main thread to prevent UI freezing.

import { pipeline, env, RawImage } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2';

// Skip local model checks
env.allowLocalModels = false;

let depthModel = null;

// Initialize model
async function initModel() {
    if (!depthModel) {
        console.log("Worker: Loading Depth Model...");
        depthModel = await pipeline('depth-estimation', 'Xenova/depth-anything-small-hf', {
            device: 'webgpu', // Try WebGPU first, fall back to wasm automatically
        });
        console.log("Worker: Model Loaded.");
    }
}

self.onmessage = async (e) => {
    const { action, imageUrl, id } = e.data;

    if (action === 'preload') {
        // Just load the model into memory
        await initModel();
        self.postMessage({ status: 'preloaded' });
        return;
    }

    if (action === 'generate') {
        try {
            await initModel();

            // Fetch image in worker
            // We use RawImage from transformers.js or simple fetch
            // But pipeline accepts URLs directly too (usually).
            // Let's use the URL.

            const result = await depthModel(imageUrl);

            // result.depth is the tensor/raw image data
            // We need to send back transferable data to keep it fast
            // The result.depth is usually { data, width, height, channels }

            // Convert to RGBA for canvas
            const rawData = result.depth.data;
            const width = result.depth.width;
            const height = result.depth.height;
            const channels = result.depth.channels || 1;

            const rgbaData = new Uint8ClampedArray(width * height * 4);

            for (let i = 0; i < width * height; i++) {
                const val = rawData[i * channels];
                rgbaData[i * 4] = val;
                rgbaData[i * 4 + 1] = val;
                rgbaData[i * 4 + 2] = val;
                rgbaData[i * 4 + 3] = 255;
            }

            // Send back the buffer
            self.postMessage({
                status: 'success',
                id: id,
                width: width,
                height: height,
                buffer: rgbaData.buffer
            }, [rgbaData.buffer]); // Transferable

        } catch (err) {
            console.error("Worker Error:", err);
            self.postMessage({ status: 'error', id: id, error: err.message });
        }
    }
};
