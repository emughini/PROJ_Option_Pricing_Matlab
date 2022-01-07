# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Get_psis_swing.m

    
@function
def Get_psis_swing(rhos=None,zetas=None,q_plus=None,q_minus=None,Ks=None,a=None,varthet_01=None,E=None,nms=None,nbars=None,edn=None,*args,**kwargs):
    varargin = Get_psis_swing.varargin
    nargin = Get_psis_swing.nargin

    #UNTITLED Summary of this function goes here
#   Detailed explanation goes here
    K1=Ks(1)
# Get_psis_swing.m:4
    K2=Ks(2)
# Get_psis_swing.m:4
    K3=Ks(3)
# Get_psis_swing.m:4
    K4=Ks(4)
# Get_psis_swing.m:4
    dK21=K2 - K1
# Get_psis_swing.m:5
    dK43=K4 - K3
# Get_psis_swing.m:5
    psis=zeros(1,4)
# Get_psis_swing.m:7
    zetas2=zetas ** 2
# Get_psis_swing.m:9
    ###----------------------------------------
    rhos_plus=dot(rhos,q_plus)
# Get_psis_swing.m:12
    rhos_minus=dot(rhos,q_minus)
# Get_psis_swing.m:12
    zetas_plus=dot(a,rhos_plus)
# Get_psis_swing.m:13
    zetas_minus=dot(a,rhos_minus)
# Get_psis_swing.m:13
    eds1=exp(rhos_minus)
# Get_psis_swing.m:14
    eds2=exp(rhos / 2)
# Get_psis_swing.m:14
    eds3=exp(rhos_plus)
# Get_psis_swing.m:14
    dbars_1=zetas2 / 2
# Get_psis_swing.m:15
    dbars_0=zetas - dbars_1
# Get_psis_swing.m:16
    
    ds_0=multiply(zetas,(dot(5,(multiply((1 - zetas_minus),eds1) + multiply((1 - zetas_plus),eds3))) + multiply(dot(4,(2 - zetas)),eds2))) / 18
# Get_psis_swing.m:17
    ds_1=multiply(dot(edn,zetas),(dot(5,(multiply(zetas_minus,eds1) + multiply(zetas_plus,eds3))) + multiply(dot(4,zetas),eds2))) / 18
# Get_psis_swing.m:18
    ###-------------------
    
    if nms(1) >= nbars(1):
        if nms(1) < nbars(2):
            psis[1]=dot(K2,(0.5 - dbars_0(1))) - dot(E(nms(1)),(varthet_01 - ds_0(1)))
# Get_psis_swing.m:23
        else:
            psis[1]=0
# Get_psis_swing.m:25
        psis[2]=dot(K2,dbars_1(1)) - dot(E(nms(1) + 1),ds_1(1))
# Get_psis_swing.m:27
    else:
        psis[1]=dot(dK21,(0.5 - dbars_0(1)))
# Get_psis_swing.m:29
        psis[2]=dot(dK21,dbars_1(1))
# Get_psis_swing.m:30
    
    ###-------------------
    if nms(2) < nbars(4):
        psis[3]=dot(E(nms(2)),(varthet_01 - ds_0(2))) - dot(K3,(0.5 - dbars_0(2)))
# Get_psis_swing.m:35
        if nms(2) > nbars(3):
            psis[4]=dot(E(nms(2) + 1),ds_1(2)) - dot(K3,dbars_1(2))
# Get_psis_swing.m:37
        else:
            psis[4]=0
# Get_psis_swing.m:39
    else:
        psis[3]=dot(dK43,(0.5 - dbars_0(2)))
# Get_psis_swing.m:42
        psis[4]=dot(dK43,dbars_1(2))
# Get_psis_swing.m:43
    
    ###----------------------------------------
    
    return psis
    
if __name__ == '__main__':
    pass
    