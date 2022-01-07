# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Simulate_RegimeSwitching_Diffusion_Unbiased.m

    
@function
def Simulate_RegimeSwitching_Diffusion_Unbiased(N_sim=None,T=None,S_0=None,drift_vec=None,sigma_vec=None,Q=None,initial_state=None,*args,**kwargs):
    varargin = Simulate_RegimeSwitching_Diffusion_Unbiased.varargin
    nargin = Simulate_RegimeSwitching_Diffusion_Unbiased.nargin

    #######################################################
# About: Simulates Terminal Value (S_T) of Regime Switching Diffusion Models
#        This scheme is unbiased, but only generates the terminal S values
# Returns: vector of size N_sim
# Author: Justin Lars Kirkby
    
    # -----------------
# Params
# -----------------
# N_sim = # samples
# T = time to maturity, ie path is on [0,T]
# S_0 = initial underlying value (e.g. S_0=100)
# drift_vec = vector of drift coefficient by regime state, e.g. r_i - q_i, where r is interest rate in state i, and q is div yield
# sigma_vec = diffusion coefficients in each state
    
    #######################################################
    
    Svals=zeros(N_sim,1)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:19
    lambdas=- diag(Q)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:20
    
    P=(Q + diag(lambdas)) / lambdas
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:21
    
    cdfs=cumsum(P,2)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:22
    for n in arange(1,N_sim).reshape(-1):
        S=copy(S_0)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:25
        t_last=0
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:26
        state=copy(initial_state)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:27
        while t_last < T:

            tau=exprnd(lambdas(state))
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:29
            t=min(T,t_last + tau)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:30
            tau=t - t_last
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:31
            Sigsqdt=dot(sigma_vec(state),sqrt(tau))
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:33
            drift=dot((drift_vec(state) - dot(0.5,sigma_vec(state) ** 2)),tau)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:34
            S=multiply(S,exp(drift + dot(Sigsqdt,randn())))
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:36
            state=next_state(cdfs(state,arange()))
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:37
            t_last=copy(t)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:38

        Svals[n]=S
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:40
    
    return Svals
    
if __name__ == '__main__':
    pass
    
    
@function
def next_state(cdf=None,*args,**kwargs):
    varargin = next_state.varargin
    nargin = next_state.nargin

    u=rand()
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:46
    j=find(u <= cdf,1)
# Simulate_RegimeSwitching_Diffusion_Unbiased.m:47
    return j
    
if __name__ == '__main__':
    pass
    