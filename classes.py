import os
from moviepy.editor import VideoFileClip


class Wrapper:
    def get_batch(self, *args):
        return []

    def get_last_batch(self, *args):
        return []


class VideoFileClipWrapper(Wrapper):
    def __init__(self, video, num_threads, subclip_bounds=()):
        self.video = video.subclip(subclip_bounds[0], subclip_bounds[1]) if subclip_bounds else video
        self.fps = self.video.fps
        self.duration = self.video.duration
        self.batch_len = int(self.duration * self.fps)
        self.num_threads = num_threads

    def get_batch(self, thread_num):
        idx_bounds = (thread_num * self.batch_len, (thread_num + 1) * self.batch_len)
        time_bounds = (idx_bounds[0] / self.fps, idx_bounds[1] / self.fps)
        batch = []
        time_code = time_bounds[0]
        while time_code <= time_bounds[1]:
            batch.append(self.video.get_frame(time_code))
            time_code += 1 / self.fps
        return batch

    def get_last_batch(self):
        if self.batch_len % self.num_threads != 0:
            time_bounds = (self.batch_len * self.num_threads * self.fps, self.duration)
            batch = []
            time_code = time_bounds[0]
            while time_code <= time_bounds[1]:
                batch.append(self.video.get_frame(time_code))
                time_code += 1 / self.fps
            return batch
        else:
            return None


class ListWrapper(Wrapper):
    def __init__(self, video_list, num_threads):
        self.video = video_list
        self.frames_num = len(video_list)
        self.num_threads = num_threads
        self.batch_len = self.frames_num // self.num_threads

    def get_batch(self, thread_num):
        idx_bounds = (thread_num * self.batch_len, (thread_num + 1) * self.batch_len)
        return self.video[idx_bounds[0]: idx_bounds[1]]

    def get_last_batch(self):
        if self.batch_len % self.num_threads != 0:
            last_frames_batch = self.video[self.batch_len * self.num_threads: self.frames_num]
            return last_frames_batch
        else:
            return None


class FileWrapper(VideoFileClipWrapper):
    def __init__(self, path, num_threads, subclip_bounds=()):
        if os.path.isfile(path):
            super().__init__(VideoFileClip(path), subclip_bounds=subclip_bounds, num_threads=num_threads)
        else:
            raise ValueError(f'file path: {path} is not valid')
