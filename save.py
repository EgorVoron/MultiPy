from utils import handle_input, gen_fp

import concurrent.futures

from PIL import Image


def save_frames_batch(batch, output_path):
    for frame_idx, frame in enumerate(batch):
        pil_frame = Image.fromarray(frame)
        fp = gen_fp(output_path, frame_idx)
        pil_frame.save(fp=fp)


def save_video(input_object, output_path, num_threads=4, subclip_bounds=()):
    video = handle_input(input_object, num_threads, subclip_bounds)

    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for thread_num in range(num_threads - 1):
            frames_batch = video.get_batch(thread_num)
            futures.append(executor.submit(save_frames_batch, frames_batch, output_path))

        last_batch = video.get_last_batch()
        if list(last_batch):
            futures.append(
                executor.submit(save_frames_batch, video.get_last_batch(), output_path))
