#!/usr/bin/python
"""
A library that provides configuration loading and saving for the selfietorium project

This is a python library for handling the configuration for selfietorium.

Notes:
Pyxser is a library that aparently also provides object serialisation, but
attempts to locate this package in the repos has so far failed. This class
therefore provides specific serialisation methods mentioned in:
http://www.diveintopython3.net/serializing.html

Example:
    import configuration
    cfile = ConfigFile("boothsettings.json")
    c.Save()
"""
import json

class ConfigFile:
    """A Configuration object - this object serialises / deserialises data to JSON format."""
    def __init__(self,iniFile):
        """Constructor for this object."""
        print "--BUILDING"
        self.inifile = iniFile
        self.layout = '../6x4.Template1.-.Linked.Files.svg'
        self.prePhotoPhrase = 'Smile'
        self.photostore = 'Photos/'
        self.preenTime = 5
        self.photosTaken = 0
        self.sheetspercartidge = 0
        self.shutterSound = "62491__benboncan__dslr-click.wav"
        print self
        print "----"

    def Load(self):
        print "--LOADING"
        with open(self.inifile, mode='r') as f:
            entry = json.load(f)
            self.layout = entry['layout']
            self.preenTime = entry['preenTime']
            print self
            print "----"
            return entry

    def Save(self):
        """Save data to config file."""
        configuration={}
        configuration['layout'] = self.layout
        configuration['prePhotoPhrase']=self.prePhotoPhrase
        configuration['preenTime']=self.preenTime
        configuration['photosTaken']=self.photosTaken
        configuration['sheetspercartidge'] = self.sheetspercartidge
        configuration['shutterSound'] = self.shutterSound

        print self.inifile
        with open(self.inifile, mode='w') as f:
            json.dump(configuration,f, indent=2)


if __name__ == '__main__':
    c = ConfigFile("boothsettings.json")
    c.Save()
    config = c.Load()

    print config
    print config['layout']
