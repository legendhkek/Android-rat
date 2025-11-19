#!/usr/bin/env python3
"""
Generate APK Modifier icons for all resolutions
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'Pillow'])
    from PIL import Image, ImageDraw, ImageFont
    import os

def create_apk_modifier_icon(size):
    """Create an APK Modifier icon"""
    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background (purple to blue)
    for y in range(size):
        # Gradient from #6366F1 to #8B5CF6
        ratio = y / size
        r = int(99 + (139 - 99) * ratio)
        g = int(102 + (92 - 102) * ratio)
        b = int(241 + (246 - 241) * ratio)
        draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b, 255))
    
    # Draw rounded rectangle for modern look
    margin = int(size * 0.1)
    corner_radius = int(size * 0.15)
    
    # Draw APK box shape
    box_margin = int(size * 0.2)
    box_size = size - 2 * box_margin
    
    # Draw hexagon (APK shape)
    points = []
    center_x = size // 2
    center_y = size // 2
    radius = size // 3
    
    for i in range(6):
        angle = 3.14159 / 3 * i
        x = center_x + radius * (1 if i % 2 == 0 else 0.866) * (1 if i < 3 else -1)
        y = center_y + radius * (0.5 if i % 2 == 0 else 0) * (1 if i in [1, 2] else -1)
        if i == 0:
            x = center_x
            y = center_y - radius
        elif i == 1:
            x = center_x + int(radius * 0.866)
            y = center_y - int(radius * 0.5)
        elif i == 2:
            x = center_x + int(radius * 0.866)
            y = center_y + int(radius * 0.5)
        elif i == 3:
            x = center_x
            y = center_y + radius
        elif i == 4:
            x = center_x - int(radius * 0.866)
            y = center_y + int(radius * 0.5)
        elif i == 5:
            x = center_x - int(radius * 0.866)
            y = center_y - int(radius * 0.5)
        points.append((x, y))
    
    # Draw hexagon outline
    draw.polygon(points, outline=(255, 255, 255, 255), width=max(2, size//40))
    
    # Draw "A" letter for APK
    font_size = int(size * 0.35)
    try:
        # Try to use a bold font if available
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw "A" text
    text = "A"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - int(size * 0.05)
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Draw small wrench/tool icon in corner
    tool_size = int(size * 0.15)
    tool_x = size - tool_size - int(size * 0.15)
    tool_y = size - tool_size - int(size * 0.15)
    
    # Draw checkmark or tool symbol
    draw.ellipse([(tool_x, tool_y), (tool_x + tool_size, tool_y + tool_size)], 
                 fill=(16, 185, 129, 255))
    
    # Draw checkmark
    check_points = [
        (tool_x + tool_size * 0.3, tool_y + tool_size * 0.5),
        (tool_x + tool_size * 0.45, tool_y + tool_size * 0.65),
        (tool_x + tool_size * 0.7, tool_y + tool_size * 0.35)
    ]
    draw.line(check_points, fill=(255, 255, 255, 255), width=max(2, size//60))
    
    return img

def generate_all_icons():
    """Generate icons for all Android resolutions"""
    sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    base_path = 'android-app/app/src/main/res'
    
    for density, size in sizes.items():
        output_dir = f'{base_path}/mipmap-{density}'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate launcher icon
        icon = create_apk_modifier_icon(size)
        icon.save(f'{output_dir}/ic_launcher.png', 'PNG')
        print(f'✓ Generated {density} launcher icon ({size}x{size})')
        
        # Generate round icon
        round_icon = create_apk_modifier_icon(size)
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), (size, size)], fill=255)
        
        # Apply mask
        round_icon.putalpha(mask)
        round_icon.save(f'{output_dir}/ic_launcher_round.png', 'PNG')
        print(f'✓ Generated {density} round icon ({size}x{size})')

if __name__ == '__main__':
    print("Generating APK Modifier icons...")
    print("=" * 50)
    generate_all_icons()
    print("=" * 50)
    print("✓ All icons generated successfully!")
