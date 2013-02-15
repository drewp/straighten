#from http://marahu.dca.fee.unicamp.br/~alexgs/ia636/python/ia636/iaind2sub.html

def iaind2sub(dim,i):
    """  o Purpose
      Convert linear index to double subscripts.

  o Synopsis
      x,y = iaind2sub(dim,i)

  o Input
      dim: Dimension.
    i: Index.

  o Output
      x: 
    y: 

  o Description
  
  o Examples
      f = Numeric.array([[0,6,0,2],[4,0,1,8],[0,0,3,0]])
      print f
      i = Numeric.nonzero(Numeric.ravel(f))
      (x,y) = iaind2sub(f.shape, i)
      print x
      print y
      print f[x[0],y[0]]
      print f[x[4],y[4]]
      
"""
    from Numeric import asarray 
    
    i = asarray(i)
    x = i / dim[1]
    y = i % dim[1]
    
    return x,y

#from http://marahu.dca.fee.unicamp.br/~alexgs/ia636/python/ia636/iagaussian.html

def iagaussian(s,mu,sigma):
    """  o Purpose
      Generate a 2D Gaussian image.

  o Synopsis
      g = iagaussian(s,mu,sigma)

  o Input
      s: [rows columns]
    mu: Mean vector. 2D point (x;y). Point of maximum value.
    sigma: covariance matrix (square).  [ Sx^2 Sxy; Syx Sy^2]

  o Output
      g: 

  o Description
      A 2D Gaussian image is an image with a Gaussian distribution. It can be used to generate test patterns or Gaussian filters both for spatial and frequency domain. The integral of the gaussian function is 1.0.

  o Examples
      import Numeric
      f = iagaussian([8,4], [3,1], [[1,0],[0,1]])
      print Numeric.array2string(f, precision=4, suppress_small=1)
      g = ianormalize(f, [0,255]).astype(Numeric.UnsignedInt8)
      print g
    f = iagaussian(100, 50, 10*10)
      g = ianormalize(f, [0,1])
      g,d = iaplot(g)
      showfig(g)
    f = iagaussian([50,50], [25,10], [[10*10,0],[0,20*20]])
      g = ianormalize(f, [0,255]).astype(Numeric.UnsignedInt8)
      iashow(g)
"""
    from Numeric import asarray,product,arange,NewAxis,transpose,matrixmultiply,reshape,concatenate,resize,sum,zeros,Float,ravel,pi,sqrt,exp 
    from LinearAlgebra import inverse,determinant 
    
    if type(sigma).__name__ in ['int', 'float', 'complex']: sigma = [sigma]
    s, mu, sigma = asarray(s), asarray(mu), asarray(sigma)
    
    if (product(s) == max(s)):
        x = arange(product(s))
        d = x - mu
        if len(d.shape) == 1:
            tmp1 = d[:,NewAxis]
            tmp3 = d
        else:
            tmp1 = transpose(d)
            tmp3 = tmp1
        if len(sigma) == 1:
            tmp2 = 1./sigma
        else:
            tmp2 = inverse(sigma)
        k = matrixmultiply(tmp1, tmp2) * tmp3
    else:
        aux = arange(product(s))
        x, y = iaind2sub(s, aux)
        xx = reshape(concatenate((x,y)), (2, product(x.shape)))
    
        d = transpose(xx) - resize(reshape(mu,(len(mu),1)), (s[0]*s[1],len(mu)))
    
        if len(sigma) == 1:
            tmp = 1./sigma
        else:
            tmp = inverse(sigma)
        k = matrixmultiply(d, tmp) * d
        k = sum(transpose(k))
    
    g = zeros(s, Float)
    aux = ravel(g)
    if len(sigma) == 1:
        tmp = sigma
    else:
        tmp = determinant(sigma)
    aux[:] = 1./(2*pi*sqrt(tmp)) * exp(-1./2 * k)
    
    return g
