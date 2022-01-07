# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_RegimeSwitching_Diffusion_func.m

    
@function
def Simulate_RegimeSwitching_Diffusion_func(N_sim=None,M=None,T=None,S_0=None,drift_vec=None,sigma_vec=None,Q=None,initial_state=None,*args,**kwargs):
    varargin = Simulate_RegimeSwitching_Diffusion_func.varargin
    nargin = Simulate_RegimeSwitching_Diffusion_func.nargin

    #######################################################
# About: Simulates Paths of Regime Switching Diffusion Models
#        Uses log-Euler scheme
# Returns: paths of dimension (N_sim, M+1), since they include S_0 
#          ... Simulates N_sim paths, each row is a full path starting from S_0, ending with S_M (M+1 points in path)
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# N_sim = # paths
# M = #time steps on [0,T], time step is dt=T/M, so each path has M+1 points
# T = time to maturity, ie path is on [0,T]
# S_0 = initial underlying value (e.g. S_0=100)
# drift_vec = vector of drift coefficient by regime state, e.g. r_i - q_i, where r is interest rate in state i, and q is div yield
# sigma_vec = diffusion coefficients in each state
    
    #######################################################
    
    dt=T / M
# Simulate_RegimeSwitching_Diffusion_func.m:21
    # Initialize the CDFs used to simulate transitions between regimes
    cdfs=cumsum(expm(dot(Q,dt)).T,2)
# Simulate_RegimeSwitching_Diffusion_func.m:24
    ##################################################################################
    
    Spath=zeros(N_sim,M + 1)
# Simulate_RegimeSwitching_Diffusion_func.m:28
    Spath[arange(),1]=S_0
# Simulate_RegimeSwitching_Diffusion_func.m:29
    Sigsqdt_vec=reshape(dot(sigma_vec,sqrt(dt)),length(Q),1)
# Simulate_RegimeSwitching_Diffusion_func.m:30
    drift_vec=reshape(dot((drift_vec - dot(0.5,sigma_vec ** 2)),dt),length(Q),1)
# Simulate_RegimeSwitching_Diffusion_func.m:31
    
    prev_states=dot(initial_state,ones(N_sim,1))
# Simulate_RegimeSwitching_Diffusion_func.m:33
    for m in arange(1,M).reshape(-1):
        W1=randn(N_sim,1)
# Simulate_RegimeSwitching_Diffusion_func.m:37
        states=sim_ctmc_step(prev_states,cdfs)
# Simulate_RegimeSwitching_Diffusion_func.m:40
        prev_states=copy(states)
# Simulate_RegimeSwitching_Diffusion_func.m:41
        Sigsqdt=Sigsqdt_vec(states)
# Simulate_RegimeSwitching_Diffusion_func.m:43
        drift=drift_vec(states)
# Simulate_RegimeSwitching_Diffusion_func.m:44
        Spath[arange(),m + 1]=multiply(Spath(arange(),m),exp(drift + multiply(Sigsqdt,W1)))
# Simulate_RegimeSwitching_Diffusion_func.m:47
    
    return Spath
    
if __name__ == '__main__':
    pass
    
    
@function
def sim_ctmc_step(states=None,cdfs=None,*args,**kwargs):
    varargin = sim_ctmc_step.varargin
    nargin = sim_ctmc_step.nargin

    u=rand(size(states))
# Simulate_RegimeSwitching_Diffusion_func.m:53
    __,k=max(u <= cdfs(states,arange()),[],2,nargout=2)
# Simulate_RegimeSwitching_Diffusion_func.m:54
    
    return k
    
if __name__ == '__main__':
    pass
    
    ##################
# Non-Vectorized Version (Slow)
##################
    
    # function k = sim_ctmc_step(i, cdfs)
#     # TODO: use find instead   j_0 = find(v >= v0, 1, 'first');
#     u = rand;
#     k =find(u <= cdfs(i,:), 1, 'first');
# end
    
    # for m = 1:M
#     W1 = randn(N_sim,1); 
#     for j = 1: N_sim
#         # Simulate the next Regime
#         state = sim_ctmc_step(prev_states(j), cdfs);
#         prev_states(j) = state;
#         
#         Sigsqdt = Sigsqdt_vec(state);
#         drift = drift_vec(state);
#         
#         # Simulate Underlying With this new regime
#         Spath(j,m+1) = Spath(j,m).*exp(drift + Sigsqdt*W1(j));  #log scheme
#     end
# end
    