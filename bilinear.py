import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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

image = Image.open('2nabiji.png').convert('RGB')
image_array = np.array(image)

num_cycles = 100
new_width = 1000

if num_cycles == 0:
    final_image_array = resize_image_aspect_ratio(image_array, new_width)
else:
    current_image_array = image_array.copy()
    for i in range(num_cycles):
        current_image_array = resize_image_aspect_ratio(current_image_array, new_width)
        current_image_array = resize_image_aspect_ratio(current_image_array, image_array.shape[1], image_array.shape[0])
    
    final_image_array = current_image_array

    absolute_error_final = np.abs(image_array - final_image_array)
    mean_absolute_error_final = np.mean(absolute_error_final)
    rmse_final = np.sqrt(np.mean((image_array - final_image_array) ** 2))
    l2_norm_error_final = np.linalg.norm(image_array - final_image_array)

    final_image_array = resize_image_aspect_ratio(current_image_array, new_width)

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
plt.title(f'After {num_cycles} Cycles' if num_cycles > 0 else 'Resized Image')
plt.axis('off')

plt.show()
