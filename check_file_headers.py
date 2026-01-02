import os

def check_image_header(file_path):
    if not os.path.exists(file_path):
        return "File not found"
    
    with open(file_path, 'rb') as f:
        header = f.read(8)
        # PNG header: 89 50 4E 47 0D 0A 1A 0A
        if header == b'\x89PNG\r\n\x1a\n':
            return "Valid PNG Header"
        else:
            try:
                content = header + f.read(100)
                return f"INVALID HEADER: {content.decode('utf-8', errors='ignore')}"
            except:
                return f"INVALID HEADER: {header}"

files = [
    'media/depth_maps/depth_front_50.png',
    'media/depth_maps/depth_front_51.png',
    'media/depth_maps/depth_front_49.png',
    'media/depth_maps/depth_front_43.png' # An older one that "works"
]

for f in files:
    print(f"{f}: {check_image_header(f)}")
