import cv2
import numpy as np
from threading import Condition

from seekcamera import (
    SeekCamera,
    SeekFrame
)


class Renderer:
    """Contains camera and image data required to render images to the screen."""

    def __init__(self):
        self.busy = False
        self.frame = SeekFrame()
        self.camera = SeekCamera()
        self.frame_condition = Condition()
        self.first_frame = True


class RawVideoWriter:
    """
    Class to write raw frames to a binary file. The metadata of frame width and height, number of channels and data type
    (number of bits per channel) is not saved into the file. The user must take note of this information to be able
    to read the file in the future. The user can obtain this information with the helper function "print_frame_metadata".
    """

    def __init__(self, filename: str):
        self.f = open(filename, 'wb')

    def write(self, frame: np.ndarray):
        self.f.write(frame.tobytes())

    def release(self):
        self.f.close()

    def __del__(self):
        self.release()


def get_metadata(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2] if len(frame.shape) > 2 else 1
    dtype = frame.dtype

    return [width, height, channels, dtype]


def store_metadata(metadata, mean_fps, filename, video_count):
    with open('metadata_' + str(video_count) + '.txt', 'w+') as file:
        file.write(f'filename: {filename}\n' +
                   f'width: {metadata[0]}\n' +
                   f'height: {metadata[1]}\n' +
                   f'channels: {metadata[2]}\n' +
                   f'fps: {mean_fps}\n' +
                   f'dtype: {metadata[3]}'
                   )


def normalize(frame, choice):
    """
    Normalize an image

    :param: frame: frame we want to normalize / type: np.ndarray
    :return: norm_frame: normalized frame / type: np.ndarray
    """
    if choice == 'corrected':
        norm_frame = np.round((frame - np.min(frame)) / (np.max(frame) - np.min(frame)) * 255).astype(np.uint8)
    else:
        norm_frame = frame

    return norm_frame


def get_fps(time_init, time_new, fps_hist):
    fps = 1 / (time_new - time_init)
    fps_hist.append(fps)
    return fps_hist


def write_video(metadata, mean_fps, video_count, choice):
    filename = 'output_video_' + str(video_count)

    if choice == 'corrected':
        filename = filename + '.raw'
        vw = RawVideoWriter(filename)

    else:
        filename = filename + '.mkv'
        vw = cv2.VideoWriter(filename=filename,
                             fourcc=cv2.VideoWriter_fourcc('F','F','V','1'),
                             fps=mean_fps,
                             frameSize=(metadata[0], metadata[1]),  # Max LIR320 camera resolution.
                             isColor=False)
    return filename, vw




