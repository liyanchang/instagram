#!/bin/python

from PIL import Image
from pylab import *
#import operator
#import numpy

num_cols = 20
CUTOFF = 60

class Shred:
    def __init__(self, image, num):
        width, height = image.size
        shred_width = width / num_cols
        lx, rx = shred_width * num, shred_width * (num + 1)
        self.left = list(image.crop((lx,0,lx+1,height)).getdata())
        self.right = list(image.crop((rx-1,0,rx,height)).getdata())

    def compare_right(self, shred):
        # by convention, we want lower numbers to be better
        # mostly so I can plug and play some other metrics
        def diff(t1, t2):
            return sum(map(lambda x, y: (x-y)**2, t1, t2)) > CUTOFF
        ans = abs(sum(map(diff, self.right, shred.left)))
        return ans

def sort_shreds(diffs):
    diffs.sort()

    g = {}
    used = []
    i = 0
    while len(g) < num_cols:
        num, left, right = diffs[i]
        if left not in g and left != right and right not in used:
            g[left] = right
            used.append(right)
        i += 1

    ans = [right]
    while len(ans) < num_cols:
        ans.append(g[ans[-1]])
    print ans
    return ans
    
def combine_shreds(image, order):
    unshredded = Image.new("RGBA", image.size)
    width, height = image.size
    shred_width = width / num_cols
    
    for index, shred_number in enumerate(order):
        x1, x2 = shred_width * shred_number, shred_width * (shred_number + 1)
        source_region = image.crop((x1, 0, x2, height))
        destination_point = (index*shred_width, 0)
        unshredded.paste(source_region, destination_point)
    unshredded.save("unshredded.jpg", "JPEG")

'''
image = Image.open('file.jpg')
s = [Shred(image, i) for i in range(num_cols)]
diffs = [(s[i].compare_right(s[j]), i, j) for i in range(num_cols) for j in range(num_cols)]

combine_shreds(image, sort_shreds(diffs))
'''

class Lines:
    added = []
    def __init__(self, width):
        self.guesses = dict([(x, (width/x-1)/2) for x in filter(lambda x: width%x==0, range(2,width))])
        self.width = width
        return
    def add(self, new):
        for g in self.guesses:
            if new%g == 0:
                self.guesses[g] -= 1
                if self.guesses[g] == 0:
                    #print "ANSWER", self.width/g
                    return self.width/g
        #print self.guesses
        return 1


def find_lines(image):
    width, height = image.size
    out = []
    for i in xrange(width-1):
        coli = list(image.crop((i, 0, i+1, height)).getdata())
        colj = list(image.crop((i+1, 0, i+2, height)).getdata())
        def diff(t1, t2):
            return sum(map(lambda x, y: (x-y)**2, t1, t2)) > CUTOFF
        ans = abs(sum(map(diff, coli, colj)))
        out.append((ans, i))
    out.sort(reverse=True)
    l = Lines(width)
    for num, i in out:
        l.add(i+1)
    return

#image = Image.open('file.jpg')
#find_lines(image)

t = arange(0.0, 2.0, 0.01)
s = sin(2*pi*t)
plot(t, s, linewidth=1.0)

xlabel('time (s)')
ylabel('voltage (mV)')
title('About as simple as it gets, folks')
grid(True)
show()
