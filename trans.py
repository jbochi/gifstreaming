# -*- coding: utf-8 -*-

# Reference
# GIF Spec: http://tronche.com/computer-graphics/gif/gif89a.html#image-descriptor
# GIF for Dummies: http://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp
# Animated GIF extension: http://odur.let.rug.nl/~kleiweg/gif/netscape.html

def hex_to_binary(hex_string):
    return ''.join([b.decode('hex') for b in hex_string.split(" ")])

def get_logical_screen_description(raw_gif):
    assert raw_gif.startswith("GIF89a")
    width = ord(raw_gif[6]) + 256 * ord(raw_gif[7])
    height = ord(raw_gif[8]) + 256 * ord(raw_gif[9])
    return raw_gif[:13]

def full_gif_to_animated_gif_header(raw_gif):
    # Remove global color table
    logical_description = [c for c in get_logical_screen_description(raw_gif)]
    logical_description[10] = chr(0)
    logical_description = ''.join(logical_description)

    # Animated GIF extension
    ANIMATED_GIF_EXTENSION = hex_to_binary("21 ff 0b") + "NETSCAPE2.0" + hex_to_binary("03 01 01 00 00")
    return logical_description + ANIMATED_GIF_EXTENSION

def full_gif_to_frame(raw_gif):
     # Assert header is valid, we don't use any info
    get_logical_screen_description(raw_gif)

    # Global color table
    assert hex(ord(raw_gif[10])) == "0xf7"
    gct_len = 256
    gct_range = 13, 13 + (gct_len * 3)
    color_table = raw_gif[gct_range[0]:gct_range[1]]

    # Image descriptor
    image_descriptor_range = gct_range[1], gct_range[1] + 10
    image_descriptor = raw_gif[image_descriptor_range[0] : image_descriptor_range[1]]
    assert image_descriptor[0] == ","
    assert ord(image_descriptor[-1]) == 0        # Packed Fields
    packed_fields = chr(int("10000111", base=2)) # Local Color Table Flag        1 Bit
                                                 # Interlace Flag                1 Bit
                                                 # Sort Flag                     1 Bit
                                                 # Reserved                      2 Bits
                                                 # Size of Local Color Table     3 Bits

    new_image_descriptor = image_descriptor[:-1] + packed_fields

    # Image data
    data_range = image_descriptor_range[1], len(raw_gif) - 1
    data = raw_gif[data_range[0] : data_range[1]]
    assert raw_gif[data_range[1]] == ";" # file terminator

    # New frame data
    frame = hex_to_binary("21 f9 04 04 0d 00 1f 00")
    frame += new_image_descriptor
    frame += color_table
    frame += data

    return frame


if __name__ == "__main__":
  with open("full/frame1.gif", "rb") as f:
      raw_gif = f.read()
  with open("split/out0.part", "wb") as f:
      f.write(full_gif_to_animated_gif_header(raw_gif))

  for i in xrange(1, 500):
      print i
      with open("full/frame%d.gif" % i, "rb") as f:
          raw_gif = f.read()
      with open("split/out%d.part" % i, "wb") as f:
          f.write(full_gif_to_frame(raw_gif))
