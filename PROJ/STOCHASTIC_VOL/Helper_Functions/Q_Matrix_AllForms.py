# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Q_Matrix_AllForms.m

    
@function
def Q_Matrix_AllForms(m_0=None,mu_func=None,sig_func=None,lx=None,ux=None,gridMethod=None,gridMultParam=None,center=None,boundaryMethod=None,*args,**kwargs):
    varargin = Q_Matrix_AllForms.varargin
    nargin = Q_Matrix_AllForms.nargin

    #GENERATES VARIANCE GRID v and generator matrix Q
    
    # variance process: dv_t = mu(v_t)dt + sig(v_t)dW_t
# mu_func: function handle, mu(v)
# sig_func: function handle, sig(v)
# lx: lower variance bound
# ux: upper variance bound
# m_0: number of states (grid points)
# gridMethod: 1 for uniform spacing
#             2 for Mijatovic and Pistorious ...
# gridMultParam: set within (0,1), closer to 1 is more uniform grid, closer to zero is more nonuniform, clustered at center
# 
# center: applies to gridMethod 2,3,4,5: determines where the grid points should
#           cluster.. e.g. set to v_0 or estimated mean of variance process
# boundaryMethod: 1 = original boundary method, 2 = newer approach
    
    if nargin < 9:
        boundaryMethod=1
# Q_Matrix_AllForms.m:19
    
    nx=copy(m_0)
# Q_Matrix_AllForms.m:22
    dx=(ux - lx) / nx
# Q_Matrix_AllForms.m:22
    #==========================
# Step 1): Generate Grid
#==========================
    if gridMethod == 1:
        v=lx + dot((arange(1,nx)).T,dx)
# Q_Matrix_AllForms.m:28
    else:
        if gridMethod == 2:
            v=zeros(m_0,1)
# Q_Matrix_AllForms.m:31
            v[1]=lx
# Q_Matrix_AllForms.m:32
            v[m_0]=ux
# Q_Matrix_AllForms.m:32
            mid=floor(m_0 / 2)
# Q_Matrix_AllForms.m:33
            for k in arange(2,mid).reshape(-1):
                v[k]=center + sinh(dot((1 - (k - 1) / (mid - 1)),asinh(v(1) - center)))
# Q_Matrix_AllForms.m:35
            for k in arange(mid + 1,m_0 - 1).reshape(-1):
                v[k]=center + sinh(dot(((k - mid) / (mid)),asinh(v(m_0) - center)))
# Q_Matrix_AllForms.m:38
        else:
            if gridMethod == 3:
                x=arange(0,1,1 / (m_0 - 1))
# Q_Matrix_AllForms.m:42
                alpha=dot(gridMultParam,(ux - lx))
# Q_Matrix_AllForms.m:43
                c1=asinh((lx - center) / alpha)
# Q_Matrix_AllForms.m:44
                c2=asinh((ux - center) / alpha)
# Q_Matrix_AllForms.m:45
                v=center + dot(alpha,(dot(c2,sinh(multiply(c2,x) + multiply(c1,(1 - x))))))
# Q_Matrix_AllForms.m:46
            else:
                if gridMethod == 4:
                    v=zeros(m_0,1)
# Q_Matrix_AllForms.m:49
                    v[1]=lx
# Q_Matrix_AllForms.m:50
                    v[m_0]=ux
# Q_Matrix_AllForms.m:51
                    alpha=dot(gridMultParam,(v(m_0) - v(1)))
# Q_Matrix_AllForms.m:52
                    c1=asinh((v(1) - center) / alpha)
# Q_Matrix_AllForms.m:53
                    c2=asinh((v(m_0) - center) / alpha)
# Q_Matrix_AllForms.m:54
                    v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / m_0,(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / m_0))))
# Q_Matrix_AllForms.m:55
                else:
                    if gridMethod == 5:
                        v=zeros(m_0,1)
# Q_Matrix_AllForms.m:58
                        v[1]=lx
# Q_Matrix_AllForms.m:59
                        v[m_0]=ux
# Q_Matrix_AllForms.m:60
                        alpha=dot(gridMultParam,(v(m_0) - v(1)))
# Q_Matrix_AllForms.m:61
                        c1=asinh((v(1) - center) / alpha)
# Q_Matrix_AllForms.m:62
                        c2=asinh((v(m_0) - center) / alpha)
# Q_Matrix_AllForms.m:63
                        vtil=zeros(m_0 - 1,1)
# Q_Matrix_AllForms.m:64
                        vtil[arange(2,m_0 - 2)]=center + dot(alpha,sinh(dot(c2 / (m_0 - 1),(arange(2,m_0 - 2))) + dot(c1,(1 - (arange(2,m_0 - 2)) / (m_0 - 1)))))
# Q_Matrix_AllForms.m:65
                        nnot_til=1
# Q_Matrix_AllForms.m:66
                        while vtil(nnot_til) < center:

                            nnot_til=nnot_til + 1
# Q_Matrix_AllForms.m:68

                        nnot_til=nnot_til - 1
# Q_Matrix_AllForms.m:70
                        v[arange(2,nnot_til)]=vtil(arange(2,nnot_til))
# Q_Matrix_AllForms.m:71
                        v[nnot_til + 1]=center
# Q_Matrix_AllForms.m:72
                        v[arange(nnot_til + 2,m_0 - 1)]=vtil(arange(nnot_til + 1,m_0 - 2))
# Q_Matrix_AllForms.m:73
                    else:
                        if gridMethod == 6:
                            v=zeros(m_0,1)
# Q_Matrix_AllForms.m:76
                            v[1]=lx
# Q_Matrix_AllForms.m:77
                            v[m_0]=ux
# Q_Matrix_AllForms.m:78
                            alpha=dot(gridMultParam,(v(m_0) - v(1)))
# Q_Matrix_AllForms.m:79
                            c1=asinh((v(1) - center) / alpha)
# Q_Matrix_AllForms.m:80
                            c2=asinh((v(m_0) - center) / alpha)
# Q_Matrix_AllForms.m:81
                            v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / m_0,(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / m_0))))
# Q_Matrix_AllForms.m:82
                            nnot_til=1
# Q_Matrix_AllForms.m:83
                            while v(nnot_til) < center:

                                nnot_til=nnot_til + 1
# Q_Matrix_AllForms.m:85

                            nnot_til=nnot_til - 1
# Q_Matrix_AllForms.m:87
                            shift_=center - v(nnot_til)
# Q_Matrix_AllForms.m:88
                            v[arange(3,end())]=v(arange(3,end())) + shift_
# Q_Matrix_AllForms.m:90
    
    #==========================
# Step 2): Generate Q (rate) Matrix
#==========================
    Q=zeros(m_0,m_0)
# Q_Matrix_AllForms.m:96
    mu_vec=mu_func(v)
# Q_Matrix_AllForms.m:97
    mu_plus=max(0,mu_vec)
# Q_Matrix_AllForms.m:98
    mu_minus=max(0,- mu_vec)
# Q_Matrix_AllForms.m:99
    sig2=sig_func(v) ** 2
# Q_Matrix_AllForms.m:100
    if gridMethod == 0:
        for i in arange(2,m_0 - 1).reshape(-1):
            temp=max(sig2(i) - dot(dx,(mu_minus(i) + mu_plus(i))),0) / (dot(2,dx ** 2))
# Q_Matrix_AllForms.m:104
            Q[i,i - 1]=mu_minus(i) / dx + temp
# Q_Matrix_AllForms.m:105
            Q[i,i + 1]=mu_plus(i) / dx + temp
# Q_Matrix_AllForms.m:106
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix_AllForms.m:107
        Q[1,2]=abs(mu_vec(1)) / dx
# Q_Matrix_AllForms.m:109
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / dx
# Q_Matrix_AllForms.m:110
    else:
        H=diff(v)
# Q_Matrix_AllForms.m:113
        for i in arange(2,m_0 - 1).reshape(-1):
            HD=H(i - 1)
# Q_Matrix_AllForms.m:115
            HU=H(i)
# Q_Matrix_AllForms.m:116
            AA=max(sig2(i) - (dot(HU,mu_plus(i)) + dot(HD,mu_minus(i))),0) / (HU + HD)
# Q_Matrix_AllForms.m:117
            Q[i,i - 1]=(mu_minus(i) + AA) / HD
# Q_Matrix_AllForms.m:118
            Q[i,i + 1]=(mu_plus(i) + AA) / HU
# Q_Matrix_AllForms.m:119
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix_AllForms.m:120
        if boundaryMethod == 1:
            HU=H(1)
# Q_Matrix_AllForms.m:124
            Q[1,2]=abs(mu_vec(1)) / HU
# Q_Matrix_AllForms.m:125
            HD=H(m_0 - 1)
# Q_Matrix_AllForms.m:127
            Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / HD
# Q_Matrix_AllForms.m:128
        else:
            if boundaryMethod == 2:
                HD=H(1)
# Q_Matrix_AllForms.m:131
                HU=H(1)
# Q_Matrix_AllForms.m:131
                AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# Q_Matrix_AllForms.m:132
                Q[1,2]=(mu_plus(1) + AA) / HU
# Q_Matrix_AllForms.m:133
                HD=H(m_0 - 1)
# Q_Matrix_AllForms.m:135
                HU=H(m_0 - 1)
# Q_Matrix_AllForms.m:135
                AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# Q_Matrix_AllForms.m:136
                Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# Q_Matrix_AllForms.m:137
            else:
                if boundaryMethod == 3:
                    HU=H(1)
# Q_Matrix_AllForms.m:140
                    Q[1,2]=sig2(1) / HU ** 2
# Q_Matrix_AllForms.m:141
                    HD=H(m_0 - 1)
# Q_Matrix_AllForms.m:143
                    Q[m_0,m_0 - 1]=sig2(m_0) / HD ** 2
# Q_Matrix_AllForms.m:144
                else:
                    if boundaryMethod == 4:
                        Q[1,2]=0
# Q_Matrix_AllForms.m:146
                        Q[m_0,m_0 - 1]=0
# Q_Matrix_AllForms.m:147
    
    Q[1,1]=- Q(1,2)
# Q_Matrix_AllForms.m:151
    Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# Q_Matrix_AllForms.m:152
    return Q,v
    
if __name__ == '__main__':
    pass
    