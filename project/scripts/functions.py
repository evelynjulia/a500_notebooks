# functions
# list of useful functions for project

def make_theta(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K
    theta=temp*(p0/press)**(Rd/cpd)
    return theta



def make_theta_v(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K
    theta=temp*(p0/press)**(Rd/cpd)
    return theta


def calc_thetav(theta, wv, wl):
    """
    Thetav using stull 1.5.1a
    
    Parameters
    ----------
    
    theta: float
       potential temperature(K)
    wv: float
       vapor mixing ratio (kg/kg)
       
    wl: float
       liquid mixing ratio (kg/kg)
       
    Returns
    -------
    
    theta_v: float
      virtual potential temperature
    """
    theta_v = theta*(1 + 0.61*wv - wl)
    return theta_v