import textToSpeech from '@google-cloud/text-to-speech';
import fs from 'fs';
import util from 'util';
import path from 'path';
import { fileURLToPath } from 'url';

// --- Configuration ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const credentialsPath = path.join(__dirname, 'gcp-credentials.json');
const inputFile = path.join(__dirname, 'scripts.txt');
const outputDir = path.join(__dirname, 'static/audio');
// -------------------

// Check if credentials file exists
if (!fs.existsSync(credentialsPath)) {
    console.error(`ERROR: Google Cloud credentials file not found at ${credentialsPath}`);
    console.error('Please follow the setup instructions to create and place the file.');
    process.exit(1);
}

// Creates a client with the credentials
const client = new textToSpeech.TextToSpeechClient({
    keyFilename: credentialsPath,
});

async function generateAudio() {
    console.log('Starting audio generation process...');

    try {
        const fileContent = fs.readFileSync(inputFile, 'utf8');
        const lines = fileContent.split('\n').filter(line => line.trim() !== '');

        for (const line of lines) {
            const parts = line.split('|');
            if (parts.length !== 2) {
                console.warn(`Skipping malformed line: ${line}`);
                continue;
            }

            const [filename, text] = parts;
            const outputPath = path.join(outputDir, `${filename.trim()}.mp3`);
            
            console.log(`Generating: ${filename.trim()}.mp3`);

            const request = {
                input: { text: text.trim() },
                // See https://cloud.google.com/text-to-speech/docs/voices for more voice options
                voice: { languageCode: 'en-US', name: 'en-US-Studio-M' },
                audioConfig: { audioEncoding: 'MP3' },
            };

            const [response] = await client.synthesizeSpeech(request);
            const writeFile = util.promisify(fs.writeFile);
            await writeFile(outputPath, response.audioContent, 'binary');
            console.log(`  -> Successfully wrote to ${outputPath}`);
        }

        console.log('\nAudio generation complete.');

    } catch (error) {
        console.error('\nAn error occurred during audio generation:');
        console.error(error);
        process.exit(1);
    }
}

generateAudio(); 