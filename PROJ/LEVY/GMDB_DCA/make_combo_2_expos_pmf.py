# Generated with SMOP  0.41-beta
try:
    from smop.libsmop import *
except ImportError:
    raise ImportError('File compiled with `smop3`, please install `smop3` to run it.') from None
# make_combo_2_expos_pmf.m

    
@function
def make_combo_2_expos_pmf(b1=None,b2=None,xi1=None,xi2=None,Nmax=None,*args,**kwargs):
    varargin = make_combo_2_expos_pmf.varargin
    nargin = make_combo_2_expos_pmf.nargin

    # Creates a pmf from combination of 2 exponentials
    
    p=dot(dot(b1,exp(dot(- xi1,(arange(1,Nmax))))),(exp(xi1) - 1)) + dot(dot(b2,exp(dot(- xi2,(arange(1,Nmax))))),(exp(xi2) - 1))
# make_combo_2_expos_pmf.m:4
    temp=dot(b1,(1 - exp(dot(- xi1,(Nmax - 1))))) + dot(b2,(1 - exp(dot(- xi2,(Nmax - 1)))))
# make_combo_2_expos_pmf.m:6
    p[end()]=1 - temp
# make_combo_2_expos_pmf.m:7
    return p
    
if __name__ == '__main__':
    pass
    