from moviepy.editor import *

video1 = VideoFileClip("E:/data/央视配音24fs/我爱爆米花.mp4")
video2 = VideoFileClip("E:/data/央视配音24fs/我爱爆米花(2).mp4")

video1_audio = video1.audio
final_video = video2.set_audio(video1_audio)

final_video.write_videofile("output.mp4", codec='libx264', audio_codec='aac')
