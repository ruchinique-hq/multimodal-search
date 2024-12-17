import os
import subprocess

def video_to_frames(video_path, output_path):
    try:
        os.makedirs(output_path, exist_ok=True)

        command = [
            'ffmpeg',
            '-i', video_path,  # input video file
            '-q:v', '2',  # quality of the output frames (lower is better quality, 2 is a good balance)
            '-start_number', str(0),  # start numbering from
            os.path.join(output_path, '%05d.jpg')  # output path with filename pattern for frames
        ]

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"video converted to frames successfully {output_path}")

    except subprocess.CalledProcessError as e:
        print(f'failed to convert to frames {video_path} {e.__str__()}')
        return False

    return True

video_to_frames("./data/sample.mp4", "./data/frames")
print("process completed")
