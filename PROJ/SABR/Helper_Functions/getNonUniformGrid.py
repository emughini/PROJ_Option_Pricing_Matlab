# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# getNonUniformGrid.m

    
@function
def getNonUniformGrid(m_0=None,lx=None,ux=None,gridMethod=None,center=None,manualPoint=None,gridMultParam=None,*args,**kwargs):
    varargin = getNonUniformGrid.varargin
    nargin = getNonUniformGrid.nargin

    #UNTITLED Summary of this function goes here
#   Detailed explanation goes here
    
    nx=copy(m_0)
# getNonUniformGrid.m:5
    dx=(ux - lx) / nx
# getNonUniformGrid.m:5
    if gridMethod == 1:
        v=lx + dot((arange(1,nx)).T,dx)
# getNonUniformGrid.m:8
    else:
        if gridMethod == 2:
            v=zeros(m_0,1)
# getNonUniformGrid.m:10
            v[1]=lx
# getNonUniformGrid.m:11
            v[m_0]=ux
# getNonUniformGrid.m:11
            mid=floor(m_0 / 2)
# getNonUniformGrid.m:12
            for k in arange(2,mid).reshape(-1):
                v[k]=center + sinh(dot((1 - (k - 1) / (mid - 1)),asinh(v(1) - center)))
# getNonUniformGrid.m:14
            for k in arange(mid + 1,m_0 - 1).reshape(-1):
                v[k]=center + sinh(dot(((k - mid) / (mid)),asinh(v(m_0) - center)))
# getNonUniformGrid.m:17
        else:
            if gridMethod == 3:
                x=arange(0,1,1 / (m_0 - 1))
# getNonUniformGrid.m:20
                alpha=dot(0.8,(ux - lx))
# getNonUniformGrid.m:21
                c1=asinh((lx - center) / alpha)
# getNonUniformGrid.m:22
                c2=asinh((ux - center) / alpha)
# getNonUniformGrid.m:23
                v=center + dot(alpha,(dot(c2,sinh(multiply(c2,x) + multiply(c1,(1 - x))))))
# getNonUniformGrid.m:24
            else:
                if gridMethod == 4:
                    v=zeros(m_0,1)
# getNonUniformGrid.m:26
                    v[1]=lx
# getNonUniformGrid.m:27
                    v[m_0]=ux
# getNonUniformGrid.m:28
                    alpha=dot(gridMultParam,(v(m_0) - v(1)))
# getNonUniformGrid.m:29
                    c1=asinh((v(1) - center) / alpha)
# getNonUniformGrid.m:30
                    c2=asinh((v(m_0) - center) / alpha)
# getNonUniformGrid.m:31
                    v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / m_0,(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / m_0))))
# getNonUniformGrid.m:32
                else:
                    if gridMethod == 5:
                        tol=1e-07
# getNonUniformGrid.m:34
                        v=zeros(m_0,1)
# getNonUniformGrid.m:35
                        v[1]=lx
# getNonUniformGrid.m:36
                        v[m_0]=ux
# getNonUniformGrid.m:37
                        alpha=dot(gridMultParam,(v(m_0) - v(1)))
# getNonUniformGrid.m:38
                        c1=asinh((v(1) - center) / alpha)
# getNonUniformGrid.m:39
                        c2=asinh((v(m_0) - center) / alpha)
# getNonUniformGrid.m:40
                        vtil=zeros(m_0 - 1,1)
# getNonUniformGrid.m:41
                        vtil[arange(2,m_0 - 2)]=center + dot(alpha,sinh(dot(c2 / (m_0 - 1),(arange(2,m_0 - 2))) + dot(c1,(1 - (arange(2,m_0 - 2)) / (m_0 - 1)))))
# getNonUniformGrid.m:42
                        nnot_til=1
# getNonUniformGrid.m:43
                        while vtil(nnot_til) < manualPoint:

                            nnot_til=nnot_til + 1
# getNonUniformGrid.m:45

                        nnot_til=nnot_til - 1
# getNonUniformGrid.m:47
                        v[arange(2,nnot_til)]=vtil(arange(2,nnot_til))
# getNonUniformGrid.m:48
                        v[arange(nnot_til + 2,m_0 - 1)]=vtil(arange(nnot_til + 1,m_0 - 2))
# getNonUniformGrid.m:49
                        if manualPoint - vtil(nnot_til) < tol:
                            v[nnot_til]=manualPoint
# getNonUniformGrid.m:51
                            v[nnot_til + 1]=(manualPoint + vtil(nnot_til + 1)) / 2
# getNonUniformGrid.m:52
                        else:
                            if vtil(nnot_til + 1) - manualPoint < tol:
                                v[nnot_til + 2]=manualPoint
# getNonUniformGrid.m:54
                                v[nnot_til + 1]=(v(nnot_til + 2) + v(nnot_til)) / 2
# getNonUniformGrid.m:55
                            else:
                                v[nnot_til + 1]=manualPoint
# getNonUniformGrid.m:57
    
    return v
    
if __name__ == '__main__':
    pass
    