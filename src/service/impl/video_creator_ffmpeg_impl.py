import ffmpeg
import numpy as np
import os

from src.service.video_creator_interface import VideoCreatorI


class VideoCreatorFfmpegImpl(VideoCreatorI):
    def __init__(self, filename: str, fps=30, frame_size=(1920, 1080), vcodec='libx264', crf=28):
        super().__init__(filename)
        self.output_filename = self._get_unique_filename(filename)

        self.temp_filename = self._get_unique_tmp_filename(self.output_filename)
        self.audio_file = filename
        self.frame_size = frame_size  # 定义视频的帧尺寸
        width, height = self.frame_size
        self.process = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}', framerate=fps)
            .output(self.temp_filename, vcodec=vcodec, crf=crf)  # crf 越低，视频质量越高，但文件大小也越大
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

    @staticmethod
    def _get_unique_tmp_filename(filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"temp__{base}({counter}){ext}"
            counter += 1
        print(f"set temp video path: {filename}")
        return filename

    @staticmethod
    def _get_unique_filename(filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}({counter}){ext}"
            counter += 1
        print(f"set output path: {filename}")
        return filename

    def write_frame(self, frame: np.ndarray):
        # 检查帧的尺寸是否匹配
        if (frame.shape[1], frame.shape[0]) != self.frame_size:
            raise ValueError(
                f"Frame size mismatch: current ({frame.shape[1], frame.shape[0]}), expected {self.frame_size}")
        self.process.stdin.write(
            frame
            .astype('uint8')
            .tobytes()
        )

    def release(self):
        self.process.stdin.close()
        self.process.wait()

        try:
            # 合并视频和音频
            video_stream = ffmpeg.input(self.temp_filename)
            audio_stream = ffmpeg.input(self.audio_file).audio
            ffmpeg.output(video_stream, audio_stream, self.output_filename, vcodec='copy', acodec='copy').run()

            # 删除临时文件
            os.remove(self.temp_filename)
        except Exception as e:
            print(f"在保存音频时发生了一些问题： {e.args}")
