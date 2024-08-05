const axios = require('axios');
const fs = require('fs');
const { JSDOM } = require('jsdom');
const path = require('path');

// URL of the webpage to fetch
const url = 'https://frankenbottle.com/gallery';

// Function to download a file
const downloadFile = async (fileUrl, outputLocationPath) => {
    const writer = fs.createWriteStream(outputLocationPath);
    const response = await axios({
        url: fileUrl,
        method: 'GET',
        responseType: 'stream'
    });

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
        writer.on('finish', resolve);
        writer.on('error', reject);
    });
};

// Fetch the webpage
axios.get(url)
    .then(async response => {
        const htmlContent = response.data;

        // Parse the HTML content
        const dom = new JSDOM(htmlContent);
        const document = dom.window.document;

        // Ensure the DOM is fully loaded
        dom.window.addEventListener('load', async () => {
            // Get the <g> element with the specified attributes
            const gElement = document.querySelector('g[id="Base"][xmlns="http://www.w3.org/2000/svg"]');

            if (gElement) {
                // Create a new HTML document with the <g> element content
                const newHtmlContent = `
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>SVG Base Element</title>
                    </head>
                    <body>
                        ${gElement.outerHTML}
                    </body>
                    </html>
                `;

                // Save the new HTML content to a file
                fs.writeFile('svgBaseElement.html', newHtmlContent, (err) => {
                    if (err) {
                        console.error('Error writing to file:', err);
                    } else {
                        console.log('SVG Base element saved to svgBaseElement.html');
                    }
                });
            } else {
                console.error('<g> element with id="Base" not found');
            }

            // Get the content of the div with id="svgContainer"
            const svgContainer = document.getElementById('svgContainer');
            if (svgContainer) {
                console.log('Content of svgContainer:', svgContainer.innerHTML);
            } else {
                console.error('Div with id="svgContainer" not found');
            }

            // Download CSS files
            const linkElements = document.querySelectorAll('link[rel="stylesheet"]');
            for (const linkElement of linkElements) {
                const cssUrl = linkElement.href;
                const cssFileName = path.basename(cssUrl);
                try {
                    await downloadFile(cssUrl, path.join(__dirname, cssFileName));
                    console.log(`CSS file downloaded: ${cssFileName}`);
                } catch (error) {
                    console.error(`Error downloading CSS file ${cssFileName}:`, error);
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching the webpage:', error);
    });