# Monocular Vision based Collision Avoidance fusing Deep Neural Network with feature recognition algorithms

Retrieving accurate 3D position and velocity information of objects from a monocular video can potentially be used for obstacle detection and collision avoidance.
Todo so, a video is processed with the help of a segmentation network called Mask R-CNN which detects the objects and produces segmentation masks.
These masks are later on used to track objects across multiple video frames with one of three feature description algorithms: SIFT, SURF and ORB.
Experiments show that while the system is not yet real-time capable, it produces fairly accurate data.


### Examples (click of the gifs to get to a higher quality video): 
[![Example video 1](./../images/images/example_1.gif?raw=true)](https://youtu.be/LYG21iKl7QE)
Scenario 1: Static camera with moving objects

[![Example video 1](./../images/images/example_2.gif?raw=true)](https://youtu.be/ayhgmKT8KWM)
Scenario 2: Dynamic camera with moving objects. Significant camera shake poses problems to object tracking.

[![Example video 1](./../images/images/example_3.gif?raw=true)](https://youtu.be/tHlel_Hwfm0)
Scenario 3: Dynamic camera with static objects. The shape of the chair presents challenges to the segmentation network. 

The red arrows are the object's predicted trajectory.
The faint green rectangles in the middle of the objects represents the uncertainty of the Kalman Filter at that step.
One can see that it shrinks the longer an object is tracked successfully.


### Usage:

Input parameters can be specified as command line arguments. 
Example: 
```bash
data/video/IMG_5823.mov --from 0 --to 2 --matcherType ORB --inputDimensions 640 360 --inputScale 0.1666
```
This will analyze the first two seconds from the input video `data/video/IMG_5823.mov` with the Orb matcher. 
The inputs dimensions are 640x360 which is 1/6th of the original size.

##### Full list of arguments:
 - `input`: Video file or directory of images to be processed
 - `from`: From video second or image number (default: 0)
 - `to`: To video second or image number (default: None, end of the video)
 - `inputType`: Input type can be a VIDEO or a directory with IMAGEs (default: VIDEO)
 - `inputDimensions`: Input dimensions for video or image series
 - `inputScale`: Scale compared to original video (e.g. 0.5) (default: 1)
 - `matcherType`: Matcher type can be SIFT, SURF or ORB (default: SIFT)
 - `cameraType`: Camera type can be IPHONE_XR_4K_60, IPHONE_8_PLUS_4K_60 or FL2_14S3C_C (default: IPHONE_XR_4K_60)
 - `inputFps`: Fps of input video (default: 60)
 - `outputFps`: Fps of output video (default: 10)


### Requirements:
- This project requires Python 3.7 as it makes use of the new [Data Classes](https://docs.python.org/3/library/dataclasses.html) but Keras/Tensorflow do not support python 3.8 yet.
- This repository uses [Git LFS](https://git-lfs.github.com) to store the large weights files.
- The python dependencies are listed in the requirements.txt.