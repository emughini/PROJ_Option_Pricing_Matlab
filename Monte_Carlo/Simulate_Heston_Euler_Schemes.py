# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_Heston_Euler_Schemes.m

    
@function
def Simulate_Heston_Euler_Schemes(N_sim=None,M=None,T=None,S_0=None,r=None,q=None,SVModelParams=None,scheme=None,*args,**kwargs):
    varargin = Simulate_Heston_Euler_Schemes.varargin
    nargin = Simulate_Heston_Euler_Schemes.nargin

    # Simulates Paths of Heston Model under various Euler Schemes
# See Lord et al (2010) for details
# N_sim = # paths
# M = #time steps on [0,T], ie dt =T/M   
# Note: returns paths of dimension (N_sim,M+1), since they include S_0
    
    # scheme:     
#        1 = Absorbption
#        2 = Reflection
#        3 = Higham and Mao
#        4 = Partial Truncation
#        5 = Full Truncation  (Least Bias)
    
    #==============================
# Initialize Params/Vectors
#==============================
    
    if nargin < 8:
        scheme=5
# Simulate_Heston_Euler_Schemes.m:20
    
    Sigmav=SVModelParams.Sigmav
# Simulate_Heston_Euler_Schemes.m:23
    v0=SVModelParams.v0
# Simulate_Heston_Euler_Schemes.m:24
    rho=SVModelParams.rho
# Simulate_Heston_Euler_Schemes.m:25
    theta=SVModelParams.theta
# Simulate_Heston_Euler_Schemes.m:26
    eta=SVModelParams.eta
# Simulate_Heston_Euler_Schemes.m:27
    Spath=zeros(N_sim,M + 1)
# Simulate_Heston_Euler_Schemes.m:30
    Spath[arange(),1]=S_0
# Simulate_Heston_Euler_Schemes.m:31
    dt=T / M
# Simulate_Heston_Euler_Schemes.m:33
    sqdt=sqrt(dt)
# Simulate_Heston_Euler_Schemes.m:34
    sqdtrho1=dot(sqdt,rho)
# Simulate_Heston_Euler_Schemes.m:35
    sqdtrho2=dot(sqdt,sqrt(1 - rho ** 2))
# Simulate_Heston_Euler_Schemes.m:36
    Zeta=r - q
# Simulate_Heston_Euler_Schemes.m:38
    edt=dot(eta,dt)
# Simulate_Heston_Euler_Schemes.m:40
    coeffv=1 - dot(eta,dt)
# Simulate_Heston_Euler_Schemes.m:41
    
    driftdt=dot(dot(eta,theta),dt)
# Simulate_Heston_Euler_Schemes.m:42
    vOld=dot(v0,ones(N_sim,1))
# Simulate_Heston_Euler_Schemes.m:44
    
    sqvOld=dot(sqrt(v0),ones(N_sim,1))
# Simulate_Heston_Euler_Schemes.m:45
    if scheme == 1:
        for m in arange(1,M).reshape(-1):
            W1=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:49
            W2=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:49
            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_Heston_Euler_Schemes.m:50
            vNew=driftdt + dot(vOld,coeffv) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_Heston_Euler_Schemes.m:52
            vOld=max(0,vNew)
# Simulate_Heston_Euler_Schemes.m:54
            sqvOld=sqrt(vOld)
# Simulate_Heston_Euler_Schemes.m:55
    else:
        if scheme == 2:
            for m in arange(1,M).reshape(-1):
                W1=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:61
                W2=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:61
                Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,vOld)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_Heston_Euler_Schemes.m:62
                vNew=driftdt + dot(vOld,coeffv) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_Heston_Euler_Schemes.m:64
                vOld=abs(vNew)
# Simulate_Heston_Euler_Schemes.m:65
                sqvOld=sqrt(vOld)
# Simulate_Heston_Euler_Schemes.m:67
        else:
            if scheme == 3:
                for m in arange(1,M).reshape(-1):
                    W1=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:73
                    W2=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:73
                    Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,sqvOld ** 2)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_Heston_Euler_Schemes.m:74
                    vNew=driftdt + dot(vOld,coeffv) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_Heston_Euler_Schemes.m:76
                    vOld=copy(vNew)
# Simulate_Heston_Euler_Schemes.m:77
                    sqvOld=sqrt(abs(vOld))
# Simulate_Heston_Euler_Schemes.m:79
            else:
                if scheme == 4:
                    for m in arange(1,M).reshape(-1):
                        W1=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:85
                        W2=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:85
                        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,sqvOld ** 2)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_Heston_Euler_Schemes.m:86
                        vNew=driftdt + dot(vOld,coeffv) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_Heston_Euler_Schemes.m:88
                        vOld=copy(vNew)
# Simulate_Heston_Euler_Schemes.m:90
                        sqvOld=sqrt(max(0,vOld))
# Simulate_Heston_Euler_Schemes.m:91
                else:
                    if scheme == 5:
                        for m in arange(1,M).reshape(-1):
                            W1=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:97
                            W2=randn(N_sim,1)
# Simulate_Heston_Euler_Schemes.m:97
                            Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(dot((Zeta - dot(0.5,sqvOld ** 2)),dt) + multiply(dot(sqdt,sqvOld),W1)))
# Simulate_Heston_Euler_Schemes.m:98
                            vNew=vOld - dot(edt,(max(0,vOld) - theta)) + multiply(dot(Sigmav,sqvOld),(dot(sqdtrho1,W1) + dot(sqdtrho2,W2)))
# Simulate_Heston_Euler_Schemes.m:100
                            vOld=copy(vNew)
# Simulate_Heston_Euler_Schemes.m:101
                            sqvOld=sqrt(max(0,vOld))
# Simulate_Heston_Euler_Schemes.m:102
    