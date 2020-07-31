from classes import VideoFileClipWrapper, ListWrapper, FileWrapper

from moviepy.editor import VideoFileClip
from numpy import ndarray


def handle_input(input_object, num_threads, subclip_bounds):
    if isinstance(input_object, VideoFileClip):
        video = VideoFileClipWrapper(input_object, num_threads, subclip_bounds=subclip_bounds)
    elif isinstance(input_object, list) or isinstance(input_object, ndarray):
        if subclip_bounds:
            raise ValueError('cannot subclip list or numpy.ndarray')
        video = ListWrapper(list(input_object), num_threads)
    elif isinstance(input_object, str):
        video = FileWrapper(input_object, num_threads, subclip_bounds=subclip_bounds)
    else:
        raise ValueError('input_object is not moviepy.VideoFileClip or list or file path or numpy.ndarray')
    return video
