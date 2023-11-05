# from moviepy.editor import *
#
# video1 = VideoFileClip("E:/data/央视配音24fs/我爱爆米花.mp4")
# video2 = VideoFileClip("E:/data/央视配音24fs/我爱爆米花(2).mp4")
#
# video1_audio = video1.audio
# final_video = video2.set_audio(video1_audio)
#
# final_video.write_videofile("output.mp4", codec='libx264', audio_codec='aac')
import ffmpeg

output_path = "E:/360MoveData/Users/MrB/Desktop/penguins_new_result/1 我爱大毛_(Gone In A Flash)(13).mp4"
b_path = "E:/data/Penguins/1 我爱大毛_(Gone In A Flash).mp4"
final_output_path = 'now_yes_6.mp4'


# video_stream = ffmpeg.input(output_path)
# audio_stream = ffmpeg.input(b_path).audio
# ffmpeg.output(video_stream, audio_stream, final_output_path, vcodec='copy', acodec='copy').run()


def get_media_duration(file_path):
    probe = ffmpeg.probe(file_path)
    duration = float(probe['format']['duration'])
    return duration


video_duration = get_media_duration(output_path)
audio_duration = get_media_duration(b_path)

speed_factor = audio_duration / video_duration

# Use the speed factor in the setpts filter
video_stream = ffmpeg.input(output_path, hwaccel='cuvid').filter('setpts', f'{speed_factor}*PTS')
audio_stream = ffmpeg.input(b_path).audio
# ffmpeg.output(video_stream, audio_stream, final_output_path, vcodec='copy', acodec='copy').run()
ffmpeg.output(video_stream, audio_stream, final_output_path, acodec='copy', vcodec='h264_nvenc').run()
