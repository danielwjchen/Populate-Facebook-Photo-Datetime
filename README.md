# Populate Facebookg Photo Datetime
This is a script that sets EXIF creation timestamp for photos exported from Facebook. This is for people wishing to recover photos from Facebook, which are unfortunately without their original EXIF data as of April 2019.

## Usage
To use this script, please go to Facebook's "Download Your Information" page and create a file in JSON format. Download and extract the file.

Make sure the required library `piexif` is installed by running `pip install -r requirements.txt`. `virtualenv` is recommended.

Run the following command `./main.py /PATH/TO/FACEBOOK/FILE/FOLDER`.