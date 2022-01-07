# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# getGenerator_Q_MatrixOnly.m

    
@function
def getGenerator_Q_MatrixOnly(v=None,mu_func=None,sig_func=None,gridMethod=None,*args,**kwargs):
    varargin = getGenerator_Q_MatrixOnly.varargin
    nargin = getGenerator_Q_MatrixOnly.nargin

    #UNTITLED2 Summary of this function goes here
#   Detailed explanation goes here
    
    ### Now Generate Q Matrix
    m_0=length(v)
# getGenerator_Q_MatrixOnly.m:6
    Q=zeros(m_0,m_0)
# getGenerator_Q_MatrixOnly.m:7
    mu_vec=mu_func(v)
# getGenerator_Q_MatrixOnly.m:8
    mu_plus=max(0,mu_vec)
# getGenerator_Q_MatrixOnly.m:9
    mu_minus=max(0,- mu_vec)
# getGenerator_Q_MatrixOnly.m:10
    sig2=sig_func(v) ** 2
# getGenerator_Q_MatrixOnly.m:11
    if gridMethod == 0:
        for i in arange(2,m_0 - 1).reshape(-1):
            temp=max(sig2(i) - dot(dx,(mu_minus(i) + mu_plus(i))),0) / (dot(2,dx ** 2))
# getGenerator_Q_MatrixOnly.m:15
            Q[i,i - 1]=mu_minus(i) / dx + temp
# getGenerator_Q_MatrixOnly.m:16
            Q[i,i + 1]=mu_plus(i) / dx + temp
# getGenerator_Q_MatrixOnly.m:17
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# getGenerator_Q_MatrixOnly.m:18
        Q[1,2]=abs(mu_vec(1)) / dx
# getGenerator_Q_MatrixOnly.m:20
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / dx
# getGenerator_Q_MatrixOnly.m:21
    else:
        H=diff(v)
# getGenerator_Q_MatrixOnly.m:23
        for i in arange(2,m_0 - 1).reshape(-1):
            HD=H(i - 1)
# getGenerator_Q_MatrixOnly.m:25
            HU=H(i)
# getGenerator_Q_MatrixOnly.m:26
            AA=max(sig2(i) - (dot(HU,mu_plus(i)) + dot(HD,mu_minus(i))),0) / (HU + HD)
# getGenerator_Q_MatrixOnly.m:27
            Q[i,i - 1]=(mu_minus(i) + AA) / HD
# getGenerator_Q_MatrixOnly.m:28
            Q[i,i + 1]=(mu_plus(i) + AA) / HU
# getGenerator_Q_MatrixOnly.m:29
            Q[i,i]=- Q(i,i - 1) - Q(i,i + 1)
# getGenerator_Q_MatrixOnly.m:30
        HU=H(1)
# getGenerator_Q_MatrixOnly.m:32
        Q[1,2]=abs(mu_vec(1)) / HU
# getGenerator_Q_MatrixOnly.m:32
        HD=H(m_0 - 1)
# getGenerator_Q_MatrixOnly.m:33
        Q[m_0,m_0 - 1]=abs(mu_vec(m_0)) / HD
# getGenerator_Q_MatrixOnly.m:33
    
    Q[1,1]=- Q(1,2)
# getGenerator_Q_MatrixOnly.m:35
    Q[m_0,m_0]=- Q(m_0,m_0 - 1)
# getGenerator_Q_MatrixOnly.m:36
    return Q
    
if __name__ == '__main__':
    pass
    