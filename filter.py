from handle_input import handle_input
from classes import VideoFileClipWrapper, FileWrapper

import concurrent.futures


def analyse_frames_batch(frames_batch, one_frame_func, thread_num):
    output = []
    for frame_idx, frame in enumerate(frames_batch):
        output.append({'thread_num': thread_num, 'frame_idx': frame_idx, 'result': one_frame_func(frame)})
    return output


def filter_video(input_object, process_func, num_threads=4, subclip_bounds=()):
    video = handle_input(input_object, num_threads, subclip_bounds)

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_num in range(num_threads - 1):
            frames_batch = video.get_batch(thread_num)
            futures.append(executor.submit(analyse_frames_batch, frames_batch, process_func, thread_num))

        last_batch = video.get_last_batch()
        if last_batch != None:
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
