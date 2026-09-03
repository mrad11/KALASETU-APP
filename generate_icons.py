import os
from PIL import Image, ImageDraw

def create_emblem(scale, maskable=False):
    S = 512 * scale
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    bg = (31, 93, 78, 255)       # #1f5d4e
    gold = (241, 197, 111, 255)  # #f1c56f
    cream = (255, 248, 232, 255) # #fff8e8

    if maskable:
        draw.rectangle([0, 0, S, S], fill=bg)
        center_x = S / 2
        center_y = S / 2
        factor = 0.82
    else:
        draw.rounded_rectangle([0, 0, S, S], radius=int(112 * scale), fill=bg)
        center_x = S / 2
        center_y = S / 2
        factor = 1.0

    def tx(x):
        return center_x + (x - 256) * scale * factor

    def ty(y):
        return center_y + (y - 256) * scale * factor

    r = 141 * scale * factor
    draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r],
                 outline=gold, width=max(1, int(22 * scale * factor)))

    draw.line([tx(256), ty(146), tx(256), ty(366)],
              fill=gold, width=max(1, int(20 * scale * factor)))

    rd = 30 * scale * factor
    draw.ellipse([center_x - rd, center_y - rd, center_x + rd, center_y + rd], fill=cream)

    def get_cubic_bezier(p0, p1, p2, p3, steps=100):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
            pts.append((tx(x), ty(y)))
        return pts

    curve_width = max(1, int(23 * scale * factor))
    top_curve = get_cubic_bezier((169, 215), (217, 173), (295, 173), (343, 215))
    draw.line(top_curve, fill=cream, width=curve_width, joint='curve')

    bot_curve = get_cubic_bezier((169, 297), (217, 339), (295, 339), (343, 297))
    draw.line(bot_curve, fill=cream, width=curve_width, joint='curve')

    return im

def main():
    scale = 4
    std_master = create_emblem(scale, maskable=False)
    mask_master = create_emblem(scale, maskable=True)

    std_master.resize((512, 512), Image.Resampling.LANCZOS).save('icon-512.png', 'PNG')
    std_master.resize((192, 192), Image.Resampling.LANCZOS).save('icon-192.png', 'PNG')
    std_master.resize((180, 180), Image.Resampling.LANCZOS).save('apple-touch-icon.png', 'PNG')

    mask_master.resize((512, 512), Image.Resampling.LANCZOS).save('icon-maskable-512.png', 'PNG')
    mask_master.resize((192, 192), Image.Resampling.LANCZOS).save('icon-maskable-192.png', 'PNG')

    std_master.save('kalasetu-icon.ico', format='ICO', sizes=[(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)])
    print("All icons successfully generated!")

if __name__ == '__main__':
    main()
