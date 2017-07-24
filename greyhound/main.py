import greyhound



def random(resource):

    bounds = [float(i) for i in resource.info['boundsConforming']]
    minx = bounds[0]; maxx = bounds[3]
    miny = bounds[1]; maxy = bounds[4]
    minz = bounds[2]; maxz = bounds[5]
    b = greyhound.box.Box(minx, miny, maxx, maxy, minz, maxz)
    print (b.url)

def entry():
    import argparse

    parser = argparse.ArgumentParser(description='')
#    parser.add_argument('query', nargs='+')
#    parser.add_argument('count', nargs="?", default=2)

    args = parser.parse_args()


    base = 'http://data.greyhound.io/'

    r = greyhound.resource.Resource(base, 'mn-z')

    random(r)


    x = -10375539.03
    y = 6210523.43
    b = greyhound.box.Box.from_point(x,y,1000)
    data = r.read(b, 0, 16, True)
    print (data)

#    greyhound.util.writeLASfile(data, 'somefile.las')


