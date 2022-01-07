# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# General_Q_Matrix_Newest.m

    
@function
def General_Q_Matrix_Newest(m_0=None,mu_func=None,sig_func=None,lx=None,ux=None,gridMethod=None,center=None,GridMultParam=None,*args,**kwargs):
    varargin = General_Q_Matrix_Newest.varargin
    nargin = General_Q_Matrix_Newest.nargin

    #GENERATES VARIANCE GRID
    
    # variance process: dv_t = mu(v_t)dt + sig(v_t)dW_t
# mu_func: function handle, mu(v)
# sig_func: function handle, sig(v)
# lx: lower variance bound
# ux: upper variance bound
# m_0: number of states (grid points)
# gridMethod: 1 for uniform spacing
#             2 for Mijatovic and Pistorious
# center: applies to gridMethod 2,3,4,5: determines where the grid points should
#           cluster.. e.g. set to v_0 or estimated mean of variance process
# gridMult: alphabar = gridmult*(v_{m_0) - v_1)
    
    nx=copy(m_0)
# General_Q_Matrix_Newest.m:16
    dx=(ux - lx) / nx
# General_Q_Matrix_Newest.m:16
    if gridMethod == 1:
        v=lx + dot((arange(1,nx)).T,dx)
# General_Q_Matrix_Newest.m:19
    else:
        if gridMethod == 2:
            v=zeros(m_0,1)
# General_Q_Matrix_Newest.m:21
            v[1]=lx
# General_Q_Matrix_Newest.m:22
            v[m_0]=ux
# General_Q_Matrix_Newest.m:22
            mid=floor(m_0 / 2)
# General_Q_Matrix_Newest.m:23
            for k in arange(2,mid).reshape(-1):
                v[k]=center + sinh(dot((1 - (k - 1) / (mid - 1)),asinh(v(1) - center)))
# General_Q_Matrix_Newest.m:25
            for k in arange(mid + 1,m_0 - 1).reshape(-1):
                v[k]=center + sinh(dot(((k - mid) / (mid)),asinh(v(m_0) - center)))
# General_Q_Matrix_Newest.m:28
        else:
            if gridMethod == 3:
                x=arange(0,1,1 / (m_0 - 1))
# General_Q_Matrix_Newest.m:31
                alpha=dot(GridMultParam,(ux - lx))
# General_Q_Matrix_Newest.m:32
                c1=asinh((lx - center) / alpha)
# General_Q_Matrix_Newest.m:33
                c2=asinh((ux - center) / alpha)
# General_Q_Matrix_Newest.m:34
                v=center + dot(alpha,(dot(c2,sinh(multiply(c2,x) + multiply(c1,(1 - x))))))
# General_Q_Matrix_Newest.m:35
            else:
                if gridMethod == 4:
                    v=zeros(m_0,1)
# General_Q_Matrix_Newest.m:37
                    v[1]=lx
# General_Q_Matrix_Newest.m:38
                    v[m_0]=ux
# General_Q_Matrix_Newest.m:39
                    alpha=dot(GridMultParam,(v(m_0) - v(1)))
# General_Q_Matrix_Newest.m:40
                    c1=asinh((v(1) - center) / alpha)
# General_Q_Matrix_Newest.m:41
                    c2=asinh((v(m_0) - center) / alpha)
# General_Q_Matrix_Newest.m:42
                    v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / m_0,(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / m_0))))
# General_Q_Matrix_Newest.m:43
                else:
                    if gridMethod == 5:
                        tol=0.0001
# General_Q_Matrix_Newest.m:45
                        v=zeros(m_0,1)
# General_Q_Matrix_Newest.m:46
                        v[1]=lx
# General_Q_Matrix_Newest.m:47
                        v[m_0]=ux
# General_Q_Matrix_Newest.m:48
                        alpha=dot(GridMultParam,(v(m_0) - v(1)))
# General_Q_Matrix_Newest.m:49
                        c1=asinh((v(1) - center) / alpha)
# General_Q_Matrix_Newest.m:50
                        c2=asinh((v(m_0) - center) / alpha)
# General_Q_Matrix_Newest.m:51
                        vtil=zeros(m_0 - 1,1)
# General_Q_Matrix_Newest.m:52
                        vtil[arange(2,m_0 - 2)]=center + dot(alpha,sinh(dot(c2 / (m_0 - 1),(arange(2,m_0 - 2))) + dot(c1,(1 - (arange(2,m_0 - 2)) / (m_0 - 1)))))
# General_Q_Matrix_Newest.m:53
                        nnot_til=1
# General_Q_Matrix_Newest.m:54
                        while vtil(nnot_til) < center:

                            nnot_til=nnot_til + 1
# General_Q_Matrix_Newest.m:56

                        nnot_til=nnot_til - 1
# General_Q_Matrix_Newest.m:58
                        v[arange(2,nnot_til)]=vtil(arange(2,nnot_til))
# General_Q_Matrix_Newest.m:59
                        v[arange(nnot_til + 2,m_0 - 1)]=vtil(arange(nnot_til + 1,m_0 - 2))
# General_Q_Matrix_Newest.m:60
                        if center - vtil(nnot_til) < tol:
                            v[nnot_til]=center
# General_Q_Matrix_Newest.m:62
                            v[nnot_til + 1]=(center + vtil(nnot_til + 1)) / 2
# General_Q_Matrix_Newest.m:63
                        else:
                            if vtil(nnot_til + 1) - center < tol:
                                v[nnot_til + 2]=center
# General_Q_Matrix_Newest.m:65
                                v[nnot_til + 1]=(v(nnot_til + 2) + v(nnot_til)) / 2
# General_Q_Matrix_Newest.m:66
                            else:
                                v[nnot_til + 1]=center
# General_Q_Matrix_Newest.m:68
    
    
    ### Now Generate Q Matrix
    Q=zeros(m_0,m_0)
# General_Q_Matrix_Newest.m:73
    mu_vec=mu_func(v)
# General_Q_Matrix_Newest.m:74
    mu_plus=max(0,mu_vec)
# General_Q_Matrix_Newest.m:75
    mu_minus=max(0,- mu_vec)
# General_Q_Matrix_Newest.m:76
    sig2=sig_func(v) ** 2
# General_Q_Matrix_Newest.m:77
    if gridMethod == 0:
        for i in arange(2,m_0 - 1).reshape(-1):
            temp=max(sig2(i) - dot(dx,(mu_minus(i) + mu_plus(i))),0) / (dot(2,dx ** 2))
# General_Q_Matrix_Newest.m:81
            Q[i,i - 1]=mu_minus(i) / dx + temp
# General_Q_Matrix_Newest.m:82
            Q[i,i + 1]=mu_plus(i) / dx + temp
# General_Q_Matrix_Newest.m:83
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# General_Q_Matrix_Newest.m:84
        Q[1,2]=abs(mu_vec(1)) / dx
# General_Q_Matrix_Newest.m:86
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / dx
# General_Q_Matrix_Newest.m:87
    else:
        H=diff(v)
# General_Q_Matrix_Newest.m:89
        for i in arange(2,m_0 - 1).reshape(-1):
            HD=H(i - 1)
# General_Q_Matrix_Newest.m:91
            HU=H(i)
# General_Q_Matrix_Newest.m:92
            AA=max(sig2(i) - (dot(HU,mu_plus(i)) + dot(HD,mu_minus(i))),0) / (HU + HD)
# General_Q_Matrix_Newest.m:93
            Q[i,i - 1]=(mu_minus(i) + AA) / HD
# General_Q_Matrix_Newest.m:94
            Q[i,i + 1]=(mu_plus(i) + AA) / HU
# General_Q_Matrix_Newest.m:95
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# General_Q_Matrix_Newest.m:96
        #     HU = H(1);   #Q(1,2) = abs(mu_vec(1))/HU;
#     HD = H(m_0-1);   #Q(m_0,m_0-1) = abs(mu_vec(m_0))/HD;
        # # #     Q(1,2) = Q(2,3);
# # #     Q(m_0,m_0-1) = Q(m_0-1,m_0-2);
        #New Boundary Behavior
        HD=H(1)
# General_Q_Matrix_Newest.m:105
        HU=H(1)
# General_Q_Matrix_Newest.m:105
        AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# General_Q_Matrix_Newest.m:106
        Q[1,2]=(mu_plus(1) + AA) / HU
# General_Q_Matrix_Newest.m:107
        HD=H(m_0 - 1)
# General_Q_Matrix_Newest.m:109
        HU=H(m_0 - 1)
# General_Q_Matrix_Newest.m:109
        AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# General_Q_Matrix_Newest.m:110
        Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# General_Q_Matrix_Newest.m:111
    
    Q[1,1]=- Q(1,2)
# General_Q_Matrix_Newest.m:114
    Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# General_Q_Matrix_Newest.m:115
    return Q,v
    
if __name__ == '__main__':
    pass
    