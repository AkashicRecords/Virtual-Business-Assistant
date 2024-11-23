from PIL import Image, ImageDraw

def create_placeholder_icon():
    # Create a 256x256 icon
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple envelope shape
    draw.rectangle([50, 50, 206, 206], outline='blue', width=3)
    draw.line([50, 50, 128, 128], fill='blue', width=3)
    draw.line([206, 50, 128, 128], fill='blue', width=3)
    
    # Save as .ico for Windows
    image.save('gmail_assistant/resources/icon.ico', format='ICO')
    # Save as .icns for macOS
    image.save('gmail_assistant/resources/icon.icns', format='ICNS')

if __name__ == '__main__':
    create_placeholder_icon() 