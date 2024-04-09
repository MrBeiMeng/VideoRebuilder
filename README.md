<div style="width: 100%;display: flex;justify-content: center;">
   <img src="./assets/logo.png" alt="屏幕截图 2024-03-03 173116" style="width:300px;" />
</div>



#🎬 VideoRebuilder

**📌 描述**：现在我们可以通过视频素材 **重建剪辑**。

----

### 核心功能 ✨

- [x] 重建剪辑
- [x] 去水印
- [x] 去字幕
- [x] 识别字幕

### 原理 💡

- **多进程视频读取**：使用OpenCV通过多进程技术高效读取视频到内存。
- **智能剪辑序列切分**：主进程负责切分剪辑序列，并为每个部分序列寻找最佳素材起点。
- **逐帧匹配**：通过SSIM算法计算帧之间的差异值，确定最佳匹配段【自定义匹配区域】。
- **灵活的输出格式**：可以重建剪辑并导出为PRXML文件，方便在Adobe Premiere Pro中二次编辑，或直接导出为视频文件。

### 演示 🎥

<iframe src="//player.bilibili.com/player.html?aid=1402938660&bvid=BV1Gr42147DN&cid=1499598873&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="height:560px"> </iframe>

## 如何使用 🛠

1. **安装依赖**：

   ```shell
   pip install -r requirements.txt
   ```

2. **运行VideoRebuild**：

   ```python
   runner: RunnerI = VideoRebuildFindInAImpl(素材地址,剪辑地址)
   runner.run()
   ```

## 贡献 💡

欢迎所有形式的贡献，包括但不限于新功能的建议、代码改进、文档更新等。请阅读贡献指南了解如何开始。

## 许可证 📄

本项目采用MIT许可证。更多详情请查看LICENSE文件。