from PIL import Image, ImageEnhance

def gen(img, flag_contrast, pfp_contrast):
    img = Image.open(img)
    img = img.convert('L')
    img = ImageEnhance.Contrast(img).enhance(pfp_contrast)
    tri_img = Image.open("cogs/data/INDIA.png").convert("RGB")
    tri_img = ImageEnhance.Contrast(tri_img).enhance(flag_contrast)
    tri_img = tri_img.resize((img.width, img.height))
    img.putalpha(125)
    tri_img.paste(img, (0, 0), mask=img)
    return tri_img
    # tri_img.save("tri_img_onc.png")

if __name__ == "__main__":
    gen(Image.open("test3.png"))