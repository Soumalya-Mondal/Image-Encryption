# Define "image_convert" Function
def image_convert(input_images_folder_path: str, converted_images_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import subprocess
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '1', 'message': str(error)}

    # Creating Path Object And Check Folders Are Present:S2
    try:
        input_images_folder_path_object = Path(input_images_folder_path)
        converted_images_folder_path_object = Path(converted_images_folder_path)
        for folder in (input_images_folder_path_object, converted_images_folder_path_object):
            if not (folder.exists() and folder.is_dir()):
                return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '2', 'message': f'"{folder.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '2', 'message': str(error)}

    # Empty "ConvertedImages" Folder:S3
    try:
        for output_item_path in converted_images_folder_path_object.iterdir():
            if output_item_path.is_dir():
                shutil.rmtree(output_item_path)
            else:
                output_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '3', 'message': str(error)}

    # Create Input Image File Path List:S4
    try:
        input_images_file_path_list = sorted(
            file_path for file_path in input_images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() in ('.heic', '.jpg', '.png')
        )
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '4', 'message': str(error)}

    # Create Input Image File Path Dictionary By Creation Date:S5
    try:
        input_images_file_path_dictionary = {
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
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '5', 'message': str(error)}

    # Convert Input Images To JPG Format:S6
    try:
        for image_key, input_image_file_path in input_images_file_path_dictionary.items():
            converted_image_file_path = converted_images_folder_path_object / f'img{image_key}.jpg'
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
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '6', 'message': f'FFmpeg Failed To Convert "{input_image_file_path.name}"'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Convert', 'step': '6', 'message': str(error)}

    # Return Success:S7
    return {'status': 'SUCCESS', 'file_name': 'Image-Convert', 'step': '7', 'message': 'All The Images Converted To JPG Successfully'}