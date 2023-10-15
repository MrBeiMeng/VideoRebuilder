from src.heigher_service.impl.fast_dtw_align import FastDtwAlign
from src.heigher_service.runner_interface import RunnerI

if __name__ == '__main__':
    runner: RunnerI = FastDtwAlign('E:/data/WoAiDaMaoYangShi.mp4', 'E:/data/WoAiDaMaoYangShiPianDuan.mp4')

    runner.run()
