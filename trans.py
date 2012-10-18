# -*- coding: utf-8 -*-

# CABEÇALHO DE ARQUIVO COMUM
# 00000000  47 49 46 38 39 61 9f 00  61 00 f7 1f 00 00 00 00  |GIF89a..a.......|
# ...
# 00000300  ff 90 fc ff b4 fc ff d8  fc ff fc fc ff 2c # linha onde começa Image Descriptor
# ...
# 000006c0  0e 12 10 00 3b # 3b -> File terminator


# CABEÇALHO DE FRAME
# 21 f9                   # Graphic Control Extension for frame #1
# 04                      # four bytes of data follow
# 04					  # no transparency ??
# 0d 00                   # 0.10s sec delay before painting next frame
# 1f				      # no transparent color ???
# 00					  # end of GCE block
# 2c

def full_gif_to_frame(raw_gif):
	assert raw_gif.startswith("GIF89a")
	width = ord(raw_gif[6]) + 256 * ord(raw_gif[7])
	height = ord(raw_gif[8]) + 256 * ord(raw_gif[9])

	assert hex(ord(raw_gif[10])) == "0xf7" # gct code
	gct_len = 256

	gct_range = 13, 13 + (gct_len * 3)
	gct = raw_gif[gct_range[0]:gct_range[1]]

	assert raw_gif[gct_range[1]] == "," # Image descriptor

	data_range = gct_range[1], len(raw_gif) - 1
	assert raw_gif[data_range[1]] == ";" # file terminator
	data = raw_gif[data_range[0] : data_range[1]]

	frame = ''.join([b.decode('hex') for b in "21 f9 04 04 0d 00 1f 00".split(" ")])
	frame += data
	return frame

if __name__ == "__main__":
	for i in xrange(1, 100):
		print i
		with open("full/frame%d.gif" % i, "rb") as f:
			raw_gif = f.read()
		with open("split/out%d.part" % i, "wb") as f:
			f.write(full_gif_to_frame(raw_gif))
