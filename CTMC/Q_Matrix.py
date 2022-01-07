# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Q_Matrix.m

    
@function
def Q_Matrix(m_0=None,mu_func=None,sig_func=None,lx=None,ux=None,gridMethod=None,center=None,GridMultParam=None,*args,**kwargs):
    varargin = Q_Matrix.varargin
    nargin = Q_Matrix.nargin

    #GENERATES VARIANCE GRID
    
    # variance process: dv_t = mu(v_t)dt + sig(v_t)dW_t
# mu_func: function handle, mu(v)
# sig_func: function handle, sig(v)
# lx: lower grid bound
# ux: upper grid bound
# m_0: number of states (grid points)
# gridMethod: 1 for uniform spacing
#             2 for Mijatovic and Pistorious
# center: applies to gridMethod 2,3,4,5: determines where the grid points should
#           cluster.. e.g. set to v_0 or estimated mean of variance process
# gridMult: alphabar = gridmult*(v_{m_0) - v_1)
    
    c_index=- 1
# Q_Matrix.m:16
    
    Q=zeros(m_0,m_0)
# Q_Matrix.m:17
    if gridMethod == 1:
        nx=copy(m_0)
# Q_Matrix.m:20
        dx=(ux - lx) / nx
# Q_Matrix.m:20
        v=lx + dot((arange(1,nx)).T,dx)
# Q_Matrix.m:21
    else:
        if gridMethod == 5 or gridMethod == 8:
            # TODO: MAKE MORE EFFICIENT... we need to build grid without searching over it, and always include center point
    # Build left half, add center, build right half: grid = [left_half; center; right_half]
            tol=1e-06
# Q_Matrix.m:26
            v[1]=lx
# Q_Matrix.m:27
            v[m_0]=ux
# Q_Matrix.m:28
            alpha=dot(GridMultParam,(v(m_0) - v(1)))
# Q_Matrix.m:29
            c1=asinh((v(1) - center) / alpha)
# Q_Matrix.m:30
            c2=asinh((v(m_0) - center) / alpha)
# Q_Matrix.m:31
            vtil=zeros(m_0 - 1,1)
# Q_Matrix.m:32
            vtil[arange(2,m_0 - 2)]=center + dot(alpha,sinh(dot(c2 / (m_0 - 1),(arange(2,m_0 - 2))) + dot(c1,(1 - (arange(2,m_0 - 2)) / (m_0 - 1)))))
# Q_Matrix.m:33
            nnot_til=2
# Q_Matrix.m:35
            while vtil(nnot_til) < center:

                nnot_til=nnot_til + 1
# Q_Matrix.m:37

            nnot_til=nnot_til - 1
# Q_Matrix.m:39
            v[arange(2,nnot_til)]=vtil(arange(2,nnot_til))
# Q_Matrix.m:40
            v[arange(nnot_til + 2,m_0 - 1)]=vtil(arange(nnot_til + 1,m_0 - 2))
# Q_Matrix.m:41
            if center - vtil(nnot_til) < tol:
                c_index=copy(nnot_til)
# Q_Matrix.m:44
                v[c_index]=center
# Q_Matrix.m:45
                v[nnot_til + 1]=(center + vtil(nnot_til + 1)) / 2
# Q_Matrix.m:46
            else:
                if vtil(nnot_til + 1) - center < tol:
                    c_index=nnot_til + 2
# Q_Matrix.m:48
                    v[c_index]=center
# Q_Matrix.m:49
                    v[nnot_til + 2]=(v(nnot_til + 2) + v(nnot_til)) / 2
# Q_Matrix.m:50
                else:
                    c_index=nnot_til + 1
# Q_Matrix.m:52
                    v[c_index]=center
# Q_Matrix.m:53
        else:
            if gridMethod == 7:
                v=zeros(1,m_0)
# Q_Matrix.m:58
                v[m_0]=ux
# Q_Matrix.m:59
                v[1]=lx
# Q_Matrix.m:60
                alpha=dot(GridMultParam,(ux - lx))
# Q_Matrix.m:61
                c1=asinh((lx - center) / alpha)
# Q_Matrix.m:62
                c2=asinh((ux - center) / alpha)
# Q_Matrix.m:63
                v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / (m_0),(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / (m_0)))))
# Q_Matrix.m:65
                c_index=1
# Q_Matrix.m:67
                while v(c_index) < center:

                    c_index=c_index + 1
# Q_Matrix.m:69

                if center != 0:
                    ratio=center / v(c_index)
# Q_Matrix.m:73
                    v=dot(v,ratio)
# Q_Matrix.m:74
                else:
                    v=v + center - v(c_index)
# Q_Matrix.m:76
    
    ### Now Generate Q Matrix
    mu_vec=mu_func(v)
# Q_Matrix.m:83
    mu_plus=max(0,mu_vec)
# Q_Matrix.m:84
    mu_minus=max(0,- mu_vec)
# Q_Matrix.m:85
    sig2=sig_func(v) ** 2
# Q_Matrix.m:86
    if gridMethod == 1:
        for i in arange(2,m_0 - 1).reshape(-1):
            temp=max(sig2(i) - dot(dx,(mu_minus(i) + mu_plus(i))),0) / (dot(2,dx ** 2))
# Q_Matrix.m:91
            Q[i,i - 1]=mu_minus(i) / dx + temp
# Q_Matrix.m:92
            Q[i,i + 1]=mu_plus(i) / dx + temp
# Q_Matrix.m:93
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix.m:94
        Q[1,2]=abs(mu_vec(1)) / dx
# Q_Matrix.m:96
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / dx
# Q_Matrix.m:97
    else:
        if gridMethod == 8:
            H=diff(v)
# Q_Matrix.m:100
            HD=H(1)
# Q_Matrix.m:101
            HU=H(1)
# Q_Matrix.m:101
            AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# Q_Matrix.m:102
            Q[1,2]=(mu_plus(1) + AA) / HU
# Q_Matrix.m:103
            Q[1,1]=- Q(1,2)
# Q_Matrix.m:104
            HD=H(m_0 - 1)
# Q_Matrix.m:106
            HU=H(m_0 - 1)
# Q_Matrix.m:106
            AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# Q_Matrix.m:107
            Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# Q_Matrix.m:108
            Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# Q_Matrix.m:109
            for i in arange(2,m_0 - 1).reshape(-1):
                dvU=v(i - 1) - v(i)
# Q_Matrix.m:112
                dvD=v(i + 1) - v(i)
# Q_Matrix.m:112
                C=concat([[1,1,1],[dvU,0,dvD],[dvU ** 2,0,dvD ** 2]])
# Q_Matrix.m:113
                z=concat([[0],[mu_vec(i)],[sig2(i)]])
# Q_Matrix.m:114
                hrow=numpy.linalg.solve(C,z)
# Q_Matrix.m:115
                Q[i,i - 1]=hrow(1)
# Q_Matrix.m:116
                Q[i,i]=hrow(2)
# Q_Matrix.m:116
                Q[i,i + 1]=hrow(3)
# Q_Matrix.m:116
        else:
            H=diff(v)
# Q_Matrix.m:121
            for i in arange(2,m_0 - 1).reshape(-1):
                HD=H(i - 1)
# Q_Matrix.m:123
                HU=H(i)
# Q_Matrix.m:124
                AA=max(sig2(i) - (dot(HU,mu_plus(i)) + dot(HD,mu_minus(i))),0) / (HU + HD)
# Q_Matrix.m:125
                Q[i,i - 1]=(mu_minus(i) + AA) / HD
# Q_Matrix.m:126
                Q[i,i + 1]=(mu_plus(i) + AA) / HU
# Q_Matrix.m:127
                Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix.m:128
            #New Boundary Behavior
            HD=H(1)
# Q_Matrix.m:132
            HU=H(1)
# Q_Matrix.m:132
            AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# Q_Matrix.m:133
            Q[1,2]=(mu_plus(1) + AA) / HU
# Q_Matrix.m:134
            HD=H(m_0 - 1)
# Q_Matrix.m:136
            HU=H(m_0 - 1)
# Q_Matrix.m:136
            AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# Q_Matrix.m:137
            Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# Q_Matrix.m:138
    
    Q[1,1]=- Q(1,2)
# Q_Matrix.m:142
    Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# Q_Matrix.m:143
    return Q,v,c_index
    
if __name__ == '__main__':
    pass
    