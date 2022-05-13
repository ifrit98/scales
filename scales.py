import numpy as np
import pandas as pd

def logical2idx(x):
    x = np.asarray(x)
    return np.arange(len(x))[x]

bin2 = lambda s: bin(s)[2:]
pad_bin = lambda s, padlen: '0'*(padlen-len(s)) + s

def binary(s, padlen=12):
    b = bin2(s)
    if len(b) < padlen:
        b = pad_bin(b, padlen)
    return b

binary_inc = lambda b: binary(int(b, 2) + 1)

def rotate(l, n=1):
    return l[n:] + l[:n]

def autocorr(x):
    ints = []
    for n in range(len(x)):
        y = rotate(x, n)
        m = sum(np.array(x) * np.array(y))
        if n == 6:
            m = m // 2
        ints.append(m)
    return ints


notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
NOTES = np.asarray(notes)

interval_nms = [
    "m2",
    "M2",
    "m3",
    "M3",
    "P4",
    "TT",
    "P5",
    "m6",
    "M6",
    "m7",
    "M7"
]

class Scale:
    def __init__(self, xs):
        a,b,c,d,e,f,g,h,i,j,k,l = xs

        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        self.d = int(d)
        self.e = int(e)
        self.f = int(f)
        self.g = int(g)
        self.h = int(h)
        self.i = int(i)
        self.j = int(j)
        self.k = int(k)
        self.l = int(l)

        self.list = [
            self.a, self.b, self.c, self.d, 
            self.e, self.f, self.g, self.h, 
            self.i, self.j, self.k, self.l
        ]
        self.bin = ''.join([str(x) for x in self.list])
        self.int = int(self.bin, 2)

        self.npy = np.asarray(self.list)
        self.arr = self.npy.astype(bool)
        self.idx = np.arange(len(self.arr))[self.arr]
        self.notes = NOTES[self.idx]
        self.cls = sum(self.arr)

        # Parse intervals contained in species
        self.cor = autocorr(self.list)
        self.intervals = dict(zip(interval_nms, self.cor[1:])) 
        self.density = None
        self.entropy = None

    def __str__(self):
        n =   "Notes     : {}".format(self.notes)
        b = "\nBinary    : {}".format(self.bin)
        i = "\nSpecies   : {}".format(self.int)
        s = "\nClass     : {}".format(self.cls)
        t = "\nIntervals : {}".format(list(self.intervals.values()))
        return n + b + i + s + t

    def __dict__(self):
        return {
            'notes': self.notes,
            'binary': self.bin,
            'species': self.int,
            'class': self.cls,
            'intervals': list(self.intervals.values())
        }

INTERVALS = {
    "m2": Scale("110000000000"),
    "M2": Scale("101000000000"), 
    "m3": Scale("100100000000"), 
    "M3": Scale("100010000000"), 
    "P4": Scale("100001000000"), 
    "TT": Scale("100000100000"),
    "P5": Scale("100001000000"),     
    "m6": Scale("100010000000"), 
    "M6": Scale("100100000000"), 
    "m7": Scale("101000000000"), 
    "M7": Scale("110000000000"),
}


intervals = np.asarray(list(INTERVALS.values()))

def make_scale(integer):
    return Scale(binary(integer))

def make_all_scales():
    return pd.DataFrame([make_scale(i).__dict__() for i in range(4096)])

if False:
    ds = []
    for i in range(4096):
        s = make_scale(i)
        ds.append(s.__dict__())
        print(s)
        print()
    pd.DataFrame(ds)