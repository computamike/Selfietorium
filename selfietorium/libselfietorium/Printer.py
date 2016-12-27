#!/usr/bin/python
import cups

class Printer:
    """A class for capturing images from a fake camera"""
    def __init__(self, printer_name, photo):
        """Constructor for this object."""
        print("Starting Fake Printer Object")
        self.conn = cups.Connection()
        printers = self.conn.getPrinters()

        printer = [p for p in printers if p == printer_name]
        if (len(printer)>0):
            print "Found Printer"
            print printer[0]
            self.conn.printFile(printer[0],photo,'Selfietorium',{})
    def print_photo(photo):
        pass
        #self.conn.printFile()


if __name__ == '__main__':

    # Add sample Code here
    print "hello - I am a print example"
    c = Printer('PDF','Output.svg')
    c.print_photo()
    pass