import time
import numpy as np
import cv2
import argparse
import utils
import os

from seekcamera import (
    SeekCameraColorPalette,
    SeekCameraManagerEvent,
    SeekCameraFrameFormat,
    SeekCameraIOType,
    SeekCameraManager,
)


def on_frame(_camera, camera_frame, renderer):
    with renderer.frame_condition:
        if choice == 'corrected':
            renderer.frame = camera_frame.corrected
        else:
            renderer.frame = camera_frame.grayscale

        renderer.frame_condition.notify()


def on_event(camera, event_type, event_status, renderer):
    print("{}: {}".format(str(event_type), camera.chipid))

    if event_type == SeekCameraManagerEvent.CONNECT:
        if renderer.busy:
            return

        renderer.busy = True
        renderer.camera = camera
        renderer.first_frame = True
        camera.color_palette = SeekCameraColorPalette.TYRIAN
        camera.register_frame_available_callback(on_frame, renderer)

        if choice == 'corrected':
            camera.capture_session_start(SeekCameraFrameFormat.CORRECTED)
        else:
            camera.capture_session_start(SeekCameraFrameFormat.GRAYSCALE)

    elif event_type == SeekCameraManagerEvent.DISCONNECT:
        if renderer.camera == camera:
            camera.capture_session_stop()
            renderer.camera = None
            renderer.frame = None
            renderer.busy = False

    elif event_type == SeekCameraManagerEvent.ERROR:
        print("{}: {}\n".format(str(event_status), camera.chipid))

    elif event_type == SeekCameraManagerEvent.READY_TO_PAIR:
        return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-source', '-outs', required=True, type=str, help='output video root')
    parser.add_argument('--video-format', '-vf', type=str, required=True, choices=['corrected', 'grayscale'],
                        help='Video writing format, specify: {grayscale}: .mkv video / {corrected}: .raw video.')

    return vars(parser.parse_args())


def main(args):
    out_path = args['output_source']
    time_init = 0
    fps_hist = []
    video_count = 0
    record = False

    window_name = "Real Time Video - Seek Thermal"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    with SeekCameraManager(SeekCameraIOType.USB) as manager:
        renderer = utils.Renderer()
        manager.register_event_callback(on_event, renderer)

        while True:
            with renderer.frame_condition:
                if renderer.frame_condition.wait(500.0 / 1000.0):

                    time_new = time.time()
                    img = renderer.frame.data

                    if renderer.first_frame:
                        metadata = utils.get_metadata(img)
                        cv2.resizeWindow(window_name, metadata[0] * 2, metadata[1] * 2)
                        renderer.first_frame = False
                        os.chdir(out_path)

                    fps_hist = utils.get_fps(time_init, time_new, fps_hist)
                    time_init = time_new

                    if record:
                        vw.write(img)

                    norm_img = utils.normalize(img, choice)
                    cv2.imshow(window_name, norm_img)

            key = cv2.waitKey(1)
            if key == 32:
                if record:
                    record = False
                    utils.store_metadata(metadata, mean_fps, filename, video_count)
                    video_count += 1
                    print('* Video recorded *')
                    vw.release()
                else:
                    record = True
                    mean_fps = int(np.mean(fps_hist))
                    filename, vw = utils.write_video(metadata, mean_fps, video_count, choice)
            if key == 27:
                break
            if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
                break

    cv2.destroyWindow(window_name)


if __name__ == "__main__":
    args = parse_args()
    choice = args['video_format']
    main(args)
