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
    path_dict = get_files_path()
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    ### 2. initialize you model or some other utils here or anywhere as you like

    ### 3. predict case by case
    for case in path_dict["image"].keys():
        # Convenient for participants to check whether their algorithm meet the time limit (3 mins per case).
        start = time.time()

        if path_dict["image"][case][0] is None:
            CT_obj = None
        else:
            CT_obj = sitk.ReadImage(path_dict["image"][case][0])

        if path_dict["image"][case][1] is None:
            ceCT_obj = None
        else:
            ceCT_obj = sitk.ReadImage(path_dict["image"][case][1])

        # predict
        seg_obj = generate_segmentation(CT_obj, ceCT_obj)

        # save your prediction
        save_path = os.path.join(OUTPUT_PATH, case + ".nii.gz")
        write_segmentation(seg_obj, save_path)

        end = time.time()
        print("Predict: {}, Cost: {}s".format(case, end - start))


def generate_segmentation(CT: sitk.Image, ceCT: sitk.Image):
    """
    A simple example. You can preprocess image, infer with model and postpreprocess prediction here.
    """
    print("Have CT: {}, Have ceCT: {}".format((CT is not None), (ceCT is not None)))

    if CT is not None:
        image = CT
    elif ceCT is not None:
        image = ceCT

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


def get_files_path():
    """
    I suggest not to change this function.
    path_dict = {
        "image": {
            "segrap_****": [
                "/input/Cohort1/image/segrap_****/image.nii.gz",
                "/input/Cohort1/image/segrap_****/image_contrast.nii.gz",
            ],
            "segrap_nc_****": [
                "/input/Cohort1/image/segrap_****/image.nii.gz",
                None,
            ],
            "segrap_ce_****": [
                None,
                "/input/Cohort1/image/segrap_****/image_contrast.nii.gz",
            ],
        }
    }
    """
    path_dict = {"image": dict()}
    case_lst = os.listdir(os.path.join(INPUT_PATH, "image"))
    for case in case_lst:
        if "_nc_" in case:
            path_dict["image"][case] = [
                os.path.join(INPUT_PATH, "image", case, "image.nii.gz"),
                None,
            ]
        elif "_ce_" in case:
            path_dict["image"][case] = [
                None,
                os.path.join(INPUT_PATH, "image", case, "image_contrast.nii.gz"),
            ]
        else:
            path_dict["image"][case] = [
                os.path.join(INPUT_PATH, "image", case, "image.nii.gz"),
                os.path.join(INPUT_PATH, "image", case, "image_contrast.nii.gz"),
            ]

    return path_dict


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
