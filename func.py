import concurrent.futures
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


def process_frames_batch(frames_batch, one_frame_func):
    return [one_frame_func(frame) for frame in frames_batch]


def process(input_object, process_func, num_threads=4, subclip_bounds=()):
    video = handle_input(input_object, num_threads, subclip_bounds)

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_num in range(num_threads - 1):
            frames_batch = video.get_batch(thread_num)
            futures.append(executor.submit(process_frames_batch, frames_batch, process_func))

        last_batch = video.get_last_batch()
        if list(last_batch):
            futures.append(
                executor.submit(process_frames_batch, video.get_last_batch(), process_func))

    result_list = []
    for result_batch in futures:
        for result_frame in result_batch.result():
            result_list.append(result_frame)
    return result_list


def analyse_frames_batch(frames_batch, one_frame_func, thread_num):
    output = []
    for frame_idx, frame in enumerate(frames_batch):
        output.append({'thread_num': thread_num, 'frame_idx': frame_idx, 'result': one_frame_func(frame)})
    return output


def find_all(input_object, process_func, num_threads=4, subclip_bounds=()):
    video = handle_input(input_object, num_threads, subclip_bounds)

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_num in range(num_threads - 1):
            frames_batch = video.get_batch(thread_num)
            futures.append(executor.submit(analyse_frames_batch, frames_batch, process_func, thread_num))

        last_batch = video.get_last_batch()
        if list(last_batch):
            futures.append(
                executor.submit(analyse_frames_batch, video.get_last_batch(), process_func, num_threads - 1))

        result_list = []
        for result_batch in futures:
            for result_dict in result_batch.result():
                if result_dict['result']:
                    if isinstance(video, VideoFileClipWrapper) or isinstance(video, FileWrapper):
                        result_list.append(
                            (result_dict['thread_num'] * video.batch_len + result_dict['frame_idx']) / video.fps)
                    else:
                        result_list.append(result_dict['thread_num'] * video.batch_len + result_dict['frame_idx'])
        return sorted(result_list)
