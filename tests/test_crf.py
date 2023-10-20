import av


def get_video_bitrate(filename):
    container = av.open(filename)
    for stream in container.streams:
        if stream.type == 'video':
            return stream.bit_rate


# 使用方式
filename = 'E:/xunleiyunpan/The.Penguins.Of.Madagascar.S01E03.Haunted.Habitat.1080p.WEB-DL.AAC2.0.H.264-CtrlHD.mkv'
bitrate = get_video_bitrate(filename)
print(f'Bitrate: {bitrate} bits/s')
