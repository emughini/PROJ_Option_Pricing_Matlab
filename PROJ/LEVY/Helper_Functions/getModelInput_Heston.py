# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# getModelInput_Heston.m

    
@function
def getModelInput_Heston(dt=None,r=None,q=None,modelParams=None,*args,**kwargs):
    varargin = getModelInput_Heston.varargin
    nargin = getModelInput_Heston.nargin

    # model: Levy models (BSM, CGMY, NIG, MJD, Kou)
#        Affine models (Heston)
# r: interest rate
# q: dividend yield
# dt: time increment (this could be time to maturity, or time between monitoring dates)
# modelParams: dictionary of params for specific model
# NOTE: r,q can also be chosen to model forward or FX
    
    modelInputs=cellarray([])
# getModelInput_Heston.m:10
    #----------------------------------------------
    v_0=modelParams.v_0
# getModelInput_Heston.m:13
    theta=modelParams.theta
# getModelInput_Heston.m:14
    kappa=modelParams.kappa
# getModelInput_Heston.m:15
    sigma_v=modelParams.sigma_v
# getModelInput_Heston.m:16
    rho=modelParams.rho
# getModelInput_Heston.m:17
    #----------------------------------------------
    modelInputs.RNmu = copy(r - q - dot(0.5,theta))
# getModelInput_Heston.m:19
    modelInputs.c1 = copy(dot(modelInputs.RNmu,dt) + dot((1 - exp(dot(- kappa,dt))),(theta - v_0)) / (dot(2,kappa)))
# getModelInput_Heston.m:20
    modelInputs.c2 = copy(dot(1 / (dot(8,kappa ** 3)),(dot(dot(dot(dot(dot(sigma_v,dt),kappa),exp(dot(- kappa,dt))),(v_0 - theta)),(dot(dot(8,kappa),rho) - dot(4,sigma_v))) + dot(dot(dot(dot(kappa,rho),sigma_v),(1 - exp(dot(- kappa,dt)))),(dot(16,theta) - dot(8,v_0))) + dot(dot(dot(dot(2,theta),kappa),dt),(dot(dot(dot(- 4,kappa),rho),sigma_v) + sigma_v ** 2 + dot(4,kappa ** 2))) + dot(sigma_v ** 2,(dot((theta - dot(2,v_0)),exp(dot(dot(- 2,kappa),dt))) + dot(theta,(dot(6,exp(dot(- kappa,dt))) - 7)) + dot(2,v_0))) + dot(dot(dot(8,kappa ** 2),(v_0 - theta)),(1 - exp(dot(- kappa,dt)))))))
# getModelInput_Heston.m:21
    modelInputs.c4 = copy(0)
# getModelInput_Heston.m:26
    modelInputs.rnCHF = copy(lambda u=None: cf_RN_Heston(u,dt,r - q,v_0,theta,kappa,sigma_v,rho))
# getModelInput_Heston.m:27
    # NOTE: no rnSYMB for this model, as we have no current use for it
    
    return modelInputs
    
if __name__ == '__main__':
    pass
    