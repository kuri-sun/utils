from PIL import Image, ImageOps

def process_image(input_path, output_path, size=(2000, 2000), mode="cover"):
    """
    mode:
        "cover" - Zoom & crop to fill target size, no black borders
        "fit"   - Resize to fit inside target size, keeps aspect ratio, may add padding
    """
    with Image.open(input_path) as img:
        if mode == "cover":
            # Cover mode: crop to fill target size (no black borders)
            img_ratio = img.width / img.height
            target_ratio = size[0] / size[1]

            if target_ratio > img_ratio:
                # Crop height (image is too tall)
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                img_cropped = img.crop((0, top, img.width, top + new_height))
            else:
                # Crop width (image is too wide)
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                img_cropped = img.crop((left, 0, left + new_width, img.height))

            img_resized = img_cropped.resize(size, Image.LANCZOS)

        elif mode == "fit":
            # Fit mode: maintain aspect ratio, fit inside size, add black padding if needed
            img_resized = ImageOps.pad(img, size, method=Image.LANCZOS, color=(0, 0, 0))

        else:
            raise ValueError("Invalid mode. Use 'cover' or 'fit'.")

        img_resized.save(output_path)

# Example usage:
process_image("../spongebob.png", "output_cover.jpg", mode="cover")  # Zoom + crop (no black border)
process_image("../spongebob.png", "output_fit.jpg", mode="fit")      # Resize + pad (may have black border)

