import os
import zipfile
from dotenv import load_dotenv

def rename_frames_in_order(directory, padding=5, extension=".jpg"):
    files = [f for f in os.listdir(directory) if f.lower().endswith(extension)]
    files.sort()

    for idx, filename in enumerate(files, 1):
        new_name = f"{str(idx).zfill(padding)}{extension}"
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)
        if src != dst:
            os.rename(src, dst)
            print(f"Renamed {filename} -> {new_name}")

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Zipped folder to {zip_path}")

if __name__ == "__main__":
    raw_dir = os.path.join(os.path.dirname(__file__), "RAW")
    rename_frames_in_order(raw_dir)
    if "VIDEO_NAME" not in os.environ:
        load_dotenv()
    video_name = os.environ.get("VIDEO_NAME")
    zip_path = os.path.join(os.path.dirname(__file__), f"{video_name}.zip")
    zip_folder(raw_dir, zip_path)
