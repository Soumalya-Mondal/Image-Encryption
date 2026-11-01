# Define "image_convert" Function
def image_convert(images_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import subprocess
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '1', 'message': str(error)}

    # Define Folder Path:S2
    try:
        parent_folder_path = Path.cwd()
        tmp_folder_path = Path(parent_folder_path) / 'tmp'
        converted_images_folder_path = Path(tmp_folder_path) / 'ConvertedImages'
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

    # Creating Path Object And Check If "images" Folder Is Present:S4
    try:
        images_folder_path_object = Path(images_folder_path)
        if not (images_folder_path_object.exists() and images_folder_path_object.is_dir()):
            return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '4', 'message': f'"{images_folder_path_object.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '4', 'message': str(error)}

    # Create Input Image File Path List:S5
    try:
        input_images_file_path_list = sorted(
            file_path for file_path in images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() in ('.heic', '.jpg', '.png')
        )
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '5', 'message': str(error)}

    # Create Input Image File Path Dictionary By Creation Date:S6
    try:
        input_images_file_path_date_wise_dictionary = {
            f'{image_number:05d}': file_path
            for image_number, file_path in enumerate(
                sorted(
                    input_images_file_path_list,
                    key = lambda file_path: float(getattr(file_path.stat(), 'st_birthtime', file_path.stat().st_ctime))
                ),
                start = 1
            )
        }
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '6', 'message': str(error)}

    # Convert Input Images To "*.JPG" Format:S7
    try:
        for image_key, input_image_file_path in input_images_file_path_date_wise_dictionary.items():
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
            print(f'{image_key}-> "{input_image_file_path.name}" Converted To "{converted_image_file_path.name}"')
    except subprocess.CalledProcessError as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '7', 'message': f'FFmpeg Failed To Convert "{input_image_file_path.name}"'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '7', 'message': str(error)}

    # Empty "images" Folder:S8
    try:
        for input_item_path in images_folder_path_object.iterdir():
            if input_item_path.is_dir():
                shutil.rmtree(input_item_path)
            else:
                input_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '8', 'message': str(error)}

    # Return Success:S9
    return {'status': 'SUCCESS', 'file_name': 'Image-Convert', 'step': '9', 'message': 'All The Images Converted To JPG Successfully'}