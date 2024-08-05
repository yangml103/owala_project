import json
import requests
from io import BytesIO
from colorthief import ColorThief

# This program iterates through each product in the 
# owala_products.json file and gets the color for each image

# Load the JSON file
with open('../owala_products.json', 'r') as file:
    data = json.load(file)
    products = data.get('products', [])

# Function to get the dominant color from an image URL
def get_dominant_color(image_url):
    response = requests.get(image_url)
    img = BytesIO(response.content)
    color_thief = ColorThief(img)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

# List to store the results
results = []

# Iterate through each product and each variant to get the dominant color
for product in products:
    for variant in product.get('variants', []):
        featured_image = variant.get('featured_image')
        if featured_image:
            image_url = featured_image.get('src')
            if image_url:
                dominant_color = get_dominant_color(image_url)
                results.append({
                    "product_title": product['title'],
                    "variant_title": variant['title'],
                    "dominant_color": dominant_color,
                    "image_url": image_url
                })

# Save the results to a JSON file
with open('dominant_colors.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
