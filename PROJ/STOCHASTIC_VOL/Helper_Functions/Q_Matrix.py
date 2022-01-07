# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Q_Matrix.m

    
@function
def Q_Matrix(m_0=None,mu_func=None,sig_func=None,lx=None,ux=None,gridMethod=None,center=None,GridMultParam=None,boundaryMethod=None,*args,**kwargs):
    varargin = Q_Matrix.varargin
    nargin = Q_Matrix.nargin

    #GENERATES VARIANCE GRID
    
    # NOTE: This is a newer research version, not yet stable
    
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
# boundaryMethod: 1 = original boundary method, 2 = newer approach
    
    if nargin < 8:
        boundaryMethod=1
# Q_Matrix.m:20
    
    c_index=- 1
# Q_Matrix.m:23
    
    Q=zeros(m_0,m_0)
# Q_Matrix.m:24
    if gridMethod == 1:
        nx=copy(m_0)
# Q_Matrix.m:27
        dx=(ux - lx) / nx
# Q_Matrix.m:27
        v=lx + dot((arange(1,nx)).T,dx)
# Q_Matrix.m:28
    else:
        if gridMethod == 5 or gridMethod == 8 or gridMethod == 9:
            ### Tavella and Randall PLUS we put center (e.g. v0) on grid
    # TODO: MAKE MORE EFFICIENT... we need to build grid without searching over it, and always include center point
    # Build left half, add center, build right half: grid = [left_half; center; right_half]
            tol=1e-05
# Q_Matrix.m:34
            v[1]=lx
# Q_Matrix.m:35
            v[m_0]=ux
# Q_Matrix.m:36
            alpha=dot(GridMultParam,(v(m_0) - v(1)))
# Q_Matrix.m:37
            c1=asinh((v(1) - center) / alpha)
# Q_Matrix.m:38
            c2=asinh((v(m_0) - center) / alpha)
# Q_Matrix.m:39
            vtil=zeros(m_0 - 1,1)
# Q_Matrix.m:40
            vtil[arange(2,m_0 - 2)]=center + dot(alpha,sinh(dot(c2 / (m_0 - 1),(arange(2,m_0 - 2))) + dot(c1,(1 - (arange(2,m_0 - 2)) / (m_0 - 1)))))
# Q_Matrix.m:41
            nnot_til=1
# Q_Matrix.m:43
            while vtil(nnot_til) < center:

                nnot_til=nnot_til + 1
# Q_Matrix.m:45

            nnot_til=nnot_til - 1
# Q_Matrix.m:47
            v[arange(2,nnot_til)]=vtil(arange(2,nnot_til))
# Q_Matrix.m:48
            v[arange(nnot_til + 2,m_0 - 1)]=vtil(arange(nnot_til + 1,m_0 - 2))
# Q_Matrix.m:49
            #     v(1:nnot_til) = vtil(1:nnot_til);
#     v(nnot_til + 2: m_0) = vtil(nnot_til + 1: m_0 - 1);
            if center - vtil(nnot_til) < tol:
                c_index=copy(nnot_til)
# Q_Matrix.m:54
                v[c_index]=center
# Q_Matrix.m:55
                v[nnot_til + 1]=(center + vtil(nnot_til + 1)) / 2
# Q_Matrix.m:56
            else:
                if vtil(nnot_til + 1) - center < tol:
                    c_index=nnot_til + 2
# Q_Matrix.m:58
                    v[c_index]=center
# Q_Matrix.m:59
                    v[nnot_til + 1]=(v(nnot_til + 2) + v(nnot_til)) / 2
# Q_Matrix.m:60
                else:
                    c_index=nnot_til + 1
# Q_Matrix.m:62
                    v[c_index]=center
# Q_Matrix.m:63
        else:
            if gridMethod == 7:
                v=zeros(1,m_0)
# Q_Matrix.m:68
                v[m_0]=ux
# Q_Matrix.m:69
                v[1]=lx
# Q_Matrix.m:70
                alpha=dot(GridMultParam,(ux - lx))
# Q_Matrix.m:71
                c1=asinh((lx - center) / alpha)
# Q_Matrix.m:72
                c2=asinh((ux - center) / alpha)
# Q_Matrix.m:73
                v[arange(2,m_0 - 1)]=center + dot(alpha,sinh(dot(c2 / (m_0),(arange(2,m_0 - 1))) + dot(c1,(1 - (arange(2,m_0 - 1)) / (m_0)))))
# Q_Matrix.m:75
                c_index=1
# Q_Matrix.m:77
                while v(c_index) < center:

                    c_index=c_index + 1
# Q_Matrix.m:79

                #     # Stretch the grid either up or down, by the least ammount possible
#     if center - v(c_index) < v(c_index + 1) - center
#         ratio = center / v(c_index);   # in this case, go down
#     else
#         ratio = v(c_index) / center;
#     end
                if center != 0:
                    ratio=center / v(c_index)
# Q_Matrix.m:90
                    v=dot(v,ratio)
# Q_Matrix.m:91
                else:
                    v=v + center - v(c_index)
# Q_Matrix.m:93
    
    ### Now Generate Q Matrix
    mu_vec=mu_func(v)
# Q_Matrix.m:100
    mu_plus=max(0,mu_vec)
# Q_Matrix.m:101
    mu_minus=max(0,- mu_vec)
# Q_Matrix.m:102
    sig2=sig_func(v) ** 2
# Q_Matrix.m:103
    if gridMethod == 1:
        for i in arange(2,m_0 - 1).reshape(-1):
            temp=max(sig2(i) - dot(dx,(mu_minus(i) + mu_plus(i))),0) / (dot(2,dx ** 2))
# Q_Matrix.m:108
            Q[i,i - 1]=mu_minus(i) / dx + temp
# Q_Matrix.m:109
            Q[i,i + 1]=mu_plus(i) / dx + temp
# Q_Matrix.m:110
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix.m:111
        Q[1,2]=abs(mu_vec(1)) / dx
# Q_Matrix.m:113
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / dx
# Q_Matrix.m:114
    else:
        if gridMethod == 8:
            H=diff(v)
# Q_Matrix.m:118
            HD=H(1)
# Q_Matrix.m:119
            HU=H(1)
# Q_Matrix.m:119
            AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# Q_Matrix.m:120
            Q[1,2]=(mu_plus(1) + AA) / HU
# Q_Matrix.m:121
            Q[1,1]=- Q(1,2)
# Q_Matrix.m:122
            HD=H(m_0 - 1)
# Q_Matrix.m:124
            HU=H(m_0 - 1)
# Q_Matrix.m:124
            AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# Q_Matrix.m:125
            Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# Q_Matrix.m:126
            Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# Q_Matrix.m:127
            for i in arange(2,m_0 - 1).reshape(-1):
                dvU=v(i - 1) - v(i)
# Q_Matrix.m:131
                dvD=v(i + 1) - v(i)
# Q_Matrix.m:131
                C=concat([[1,1,1],[dvU,0,dvD],[dvU ** 2,0,dvD ** 2]])
# Q_Matrix.m:132
                z=concat([[0],[mu_vec(i)],[sig2(i)]])
# Q_Matrix.m:133
                hrow=numpy.linalg.solve(C,z)
# Q_Matrix.m:134
                Q[i,i - 1]=hrow(1)
# Q_Matrix.m:135
                Q[i,i]=hrow(2)
# Q_Matrix.m:135
                Q[i,i + 1]=hrow(3)
# Q_Matrix.m:135
        else:
            H=diff(v)
# Q_Matrix.m:139
            if gridMethod == 9:
                for i in arange(2,m_0 - 1).reshape(-1):
                    HD=H(i - 1)
# Q_Matrix.m:142
                    HU=H(i)
# Q_Matrix.m:143
                    Q[i,i - 1]=(sig2(i) - dot(HU,mu_vec(i))) / (dot(HD,(HU + HD)))
# Q_Matrix.m:144
                    Q[i,i + 1]=(sig2(i) + dot(HD,mu_vec(i))) / (dot(HU,(HU + HD)))
# Q_Matrix.m:145
                    Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix.m:146
            else:
                for i in arange(2,m_0 - 1).reshape(-1):
                    HD=H(i - 1)
# Q_Matrix.m:150
                    HU=H(i)
# Q_Matrix.m:151
                    AA=max(sig2(i) - (dot(HU,mu_plus(i)) + dot(HD,mu_minus(i))),0) / (HU + HD)
# Q_Matrix.m:152
                    Q[i,i - 1]=(mu_minus(i) + AA) / HD
# Q_Matrix.m:153
                    Q[i,i + 1]=(mu_plus(i) + AA) / HU
# Q_Matrix.m:154
                    Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# Q_Matrix.m:155
            if boundaryMethod == 1:
                HU=H(1)
# Q_Matrix.m:160
                Q[1,2]=abs(mu_vec(1)) / HU
# Q_Matrix.m:161
                HD=H(m_0 - 1)
# Q_Matrix.m:163
                Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / HD
# Q_Matrix.m:164
            else:
                if boundaryMethod == 2:
                    HD=H(1)
# Q_Matrix.m:167
                    HU=H(1)
# Q_Matrix.m:167
                    AA=max(sig2(1) - (dot(HU,mu_plus(1)) + dot(HD,mu_minus(1))),0) / (HU + HD)
# Q_Matrix.m:168
                    Q[1,2]=(mu_plus(1) + AA) / HU
# Q_Matrix.m:169
                    HD=H(m_0 - 1)
# Q_Matrix.m:171
                    HU=H(m_0 - 1)
# Q_Matrix.m:171
                    AA=max(sig2(m_0) - (dot(HU,mu_plus(m_0)) + dot(HD,mu_minus(m_0))),0) / (HU + HD)
# Q_Matrix.m:172
                    Q[m_0,m_0 - 1]=(mu_plus(m_0) + AA) / HU
# Q_Matrix.m:173
                else:
                    if boundaryMethod == 3:
                        HU=H(1)
# Q_Matrix.m:176
                        Q[1,2]=sig2(1) / HU ** 2
# Q_Matrix.m:177
                        HD=H(m_0 - 1)
# Q_Matrix.m:179
                        Q[m_0,m_0 - 1]=sig2(m_0) / HD ** 2
# Q_Matrix.m:180
                    else:
                        if boundaryMethod == 4:
                            Q[1,2]=0
# Q_Matrix.m:182
                            Q[m_0,m_0 - 1]=0
# Q_Matrix.m:183
    
    Q[1,1]=- Q(1,2)
# Q_Matrix.m:187
    Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# Q_Matrix.m:188
    return Q,v,c_index
    
if __name__ == '__main__':
    pass
    