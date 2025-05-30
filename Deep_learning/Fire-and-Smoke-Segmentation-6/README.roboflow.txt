
Fire and Smoke Segmentation - v6 2025-04-09 4:59pm
==============================

This dataset was exported via roboflow.com on April 10, 2025 at 3:12 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 7110 images.
Fire-smoke are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 50 versions of each source image:
* 50% probability of horizontal flip
* Randomly crop between 0 and 15 percent of the image
* Random rotation of between -12 and +12 degrees
* Random shear of between -3° to +3° horizontally and -3° to +3° vertically
* Random brigthness adjustment of between -20 and +20 percent
* Random exposure adjustment of between -12 and +12 percent
* Random Gaussian blur of between 0 and 0.5 pixels
* Salt and pepper noise was applied to 1 percent of pixels


