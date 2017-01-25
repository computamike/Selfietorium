#!/usr/bin/python
# -*- coding: utf-8 -*-

class utilities():
    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgb_to_hex(self, rgb):
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