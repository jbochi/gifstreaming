
image_header = "21 f9 04 04 0d 00 1f 00 2c 00 00 00 00 9f 00 61".replace(' ', '').decode('hex')

with open('out.gif', 'r') as i:
    contents = i.read()


for i, data in enumerate(contents.split(image_header)):
    if i > 0:
        data = image_header + data
    filename = 'parts/out%d.part' % i
    with(open(filename, 'w')) as o:
        print 'Writing %s' % filename
        o.write(data)

