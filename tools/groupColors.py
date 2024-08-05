import json
import math
import webcolors

# Function to calculate the Euclidean distance between two colors
def color_distance(color1, color2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

# Function to check if two colors are similar based on a threshold
def is_similar_color(color1, color2, threshold=50):
    return color_distance(color1, color2) < threshold

def load_colors_from_file(file_path):
    with open(file_path, 'r') as file:
        colors = json.load(file)
    return colors

def closest_color(requested_color, color_list):
    min_distance = float('inf')
    closest_color = None
    
    for color in color_list:
        distance = color_distance(requested_color, color)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    
    return closest_color

def group_similar_colors(unique_dominant_colors):
    grouped_colors = {}
    
    for color in unique_dominant_colors:
        found_group = False
        for group_name, group_colors in grouped_colors.items():
            if any(is_similar_color(color, group_color) for group_color in group_colors):
                group_colors.append(color)
                found_group = True
                break
        if not found_group:
            closest = closest_color(color, unique_dominant_colors)
            grouped_colors[tuple(closest)] = [color]  # Convert list to tuple
    
    return grouped_colors

def save_grouped_colors_to_file(grouped_colors, file_path):
    def closest_color_name(requested_color):
        min_distance = float('inf')
        closest_name = None
        
        for name in webcolors.CSS3:
            hex_color = webcolors.html5_parse_legacy_color(name)
            hex_color = webcolors.hex_to_rgb(hex_color)
            r, g, b = hex_color
            distance = color_distance(requested_color, (r, g, b))
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        return closest_name

    # Convert tuple keys to closest color names
    grouped_colors_str_keys = {closest_color_name(k): v for k, v in grouped_colors.items()}
    
    with open(file_path, 'w') as file:
        json.dump(grouped_colors_str_keys, file)



# Load colors from file
file_path = '../front_end/unique_dominant_colors.json'
unique_dominant_colors = load_colors_from_file(file_path)

# Group similar colors
grouped_colors = group_similar_colors(unique_dominant_colors)

# Save grouped colors to file
output_file_path = 'grouped_colors.json'
save_grouped_colors_to_file(grouped_colors, output_file_path)

print(f"Grouped colors saved to {output_file_path}")