# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# Get_VarthsDD_swing.m

    
@function
def Get_VarthsDD_swing(zetas=None,nms=None,Cont_D=None,*args,**kwargs):
    varargin = Get_VarthsDD_swing.varargin
    nargin = Get_VarthsDD_swing.nargin

    
    #
    
    zetas2=zetas ** 2
# Get_VarthsDD_swing.m:5
    zetas3=multiply(zetas,zetas2)
# Get_VarthsDD_swing.m:5
    zetas4=multiply(zetas,zetas3)
# Get_VarthsDD_swing.m:5
    varths=zeros(1,4)
# Get_VarthsDD_swing.m:7
    gamms=zeros(1,3)
# Get_VarthsDD_swing.m:8
    gamms[1]=(1 - zetas4(1)) / 8 + zetas3(1) / 3 - zetas2(1) / 4
# Get_VarthsDD_swing.m:13
    gamms[2]=5 / 12 + zetas4(1) / 4 - zetas3(1) / 3 - zetas2(1) / 2 + zetas(1)
# Get_VarthsDD_swing.m:14
    gamms[3]=1 / 12 - (1 + zetas4(1)) / 8 + zetas2(1) / 4
# Get_VarthsDD_swing.m:15
    varths[3]=dot(Cont_D(nms(1) - 1),gamms(1)) + dot(Cont_D(nms(1)),gamms(2)) + dot(Cont_D(nms(1) + 1),gamms(3))
# Get_VarthsDD_swing.m:17
    ###----------------------
    
    gamms[1]=zetas4(1) / 8 - zetas3(1) / 2 + zetas2(1) / 2
# Get_VarthsDD_swing.m:20
    gamms[2]=- zetas4(1) / 4 + dot(2,zetas3(1)) / 3
# Get_VarthsDD_swing.m:21
    gamms[3]=zetas4(1) / 8 - zetas3(1) / 6
# Get_VarthsDD_swing.m:22
    varths[4]=dot(Cont_D(nms(1)),gamms(1)) + dot(Cont_D(nms(1) + 1),gamms(2)) + dot(Cont_D(nms(1) + 2),gamms(3))
# Get_VarthsDD_swing.m:24
    ###----------------------
### in this case varths_D(1) uses zetas(2)
    gamms[1]=- 1 / 24 + zetas4(2) / 8 - zetas3(2) / 3 + zetas2(2) / 4
# Get_VarthsDD_swing.m:29
    gamms[2]=5 / 12 - zetas4(2) / 4 + zetas3(2) / 3 + zetas2(2) / 2 - zetas(2)
# Get_VarthsDD_swing.m:30
    gamms[3]=(1 + zetas4(2)) / 8 - zetas2(2) / 4
# Get_VarthsDD_swing.m:31
    varths[1]=dot(Cont_D(nms(2) - 1),gamms(1)) + dot(Cont_D(nms(2)),gamms(2)) + dot(Cont_D(nms(2) + 1),gamms(3))
# Get_VarthsDD_swing.m:33
    ###----------------------
### in this case varths_D(2) uses zetas(2)
    gamms[1]=1 / 12 - zetas4(2) / 8 + (zetas3(2) - zetas2(2)) / 2
# Get_VarthsDD_swing.m:36
    gamms[2]=5 / 6 + zetas4(2) / 4 - dot(2,zetas3(2)) / 3
# Get_VarthsDD_swing.m:37
    gamms[3]=1 / 12 - zetas4(2) / 8 + zetas3(2) / 6
# Get_VarthsDD_swing.m:38
    varths[2]=dot(Cont_D(nms(2)),gamms(1)) + dot(Cont_D(nms(2) + 1),gamms(2)) + dot(Cont_D(nms(2) + 2),gamms(3))
# Get_VarthsDD_swing.m:40
    ###----------------------
    
    return varths
    
if __name__ == '__main__':
    pass
    