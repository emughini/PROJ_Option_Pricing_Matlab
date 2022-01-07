# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# SABR_European_AntonovApprox.m

    
@function
def SABR_European_AntonovApprox(f=None,K=None,T=None,call=None,r=None,ModParams=None,UB=None,*args,**kwargs):
    varargin = SABR_European_AntonovApprox.varargin
    nargin = SABR_European_AntonovApprox.nargin

    # About: Price European Option under SABR model using Antonov approximation
# K: strike
# f: initial forward value
# call: 1 if call option, else put-call
# ModParams: container of model parameters (.beta, .alpha, .v0, .rho)
# UB: upper bound numerical parameter (optional)
    
    if nargin < 7:
        UB=100
# SABR_European_AntonovApprox.m:10
    
    beta=ModParams.beta
# SABR_European_AntonovApprox.m:13
    alpha=ModParams.alpha
# SABR_European_AntonovApprox.m:14
    v0=ModParams.v0
# SABR_European_AntonovApprox.m:15
    rho=ModParams.rho
# SABR_European_AntonovApprox.m:16
    mimic_parameters=mimicprocess(f,v0,beta,rho,alpha,K,T)
# SABR_European_AntonovApprox.m:18
    
    price=Vcallapprox(f,mimic_parameters(1),mimic_parameters(2),mimic_parameters(3),K,T,UB)
# SABR_European_AntonovApprox.m:19
    
    price=dot(exp(dot(- r,T)),price)
# SABR_European_AntonovApprox.m:20
    if call != 1:
        price=price - dot(exp(dot(- r,T)),(f - K))
# SABR_European_AntonovApprox.m:23
    
    return price
    
if __name__ == '__main__':
    pass
    
    
@function
def Vcallapprox(f=None,v0=None,beta=None,nu=None,K=None,T=None,UB=None,*args,**kwargs):
    varargin = Vcallapprox.varargin
    nargin = Vcallapprox.nargin

    # Function to calculate the forward value of an European call with
# Antonov's method in the zero correlation case and with G approximated by
# (11)
    
    #f     = initial forward value
#v0    = initial volatility 
#beta  = exponent
#nu    = vol-vol
#correlation rho is assumed to be zero
    
    q=K ** (1 - beta) / (1 - beta)
# SABR_European_AntonovApprox.m:38
    q0=f ** (1 - beta) / (1 - beta)
# SABR_European_AntonovApprox.m:39
    smin=asinh(dot(nu,abs(q - q0)) / v0)
# SABR_European_AntonovApprox.m:40
    splus=asinh(dot(nu,(q + q0)) / v0)
# SABR_European_AntonovApprox.m:41
    eta=abs(1 / (dot(2,(beta - 1))))
# SABR_European_AntonovApprox.m:42
    g=lambda s=None: multiply(s,coth(s)) - 1
# SABR_European_AntonovApprox.m:44
    R=lambda t=None,s=None: 1 + dot(dot(3,t),g(s)) / (dot(8,s ** 2)) - dot(dot(5,t ** 2),(dot(- 8,s ** 2) + dot(3,g(s) ** 2) + dot(24,g(s)))) / (dot(128,s ** 4)) + dot(dot(35,t ** 3),(dot(- 40,s ** 2) + dot(3,g(s) ** 3) + dot(24,g(s) ** 2) + dot(120,g(s)))) / (dot(1024,s ** 6))
# SABR_European_AntonovApprox.m:45
    dR=lambda t=None,s=None: exp(t / 8) - (3072 + dot(384,t) + dot(24,t ** 2) + t ** 3) / 3072
# SABR_European_AntonovApprox.m:46
    G=lambda t=None,s=None: multiply(multiply(sqrt(sinh(s) / s),exp(- s ** 2 / (dot(2,t)) - t / 8)),(R(t,s) + dR(t,s)))
# SABR_European_AntonovApprox.m:47
    phi=lambda s=None: dot(2,atan(sqrt((sinh(s) ** 2 - sinh(smin) ** 2) / (sinh(splus) ** 2 - sinh(s) ** 2))))
# SABR_European_AntonovApprox.m:49
    psi=lambda s=None: dot(2,atanh(sqrt((sinh(s) ** 2 - sinh(splus) ** 2) / (sinh(s) ** 2 - sinh(smin) ** 2))))
# SABR_European_AntonovApprox.m:50
    Vcall=max(0,f - K) + multiply(dot(2 / pi,sqrt(dot(K,f))),(quad(lambda s=None: multiply(sin(dot(eta,phi(s))) / (sinh(s)),G(dot(T,nu ** 2),s)),smin,splus) + dot(sin(dot(eta,pi)),quad(lambda s=None: multiply(exp(dot(- eta,psi(s))) / sinh(s),G(dot(T,nu ** 2),s)),splus,UB))))
# SABR_European_AntonovApprox.m:52
    return Vcall
    
if __name__ == '__main__':
    pass
    
    
@function
def mimicprocess(f=None,v0=None,beta=None,rho=None,nu=None,K=None,T=None,*args,**kwargs):
    varargin = mimicprocess.varargin
    nargin = mimicprocess.nargin

    # Function to find the mimic parameters to find the forward value of an European call with
# Antonov's method in the correlated case
    
    #f     = initial forward value
#v0    = initial volatility 
#beta  = exponent
#nu    = vol-vol
#K     = Strike price
#T     = Time to maturity
#correlation rho is assumed to be non-zero
    
    #alpha_mimic = initial volatility of the mimic process
#beta_mimic = exponent of the mimic process
#nu_mimic = vol-vol of the mimic process
    
    beta_mimic=copy(beta)
# SABR_European_AntonovApprox.m:72
    
    nu_mimic=sqrt(nu ** 2 - dot(3,(dot(nu ** 2,rho ** 2) + dot(dot(dot(dot(v0,nu),rho),(1 - beta)),f ** (beta - 1)))) / 2)
# SABR_European_AntonovApprox.m:73
    
    dq=(K ** (1 - beta) - f ** (1 - beta)) / (1 - beta)
# SABR_European_AntonovApprox.m:74
    
    dq_mimic=(K ** (1 - beta_mimic) - f ** (1 - beta_mimic)) / (1 - beta_mimic)
# SABR_European_AntonovApprox.m:75
    
    vmin=sqrt(dot(nu ** 2,dq ** 2) + dot(dot(dot(dot(2,rho),nu),dq),v0) + v0 ** 2)
# SABR_European_AntonovApprox.m:76
    
    Phi=((vmin + dot(rho,v0) + dot(nu,dq)) / (dot((1 + rho),v0))) ** (nu_mimic / nu)
# SABR_European_AntonovApprox.m:77
    
    v_mimic0=dot(dot(dot(2,Phi),dq_mimic),nu_mimic) / (Phi ** 2 - 1)
# SABR_European_AntonovApprox.m:78
    
    u0=(dot(dot(dq,nu),rho) + v0 - vmin) / (dot(dot(dq,nu),sqrt(1 - rho ** 2)))
# SABR_European_AntonovApprox.m:79
    
    L=dot(vmin,(1 - beta)) / (dot(dot(K ** (1 - beta),nu),sqrt(1 - rho ** 2)))
# SABR_European_AntonovApprox.m:80
    
    if L < 1:
        I=dot(2,(atan((u0 + L) / sqrt(1 - L ** 2)) - atan(L / sqrt(1 - L ** 2)))) / sqrt(1 - L ** 2)
# SABR_European_AntonovApprox.m:83
    else:
        I=log((dot(u0,(L + sqrt(L ** 2 - 1))) + 1) / (dot(u0,(L - sqrt(L ** 2 - 1))) + 1)) / sqrt(L ** 2 - 1)
# SABR_European_AntonovApprox.m:85
    
    phi0=acos(- (dot(dq,nu) + dot(v0,rho)) / vmin)
# SABR_European_AntonovApprox.m:88
    
    betamin=dot(dot(- beta,rho),(pi - phi0 - acos(rho) - I)) / (dot(dot(2,(1 - beta)),sqrt(1 - rho ** 2)))
# SABR_European_AntonovApprox.m:89
    
    v_mimic1=dot(dot(v_mimic0,nu_mimic ** 2),((dot((beta - beta_mimic),log(dot(K,f))) + log(dot(v0,vmin)) - log(dot(v_mimic0,sqrt(dot(dq_mimic ** 2,nu_mimic ** 2) + v_mimic0 ** 2)))) / 2 - betamin)) / (dot((Phi ** 2 - 1),log(Phi)) / (Phi ** 2 + 1))
# SABR_European_AntonovApprox.m:90
    
    alpha_mimic=v_mimic0 + dot(T,v_mimic1)
# SABR_European_AntonovApprox.m:91
    
    parameters=concat([alpha_mimic,beta_mimic,nu_mimic])
# SABR_European_AntonovApprox.m:93
    return parameters
    
if __name__ == '__main__':
    pass
    