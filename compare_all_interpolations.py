import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def u(s, a=-0.5):
    s = abs(s)
    if s <= 1:
        return (a + 2) * s**3 - (a + 3) * s**2 + 1
    elif s < 2:
        return a * s**3 - 5 * a * s**2 + 8 * a * s - 4 * a
    return 0

def padding(img, H, W, C):
    zimg = np.zeros((H+4, W+4, C))
    zimg[2:H+2, 2:W+2, :] = img

    zimg[2:H+2, 0:2] = img[:, 0:1]
    zimg[2:H+2, W+2:W+4] = img[:, W-1:W]
    
    zimg[0:2, 2:W+2] = img[0:1, :]
    zimg[H+2:H+4, 2:W+2] = img[H-1:H, :]

    zimg[0:2, 0:2] = img[0, 0]
    zimg[H+2:H+4, 0:2] = img[H-1, 0]
    zimg[0:2, W+2:W+4] = img[0, W-1]
    zimg[H+2:H+4, W+2:W+4] = img[H-1, W-1]
    return zimg

def bicubic(img, new_width, a=-1/2):
    H, W, C = img.shape
    aspect_ratio = H / W
    new_height = int(new_width * aspect_ratio)

    img = padding(img, H, W, C)
    result = np.zeros((new_height, new_width, C))

    h_x = W / new_width
    h_y = H / new_height

    for c in range(C):
        for i in range(new_height):
            for j in range(new_width):
                x = j * h_x + 2
                y = i * h_y + 2

                x_floor = int(np.floor(x))
                y_floor = int(np.floor(y))

                x_diff = x - x_floor
                y_diff = y - y_floor

                wx = [u(x_diff + 1, a), u(x_diff, a), u(1 - x_diff, a), u(2 - x_diff, a)]
                wy = [u(y_diff + 1, a), u(y_diff, a), u(1 - y_diff, a), u(2 - y_diff, a)]

                mat_m = img[y_floor - 1: y_floor + 3, x_floor - 1: x_floor + 3, c]

                result[i, j, c] = np.dot(np.dot(wy, mat_m), wx)

    return np.clip(result, 0, 255).astype(np.uint8)


def bi_interpolation(arr, x, y):
    height, width = arr.shape
    x1 = np.floor(x).astype(int)
    y1 = np.floor(y).astype(int)
    x2 = np.clip(x1 + 1, 0, width - 1)
    y2 = np.clip(y1 + 1, 0, height - 1)

    p11 = arr[y1, x1]
    p12 = arr[y2, x1]
    p21 = arr[y1, x2]
    p22 = arr[y2, x2]

    x_diff = x - x1
    y_diff = y - y1

    interpolated = (p11 * (1 - x_diff) * (1 - y_diff) +
                   p21 * x_diff * (1 - y_diff) +
                   p12 * (1 - x_diff) * y_diff +
                   p22 * x_diff * y_diff)

    return interpolated

def resize_image_aspect_ratio(image, new_width, new_height=None):
    original_height, original_width, num_channels = image.shape
    aspect_ratio = original_height / original_width

    if new_height is None:
        new_height = int(new_width * aspect_ratio)

    resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)

    x_ratio = original_width / new_width
    y_ratio = original_height / new_height

    x = np.arange(new_width) * x_ratio
    y = np.arange(new_height) * y_ratio

    x_grid, y_grid = np.meshgrid(x, y)

    for c in range(num_channels):
        resized_image[..., c] = bi_interpolation(image[..., c], x_grid, y_grid)

    return resized_image    

def show_images(event):
    if event.key == '1':
        plt.clf()
        plt.imshow(image_array)
        plt.title('Original Image')
        plt.axis('off')
    elif event.key == '2':
        plt.clf()
        plt.imshow(bilinear_result)
        plt.title('Bilinear Interpolation')
        plt.axis('off')
    elif event.key == '3':
        plt.clf()
        plt.imshow(bicubic_result)
        plt.title('Bicubic Interpolation')
        plt.axis('off')
    plt.draw()

try:
    image = Image.open('2nabiji.png').convert('RGB')
    image_array = np.array(image)

    new_width = 1000
    bilinear_result = resize_image_aspect_ratio(image_array, new_width)

    bicubic_result = bicubic(image_array, new_width, a=-1/2)

    plt.figure(figsize=(8, 8))
    plt.imshow(image_array)
    plt.title('Original Image (Press 1, 2, or 3 to switch views)')
    plt.axis('off')

    plt.gcf().canvas.mpl_connect('key_press_event', show_images)
    plt.show()
    
except FileNotFoundError:
    print("Error: Image file not found")
except Exception as e:
    print(f"An error occurred: {str(e)}")