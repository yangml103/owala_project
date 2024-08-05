import json

# This script extracts the unique dominant colors from the dominant_colors.json file
# and saves them to a new file called unique_dominant_colors.json

def get_unique_dominant_colors(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract dominant colors along with image URL and product name
        dominant_colors = {}
        for item in data:
            color = tuple(item['dominant_color'])
            if color not in dominant_colors:
                dominant_colors[color] = {
                    'image_url': item['image_url'],
                    'product_name': item['product_name']
                }
        
        return dominant_colors
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def save_unique_colors_to_file(colors, output_file_path):
    try:
        # Convert tuple keys to strings
        colors_str_keys = {str(k): v for k, v in colors.items()}
        
        with open(output_file_path, 'w') as file:
            json.dump(colors_str_keys, file, indent=4)
        print(f"Unique colors saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# ... existing code ...

if __name__ == "__main__":
    input_file_path = '../front_end/dominant_colors.json'
    output_file_path = '../front_end/unique_dominant_colors.json'
    
    unique_colors = get_unique_dominant_colors(input_file_path)
    save_unique_colors_to_file(unique_colors, output_file_path)
    print("Unique Dominant Colors:", unique_colors)