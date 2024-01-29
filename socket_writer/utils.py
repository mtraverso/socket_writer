import os
import random

def list_files_by_extension(directory, extension):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files.append(filename)
    return files




def set_image(json_data, images):
    # get random element from images list


    # Get random element from images list
    random_image = random.choice(images)

    target_detector = 'gsai-xray-v1.2'

    # Iterate through the "image_list" and modify the element with the specified detector
    for image_element in json_data.get('images', {}).get('image_list', []):
        if image_element.get('detector') == target_detector:
            # Modify the element as needed
            image_element['file_image_url'] = '/Users/matias/gsaidata/images/'+random_image