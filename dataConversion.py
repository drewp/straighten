
#from http://scipy.net/pipermail/scipy-user/2002-December/001042.html

##########################################################
##dataConversion.py
##functions for data conversion between Numeric and PIL
#
import Numeric
import Image
from ArrayPrinter import array2string

#conversion image object (PIL) to narray object (Numeric)
#outputDim: rank of output array
def image2array(im,outputDim=3):
     if im.mode=="1":
	a=Numeric.fromstring(im.tostring(),Numeric.UnsignedInt8) 
#mystery why is needed
	im.mode="L"
	a = Numeric.fromstring(im.tostring(), Numeric.UnsignedInt8)
	a = a > 0
	bands=1
     elif im.mode == "L":
        a = Numeric.fromstring(im.tostring(), Numeric.UnsignedInt8)
	bands=1
     elif im.mode == "F":
        a = Numeric.fromstring(im.tostring(), Numeric.Float32)
	bands=1
     elif (im.mode=='RGB')|(im.mode=='YCbCr'):
	a = Numeric.fromstring(im.tostring(), Numeric.UnsignedInt8)
	bands=3
     elif (im.mode=='RGBA')|(im.mode=='CMYK'):
	a = Numeric.fromstring(im.tostring(), Numeric.UnsignedInt8)
	bands=4
     else:
	 raise ValueError, im.mode+" mode not considered"
     #print "array u to now"
     #print a
     if outputDim==3:
	    a.shape=(im.size[1],im.size[0],bands)
     elif outputDim==2:
	    a=Numeric.reshape(a,(im.size[1],im.size[0]))
     elif outputDim==1:
	    a=Numeric.reshape(a,(im.size[1]*im.size[0],))
     #print "shape change"
     #print a
     return a

    
#autoescaling function for representation with UnsignedInt8
def _imagesc(mat):

	maxV=max(Numeric.ravel(mat))
	minV=min(Numeric.ravel(mat))
	if maxV<>minV:
		return (255*(mat-minV)/(maxV-minV)).astype(Numeric.UnsignedInt8)

#conversion array object (Numeric) to image object (PIL)
#scale=1: autoscales image, each chanel independently
#scale=2: autoscales image, with max value of all channels
#scale=0: do not autoscale
def array2image(a,scale=1):
     #print a.shape
     if len(a.shape)==3:
	b=()
	if scale==2:
		a=_imagesc(a)
	for i in range(a.shape[2]):
		#print a[:,:,i].shape

		if scale==1:
			a[:,:,i]=_imagesc(a[:,:,i])
		b+=(array2image(a[:,:,i]),)
	#print b[0].size
	if a.shape[2]==3:
		#print "here shape 3",b
		#return b
		return Image.merge("RGB",b)
	elif a.shape[2]==1:
		#print "here shape 1",b
		return b[0]
     elif len(a.shape)==2:
	    print "autoescaling image"
	    a=_imagesc(a)
	    mode ="L"
     elif a.typecode() == Numeric.UnsignedInt8:
         mode = "L"
     elif a.typecode() == Numeric.Float32:
         mode = "F"
     else:
         raise ValueError, "unsupported image mode"
     return Image.fromstring(mode, (a.shape[1], a.shape[0]), a.astype(a.typecode()).tostring())

