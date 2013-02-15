#!/usr/bin/python

"""Object: find the profile of angles in an image. Return a histogram
of angles and how popular they are in the image"""

from __future__ import division

import Image,ImageTk,ImageFilter
import Numeric,MLab,FFT
import Tkinter as tk
import dataConversion
import time,inspect,sys,math

from iagaussian import iagaussian
from iaconv import iaconv
from Numeric import pi

root=tk.Tk()

saveimgs=[]

def view(arr,title="",autolevel=1):
    "show Numeric array"
    global root,saveimgs

    if not title:
        # automatic titles are the line of code used to call view()
        caller=sys._getframe(1)
        lines,startnum=inspect.getsourcelines(caller)
        title=lines[caller.f_lineno-startnum]

    # autoscale brightness
    arr=abs(arr) # take magnitude of complex values
    if autolevel:
        maxval=MLab.max(MLab.max(arr)) # find maximum
        if maxval>0:
            arr=arr*255/maxval # scale so 255 is the max
    arr=arr.astype(Numeric.UnsignedInt8)

    size=arr.shape[1],arr.shape[0]
    im=Image.fromstring("L",size,arr.tostring())
  
    #im=im.resize((500,500))
    
    image = ImageTk.PhotoImage(im)
    saveimgs.append(image)

    f=tk.Frame(root, relief='raised',bd=2)
    tk.Label(f,text=title).pack(side='bottom')
    x = tk.Label(f, image=image)
    x.pack(side='top')
    f.pack(side='left')

def deriv(arr,axis):
    """takes derivative along the axis and pads with 0 to return a same-size array.
    only works with 2d.
    """
    if axis==0:
        #print "r",arr[1:,:]
        #print "l",arr[:-1,:]
        diff=arr[1:,:]-arr[:-1,:]
        pad=Numeric.zeros((1,arr.shape[1]))
    else:
        diff=arr[:,1:]-arr[:,:-1]
        pad=Numeric.zeros((arr.shape[0],1))
    
    return Numeric.concatenate((diff,pad),axis=axis)
    

def angles(imagefilename):
    im=Image.open(imagefilename)
    #im.thumbnail((20,50))
    for i in range(0):
        im=im.filter(ImageFilter.SMOOTH)

    img=Numeric.reshape(Numeric.fromstring(im.convert("L").tostring(),
                                                Numeric.UnsignedInt8),
                             (im.size[1],im.size[0]))

    img=img.astype(Numeric.Complex16)


#    img_freq=FFT.fft2d(img)
    gsize=11
    sigma=1
    gauss=iagaussian([gsize,gsize],[gsize//2,gsize//2],
                     [[sigma,0],[0,sigma]]).astype(Numeric.Complex16)
    #print Numeric.array2string(gauss,precision=3,suppress_small=1)
#    kernel_freq=FFT.fft2d(gauss)

    sys.stdout.write("convolve...")
    sys.stdout.flush()
    img=iaconv(img,gauss)
    print "done"

#    img=FFT.inverse_fft2d(img_freq)

    # we can skip borders, which have blur errors anyhow
    margin=gsize
    img=img[margin:-1-margin,margin:-1-margin]

    view(img)

    ix=deriv(img,0)
    view(ix)

    iy=deriv(img,1)
    view(iy)

    x=ix-iy*1j
    angs=Numeric.fmod(-Numeric.arctan2(x.imag,x.real)+pi,pi)
    mags=abs(Numeric.sqrt(ix*ix+iy*iy))

    view(angs)
    
    histo={} # angle:freq
    degreesperbucket=.1
    buckets=180/degreesperbucket
    totalcounted=0
    for ang,mag in zip(Numeric.ravel(angs),Numeric.ravel(mags)):
        ang=int(ang*buckets)/buckets
        histo[ang]=histo.get(ang,0)+mag
        totalcounted+=mag

    keys=histo.keys()
    keys.sort()
    f=open("angles.data",'w')
    for k in keys:
        degrees=k*360/(2*pi)
        print >>f,"%.3f %f" % (degrees,histo[k])

        # remark on counts that are more than 1% of the total
        if histo[k]>totalcounted*.005:
            print "peak at",degrees

if __name__=='__main__':

    filename="ct1-small.png"
    if len(sys.argv)>1:
        filename=sys.argv[1]
    angles(filename)

    root.mainloop()
