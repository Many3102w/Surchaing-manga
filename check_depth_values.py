from PIL import Image
import numpy as np

def check_depth_map(file_path):
    try:
        img = Image.open(file_path).convert('L') # Convert to grayscale
        data = np.array(img)
        min_p = np.min(data)
        max_p = np.max(data)
        avg_p = np.mean(data)
        std_p = np.std(data)
        return f"Min: {min_p}, Max: {max_p}, Avg: {avg_p:.2f}, Std: {std_p:.2f}"
    except Exception as e:
        return f"Error: {e}"

files = [
    'media/depth_maps/depth_front_50.png',
    'media/depth_maps/depth_front_51.png',
    'media/depth_maps/depth_front_49.png',
    'media/depth_maps/depth_front_43.png'
]

for f in files:
    print(f"{f}: {check_depth_map(f)}")
