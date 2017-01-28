#!/usr/bin/python
# -*- coding: utf-8 -*-


class utilities():
    """Utility functions used throughout selfietorium.  These functions may move
    to a more appropriate module later on."""
    def hex_to_rgb(self, value):
        """Convert a colour representation in the form of #RRGGBB to a python
        tuple.

        Args:
            value (string): string representing the hexadecimal colour to convert.

        Returns:
            Tuple containing the RGB values from the hexadecimal version of the colour.

        """
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgb_to_hex(self, rgb):
        """Convert an RGB Tuple to a hexadecimal representation of the colour.

        Args:
            rgb (tuple): tuple containing the rgb value for a colour

        Returns:
            String representing the hexadecimal representation of the colour.
        """
        return '#%02x%02x%02x' % rgb

if __name__ == '__main__':
    util = utilities()
    print('{}, {}'.format(util.hex_to_rgb('aabbcc'), util.hex_to_rgb('AABBCC')))
    # -> (170, 187, 204), (170, 187, 204)

    print('{}, {}'.format(util.rgb_to_hex((170, 187, 204)),
                          util.rgb_to_hex((170, 187, 204))))
    # -> aabbcc, AABBCC
    print('{}, {}'.format(util.hex_to_rgb('aa0200'), util.hex_to_rgb('AA0200')))
    # -> (170, 2, 0), (170, 2, 0)

    print('{}, {}'.format(util.hex_to_rgb('#aa0200'), util.hex_to_rgb('#AA0200')))
    # -> (170, 2, 0), (170, 2, 0)