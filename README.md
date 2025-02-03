# Image Resizing with Bilinear and Bicubic Interpolation

This project demonstrates image resizing using two common interpolation algorithms: bilinear and bicubic. It was developed as part of a numerical programming course and showcases the differences in image quality and computational cost between the two methods.

## Introduction

Image resizing is a fundamental operation in image processing. Interpolation algorithms are used to estimate pixel values when upscaling or downscaling an image. This project implements and compares two popular interpolation methods:

*   **Bilinear Interpolation:** A relatively fast method that uses a weighted average of the four nearest pixels. It's suitable for small-scale resizing but can introduce blurriness and artifacts with repeated resizing or large-scale enlargements.
*   **Bicubic Interpolation:** A more computationally intensive method that uses a 4x4 neighborhood of pixels and a cubic function for approximation. It produces smoother results than bilinear, especially for larger resizes, but it's slower.

## Project Structure

*   **`bicubic.py`:** Contains the implementation of the bicubic interpolation algorithm, along with code to run resizing cycles and calculate error metrics.
*   **`bilinear.py`:**  Contains the implementation of the bilinear interpolation algorithm, with similar functionality to `bicubic.py`.
*   **`compare_all_interpolations.py`:** Allows for an interactive visual comparison of the original image, bilinear resized image, and bicubic resized image.
*   **`input_images/`:**  A directory containing the original images used for testing.
*   **`output_images/`:**  A directory where the resized images will be saved.

## Getting Started

### Prerequisites

*   Python 3.x
*   Required libraries:
    ```bash
    pip install numpy matplotlib pillow
    ```

### Running the Code

1. **Clone the Repository:**

    ```bash
    git clone <your-github-repository-url>
    cd image-resizing-interpolation
    ```

2. **Run `bicubic.py` or `bilinear.py`:**

    *   To test resizing with either method and see error metrics (MAE, RMSE, L2 Norm).
    *   You can modify the `num_cycles` and `new_width` variables at the bottom of each file to experiment.
    *   The code will display the original and resized images.
    *   For example,
    ```bash
    python bicubic.py
    python bilinear.py
    ```

3. **Run `compare_all_interpolations.py`:**

    *   This script provides an interactive comparison.
    *   After running the code, you'll see the original image. Press the following keys to switch views:
        *   **1:** Original Image
        *   **2:** Bilinear Resized Image
        *   **3:** Bicubic Resized Image
        *   For example,
            ```bash
            python compare_all_interpolations.py
            ```

## Experiment Results

The project includes examples of resizing an image of clouds and a test image with distinct color blocks using both methods over 100 cycles (resizing to a larger size and then back to the original size repeatedly).

**Observations:**

*   The cloud image demonstrates that repeated resizing with either method leads to degradation, but bicubic interpolation preserves more detail.
*   The color block image highlights that degradation is more pronounced at color boundaries. Regions with uniform color are less affected.

Error metrics (MAE, RMSE, L2 Norm) are calculated and printed in the console when running `bicubic.py` and `bilinear.py`. These metrics provide a quantitative measure of the difference between the original and resized images.

**Example using `2nabiji.png` and comparison:**

\[Insert here two images from your provided files: “Original Image vs. After 100 Cycles” - for Clouds and for distinct colors.]

It can be seen that on image with distinct colors the degradation is not as much visible as on clouds image. This occurs because the interpolation algorithms calculates changes between pixels and when there are large number of distinct colors image tends to keep the initial quality better.

The example images of numbers (original, bilinear, bicubic) also demonstrate the differences in sharpness and smoothness between the two methods, where bicubic interpolation generally produces smoother edges and curves.

**Example using `2nabiji.png` of number and comparison:**

\[Insert here 3 images from your provided files: original, bilinear, and bicubic, and then press `2` and `3` buttons to see the difference as you suggested before]

You may find difficult to see a huge difference between bilinear and bicubic methods, however, if you run a comparison file and press buttons `2` (for bilinear) and `3` (for bicubic) it can be observed that bicubic interpolation creates a smoother and more aesthetically pleasing result.

## Conclusion

Bicubic interpolation generally provides better visual quality than bilinear interpolation, especially for significant resizing or when smoothness is important. However, it is more computationally demanding. The choice between the two depends on the specific application's requirements for quality and speed.
