from handle_input import handle_input

import concurrent.futures


def process_frames_batch(frames_batch, one_frame_func):
    return [one_frame_func(frame) for frame in frames_batch]


def map_video(input_object, process_func, num_threads=4, subclip_bounds=()):
    video = handle_input(input_object, num_threads, subclip_bounds)

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_num in range(num_threads - 1):
            frames_batch = video.get_batch(thread_num)
            futures.append(executor.submit(process_frames_batch, frames_batch, process_func))

        last_batch = video.get_last_batch()
        if last_batch != None:
            futures.append(
                executor.submit(process_frames_batch, video.get_last_batch(), process_func))

    result_list = []
    for result_batch in futures:
        for result_frame in result_batch.result():
            result_list.append(result_frame)
    return result_list
