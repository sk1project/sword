# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2019 by Igor E. Novikov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gtk
import struct
from copy import deepcopy

VALUES = {
    'hex': '--',
    'Char': '--',
    'UChar': '--',
    'Short': '--',
    'UShort': '--',
    'Int': '--',
    'UInt': '--',
    'Long': '--',
    'ULong': '--',
    'LongLong': '--',
    'ULongLong': '--',
    'Float': '--',
    'Double': '--',
    'Int24': '--',
    'UInt24': '--',
}

ORDER = [
    'hex',
    'Char',
    'UChar',
    'Short',
    'UShort',
    'Int',
    'UInt',
    'Long',
    'ULong',
    'LongLong',
    'ULongLong',
    'Float',
    'Double',
    'Int24',
    'UInt24',
]


class DecoderListModel(gtk.ListStore):

    def __init__(self, data='', flag=False):

        gtk.ListStore.__init__(self, str, str)

        values = deepcopy(VALUES)
        data = data.replace(' ', '')
        data = data.replace('\n', '')

        if data: values['hex'] = data

        endian = '<'
        if flag: endian = '>'

        if not len(data) & 1:
            bytes = data.decode('hex')
            if len(bytes) == 1:
                values['Char'], = struct.unpack('b', bytes)
                values['UChar'], = struct.unpack('B', bytes)
            elif len(bytes) == 2:
                values['Short'], = struct.unpack(endian + 'h', bytes)
                values['UShort'], = struct.unpack(endian + 'H', bytes)
            elif len(bytes) == 4:
                values['Int'], = struct.unpack(endian + 'i', bytes)
                values['UInt'], = struct.unpack(endian + 'I', bytes)
                values['Long'], = struct.unpack(endian + 'l', bytes)
                values['ULong'], = struct.unpack(endian + 'L', bytes)
                values['Float'], = struct.unpack(endian + 'f', bytes)
            elif len(bytes) == 8:
                values['LongLong'], = struct.unpack(endian + 'q', bytes)
                values['ULongLong'], = struct.unpack(endian + 'Q', bytes)
                values['Double'], = struct.unpack(endian + 'd', bytes)
            elif len(bytes) == 3:
                if endian == '<':
                    values['Int24'] = unpack_int24le(bytes)
                    values['UInt24'] = unpack_uint24le(bytes)
                else:
                    values['Int24'] = unpack_int24be(bytes)
                    values['UInt24'] = unpack_uint24be(bytes)

        for item in ORDER:
            self.append((item, values[item]))


def unpack_uint24le(b):
    b = bytearray(b)
    return (b[0] & 0xFF) + ((b[1] & 0xFF) << 8) + ((b[2] & 0xFF) << 16)


def unpack_uint24be(b):
    b = bytearray(b)
    return (b[2] & 0xFF) + ((b[1] & 0xFF) << 8) + ((b[0] & 0xFF) << 16)


def unpack_int24le(b):
    return signed24(unpack_uint24le(b))


def unpack_int24be(b):
    return signed24(unpack_uint24be(b))


def signed24(v):
    v &= 0xFFFFFF
    return v - 0x1000000 if v & 0x800000 else v
