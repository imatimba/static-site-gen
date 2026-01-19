import os
import shutil


def copy_static_files(static_dir, output_dir):
    try:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    except Exception as e:
        raise ValueError(e)

    if os.path.exists(static_dir):
        contents = os.listdir(static_dir)
        for item in contents:
            src_path = os.path.join(static_dir, item)
            dest_path = os.path.join(output_dir, item)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
            else:
                os.mkdir(dest_path)
                copy_static_files(src_path, dest_path)
    else:
        raise ValueError(f"Static directory does not exist: {static_dir}")
