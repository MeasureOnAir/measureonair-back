from PIL import Image


def resize_image(image: Image):
    # Set the target max size of the image
    max_size = (1500, 1500)

    # Resize the image while keeping the aspect ratio
    image.thumbnail(max_size, Image.ANTIALIAS)

    return image
