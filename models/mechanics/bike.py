from sympy import (Symbol, symbols, Matrix, sin, cos, asin, diff, sqrt, S,
                   diag, Eq, hessian, Function, flatten, Tuple, im, pi, latex,
                   dsolve, solve, fraction, factorial, Subs, Number, oo, Abs,
                   N, solveset, atan)

from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point
from sympy.physics.vector import vpprint, vlatex
from dynpy.models.mechanics.principles import ComposedSystem
from dynpy.models.mechanics.disk import RollingDisk
from dynpy.models.electric.elements import *
from dynpy.models.electric.engine import *
from functools import cached_property, lru_cache

class ReducedMotorbike(ComposedSystem):
    scheme_name = 'DC_motor.png'

    M = Symbol('M', positive=True)
    m_b = Symbol('m_bike',positive=True)
    m_d = Symbol('m_driver',positive=True)
    m_r= Symbol('m_r',positive=True)
    m_f = Symbol('m_f',positive=True)
    r = Symbol('r',positive=True)
    Cd=Symbol('C_d',positive=True) #dragcoefficient
    Ad=Symbol('A_d',positive=True) #air density
    Af=Symbol('A_f',positive=True) #front area of the vehicle
    T=Symbol('T')

    x=dynamicsymbols('x')
    phi=dynamicsymbols('\phi')

    def __init__(self,
                 M=None,
                 m_b=None,
                 m_d=None,
                 m_r=None,
                 m_f=None,
                 x=None,
                 r=None,
                 Cd=None,
                 Ad=None,
                 Af=None,
                 T=None,
                 phi=None,
                 ivar=Symbol('t'),
                 **kwargs):

        if M is not None: self.M=M
        if m_b is not None: self.m_b = m_b
        if m_d is not None: self.m_d = m_d
        if m_r is not None: self.m_r = m_r
        if m_f is not None: self.m_f = m_f
        if x is not None: self.x = x
        if r is not None: self.r=r
        if Cd is not None: self.Cd=Cd
        if Ad is not None: self.Ad=Ad
        if Af is not None: self.Af=Af
        if T is not None: self.T=T
        if phi is not None: self.phi=phi

        self.ivar = ivar

        self.qs = [self.x]
        self._init_from_components(**kwargs)

    @property
    def linear_displacement(self):

        return self.x

    @property
    def angular_displacement(self):

        return ((self.x)/(self.r))

    @property
    def linear_velocity(self):

        return self.x.diff(self.ivar)

    @cached_property
    def components(self):
        components = {}

        self.mass_bike=MaterialPoint(self.m_b,self.linear_displacement,qs=self.qs,ivar=self.ivar)
        self.mass_driver=MaterialPoint(self.m_d,self.linear_displacement,qs=self.qs,ivar=self.ivar)
        self.rear_wheel=RollingDisk(self.m_r, R=self.r, x=self.x, qs=self.qs, ivar = self.ivar)(label='Rear wheel')
        self.front_wheel=RollingDisk(self.m_f, R=self.r, x=self.x, qs=self.qs, ivar = self.ivar)(label='Front wheel')
        self.engine_moment=Force(self.T,pos1 = self.angular_displacement,qs =self.qs,ivar=self.ivar)(label='Bike engine')
        self.drag_force=Force(-S.One/2*self.Ad*self.Cd*self.Af*(self.linear_velocity)**2,self.x,qs=self.qs,ivar=self.ivar)
        components['mass_bike'] = self.mass_bike
        components['mass_driver']=self.mass_driver
        components['rear_wheel']=self.rear_wheel
        components['front_wheel']=self.front_wheel
        components['engine_moment']=self.engine_moment
        components['drag_force']=self.drag_force


        return components

    def v_max(self):
        vmax=Symbol("v_{max}",positive=True)
        eq=Eq(self.eoms[0].subs(self.linear_velocity,vmax).doit(),0)
        sol=solve(eq,vmax)[1]
        return Eq(vmax,sol)
    
    def symbols_description(self):
        i_roc=self.i_w.diff(self.ivar)
        self.sym_desc_dict = {
            self.U_z: r'voltage supplying the rotor',
            self.R_w: r'equivalent resistance of the rotor windings',
            self.L_w: r'equivalent inductance of the rotor windings',
            self.E: r'electromotive force of induction',
            self.U_Rw: r'voltage across the rotor winding resistance',
            self.U_Lw: r'voltage related to the rotor inductance',
            self.k_e: r'back electromotive force constant',
            self.M_s: r'rotor torque',
            self.B: r'coefficient of viscous friction reduced to the rotor shaft',
            self.J: r'moment of inertia reduced to the rotor shaft',
            self.M_obc: r'engine load torque',
            self.k_m: r'torque constant',
            self.i_w: r'rotor winding current',
            i_roc:r'rotor winding current rate of change',
            self.omega_s:r'angular velocity of the rotor',
            self.M_a:r'rotor angular acceleration torque',
            self.M_r:r'rotor motion resistance torque',
            self.omega_s.diff(self.ivar):r'angular acceleration of the rotor',
        }
        return self.sym_desc_dict

    def get_default_data(self):
        default_data_dict = {
#             self.U_z: [10],
#             self.R_w: [2],
#             self.L_w: [0.1],
#             self.k_e: [0.1],
#             self.k_m: [0.1],
#             self.J: [0.1],
#             self.B: [0.5],
#             self.M_obc: [0.2],
            self.r:[0.3175],
#             self.c:[1000],
            self.m_b:[270],
            self.m_d:[80],
            self.m_r:[19],
            self.m_f:[15],
            self.Cd:[0.65],
            self.Ad:[1.2047],
            self.Af:[0.6]
        }
        return default_data_dict


    def _dimensionless_ode(self):

        from ...solvers.linear import ODESystem,FirstOrderLinearODESystem

        t = self.ivar
        tau = Symbol('tau')

        syms_dict = {
                    # dcmotor.U_z: 0,
                    self.R_w: 1,
                    self.L_w: 1,
                    # dcmotor.k_e: Symbol('kappa',positive=True),
                    # dcmotor.k_m: Symbol('kappa',positive=True),

                    self.k_e: Symbol('kappa',negative=True),
                    self.k_m: Symbol('kappa',negative=True),

                    self.J: 1,
                    self.B: 1,
                    t:tau,
                    # dcmotor.M_obc: 10,
                    }
        dvars = Matrix([[self.i_w], [self.omega_s]]).subs({t:tau})

        ode = ODESystem(odes=(self._eoms.subs(syms_dict))*-1, dvars = dvars, ode_order=1,ivar=tau)

        #return FirstOrderLinearODESystem.from_ode_system(ode)
        return ode

class MotorbikeReducedToDisk(ReducedMotorbike):

    phi=dynamicsymbols('\phi')

    def __init__(self,
             M=None,
             m_b=None,
             m_d=None,
             m_r=None,
             m_f=None,
             x=None,
             r=None,
             Cd=None,
             Ad=None,
             Af=None,
             T=None,
             phi=None,
             ivar=Symbol('t'),
             **kwargs):

        if M is not None: self.M=M
        if m_b is not None: self.m_b = m_b
        if m_d is not None: self.m_d = m_d
        if m_r is not None: self.m_r = m_r
        if m_f is not None: self.m_f = m_f
        if x is not None: self.x = x
        if r is not None: self.r=r
        if Cd is not None: self.Cd=Cd
        if Ad is not None: self.Ad=Ad
        if Af is not None: self.Af=Af
        if T is not None: self.T=T
        if phi is not None: self.phi=phi

        self.ivar = ivar

        self.qs = [self.phi]
        self._init_from_components(**kwargs)

    @property
    def linear_displacement(self):

        return self.phi*self.r

    @property
    def angular_displacement(self):

        return self.phi

    @property
    def linear_velocity(self):

        return (self.phi*self.r).diff(self.ivar)

    @cached_property
    def components(self):
        components = {}

        self.mass_bike=MaterialPoint(self.m_b,self.linear_displacement,qs=self.qs,ivar=self.ivar)
        self.mass_driver=MaterialPoint(self.m_d,self.linear_displacement,qs=self.qs,ivar=self.ivar)
        self.rear_wheel=RollingDisk(self.m_r, R=self.r, x=self.linear_displacement, qs=self.qs, ivar = self.ivar)(label='Rear wheel')
        self.front_wheel=RollingDisk(self.m_f, R=self.r, x=self.linear_displacement, qs=self.qs, ivar = self.ivar)(label='Front wheel')
        self.engine_moment=Force(self.T,pos1 = self.angular_displacement,qs =self.qs,ivar=self.ivar)(label='Bike engine')
        self.drag_force=Force(-S.One/2*self.Ad*self.Cd*self.Af*(self.linear_displacement.diff(self.ivar))**2,self.phi,qs=self.qs,ivar=self.ivar)

        components['mass_bike'] = self.mass_bike
        components['mass_driver']=self.mass_driver
        components['rear_wheel']=self.rear_wheel
        components['front_wheel']=self.front_wheel
        components['engine_moment']=self.engine_moment
        components['drag_force']=self.drag_force


        return components


    def omega_max(self):
        omega_max=Symbol("\omega_{max}")
        eq=Eq(self.eoms[0].subs(self.angular_displacement.diff(self.ivar),omega_max).doit(),0)
        sol=solve(eq,omega_max)
        return Eq(omega_max,sol[1])