# from http://marahu.dca.fee.unicamp.br/~alexgs/ia636/python/ia636/iaconv.py.html

def iaconv(f,h):
    """  o Purpose
      2D convolution.

      modified by drewp to build a result array of the same typecode
      as 'f', which makes this work on complex arrays.

  o Synopsis
      g = iaconv(f,h)

  o Input
      f: input image.
    h: PSF (point spread function), or kernel. The origin is at the array center.

  o Output
      g: 

  o Description
      Perform a 2D discrete convolution. The kernel origin is at the center of image h.

  o Examples
      import Numeric
      f = Numeric.zeros((5,5))
      f[2,2] = 1
      print f
      h = Numeric.array([[1,2,3],[4,5,6]])
      print h
      a = iaconv(f,h)
      print a
      
    f = Numeric.array([[1,0,0,0],[0,0,0,0]])
      print f
      h = Numeric.array([1,2,3])
      print h
      a = iaconv(f,h)
      print a
      
    f = Numeric.array([[1,0,0,0,0,0],[0,0,0,0,0,0]])
      print f
      h = Numeric.array([1,2,3,4])
      print h
      a = iaconv(f,h)
      print a
      
    f = iaread('cameraman.pgm')
      h = [[1,2,1],[0,0,0],[-1,-2,-1]]
      g = iaconv(f,h)
      gn = ianormalize(g, [0,255])
      iashow(gn)
      
"""
    from Numeric import asarray,NewAxis,zeros,array,product
    
    f, h = asarray(f), asarray(h)
    if len(f.shape) == 1: f = f[NewAxis,:]
    if len(h.shape) == 1: h = h[NewAxis,:]
    if product(f.shape) < product(h.shape):
        f, h = h, f
    g = zeros(array(f.shape) + array(h.shape) - 1,f.typecode())
    for i in range(h.shape[0]):
        for j in range(h.shape[1]):
            g[i:i+f.shape[0], j:j+f.shape[1]] += h[i,j] * f
    
    return g
