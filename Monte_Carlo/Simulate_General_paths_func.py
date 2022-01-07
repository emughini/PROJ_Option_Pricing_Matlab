# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_General_paths_func.m

    
@function
def Simulate_General_paths_func(N_sim=None,M=None,mult=None,T=None,S_0=None,r=None,q=None,model=None,modelParams=None,jumpModel=None,jumpParams=None,*args,**kwargs):
    varargin = Simulate_General_paths_func.varargin
    nargin = Simulate_General_paths_func.nargin

    #UNTITLED Summary of this function goes here
#   Detailed explanation goes here
    M_mult=dot(M,mult)
# Simulate_General_paths_func.m:4
    
    modelType=modelParams.modelType
# Simulate_General_paths_func.m:5
    if modelType == 1:
        Spath=Simulate_StochVol_Jumps_func(N_sim,M_mult + 1,T,S_0,r,q,model,modelParams,jumpModel,jumpParams)
# Simulate_General_paths_func.m:8
    else:
        if modelType == 2:
            sigma=modelParams.sigma
# Simulate_General_paths_func.m:11
            Spath=Simulate_Jump_Diffusion_func(N_sim,M_mult + 1,T,S_0,r,q,sigma,jumpModel,jumpParams)
# Simulate_General_paths_func.m:12
        else:
            if modelType == 3:
                Spath=Simulate_SLV_func(N_sim,M_mult + 1,T,S_0,r,q,model,modelParams)
# Simulate_General_paths_func.m:15
    
    return Spath
    
if __name__ == '__main__':
    pass
    