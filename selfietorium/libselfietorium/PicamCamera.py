#!/usr/bin/python

import picamera
import io
from PIL import Image


class PicamCamera:
    """A class for capturing images from Picam"""

    def __init__(self):
        """Constructor for this object."""
        print("Starting picam Camera Object")
        self.cam = picamera.PiCamera()
        self.stream = io.BytesIO()

    def GetPhoto(self):
        """
        Todo:
            document the picamera image aquisition, and how it is converted to
            a surface
        """
        self.cam.capture(self.stream, format='jpeg')
        self.stream.seek(0)
        img = Image.open(self.stream)

        return img


if __name__ == '__main__':
    # Add sample Code here
    pass
