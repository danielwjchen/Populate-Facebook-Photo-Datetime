#!/usr/bin/env python
import json
import sys
import piexif

from datetime import datetime
from os import listdir
from os.path import isdir, isfile, join
from typing import List

def get_album_json_filepaths(album_path: str) -> List[str]:
    '''Gets list of json file paths'''
    result = []
    for item in listdir(album_path):
        filepath = join(album_path, item)
        if item.endswith('.json') and isfile(filepath):
            result.append(filepath)

    return result

def populate_facebook_photo_datetime(facebook_folder_path: str) -> List[str]:
    album_path = join(facebook_folder_path, 'photos_and_videos', 'album')
    result = []
    if not isdir(album_path):
        raise Exception(
            'Folder ./photos_and_videos does not exist in the given path.'
        )

    for json_filepath in get_album_json_filepaths(album_path):
        with open(json_filepath, 'r') as json_file:
            album_data = json.load(json_file)
            for photo in album_data['photos']:
                photo_filepath = join(facebook_folder_path, photo['uri'])
                if not photo_filepath.endswith('.jpg'):
                    continue

                if not isfile(photo_filepath):
                    print(f'Fails to open photo file: {photo["uri"]}')
                    continue

                create_datetime = datetime.fromtimestamp(
                    photo['creation_timestamp']
                )
                exif_dict = piexif.load(photo_filepath)
                original_datetime = \
                    create_datetime.strftime("%Y:%m:%d %H:%M:%S")
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = \
                    original_datetime
                    

                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, photo_filepath)
                result.append(
                    f'Sets origin datetime of {photo_filepath} '
                    f'to {original_datetime}'
                )

    return result

if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise Exception('Only 1 argument is accepted.')

    elif len(sys.argv) == 1:
        raise Exception('Must specify filepath to the facebook folder.')

    result = populate_facebook_photo_datetime(sys.argv[1])
    for photo in result:
        print(photo)