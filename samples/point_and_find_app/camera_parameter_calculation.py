import numpy as np

# Function to calculate the camera matrix from FOV and image dimensions
def calculate_camera_matrix(fov_x_deg, fov_y_deg, image_width, image_height):
    # Convert FOV from degrees to radians
    fov_x_rad = np.deg2rad(fov_x_deg)
    fov_y_rad = np.deg2rad(fov_y_deg)

    # Calculate focal lengths (f_x and f_y)
    f_x = (image_width / 2) / np.tan(fov_x_rad / 2)
    f_y = (image_height / 2) / np.tan(fov_y_rad / 2)

    # Calculate principal point (c_x and c_y)
    c_x = image_width / 2
    c_y = image_height / 2

    # Construct the camera matrix K
    K = np.array([[f_x, 0, c_x],
                  [0, f_y, c_y],
                  [0, 0, 1]])

    return K

# Input parameters
fov_x_deg = 35  # Horizontal FOV in degrees
fov_y_deg = 27  # Vertical FOV in degrees
image_width = 336 # Image width in pixels
image_height = 256 # Image height in pixels
path = "./vuepro_camara_data/"

# Calculate the camera matrix
camera_matrix = calculate_camera_matrix(fov_x_deg, fov_y_deg, image_width, image_height)
distortion_coefficients = np.zeros((1, 5))

# Save the camera matrix as a .npy file
np.save(path + "calibration_matrix.npy", camera_matrix)
np.save(path + "distortion_coefficients.npy", distortion_coefficients)

print(camera_matrix)
print(distortion_coefficients)

print("Camera matrix saved as 'camera_matrix.npy'")

