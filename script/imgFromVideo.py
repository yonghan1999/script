import cv2
import os


def extract_frames(video_path, output_dir, interval=5):
    # 检查输出目录是否存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 获取视频的帧率（FPS）和总帧数
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps  # 视频时长（秒）

    print(f"视频总时长: {duration:.2f} 秒, 帧率: {fps} FPS")

    frame_interval = fps * interval  # 根据时间间隔计算要截取的帧的间隔

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 每隔 frame_interval 帧截取一次
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"保存 {frame_filename}")
            saved_count += 1

        frame_count += 1

    cap.release()
    print("视频帧提取完成。")


# 使用示例
video_path = 'your_video_file.mp4'
output_dir = 'extracted_frames'
extract_frames(video_path, output_dir, interval=5)  # 每隔5秒截取一张图片
