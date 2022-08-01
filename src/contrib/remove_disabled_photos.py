import datetime
import shutil
import Metashape
import os
import sys
from pathlib import Path

"""
Script for moving disabled photos, Metashape (v 1.7)
Matjaz Mori, CPA, October 2019

The script will create a new subdirectory in the photos directory,
move all the photos from the project marked "Disabled" into it and remove "Disabled" cameras prom Metashape project.
When using, it is advisable to monitor the Console (View -> Console). 

"""

compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))


def remove_disabled_photos():
    print (datetime.datetime.now())

    doc = Metashape.app.document
    chunk = doc.chunk
    counter = 0
    counter_fail = 0
    counter_not_moved = 0
    counter_errors = 0
    counter_cameras = 0

    print (f"Starting to evaluate {len(chunk.cameras)} photos...")

    for camera in chunk.cameras:
        if camera.enabled is True:
            counter_not_moved += 1
            continue # skipping enabled cameras

        photo_path = Path(camera.photo.path)
        photo_name = camera.label
        destination_dir = Path.joinpath(photo_path.parent, 'Disabled')
        destination = Path.joinpath(destination_dir, photo_path.name)

        if not destination_dir.exists():
            try:
                destination_dir.mkdir()
                print (f"Successfully created the directory {destination_dir}")
            except OSError:
                print (f"Error creating {destination_dir}")
                counter_errors += 1
                continue # we can't create directory - thus we can't move photo - thus we shouldn't delete it

        try:
            if photo_path.is_file():
                print (f"Moving {photo_name} ...")
                shutil.move(photo_path, destination)

                counter += 1
                counter_cameras += 1
            else:
                print (f"Photo {photo_name} does not exist!")
                counter_cameras += 1
                counter_fail += 1

            chunk.remove(camera)

        except OSError:
            counter_errors = counter_errors + 1
            print (f"Error {photo_name}!")

    message_end = f"Success, {counter}  photos moved, {counter_not_moved}  photos not moved.\nNumber of files unable to move: {counter_fail} \nNumber of cameras removed: {counter_cameras} \nNumber of unknown errorrs: {counter_errors}"
    print (message_end)


label = "Scripts/Remove disabled photos"
Metashape.app.addMenuItem(label, remove_disabled_photos)
print(f"To execute this script press {label}")
