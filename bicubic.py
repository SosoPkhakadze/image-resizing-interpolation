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

def bicubic(img, new_width, a=-0.5):
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

image = Image.open('2nabiji.png').convert('RGB')
image_array = np.array(image)

num_cycles = 0
new_width = 1000

if num_cycles == 0:
    final_image_array = bicubic(image_array, new_width)
else:
    current_image_array = image_array.copy()
    for i in range(num_cycles):
        current_image_array = bicubic(current_image_array, new_width)
        current_image_array = bicubic(current_image_array, image_array.shape[1])

    final_image_array = current_image_array

    absolute_error_final = np.abs(image_array - final_image_array)
    mean_absolute_error_final = np.mean(absolute_error_final)
    rmse_final = np.sqrt(np.mean((image_array - final_image_array) ** 2))
    l2_norm_error_final = np.linalg.norm(image_array - final_image_array)

    final_image_array = bicubic(current_image_array, new_width)

    print(f"Mean Absolute Error (MAE): {mean_absolute_error_final:.2f}")
    print(f"Root Mean Square Error (RMSE): {rmse_final:.2f}")
    print(f"L2 Norm Error: {l2_norm_error_final:.2f}")

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(image_array)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(final_image_array)
plt.title(f'After {num_cycles} Cycles' if num_cycles > 0 else 'Bicubic Resized Image')
plt.axis('off')

plt.show()
