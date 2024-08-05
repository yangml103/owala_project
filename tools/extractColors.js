// extractColors.js
const fs = require('fs');

// Read the JSON file
fs.readFile('./owala_products.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }

    // Parse the JSON data
    let parsedData;
    try {
        parsedData = JSON.parse(data);
    } catch (parseErr) {
        console.error('Error parsing JSON:', parseErr);
        return;
    }

    // Access the products array
    const products = parsedData.products;

    // Check if products is an array
    if (!Array.isArray(products)) {
        console.error('Expected an array of products');
        console.log('Parsed data:', parsedData);
        return;
    }

    // Extract color information
    const colorSet = new Set();
    products.forEach(product => {
        product.variants.forEach(variant => {
            if (variant.option1) {
                colorSet.add(variant.option1);
            }
        });
    });

    // Print the unique colors
    console.log('Unique Colors:', Array.from(colorSet));
});