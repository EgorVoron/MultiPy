# MultiPy
A python package for easy video processing with multithreading, based on concurrent package.

### Dependencies
* Python3 >= 3.6
* [Moviepy](https://github.com/Zulko/moviepy)
* [NumPy](https://github.com/numpy/numpy)

### Example
```
from multipy import map_video
import cv2

def resize(x):
    return cv2.resize(x, (256, 256))

result = map_video('video.mp4',
                       resize,
                       num_threads=5, 
                       subclip_bounds=(1, 5))  # return list of resized frames from subclip of video
```