# Define "image_convert" Function
def image_convert(input_images_folder_path: str, converted_images_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
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

    # Return Success:S4
    return {'status': 'SUCCESS', 'file_name': 'Image-Convert', 'step': '4', 'message': '"ConvertedImages" Folder Emptied Successfully'}