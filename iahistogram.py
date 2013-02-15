# from http://marahu.dca.fee.unicamp.br/~alexgs/ia636/python/ia636/iahistogram.py.html

def iahistogram(f):
    """  o Purpose
      Image histogram.

  o Synopsis
      h = iahistogram(f)

  o Input
      f: 

  o Output
      h: 

  o Description
  
  o Examples
      f = iaread('woodlog.pgm')
      iashow(f)
      h = iahistogram(f)
      g,d = iaplot(h)
      g('set data style boxes')
      g.plot(d)
      showfig(h)
      
"""
    from Numeric import asarray,searchsorted,sort,ravel,concatenate,product 
    
    f = asarray(f)
    n = searchsorted(sort(ravel(f)), range(max(ravel(f))+1))
    n = concatenate([n, [product(f.shape)]])
    h = n[1:]-n[:-1]
    
    return h
