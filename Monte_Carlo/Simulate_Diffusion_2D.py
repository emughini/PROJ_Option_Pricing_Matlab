# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_Diffusion_2D.m

    
@function
def Simulate_Diffusion_2D(S_0s=None,drifts=None,sigmas=None,rho=None,N_sim=None,M=None,dt=None,exponential=None,*args,**kwargs):
    varargin = Simulate_Diffusion_2D.varargin
    nargin = Simulate_Diffusion_2D.nargin

    # R = correlation matrix
#
    
    paths_1=zeros(N_sim,M + 1)
# Simulate_Diffusion_2D.m:5
    paths_2=zeros(N_sim,M + 1)
# Simulate_Diffusion_2D.m:6
    paths_1[arange(),1]=S_0s(1)
# Simulate_Diffusion_2D.m:8
    paths_2[arange(),1]=S_0s(2)
# Simulate_Diffusion_2D.m:9
    if exponential == 1:
        drifts=(drifts - dot(0.5,sigmas ** 2))
# Simulate_Diffusion_2D.m:12
    
    drifts=dot(drifts,dt)
# Simulate_Diffusion_2D.m:14
    Sigsqdt=dot(sigmas,sqrt(dt))
# Simulate_Diffusion_2D.m:16
    rhosq=sqrt(1 - rho ** 2)
# Simulate_Diffusion_2D.m:17
    if exponential:
        for m in arange(1,M).reshape(-1):
            W1=randn(N_sim,1)
# Simulate_Diffusion_2D.m:21
            W2=randn(N_sim,1)
# Simulate_Diffusion_2D.m:22
            paths_1[arange(),m + 1]=multiply(paths_1(arange(),m),exp(drifts(1) + dot(Sigsqdt(1),W1)))
# Simulate_Diffusion_2D.m:24
            paths_2[arange(),m + 1]=multiply(paths_2(arange(),m),exp(drifts(2) + dot(Sigsqdt(2),(dot(rho,W1) + dot(rhosq,W2)))))
# Simulate_Diffusion_2D.m:25
    else:
        for m in arange(1,M).reshape(-1):
            W1=randn(N_sim,1)
# Simulate_Diffusion_2D.m:29
            W2=randn(N_sim,1)
# Simulate_Diffusion_2D.m:30
            paths_1[arange(),m + 1]=paths_1(arange(),m) + drifts(1) + dot(Sigsqdt(1),W1)
# Simulate_Diffusion_2D.m:32
            paths_2[arange(),m + 1]=paths_2(arange(),m) + drifts(2) + dot(Sigsqdt(2),(dot(rho,W1) + dot(rhosq,W2)))
# Simulate_Diffusion_2D.m:33
    
    
    return paths_1,paths_2
    
if __name__ == '__main__':
    pass
    