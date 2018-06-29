# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 16:37:27 2018

@author: Doug

DotA 2 Hero Collection

This script, when given the --api-url, --collection and --token will create a
basic collection of DotA heroes. They each have an image associated with them,
and their primary stat available as metadata.
"""

import os
import sys
import argparse

from zegami_kanjidic import (
        api,
        run
)

# Define the image directories
IMAGES_DIRECTORY = 'Images/'
PORTRAITS_DIRECTORY = IMAGES_DIRECTORY + 'Portraits/'
BACKGROUNDS_DIRECTORY = IMAGES_DIRECTORY + 'Backgrounds/'


# Define the table filename
TABLE_FILENAME = 'DotA2Table.xlsx'


# Define the data specific function
def dota_heroes_upload(reporter, client, base_path):

    # Initial collection creation
    description = 'A collection of DotA 2 hero information'
    collection = client.create_collection('DotA 2', description)
    reporter('Created collection', level=0)

    # Create the imageset
    imageset_id = collection['imageset_id']
    reporter('Uploading images', level=0)
    image_directory = os.path.join(base_path, PORTRAITS_DIRECTORY)

    # For each image found in the image folder, upload to the imageset
    for filename in os.listdir(image_directory):
        with open(os.path.join(image_directory, filename), 'rb') as f:
            client.upload_png(imageset_id, filename, f)
    reporter('Uploaded %d pngs to client' % len(os.listdir(image_directory)),
        level=0)

    # Create the dataset
    dataset_id = collection['dataset_id']
    with open(os.path.join(base_path, TABLE_FILENAME), 'rb') as f:
        client.upload_data(dataset_id, TABLE_FILENAME, f)
    reporter('Uploaded data from %s to client' % TABLE_FILENAME, level=0)

    # Create the join dataset
    join_ds = client.create_join('Join for DotA2 dataset', imageset_id, dataset_id,
                                 join_field='Image Name')
    collection['join_dataset_id'] = join_ds['id']
    client.update_collection(collection['id'], collection)


# Define the argument parser
def parse_args(argv):
    parser = argparse.ArgumentParser(argv[0])
    parser.add_argument('--api-url', required=True, help='Zegami api endpoint')
    parser.add_argument(
            '--project', required=True, help='Project ID to make collection in')
    parser.add_argument(
            '--token', required=True, help='Temp hack to avoid login')
    parser.add_argument(
            '-v', '--verbose', action='count', default=0, help='Show progress')
    return parser.parse_args(argv[1:])


# Define main to run from the start
def main(argv):
    args = parse_args(argv)
    reporter = run.Reporter(sys.stderr, args.verbose)
    client = api.Client(args.api_url, args.project, args.token)
    try:
        dota_heroes_upload(reporter, client, './')
    except (EnvironmentError, ValueError) as e:
        sys.stderr.write('error: %s\n' % e)
        return 1 # Return with error
    return 0 # Return fine


# Run the script
if __name__ == '__main__':
    sys.exit(main(sys.argv))