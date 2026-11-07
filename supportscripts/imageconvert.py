# Define "image_convert" Function
def image_convert(database_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import subprocess
        import sqlite3
        import hashlib
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '1', 'message': str(error)}

    # Define Folder Path:S2
    try:
        parent_folder_path = Path.cwd()
        database_folder_path_object = Path(database_folder_path)
        image_encryption_database_file_path = database_folder_path_object / 'ImageEncryption.db'
        tmp_folder_path = parent_folder_path / 'tmp'
        converted_images_folder_path = tmp_folder_path / 'ConvertedImages'
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '2', 'message': str(error)}

    # Recreate "tmp" And "ConvertedImages" Folders:S3
    try:
        if tmp_folder_path.exists() and tmp_folder_path.is_dir():
            shutil.rmtree(tmp_folder_path)
        tmp_folder_path.mkdir(parents = True, exist_ok = True)
        converted_images_folder_path.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '3', 'message': str(error)}

    # Fetch Raw Image Details From Database:S4
    try:
        with sqlite3.connect(str(image_encryption_database_file_path)) as db_connection:
            db_connection.row_factory = sqlite3.Row
            db_cursor = db_connection.cursor()
            raw_images_details_rows = db_cursor.execute(
                'SELECT file_id, file_path FROM raw_images_details ORDER BY id'
            ).fetchall()
        if not raw_images_details_rows:
            return {'status': 'INFO', 'file_name': 'Image-Convert', 'step': '4', 'message': 'No Raw Image Details Found In Database'}
        input_images_file_path_list = [Path(row['file_path']) for row in raw_images_details_rows]
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '4', 'message': str(error)}

    # Convert Input Images To "*.JPG" Format:S5
    try:
        converted_images_details_nested_list = []
        for image_number, input_image_file_path in enumerate(input_images_file_path_list, start = 1):
            image_key = f'{image_number:05d}'
            converted_image_file_path = Path(converted_images_folder_path) / f'img{image_key}.jpg'
            ffmpeg_command = [
                'ffmpeg',
                '-y',
                '-i', str(input_image_file_path),
                '-q:v', '1',
                '-qmin', '1',
                '-qmax', '1',
                '-pix_fmt', 'yuvj444p',
                str(converted_image_file_path)
            ]
            subprocess.run(ffmpeg_command, check = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            raw_file_id = raw_images_details_rows[image_number - 1]['file_id']
            file_name = converted_image_file_path.name
            file_size_bytes = converted_image_file_path.stat().st_size
            file_hash = hashlib.sha256(converted_image_file_path.read_bytes()).hexdigest()
            converted_images_details_nested_list.append(
                (raw_file_id, file_name, file_size_bytes, file_hash)
            )
            print(f'{image_key}-> "{input_image_file_path.name}" Converted To "{file_name}"')
    except subprocess.CalledProcessError as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '5', 'message': f'FFmpeg Failed To Convert "{input_image_file_path.name}"'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '5', 'message': str(error)}

    # Insert Converted Image Details Into Database:S6
    try:
        with sqlite3.connect(str(image_encryption_database_file_path)) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.executemany('''
                INSERT INTO converted_images_details (raw_file_id, file_name, file_size_bytes, file_hash)
                VALUES (?, ?, ?, ?)
            ''', converted_images_details_nested_list)
            db_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '6', 'message': str(error)}

    # Return Success:S7
    return {'status': 'SUCCESS', 'file_name': 'Image-Convert', 'step': '7', 'message': 'All The Images Converted To JPG Successfully'}