# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Get_VarthsPSI_swing.m

    
@function
def Get_VarthsPSI_swing(zetaj=None,ntilj=None,PSIdj=None,PSIdjm1=None,*args,**kwargs):
    varargin = Get_VarthsPSI_swing.varargin
    nargin = Get_VarthsPSI_swing.nargin

    #UNTITLED2 Summary of this function goes here
#   Detailed explanation goes here
    
    zetaj2=zetaj ** 2
# Get_VarthsPSI_swing.m:6
    zetaj3=dot(zetaj,zetaj)
# Get_VarthsPSI_swing.m:6
    zetaj4=dot(zetaj,zetaj3)
# Get_VarthsPSI_swing.m:6
    varths=zeros(1,4)
# Get_VarthsPSI_swing.m:8
    gamms=zeros(1,3)
# Get_VarthsPSI_swing.m:9
    gamms[1]=(1 - zetaj4) / 8 + zetaj3 / 3 - zetaj2 / 4
# Get_VarthsPSI_swing.m:12
    gamms[2]=5 / 12 + zetaj4 / 4 - zetaj3 / 3 - zetaj2 / 2 + zetaj
# Get_VarthsPSI_swing.m:13
    gamms[3]=1 / 12 - (1 + zetaj4) / 8 + zetaj2 / 4
# Get_VarthsPSI_swing.m:14
    varths[3]=dot(PSIdjm1(ntilj(1) - 1),gamms(1)) + dot(PSIdjm1(ntilj(1)),gamms(2)) + dot(PSIdjm1(ntilj(1) + 1),gamms(3))
# Get_VarthsPSI_swing.m:16
    gamms[1]=1 / 12 - gamms(1)
# Get_VarthsPSI_swing.m:18
    gamms[2]=5 / 6 - gamms(2)
# Get_VarthsPSI_swing.m:19
    gamms[3]=1 / 12 - gamms(3)
# Get_VarthsPSI_swing.m:20
    varths[1]=dot(PSIdj(ntilj(1) - 1),gamms(1)) + dot(PSIdj(ntilj(1)),gamms(2)) + dot(PSIdj(ntilj(1) + 1),gamms(3))
# Get_VarthsPSI_swing.m:22
    ###----------------------
    
    gamms[1]=zetaj4 / 8 - zetaj3 / 2 + zetaj2 / 2
# Get_VarthsPSI_swing.m:26
    gamms[2]=- zetaj4 / 4 + dot(2,zetaj3) / 3
# Get_VarthsPSI_swing.m:27
    gamms[3]=zetaj4 / 8 - zetaj3 / 6
# Get_VarthsPSI_swing.m:28
    varths[4]=dot(PSIdjm1(ntilj(1)),gamms(1)) + dot(PSIdjm1(ntilj(1) + 1),gamms(2)) + dot(PSIdjm1(ntilj(1) + 2),gamms(3))
# Get_VarthsPSI_swing.m:30
    gamms[1]=1 / 12 - gamms(1)
# Get_VarthsPSI_swing.m:32
    gamms[2]=5 / 6 - gamms(2)
# Get_VarthsPSI_swing.m:33
    gamms[3]=1 / 12 - gamms(3)
# Get_VarthsPSI_swing.m:34
    varths[2]=dot(PSIdj(ntilj(1)),gamms(1)) + dot(PSIdj(ntilj(1) + 1),gamms(2)) + dot(PSIdj(ntilj(1) + 2),gamms(3))
# Get_VarthsPSI_swing.m:36
    return varths
    
if __name__ == '__main__':
    pass
    