#!/usr/bin/python


from PIL import Image
import pygame


class FakeCamera:
    """A class for capturing images from a fake camera"""

    def __init__(self):
        """Constructor for this object."""
        print("Starting Fake Camera Object")
        self.cam = Image.open(open("libselfietorium/eagle.jpg", 'rb'))
        self.cam2 = pygame.image.load("libselfietorium/eagle.jpg")

    def GetPhoto(self):
        """
        Return a photo from the camera
        :return:
        """
        return self.cam2


if __name__ == '__main__':
    # Add sample Code here
    pass
