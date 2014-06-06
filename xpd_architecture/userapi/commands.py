__author__ = 'arkilic'
from dataapi.motion.motors.status import *
import cothread
from cothread.catools import *
from dataapi.config._conf import _conf


def _initpvs(_conf):
    """
    Double checks connection to Instruments"""
    print 'Connecting instruments'
    try:
        for option in _conf.options('PVs'):
            connect(_conf.get('PVs',option))
        print 'Instrument initialization complete'
    except:
        raise Exception('Some of the instruments were not found or connected\
        , namely %s'% (option,))
                
"""Motor Commands"""
def printf(value):
#    print value, test function
    return value
    
def where(verbose=False):
    """
    Returns:
        motor coordinates
    """
    if verbose==True:
        print motorD
    else:
        posd=dict()
        for option in _conf.options('PVs'):
            if 'motor' in str(_conf.get('PVs',option)):
                posd[str(option)]=caget(_conf.get('PVs',option))
        return posd

def ascan(func,*args,**kwargs):
    """
    Scan from one position to another, performing a function at each step
    
    Parameters
    ----------
    directionalias : string
        Name of direction e.g. x, y, phi, etc.
    start : float
        Starting position for scan, absolute
    finish : float
        Ending position for scan, absolute
    step : float
        Step size betwfunceen function calls
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments
    Returns
    -------
    A : ndarray
        array of motor positions and function outputs
    Example
    -------
    ascan(printf, 5, step=.5, finish=105, start=99, alias='samx')
    """
    A=None
    for entry in np.arange(kwargs['start'],kwargs['finish']+kwargs['step'],kwargs['step']):
#        print 'start move'  
        move(kwargs['alias'], entry, wait=True)
#        if caget(motor['pv']+'.RRBV')==value:
#        print 'finished sucsessfuly'
#        return True
#    else:
#        print 'finished motion, but setpoint not reached'
#        return False
        if A==None:
            print 'starting data aquesition'
            A=[position(kwargs['alias']),func(*args)]            
        else:
            A=np.vstack((A,[position(kwargs['alias']),func(*args)]))
#        print A
    return A

def rscan(func,*args,**kwargs):
    """
    Scan from one position to another, performing a function at each step
    
    Parameters
    ----------
    directionalias : string
        Name of direction e.g. x, y, phi, etc.
    start : float
        Starting position for scan, relative
    finish : float
        Ending position for scan, relative
    step : float
        Step size between function calls
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments
    Returns
    -------
    A : ndarray
        array of motor positions and function outputs
    Example
    -------
    rscan(printf, 5, step=.1, finish=5, start=-5, alias='samx')
    """
    A=None
    for entry in np.arange(float(position(kwargs['alias']))+kwargs['start'],float(position(kwargs['alias']))+kwargs['finish']+kwargs['step'], kwargs['step']):
        move(kwargs['alias'], entry,wait=True)
        #in this move function check which motors to move in order to move in the given direction
        #if the direction:motorconfig entry doesn't exist raise error
        func(*args)
        if A==None:
            print 'starting data aquesition'
            A=[position(kwargs['alias']),func(*args)]            
        else:
            A=np.vstack((A,[position(kwargs['alias']),func(*args)]))
    return A
    
def gscan(func,*args, **kwargs):
    """
    Most general scan, each row is a new direction with start stop and step functions
    
    Parameters
    ----------
    func : function
        This function gets called after each step is concluded
    *args:
        Function arguments
    **kwargs:
        Keyword arguments for the scan
    Returns
    -------
    A : ndarray
        array of motor positions and function outputs
    Example
    -------
    gscan(printf,5,axsis1={'alias':'samx','start':-1,'finish':1,'step':.5,'movetype':'ABS'},axsis2={'alias':'samy','start':-1,'finish':1,'step':.5,'movetype':'ABS'})
    """
    out=dict()
    for key in sorted(kwargs.keys()):
        motormovedict=kwargs[key]
        print motormovedict['alias']
        if motormovedict['movetype']=='ABS':
            A=ascan(func, *args,**motormovedict)
        elif motormovedict['movetype']=='REL':
            A=rscan(func, *args,**motormovedict)
        else:
            raise Exception('Movetype not correctly specified')
        out[motormovedict['alias']]=A
    return out



def stop(alias):
    """
    Stop selected process, or all processies, NOT IMPLEMENTED
    """
def mesh(func, *args, **kwargs):
    """
    Performs function on each position within the 2 coordinates, creating a matrix
    of data points.
    
    Parameters
    ----------
    func: function
        This function is called at every point within the bounds of the surface
    *args:
        Function arguments
    **kwargs:
        Keyword arguments for the motormove
    
    Returns
    -------
    B: 2D array
        This array hold all the data returned by the function
    ax1graphax: 1D array
        This array holds all the points tested in the ax1 direction
    ax2graphax: 1D array
        This array holds all the points tested in the ax2 direction
    
    Example
    -------
    mesh(printf,-1,serpentmove=True, ax1={'movetype': 'ABS', 'alias': 'samy', 'step': 0.5, 'finish': 1, 'start': -1},ax2={'movetype': 'ABS', 'alias': 'samx', 'step': 0.5, 'finish': 1, 'start': -1})
    """
#    print 'n\n\n'
#    print kwargs['serpentmove']
    A=None
    B=None
    ax1=kwargs['ax1']
    ax2=kwargs['ax2']
    if ax1['movetype']=='REL':
        ax1graphax=np.arange(float(position(ax1['alias']))+ax1['start'],float(position(ax1['alias']))+ax1['finish']+ax1['step'], ax1['step'])
    if ax2['movetype']=='REL':
        ax2graphax=np.arange(float(position(ax2['alias']))+ax2['start'],float(position(ax2['alias']))+ax2['finish']+ax2['step'], ax2['step'])
    if ax1['movetype']=='ABS':
        ax1graphax=np.arange(ax1['start'],ax1['finish']+ax1['step'], ax1['step'])
    if ax2['movetype']=='ABS':
        ax2graphax=np.arange(ax2['start'],ax2['finish']+ax2['step'], ax2['step'])
    if kwargs['serpentmove']==False:
        for entry in ax1graphax:
            move(ax1['alias'],entry, wait=True)
            for entry in ax2graphax:
                move(ax2['alias'],entry,wait=True)
                if A==None:
                    A=[position(ax2['alias']),func(*args)]
                else:
                    A=np.vstack((A,[position(ax2['alias']),func(*args)]))
            if B==None:
                B=A[:,1]
                A=None
            else:
                B=np.column_stack((B,A[:,1]))
                A=None
    else:
        i=0
        for entry in ax1graphax:
#            print i
            move(ax1['alias'],entry, wait=True)
            if i % 2 ==0:
#                print 'even'
                for entry in ax2graphax:
                    move(ax2['alias'],entry,wait=True)
                    if A==None:
                        A=[position(ax2['alias']),func(*args)]
                    else:
                        A=np.vstack((A,[position(ax2['alias']),func(*args)]))
#                if B==None:
#                    B=A[:,1]
#                    A=None
#                else:
#                    B=np.column_stack((B,A[:,1]))
#                    A=None
            else:
#                print 'odd'
                for entry in -ax2graphax:
                    move(ax2['alias'],entry,wait=True)
                    if A==None:
                        A=[position(ax2['alias']),func(*args)]
                    else:
                        A=np.vstack((A,[position(ax2['alias']),func(*args)]))
            if B==None:
                B=A[:,1]
                A=None
            else:
                B=np.column_stack((B,A[:,1]))
                A=None
            i+=1
    return B, ax1graphax, ax2graphax

"""Detector Commands"""


def CaptureSingle(filename, subframes, seconds_per_subframe, Automatic=False, **kwargs):
    """Captures an x-ray image creating a single file out of subframes with set \
    integration times
    
    Parameters
    ----------
    filename: string
        Name of a file to save to
    subframes: int
        Number of subframes to use to write the main image
    seconds_per_subframe: float
        Number of seconds of integration time for each subframe
    Automatic: bool
        If True then uses statistical analysis to create an integration time and \
        number of subframes to make the output file statisticly signifigant out to \
        a Q(A^-1) specified by the user
    
    Returns
    -------
    A: 2D array
        Numpy array which represents the image pixels
    """
    pass


def CaptureMulti(base_filename, filename_iterator,subframes, seconds_per_subframe, Automatic=False, **kwargs):
    """Captures an x-ray image creating many files out of subframes with set \
    integration times
    
    Parameters
    ----------
    base_filename: string
        Name of a file to save to
    filename_iterator: number or list
        
    subframes: int
        Number of subframes to use to write the main image
    seconds_per_subframe: float
        Number of seconds of integration time for each subframe
    Automatic: bool
        If True then uses statistical analysis to create an integration time and \
        number of subframes to make the output file statisticly signifigant out to \
        a Q(A^-1) specified by the user
    
    Returns
    -------
    A: 3D array
        Numpy array which represents the images
    """
#check that shutter is open
#take darkfield image? or do this inside the core?    
    pass

           
if __name__ == "__main__":
    _initpvs(_conf)
    print('Initial positions:')
    print(where())
    