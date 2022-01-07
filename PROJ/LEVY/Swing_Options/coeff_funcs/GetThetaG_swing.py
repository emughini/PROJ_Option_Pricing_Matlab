# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# GetThetaG_swing.m

    
@function
def GetThetaG_swing(xmin=None,K=None,dx=None,K1=None,K2=None,K3=None,K4=None,S_0=None,*args,**kwargs):
    varargin = GetThetaG_swing.varargin
    nargin = GetThetaG_swing.nargin

    
    #
    a=1 / dx
# GetThetaG_swing.m:4
    w=log(concat([K1,K2,K3,K4]) / S_0)
# GetThetaG_swing.m:5
    nbars=floor(dot(a,(w - xmin)) + 1)
# GetThetaG_swing.m:6
    xnbars=xmin + dot(dx,(nbars - 1))
# GetThetaG_swing.m:7
    rhos=(w - xnbars)
# GetThetaG_swing.m:8
    zetas=dot(a,rhos)
# GetThetaG_swing.m:9
    theta=zeros(K,1)
# GetThetaG_swing.m:11
    theta[arange(1,nbars(1) - 1)]=K2 - K1
# GetThetaG_swing.m:12
    theta[arange(nbars(4) + 2,K)]=K4 - K3
# GetThetaG_swing.m:13
    ####################################################################
######## Gaussian 3-point
####################################################################
    
    ######  Gaussian Quad Constants
    q_plus=(1 + sqrt(3 / 5)) / 2
# GetThetaG_swing.m:20
    q_minus=(1 - sqrt(3 / 5)) / 2
# GetThetaG_swing.m:20
    b3=sqrt(15)
# GetThetaG_swing.m:21
    b4=b3 / 10
# GetThetaG_swing.m:21
    #### PAYOFF CONSTANTS-----------------------------------
    varthet_01=dot(exp(dot(0.5,dx)),(dot(5,cosh(dot(b4,dx))) - dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# GetThetaG_swing.m:24
    varthet_m10=dot(exp(dot(- 0.5,dx)),(dot(5,cosh(dot(b4,dx))) + dot(b3,sinh(dot(b4,dx))) + 4)) / 18
# GetThetaG_swing.m:25
    varthet_star=varthet_01 + varthet_m10
# GetThetaG_swing.m:26
    E=dot(S_0,exp(xmin + dot(dx,(arange(0,K - 1)))))
# GetThetaG_swing.m:29
    zetas2=zetas ** 2
# GetThetaG_swing.m:31
    zetas3=multiply(zetas,zetas2)
# GetThetaG_swing.m:31
    zetas4=multiply(zetas,zetas3)
# GetThetaG_swing.m:31
    rhos_plus=dot(rhos,q_plus)
# GetThetaG_swing.m:32
    rhos_minus=dot(rhos,q_minus)
# GetThetaG_swing.m:32
    zetas_plus=dot(a,rhos_plus)
# GetThetaG_swing.m:33
    zetas_minus=dot(a,rhos_minus)
# GetThetaG_swing.m:33
    eds1=exp(rhos_minus)
# GetThetaG_swing.m:34
    eds2=exp(rhos / 2)
# GetThetaG_swing.m:34
    eds3=exp(rhos_plus)
# GetThetaG_swing.m:34
    dbars_1=zetas2 / 2
# GetThetaG_swing.m:36
    dbars_0=zetas - dbars_1
# GetThetaG_swing.m:37
    
    ds_0=multiply(zetas,(dot(5,(multiply((1 - zetas_minus),eds1) + multiply((1 - zetas_plus),eds3))) + multiply(dot(4,(2 - zetas)),eds2))) / 18
# GetThetaG_swing.m:39
    ds_1=multiply(dot(exp(- dx),zetas),(dot(5,(multiply(zetas_minus,eds1) + multiply(zetas_plus,eds3))) + multiply(dot(4,zetas),eds2))) / 18
# GetThetaG_swing.m:40
    ### Get Intial Coeffs
    theta[arange(1,nbars(1) - 1)]=K2 - K1
# GetThetaG_swing.m:43
    theta[arange(nbars(4) + 2,K)]=K4 - K3
# GetThetaG_swing.m:44
    theta[nbars(1)]=K2 - dot(K1,(0.5 + dbars_0(1))) - dot(E(nbars(1)),(varthet_01 - ds_0(1)))
# GetThetaG_swing.m:46
    theta[nbars(1) + 1]=K2 - dot(K1,dbars_1(1)) - dot(E(nbars(1) + 1),(varthet_star - ds_1(1)))
# GetThetaG_swing.m:47
    theta[arange(nbars(1) + 2,nbars(2) - 1)]=K2 - dot(varthet_star,E(arange(nbars(1) + 2,nbars(2) - 1)))
# GetThetaG_swing.m:49
    tmp1=dot(K2,(0.5 + dbars_0(2) - dot(exp(- rhos(2)),(varthet_m10 + ds_0(2)))))
# GetThetaG_swing.m:51
    tmp2=dot(K2,(dbars_1(2) - dot(exp(dx - rhos(2)),ds_1(2))))
# GetThetaG_swing.m:52
    tmp3=dot(K3,(dot((varthet_01 - ds_0(3)),exp(- rhos(3))) - (0.5 - dbars_0(3))))
# GetThetaG_swing.m:54
    tmp4=dot(K3,(dot(exp(dx - rhos(3)),(varthet_star - ds_1(3))) - (1 - dbars_1(3))))
# GetThetaG_swing.m:55
    if K3 > K2:
        theta[nbars(2)]=tmp1
# GetThetaG_swing.m:58
        theta[nbars(2) + 1]=tmp2
# GetThetaG_swing.m:59
        theta[nbars(3)]=tmp3
# GetThetaG_swing.m:60
        theta[nbars(3) + 1]=tmp4
# GetThetaG_swing.m:61
    else:
        if K3 == K2:
            theta[nbars(2)]=tmp1 + tmp3
# GetThetaG_swing.m:63
            theta[nbars(2) + 1]=tmp2 + tmp4
# GetThetaG_swing.m:64
    
    theta[arange(nbars(3) + 2,nbars(4) - 1)]=dot(E(arange(nbars(3) + 2,nbars(4) - 1)),varthet_star) - K3
# GetThetaG_swing.m:67
    theta[nbars(4)]=dot(E(nbars(4)),(varthet_m10 + ds_0(4))) - K3 + dot(K4,(0.5 - dbars_0(4)))
# GetThetaG_swing.m:69
    theta[nbars(4) + 1]=dot(K4,(1 - dbars_1(4))) - K3 + dot(E(nbars(4) + 1),ds_1(4))
# GetThetaG_swing.m:70
    return theta
    
if __name__ == '__main__':
    pass
    