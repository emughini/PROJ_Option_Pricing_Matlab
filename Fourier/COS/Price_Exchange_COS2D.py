# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Price_Exchange_COS2D.m

    #Copyright (C) 2015 M.J. Ruijter
    
    #This file is part of BENCHOP.
    #BENCHOP is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.
    
    #BENCHOP is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.
    
    #You should have received a copy of the GNU General Public License
    #along with BENCHOP. If not, see <http://www.gnu.org/licenses/>.
    
@function
def Price_Exchange_COS2D(S=None,T=None,r=None,sig1=None,sig2=None,rho=None,N=None,L=None,*args,**kwargs):
    varargin = Price_Exchange_COS2D.varargin
    nargin = Price_Exchange_COS2D.nargin

    # BENCHOP Problem 6: The Black-Scholes-Merton model for two underlying assets
# BSeuCallspread_COS computes the price for a European spread call option
    
    # Input:    S       - Initial asset price   
#           K       - Strike price
#           T       - Terminal time  
#           r       - Risk-free interest rate
#           sig1    - Volatility process 1
#           sig2    - Volatility process 2
#           rho     - Correlation coefficient
#`          N       - number of cos expansion terms (e.g. 20)
#           L       - grid width parameter (e.g. 10)
    
    # Output:   U       - Option value
    
    # This MATLAB code has been written for the BENCHOP project and is based on 
# the COS methodes developed by F. Fang, C.W. Oosterlee, and M.J. Ruijter
    
    if nargin < 7:
        N=19
# Price_Exchange_COS2D.m:36
    
    if nargin < 8:
        L=8
# Price_Exchange_COS2D.m:39
    
    # Parameters
    sigma=concat([sig1,sig2])
# Price_Exchange_COS2D.m:43
    rhoM=concat([[1,rho],[rho,1]])
# Price_Exchange_COS2D.m:44
    x=log(S)
# Price_Exchange_COS2D.m:45
    # Parameters bivariate normal distribution
    Sigma=dot(multiply((dot(sigma.T,sigma)),rhoM),T)
# Price_Exchange_COS2D.m:48
    Mu=dot((r - dot(0.5,sigma.T ** 2)),T)
# Price_Exchange_COS2D.m:49
    # Interval [a,b]
    a1=log(100) + Mu(1) - dot(dot(L,sigma(1)),sqrt(T))
# Price_Exchange_COS2D.m:51
    b1=log(100) + Mu(1) + dot(dot(L,sigma(1)),sqrt(T))
# Price_Exchange_COS2D.m:52
    a2=log(100) + Mu(2) - dot(dot(L,sigma(2)),sqrt(T))
# Price_Exchange_COS2D.m:53
    b2=log(100) + Mu(2) + dot(dot(L,sigma(2)),sqrt(T))
# Price_Exchange_COS2D.m:54
    a=min(a1,a2)
# Price_Exchange_COS2D.m:55
    b=max(b1,b2)
# Price_Exchange_COS2D.m:56
    # Number of Fourier cosine coefficients
    N1=copy(N)
# Price_Exchange_COS2D.m:59
    N2=copy(N1)
# Price_Exchange_COS2D.m:60
    k1vec=concat([arange(0,N1 - 1)]).T
# Price_Exchange_COS2D.m:61
    k2vec=concat([arange(0,N2 - 1)])
# Price_Exchange_COS2D.m:62
    omega1=repmat(dot(pi / (b - a),concat([arange(0,N2 - 1)])),N1,1)
# Price_Exchange_COS2D.m:63
    omega[arange(),2]=omega1(arange(1,end())).T
# Price_Exchange_COS2D.m:64
    omega[arange(),1]=repmat(dot(pi / (b - a),concat([arange(0,N1 - 1)]).T),N2,1)
# Price_Exchange_COS2D.m:65
    omega_p=copy(omega)
# Price_Exchange_COS2D.m:66
    omega_m=copy(omega)
# Price_Exchange_COS2D.m:67
    omega_m[arange(),2]=- omega_m(arange(),2)
# Price_Exchange_COS2D.m:68
    # Fourier cosine coefficients payoff function
    k1=repmat(k1vec,1,N2)
# Price_Exchange_COS2D.m:71
    k2=repmat(k2vec,N1,1)
# Price_Exchange_COS2D.m:72
    tempplus=dot((k1 + k2),pi)
# Price_Exchange_COS2D.m:73
    tempmin=dot((k1 - k2),pi)
# Price_Exchange_COS2D.m:74
    tempplusquad=tempplus ** 2
# Price_Exchange_COS2D.m:75
    tempminquad=tempmin ** 2
# Price_Exchange_COS2D.m:76
    bmina=b - a
# Price_Exchange_COS2D.m:77
    bminaquad=bmina ** 2
# Price_Exchange_COS2D.m:78
    piquad=pi ** 2
# Price_Exchange_COS2D.m:79
    k2quad=k2 ** 2
# Price_Exchange_COS2D.m:80
    Uk=multiply(dot(- 0.5,bmina ** 3.0) / (multiply(dot(multiply(multiply(multiply((tempplusquad + bminaquad),(tempminquad + bminaquad)),k1),k2),pi),(dot(piquad,k2quad) + bminaquad))),(multiply(multiply(multiply(dot(exp(b),k1),(tempplusquad + bminaquad)),(multiply(dot(pi,k2),tempmin) + bminaquad)),sin(tempmin)) - multiply(multiply(multiply(dot(exp(b),k1),(tempminquad + bminaquad)),(multiply(dot(pi,k2),tempplus) + bminaquad)),sin(tempplus)) + multiply(multiply(multiply(dot(dot(dot(exp(b),pi),bmina),(dot(2.0,k2) - k1)),k1),(tempplusquad + bminaquad)),cos(tempmin)) + multiply(multiply(multiply(dot(dot(dot(exp(b),pi),bmina),(dot(2.0,k2) + k1)),k1),(tempminquad + bminaquad)),cos(tempplus)) - multiply(dot(dot(2,exp(a)),k2),(multiply(multiply(tempminquad,tempplusquad),sin(multiply(k1,pi))) + multiply(dot(dot(dot(2,pi),bmina),k1),(dot(piquad,k2quad) + bminaquad))))))
# Price_Exchange_COS2D.m:82
    # for k1==k2
    for i in arange(1,min(N1,N2)).reshape(-1):
        Uk[i,i]=0
# Price_Exchange_COS2D.m:89
    
    k2=copy(k1vec)
# Price_Exchange_COS2D.m:90
    k2quad=k2 ** 2
# Price_Exchange_COS2D.m:91
    Ukdiag=multiply(- bminaquad / (multiply(dot(multiply((multiply(k2quad,piquad) + bminaquad),k2),pi),(dot(dot(4,piquad),k2quad) + bminaquad))),(multiply(dot(dot(dot(0.5,exp(b)),bmina),(dot(dot(2,piquad),k2quad) - bminaquad)),sin(dot(dot(2,pi),k2))) + multiply(multiply(dot(dot(dot(1.5,exp(b)),pi),bminaquad),k2),cos(multiply(dot(2,pi),k2))) - multiply(dot(dot(exp(a),bmina),(multiply(dot(4,piquad),k2quad) + bminaquad)),sin(dot(pi,k2))) - multiply(dot(dot(2,pi),k2),(dot((dot(- piquad,k2quad) - dot(0.25,bminaquad)),exp(b)) + dot(exp(a),(dot(piquad,k2quad) + bminaquad))))))
# Price_Exchange_COS2D.m:92
    Uk=Uk + diag(Ukdiag,0)
# Price_Exchange_COS2D.m:97
    # for (k1==0)&&(k2==0)
    Uk[1,1]=dot((bmina + 2),exp(a)) + dot(exp(b),(bmina - 2))
# Price_Exchange_COS2D.m:99
    # for k1==0
    k2=k2vec(arange(2,end()))
# Price_Exchange_COS2D.m:101
    k2quad=k2 ** 2
# Price_Exchange_COS2D.m:102
    Uk[1,(arange(2,end()))]=multiply(bmina ** 3.0 / (multiply(dot((dot(piquad,k2quad) + bminaquad) ** 2,pi),k2)),(multiply(multiply(dot(exp(b),(dot(pi,k2) + bmina)),(dot(- pi,k2) + bmina)),sin(dot(pi,k2))) + multiply(dot(pi,k2),(multiply(dot(dot(- 2,exp(b)),bmina),cos(dot(pi,k2))) + dot(exp(a),(dot(piquad,k2quad) + dot(bmina,(bmina + 2))))))))
# Price_Exchange_COS2D.m:103
    # for k2==0
    k1=k1vec(arange(2,end()))
# Price_Exchange_COS2D.m:107
    k1quad=k1 ** 2
# Price_Exchange_COS2D.m:108
    Uk[arange(2,end()),1]=multiply(bmina / (multiply(dot((multiply(k1quad,piquad) + (bminaquad)) ** 2.0,pi),k1)),(multiply((multiply(dot(dot(- (dot(dot(piquad,(- bmina + 1)),k1quad) + (dot((- bmina + 3),bminaquad))),piquad),exp(b)),k1quad) + dot(exp(a),(dot(piquad,k1quad) + (bminaquad)) ** 2)),sin(multiply(k1,pi))) + multiply(dot(dot(pi,bminaquad),k1),(multiply(dot((dot(piquad,k1quad) + (dot((a - b + 2),(- b + a)))),exp(b)),cos(dot(pi,k1))) - dot(dot(2,exp(a)),- bmina)))))
# Price_Exchange_COS2D.m:109
    Uk=dot(dot(2 / (b - a),2) / (b - a),Uk)
# Price_Exchange_COS2D.m:113
    Uk[arange(),1]=dot(0.5,Uk(arange(),1))
# Price_Exchange_COS2D.m:114
    Uk[1,arange()]=dot(0.5,Uk(1,arange()))
# Price_Exchange_COS2D.m:115
    # Characteristic function
    cfplus=exp(dot(1j,(dot(Mu.T,omega_p.T))) - dot(0.5,sum(multiply((omega_p.T),(dot(Sigma,omega_p.T))),1)))
# Price_Exchange_COS2D.m:118
    cfmin=exp(dot(1j,(dot(Mu.T,omega_m.T))) - dot(0.5,sum(multiply((omega_m.T),(dot(Sigma,omega_m.T))),1)))
# Price_Exchange_COS2D.m:119
    # Fourier cosine coefficients density function
    Recfplus=dot(1 / 2,real(multiply(repmat(cfplus,size(x,1),1),exp(dot(1j,(dot((x - a),omega_p.T)))))))
# Price_Exchange_COS2D.m:122
    Recfmin=dot(1 / 2,real(multiply(repmat(cfmin,size(x,1),1),exp(dot(1j,(dot((x - a),omega_m.T)))))))
# Price_Exchange_COS2D.m:123
    Recf=Recfplus + Recfmin
# Price_Exchange_COS2D.m:124
    # Option value
    U=dot(dot(exp(dot(- r,T)),Uk(arange(1,end()))),Recf.T)
# Price_Exchange_COS2D.m:127
    return U
    
if __name__ == '__main__':
    pass
    