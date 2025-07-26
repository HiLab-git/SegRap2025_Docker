import os
import time
import numpy as np
import SimpleITK as sitk

INPUT_PATH = "/input"  # these are the paths that Docker will use
OUTPUT_PATH = "/output"
RESOURCE_PATH = "resources"


def run():
    """
    predict all cases
    """
    _show_torch_cuda_info()

    ### 1. Get paths of images
    files_lst = [
        os.path.join(INPUT_PATH, i)
        for i in os.listdir(INPUT_PATH)
        if i.endswith(".nii.gz")
    ]

    ### 2. initialize you model or some other utils here

    ### 3. predict case by case
    for img_path in files_lst:
        # Convenient to check inference time during debugging
        start = time.time()

        img_obj = sitk.ReadImage(img_path)
        seg_obj = generate_segmentation(img_obj)

        save_path = img_path.replace(INPUT_PATH, OUTPUT_PATH).replace(
            "_0000.nii.gz", ".nii.gz"
        )
        write_segmentation(seg_obj, save_path)

        end = time.time()
        print("Predict: {} Cost: {}s".format(img_path, end - start))


def generate_segmentation(image: sitk.Image):
    """
    A simple example. You can preprocess image, infer with model and postpreprocess prediction here.
    """
    # Get image properties, original .GetSpacing() and .GetSize() are in x, y, z
    spacing = image.GetSpacing()[::-1]

    # Convert image to numpy array for manipulation
    image_array = sitk.GetArrayFromImage(image)
    segmentation = np.zeros_like(image_array).astype(np.uint8)
    size = segmentation.shape

    # Calculate the center of the image
    center = np.array(size) // 2

    # Calculate the size of the cube in voxels (50 mm all around)
    GTVp_bbox_size = (50.0 / np.array(spacing)).astype(int)

    # Define the region for the approximate position of GTVp
    GTVp_bbmin = center - GTVp_bbox_size // 2
    GTVp_bbmax = GTVp_bbmin + GTVp_bbox_size
    GTVp_bbmin[0] = GTVp_bbmax[0]
    GTVp_bbmax[0] = GTVp_bbmin[0] + GTVp_bbox_size[0]

    # Ensure the cube is within bounds
    GTVp_bbmin = np.maximum(GTVp_bbmin, 0)
    GTVp_bbmax = np.minimum(GTVp_bbmax, np.array(size))

    # Create the central cube of GTVp
    segmentation[
        GTVp_bbmin[0] : GTVp_bbmax[0],
        GTVp_bbmin[1] : GTVp_bbmax[1],
        GTVp_bbmin[2] : GTVp_bbmax[2],
    ] = 1

    # Convert the numpy array back to a SimpleITK image
    segmentation_obj = sitk.GetImageFromArray(segmentation)
    segmentation_obj.CopyInformation(image)

    return segmentation_obj


def write_segmentation(segmentation, path):
    segmentation = sitk.Cast(segmentation, sitk.sitkUInt8)
    sitk.WriteImage(segmentation, path, useCompression=True)


def _show_torch_cuda_info():
    import torch

    print("+" * 30)
    print("Collecting Torch CUDA information")
    available = torch.cuda.is_available()
    print(f"Torch CUDA is available: {available}")
    if available:
        print(f"\tnumber of devices: {torch.cuda.device_count()}")
        current_device = torch.cuda.current_device()
        print(f"\tcurrent device: {current_device}")
        print(f"\tproperties: {torch.cuda.get_device_properties(current_device)}")
    print("+" * 30)


if __name__ == "__main__":
    run()
