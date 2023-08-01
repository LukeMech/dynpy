from sympy import (Symbol, symbols, Matrix, sin, cos, asin, diff, sqrt, S,
                   diag, Eq, hessian, Function, flatten, Tuple, im, pi, latex,
                   dsolve, solve, fraction, factorial, Subs, Number, oo, Abs,
                   N, solveset)

from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point
from sympy.physics.vector import vpprint, vlatex
from ...dynamics import LagrangesDynamicSystem, HarmonicOscillator, mech_comp

from ..elements import MaterialPoint, Spring, GravitationalForce, Disk, RigidBody2D, Damper, PID, Excitation, Force, base_frame, base_origin
from ...continuous import ContinuousSystem, PlaneStressProblem

import base64
import random
import IPython as IP
import numpy as np
import inspect

import matplotlib.pyplot as plt
from functools import cached_property, lru_cache

def plots_no():
    num = 0
    while True:
        yield num
        num += 1



class ComposedSystem(HarmonicOscillator):
    """Base class for all systems

    """
    _case_no = plots_no()
    
    scheme_name = 'damped_car_new.PNG'
    real_name = 'car_real.jpg'
    detail_scheme_name = 'sruba_pasowana.png'
    detail_real_name = 'buick_regal_3800.jpg'
    _default_args = ()
    _default_folder_path = "./dynpy/models/images/"
    _path = None

    z = dynamicsymbols('z')

    m0 = Symbol('m_0', positive=True)
    k0 = Symbol('k_0', positive=True)
    F0 = Symbol('F_0', positive=True)
    Omega0 = Symbol('Omega_0', positive=True)
    ivar=Symbol('t')

    
    @classmethod
    def _scheme(cls):

        path = cls._default_folder_path + cls.scheme_name

        return path

    @classmethod
    def _real_example(cls):
        path = cls._default_folder_path + cls.real_name

        return path

    @classmethod
    def _detail_real(cls):
        path = cls._default_folder_path + cls.detail_real_name

        return path

    @classmethod
    def _detail_scheme(cls):
        path = cls._default_folder_path + cls.detail_scheme_name

        return path

    def _init_from_components(self, *args, system=None, **kwargs):

        if system is None:
            composed_system = self._elements_sum
        else:
            composed_system = system

        #print('CS',composed_system._components)
        super(HarmonicOscillator,self).__init__(None, system=composed_system)

        #print('self',self._components)
        if self._components is None:
            comps = {}
        else:
            comps = self._components

        self._components = {**comps, **self.components}

    def __init__(self,
                 Lagrangian=None,
                 m0=None,
                 qs=None,
                 forcelist=None,
                 bodies=None,
                 frame=None,
                 hol_coneqs=None,
                 nonhol_coneqs=None,
                 label=None,
                 ivar=None,
                 evaluate=True,
                 system=None,
                 **kwargs):

        if ivar is not None: self.ivar = ivar
        if m0 is not None: self.m0 = m0

        if qs is not None:
            self.qs = qs
        else:
            self.qs = [self.z]


        
        self._init_from_components(system=system, **kwargs)

    @property
    def components(self):

        components = {}

        self._material_point = MaterialPoint(Symbol('ItIsWrongCode '), self.qs[0],
                                             self.qs)('Material Point')
        components['_material_point'] = self._material_point

        self._label = 'System seems to be wrong - method components is not overload'
        
        return components

    @property
    def elements(self):

        return {**super().components, **self.components}

    @classmethod
    def preview(cls, example=False):
        if example:
            path = cls._real_example()

        elif example == 'detail_scheme_name':
            path = cls._detail_scheme()
        elif example == 'detail_real_name':
            path = cls._detail_real()
        else:
            path = cls._scheme()
        print(path)
        with open(f"{path}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        image_file.close()

        return IP.display.Image(base64.b64decode(encoded_string))

    def _components_default_data(self):
        
        data=[elem._all_default_data()   for elem in self.elements.values()]

        
        return {key:value for elem in data for key, value in elem.items()}    
    
    def _components_numerical_data(self):
        
        data=[elem._all_numerical_data()   for elem in self.elements.values()]
        
        
        return {key:value for elem in data for key, value in elem.items()}    
    
    def _all_default_data(self):
        
        

        
        return {**self._components_default_data(),**self.get_default_data()}    
    
    def _all_numerical_data(self):
        
        return {**self._components_numerical_data(),**self.get_numerical_data()}  
    
    
    def get_default_data(self):
        return {}

    def get_numerical_data(self):
        return {}

    
    
    
    def get_random_parameters(self):

        
        #print('preview for',self)
        #display(self._all_default_data())
        #display(self.get_default_data())
        
        default_data_dict = {**self._components_default_data(),**self.get_default_data()}

        if default_data_dict:
            parameters_dict = {
                key: random.choice(items_list)
                for key, items_list in default_data_dict.items()
            }
        else:
            parameters_dict = None

        return parameters_dict

    def get_numerical_parameters(self):

        default_data_dict = {**self._components_numerical_data(),**self.get_numerical_data()}

        if default_data_dict:
            parameters_dict = {
                key: random.choice(items_list)
                for key, items_list in default_data_dict.items()
            }
        else:
            parameters_dict = None

        return parameters_dict

    @property
    def _report_components(self):

        comp_list = [
            mech_comp.TitlePageComponent,
            mech_comp.SchemeComponent,
            mech_comp.ExemplaryPictureComponent,
            mech_comp.KineticEnergyComponent,
            mech_comp.KineticEnergyDynPyCodeComponent,
            mech_comp.KineticEnergyDynPyCodeComponent,
            mech_comp.PotentialEnergyComponent,
            mech_comp.PotentialEnergyDynPyCodeComponent,
            mech_comp.PotentialEnergySymPyCodeComponent,
            mech_comp.LagrangianComponent,
            mech_comp.GoverningEquationComponent,
            mech_comp.GoverningEquationDynpyCodeComponent,
            mech_comp.GoverningEquationSympyCodeComponent,
            mech_comp.FundamentalMatrixComponent,
            mech_comp.GeneralSolutionComponent,
            mech_comp.GeneralSolutionDynpyCodeComponent,
            mech_comp.GeneralSolutionSympyCodeComponent,
            mech_comp.SteadySolutionComponent,
        ]

        return comp_list
    
    @lru_cache
    # def linearized(self,): #it was missing

    #     return type(self).from_system(super().linearized())
 
    @lru_cache   
    def linearized(self, x0=None, op_point=False, hint=[], label=None):

        #temporary workaround
        lin_sys = HarmonicOscillator(self).linearized(x0=x0,op_point=op_point,hint=hint,label=label)
        
        #old version
        #lin_sys=super().linearized(x0=x0,op_point=op_point,hint=hint,label=label)
        
        return type(self).from_system(lin_sys)

    def tensioner_belt_force(self):
        return self.k_tensioner * self.steady_solution()

    def left_belt_force(self):
        return self.k_belt * self.steady_solution()

    def right_belt_force(self):
        return self.k_belt * self.steady_solution()


#     def max_static_force_pin(self):
#         return abs(self.static_load().doit()[0])

#     def max_dynamic_force_pin(self):
#         return self.frequency_response_function() * self.stiffness_matrix(
#         )[0] + self.max_static_force_pin()

    def max_static_force_pin(self):
        return abs(self.static_load().doit()[0]) / 2

    def max_dynamic_force_pin(self):
        return self._frf()[0] * self.k_m + self.max_static_force_pin()

    def static_force_pin_diameter(self):
        kt = Symbol('k_t', positive=True)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_static_force_pin()) / (pi * kt * Re))**(1 / 2)

    def dynamic_force_pin_diameter(self):
        kt = Symbol('k_t', positive=True)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_dynamic_force_pin()) / (pi * kt * Re))**(1 / 2)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_static_force_pin()) / (pi * kt * Re))**(1 / 2)

    def dynamic_force_pin_diameter(self):
        kt = Symbol('k_t', positive=True)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_dynamic_force_pin()) / (pi * kt * Re))**(1 / 2)



class NonlinearComposedSystem(ComposedSystem):

    def frequency_response_function(self,
                                    frequency=Symbol('Omega', positive=True),
                                    amplitude=Symbol('a')):

        omega = (self.linearized()).natural_frequencies()[0]
        
        
        eps = self.small_parameter()

        exciting_force = self.external_forces()[0]

        comps = exciting_force.atoms(sin, cos)
        exciting_amp = sum([exciting_force.coeff(comp) for comp in comps])
        inertia = self.inertia_matrix()[0]

        return amplitude * (-frequency**2 + omega**2) * inertia + S(
            3) / 4 * eps * amplitude**3 - exciting_amp

    def amplitude_from_frf(self, amplitude=Symbol('a')):

        return solveset(self.frequency_response_function(), amplitude)

    @property
    def _report_components(self):

        comp_list = [
            mech_comp.TitlePageComponent,
            mech_comp.SchemeComponent,
            mech_comp.ExemplaryPictureComponent,
            mech_comp.KineticEnergyComponent,
            mech_comp.PotentialEnergyComponent,
            mech_comp.LagrangianComponent,
            mech_comp.LinearizationComponent,
            mech_comp.GoverningEquationComponent,
            mech_comp.FundamentalMatrixComponent,
            mech_comp.GeneralSolutionComponent,
            mech_comp.SteadySolutionComponent,
        ]

        return comp_list

    def max_static_force_pin(self):
        return abs(self.static_load().doit()[0]) / 2

    def max_dynamic_force_pin(self):
        lin_sys = ComposedSystem(self.linearized())
        #k_m = self._given_data[self.k_m]
        k_m = self.k_m
        #         display(lin_sys.stiffness_matrix()[0])

        return lin_sys.frequency_response_function() * (
            lin_sys.stiffness_matrix()[0]) / 2 + self.max_static_force_pin()

    def max_dynamic_nonlinear_force_pin(self):
        lin_sys = ComposedSystem(self.linearized())

        amp = list(self.amplitude_from_frf())
        display(amp)
        #k_m = self._given_data[self.k_m]
        k_m = self.k_m

        return amp[0] * k_m + self.max_static_force_pin()
    
    
    
class SpringMassSystem(ComposedSystem):
    """Ready to use sample Single Degree of Freedom System with mass on spring
        Arguments:
        =========
            m = Mass
                -Mass of system on spring

            k = Spring coefficient
                -Spring carrying the system

            ivar = symbol object
                -Independant time variable

            qs = dynamicsymbol object
                -Generalized coordinates

        Example
        =======
        A mass oscillating up and down while being held up by a spring with a spring constant k

        >>> t = symbols('t')
        >>> m, k = symbols('m, k')
        >>> qs = dynamicsymbols('z') # Generalized Coordinates
        >>> mass = SDoFHarmonicOscillator(m,k, qs=[z],) # Initialization of LagrangesDynamicSystem instance

        -We define the symbols and dynamicsymbols
        -Kinetic energy T and potential energy v are evaluated to calculate the lagrangian L
        -Reference frame was created with point P defining the position and the velocity determined on the z axis
        -external forces assigned
        -Next we determine the instance of the system using class LagrangeDynamicSystem
        -We call out the instance of the class
        -If necessary assign values for the default arguments


    """
    scheme_name = 'engine.png'
    real_name = 'engine_real.PNG'

    m=Symbol('m', positive=True)
    k=Symbol('k', positive=True)
    ivar=Symbol('t')
    
    z=dynamicsymbols('z')
    
    def __init__(self,
                 m=None,
                 k=None,
                 z=None,
                 ivar=None,
                 **kwargs):

        
        
        if m is not None: self.m = m
        if k is not None: self.k = k
        if ivar is not None: self.ivar = ivar
        if z is not None: self.z = z
        
   
        self.qs = [self.z]

        self._init_from_components(**kwargs)

    @property
    def components(self):

        components = {}
        
        self.material_point = MaterialPoint(self.m, self.z, qs=self.qs)
        self.spring = Spring(self.k, self.z, qs=self.qs)
        
        components['material_point'] = self.material_point
        components['spring'] = self.spring
        
        return components
        
    def symbols_description(self):
        self.sym_desc_dict = {
            self.m: r'mass of system on the spring',
            self.k: r'Spring coefficient ',
        }

        return self.sym_desc_dict
    


class DampedMeasuringTool(ComposedSystem):

    scheme_name = 'measure_tool.PNG'
    real_name = 'measure_tool_real.PNG'
    #detail_scheme_name =
    #detail_real_name =

    m = Symbol('m', positive=True)
    l = Symbol('l', positive=True)
    k = Symbol('k', positive=True)
    k_t = Symbol('k_t', positive=True)
    Omega = Symbol('Omega', positive=True)
    F = Symbol('F', positive=True)
    phi = dynamicsymbols('\\varphi')
    c = Symbol('c', positive=True)
    c_t = Symbol('c_t', positive=True)
    lam = Symbol('lambda', positive=True)
    l0 = Symbol('l_0', positive=True)
    lam0 = Symbol('lambda_0', positive=True)

    def __init__(self,
                 m=None,
                 l=None,
                 k=None,
                 k_t=None,
                 ivar=Symbol('t'),
                 Omega=None,
                 F=None,
                 phi=None,
                 qs=None,
                 c=None,
                 c_t=None,
                 lam=None,
                 l0=None,
                 lam0=None,
                 **kwargs):
        if l is not None: self.l = l
        if m is not None: self.m = m
        if k is not None: self.k = k
        if k_t is not None: self.k_t = k_t
        if F is not None: self.F = F
        if Omega is not None: self.Omega = Omega
        if phi is not None: self.phi = phi
        if c is not None: self.c = c
        if c_t is not None: self.ct = ct
        if lam is not None: self.lam = lam
        if l0 is not None: self.l0 = l0
        if lam0 is not None: self.lam0 = lam0

        self.qs = [self.phi]
        self.ivar = ivar

        self._init_from_components(**kwargs)
        
    @property
    def components(self):
        components = {}

        self._moment_of_inertia = MaterialPoint((S.One / 3) * self.m * self.l**2, self.phi, qs=[self.phi])
        self._upper_spring = Spring(self.k, pos1=self.l * self.phi, qs=[self.phi])
        self._lower_spring = Spring(self.k, pos1=self.l * self.phi, qs=[self.phi])
        self._spiral_spring = Spring(self.k_t, self.phi, qs=[self.phi])
        self._force = Force(self.F * self.l, pos1=self.phi)
        self._springs_damping = Damper(2 * self.c, pos1=self.l * self.phi, qs=[self.phi])
        self._spiral_spring_damping = Damper(self.c_t, pos1=self.phi, qs=[self.phi])


        components['_moment_of_inertia'] = self._moment_of_inertia
        components['_upper_spring'] = self._upper_spring
        components['_lower_spring'] = self._lower_spring
        components['_spiral_spring'] = self._spiral_spring
        components['_force'] = self._force
        components['_springs_damping'] = self._springs_damping
        components['_spiral_spring_damping'] = self._spiral_spring_damping

        return components

    def get_default_data(self):

        m0, k0, F0, Omega0, lam0, l0 = self.m0, self.k0, self.F0, self.Omega0, self.lam0, self.l0

        default_data_dict = {
            self.c: [self.lam * (self.k)],
            self.c_t: [self.lam * (self.k_t)],
            self.m: [m0 * S.One * no for no in range(1, 8)],
            self.k: [k0 * S.One * no for no in range(1, 8)],
            self.k_t: [k0 * l0**2 * S.One * no for no in range(1, 8)],
            self.F: [
                F0 * S.One * no * cos(self.Omega * self.ivar)
                for no in range(1, 8)
            ],
            self.Omega: [self.Omega],
            self.lam: [self.lam],
            self.l: [l0 * S.One * no for no in range(1, 8)],
        }

        return default_data_dict
    
    def dynamic_force(self):
        data=self._given_data
        amps=self._fodes_system.steady_solution.as_dict()
        dyn_force=(self.components['_spiral_spring'].force().subs(amps)).subs(data).expand().doit()
        
        return dyn_force
    
    def static_force(self):
        data=self._given_data
        ans=self.dynamic_force()
        free_coeff=ans.subs({cos(self.Omega*self.ivar):0, sin(self.Omega*self.ivar):0}).subs(data)
        return (free_coeff)

    def steady_state(self):
        return 3 * (S.One / 2 * self.damping_coefficient())**(-1)

    def max_static_force_pin(self):
        return abs(self.static_load().doit()[0])

    def max_dynamic_force_pin(self):
        lin_sys = self.linearized()

        dyn_comp = (lin_sys.frequency_response_function() * self.l *
                    self.k).subs(self._given_data)

        total_force = (dyn_comp + self.max_static_force_pin())

        return total_force

    def static_force_pin_diameter(self):
        kt = Symbol('k_t', positive=True)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_static_force_pin()) / (pi * kt * Re))**(1 / 2)

    def dynamic_force_pin_diameter(self):
        kt = Symbol('k_t', positive=True)
        Re = Symbol('R_e', positive=True)
        return ((4 * self.max_dynamic_force_pin()) / (pi * kt * Re))**(1 / 2)


class LagrangeIBlocksOnInclinedPlane(ComposedSystem):
    scheme_name = 'ddof_disks_3_springs_scheme.png'
    real_name = 'nonlin_trolley_real.PNG'

    def __init__(self,
                 m=Symbol('m', positive=True),
                 m1=Symbol('m_1', positive=True),
                 m2=Symbol('m_2', positive=True),
                 m3=Symbol('m_3', positive=True),
                 m4=Symbol('m_4', positive=True),
                 R=Symbol('R', positive=True),
                 g=Symbol('g', positive=True),
                 alpha=Symbol('alpha',positive=True),
                 beta=Symbol('beta',positive=True),
                 ivar=Symbol('t'),
                 x1=dynamicsymbols('x_1'),
                 x2=dynamicsymbols('x_2'),
                 x3=dynamicsymbols('x_3'),
                 x4=dynamicsymbols('x_4'),
                 phi=dynamicsymbols('\\varphi'),
                 qs=dynamicsymbols('x_1, x_2, x_3, x_4, \\varphi'),
                 **kwargs):

        self.m = m
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m
        self.R = R
        self.g = g
        self.alpha = alpha
        self.beta = beta
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.phi = phi
        self.qs = qs


        #IMROVE
        self._init_from_components(**kwargs)
        
    @property
    def components(self):

        ######## ELEMENTS MOVED FROM __init__ METHOD
        self.Mass1 = MaterialPoint(self.m1, pos1=self.x1, qs=[self.x1]) + GravitationalForce(self.m1, self.g, pos1=-self.x1*sin(self.alpha), qs=[self.x1])
        self.Mass2 = MaterialPoint(self.m2, pos1=self.x2, qs=[self.x2]) + GravitationalForce(self.m2, self.g, pos1=-self.x2*sin(self.alpha), qs=[self.x2])
        self.Mass3 = MaterialPoint(self.m3, pos1=self.x3, qs=[self.x3]) + GravitationalForce(self.m3, self.g, pos1=-self.x3*sin(self.beta), qs=[self.x3])
        self.Mass4 = MaterialPoint(self.m4, pos1=self.x4, qs=[self.x4]) + GravitationalForce(self.m4, self.g, pos1=-self.x4*sin(self.beta), qs=[self.x4])
        self.Pulley = MaterialPoint(1/2*self.m*self.R**2, pos1=self.phi, qs=[self.phi])

        ####################

        components = {}

        components['Mass1'] = self.Mass1
        components['Mass2'] = self.Mass2
        components['Mass3'] = self.Mass3
        components['Mass4'] = self.Mass4
        components['Pulley'] = self.Pulley
        
        return components
        
    def get_default_data(self):

        m0 = symbols('m_0', positive=True)

        default_data_dict = {
            self.m: [S.Half * m0, 1 * m0, 2 * m0, 4 * m0, S.Half**2 * m0],
            self.m1: [S.Half * m0, 1 * m0, 2 * m0, 4 * m0, S.Half**2 * m0],
            self.m2: [S.Half * m0, 1 * m0, 2 * m0, 4 * m0, S.Half**2 * m0],
            self.m3: [S.Half * m0, 1 * m0, 2 * m0, 4 * m0, S.Half**2 * m0],
            self.m4: [S.Half * m0, 1 * m0, 2 * m0, 4 * m0, S.Half**2 * m0],
        }

        return default_data_dict

    def get_random_parameters(self):

        default_data_dict = self.get_default_data()

        parameters_dict = {
            key: random.choice(items_list)
            for key, items_list in default_data_dict.items()
        }

        return parameters_dict

    
#TODO
class LagrangeIOnMathFunction(ComposedSystem):

    scheme_name = 'mat_point_parabola.PNG'
    real_name = 'tautochrone_curve_small.gif'

    
    
    
    def __init__(self,
                 m=Symbol('m', positive=True),
                 g=Symbol('g', positive=True),
                 x=dynamicsymbols('x'),
                 y=dynamicsymbols('y'),
                 a=symbols('a',positive=True),
                 R=symbols('R',positive=True),
                 ivar=Symbol('t'),
                 qs=dynamicsymbols('x,y'),
                 **kwargs):

        self.m = m
        self.x = x
        self.y = y
        self.a = a
        self.R = R
        self.g = g

        system = HarmonicOscillator(S.Half*m*x.diff(ivar)**2+S.Half*m*y.diff(ivar)**2-m*g*y,qs=[x,y])

        super().__init__(system(qs),**kwargs)

    def get_default_data(self):


        m0 = symbols('m_0', positive=True)
        x  = self.x
        a, Omega = symbols('a, Omega', positive=True)

        default_data_dict = {
            self.m :[S.Half * m0, 1 * m0, 2 * m0, 2**2 * m0, S.Half**2 * m0,8*m0,S.Half**3],
            self.y:[ a*x**2, a*(1-cos(x)),a*sin(x)**2,a*sin(x)**4,a*x**4]

        }

        return default_data_dict
    

#TODO
class CrankSystem(ComposedSystem):

    scheme_name = 'crank_mechanismlow.jpg'
    real_name = 'crank_slider_real.jpg'

    
    _default_folder_path = "./dynpy/models/images/"



    def _detail_scheme(self):

        self.preview()

        return self._path
    
    
    def preview(self, example=False):
        

        if self._path:
            path = self._path
            
        else:

            plt.figure(figsize=(10,10))


            plt.xlim(-0.5,1)
            plt.ylim(-0.25,1.25)
            plt.grid(True)
            
            if (self._given_data)=={}:
            
                path = self.__class__._default_folder_path + self.__class__.scheme_name
            else:
                

                
                h_num=float(self.h.subs(self._given_data))
                r_num=float(self.r.subs(self._given_data))
                phi_num=float(self.phi.subs(self._given_data))
                a_num=float(self.a.subs(self._given_data))
                b_num=float(self.b.subs(self._given_data))                
                
                pOx = 0
                pOy = 0
                plt.text(-0.05+(pOx),(-0.05+pOy),'O')
                
                pAx=0
                pAy=h_num
                plt.text(-0.05+(pAx),(+0.05+pAy),'A')
                
                plt.plot([pOx,pAx],[pOy,pAy],'b',linewidth=2)
                plt.text(-0.05+(pOx+pAx)/2,(pOy+pAy)/2,'h')
                
                pBx = pAx + r_num*np.sin(phi_num)
                pBy = pAy + r_num*np.cos(phi_num)
                plt.text(+0.05+(pBx),(+0.00+pBy),'B')
                
                plt.plot([pBx,pAx],[pBy,pAy],'r',linewidth=2)
                plt.text((pBx+pAx)/2,0.05+(pBy+pAy)/2,'r')
                
                lBO = ((pBx-pOx)**2 + (pBy-pOy)**2)**0.5
                
                p1x = 1.1*(h_num+r_num)*pBx/lBO
                p1y = 1.1*(h_num+r_num)*pBy/lBO
                
                plt.plot([p1x,pOx],[p1y,pOy],'g',linewidth=2)

                pCx = a_num*pBx/lBO
                pCy = a_num*pBy/lBO
                plt.text(+0.05+(pCx),(+0.05+pCy),'C')
                
                plt.plot([pOx,pCx],[pOy,pCy],'m',linewidth=2)
                plt.text(0.05+(pOx+pCx)/2,(pOy+pCy)/2,'a')
                
#                 pDx = pCx+(b_num**2 - pCy**2)**0.5        # poprawna wartość położenia D
                pDx = (pCx+(b_num**2 - pCy**2)**0.5)*1.15   # celowo wprowadzony błąd
                pDy = 0
                plt.text(+0.05+(pDx),(+0.00+pDy),'D')
                
                plt.plot([pCx,pDx],[pCy,pDy],'k',linewidth=2)
                plt.text((pCx+pDx)/2,0.05+(pCy+pDy)/2,'b')
            
                path = self.__class__._default_folder_path + 'previews/' + self.__class__.__name__ + str(
                                            next(self.__class__._case_no)) + '.png'

                plt.savefig(path)
                self._path=path

                plt.close()

        

#        print('check' * 100)
        print(self._path)
#        print('check' * 100)
        plt.close()

        with open(f"{path}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        image_file.close()

        return IP.display.Image(base64.b64decode(encoded_string))
    
    
    
    def __init__(self,
                 I=Symbol('I', positive=True),
                 r=Symbol('r', positive=True),
                 h=Symbol('h', positive=True),
                 a=Symbol('a', positive=True),
                 b=Symbol('b', positive=True),
                 phi=dynamicsymbols('\\varphi'),
                 beta=dynamicsymbols('beta'),
#                  alpha=dynamicsymbols('alpha'),
                 **kwargs):

        self.I = I
        self.h=h
        self.r=r
        self.phi = phi
        self.beta = beta
#         self.alpha = alp
        self.a = a
        self.b = b

        self.crank = MaterialPoint(I, phi, qs=[phi])
        composed_system = (self.crank)

        super().__init__(composed_system,**kwargs)

    @property
    def _dbeta(self):
        beta=atan(self.r/self.l*self.phi) #it's probably wrong - has to be checked
        return beta.diff(self.ivar)
    
    @property
    def _displacement_d(self):

        return -(-self.b*sqrt((self.h**2 - self.h**2*self.a**2/self.b**2 + 2*self.h*self.r*cos(self.phi) - 2*self.h*self.r*self.a**2*cos(self.phi)/self.b**2 + self.r**2 - self.r**2*self.a**2*cos(self.phi)**2/self.b**2)/(self.h**2 + 2*self.h*self.r*cos(self.phi) + self.r**2)) - self.r*self.a*sin(self.phi)/sqrt(self.h**2 + 2*self.h*self.r*cos(self.phi) + self.r**2))
    
    @property
    def _velocity_b2(self):
        return (self.phi.diff(self.ivar)*self.r)
    @property
    def _velocity_b2b3(self):
        return (sqrt(self.h**2 + 2*self.h*self.r*cos(self.phi) + self.r**2)).diff(self.ivar)
    @property
    def _velocity_b3(self):
        gamma=asin(self._velocity_b2b3/self._velocity_b2)
        return self._velocity_b2*cos(gamma)
    @property
    def _velocity_d(self):
        return self._displacement_d.diff(self.ivar)
    @property
    def _velocity_c(self):
        omega3=self._velocity_b3/sqrt(self.r**2 + self.h**2 - 2*self.r*self.h*cos(pi-self.phi))
        return omega3*self.a
    @property
    def _acceleration_b2(self):
        return self.phi.diff(self.ivar)**2*self.r
    @property
    def _acceleration_b3n(self):
        return (self._velocity_b3**2/sqrt(self.r**2 + self.h**2 - 2*self.r*self.h*cos(pi-self.phi)))
    @property
    def _acceleration_cn(self):
        return (self._velocity_b3**2*(self.a/(sqrt(self.r**2 + self.h**2 - 2*self.r*self.h*cos(pi-self.phi)))**2))
    @property
    def _acceleration_d(self):
        return self._velocity_d.diff(self.ivar)

    
    @property
    def _omega_3(self):
        return (self._velocity_b3/sqrt(self.r**2 + self.h**2 - 2*self.r*self.h*cos(pi-self.phi)))
    @property
    def linkage_ang_velocity(self):
        return self._dbeta

    def symbols_description(self):
        self.sym_desc_dict = {
            self.I: r'crank moment of inertia',
            # self.k_beam: r'Beam stiffness',
            # self.g: r'gravitational field acceleration'
        }

        return self.sym_desc_dict

    def get_default_data(self):
        E, I, l, m0, k0 = symbols('E I0 l_beam m_0 k_0', positive=True)
        
        default_data_dict = {
            self.I: [20 * I, 30 * I,60 * I,50 * I,40 * I,],
            self.h:[1,2,3],
            self.r:[0.1,0.2,0.3],
            self.a:[10],
            self.b:[20],
            self.phi : [10,20,30],
        }

        return default_data_dict


#TODO
class MaterialPointMovement(ComposedSystem):

    m = Symbol('m', positive=True)
    g = Symbol('g', positive=True)
    c = Symbol('c', positive=True)
    r = Symbol('r', positive=True)
    phi = dynamicsymbols('\\varphi')

    c0 = Symbol('c0', positive=True)
    r0 = Symbol('r0', positive=True)
    phi0 = dynamicsymbols('phi0')

    def __init__(self,
                 m=None,
                 g=None,
                 c=None,
                 r=None,
                 phi=None,
                 ivar=Symbol('t'),
                 **kwargs):

        if m is not None: self.m = m
        if g is not None: self.g = g
        if c is not None: self.c = c
        if r is not None: self.r = r
        if phi is not None: self.phi = phi
        self.ivar = ivar

        self.qs = [self.phi]

        self._mass_x = MaterialPoint(self.m,
                                     pos1=self.r * sin(self.phi),
                                     qs=self.qs)
        self._mass_y = MaterialPoint(self.m,
                                     pos1=self.r * cos(self.phi),
                                     qs=self.qs)

        self._gravity_ = GravitationalForce(self.m,
                                            self.g,
                                            pos1=self.r * cos(self.phi),
                                            qs=self.qs)

        composed_system = self._mass_x + self._mass_y + self._gravity_

        super().__init__(composed_system, **kwargs)

    def symbols_description(self):
        self.sym_desc_dict = {
            self.m: r'Mass',
            self.g: r'Gravity constant',
            self.c: r'',
        }

        return self.sym_desc_dict

    def get_default_data(self):

        m0, c0, r0, phi0 = self.m0, self.c0, self.r0, self.phi0

        default_data_dict = {
            self.m: [m0 * no for no in range(1, 8)],
            self.c: [c0 * no for no in range(1, 8)],
            self.r: [r0 * no for no in range(1, 8)],
            self.phi: [phi0 * no for no in range(1, 8)],
        }

        return default_data_dict
    
    def get_numerical_data(self):

        m0, c0, r0, phi0 = self.m0, self.c0, self.r0, self.phi0

        default_data_dict = {
            self.m: [m0 * no for no in range(1, 8)],
            self.c: [c0 * no for no in range(1, 8)],
            self.r: [r0 * no for no in range(1, 8)],
            self.phi: [phi0 * no for no in range(1, 8)],
        }

        return default_data_dict

    def max_static_force(self):
        return S.Zero

    def max_dynamic_force(self):
        return S.Zero

            
#Kuba #poprawione            

class KinematicClutchWithSprings(ComposedSystem):
    #scheme_name = ''
    #real_name = ''
    #detail_scheme_name = ''
    #detail_real_name = ''

    l0 = Symbol('l_0', positive=True)
    G = Symbol('G', positive=True)
    I = Symbol('I', positive=True)
    l_1 = Symbol('l_1', positive=True)
    l_2 = Symbol('l_2', positive=True)
    I_1 = Symbol('I_1', positive=True)
    I_2 = Symbol('I_2', positive=True)
    Ms = Symbol('M_s', positive=True)
    Omega = Symbol('Omega', positive=True)
    ivar=Symbol('t')
    theta = dynamicsymbols('theta')
    phi = dynamicsymbols('\\varphi')

    def __init__(self,
                 l0=None,
                 G=None,
                 I=None,
                 l_1=None,
                 l_2=None,
                 I_1=None,
                 I_2=None,
                 Ms=None,
                 phi=None,
                 theta=None,
                 ivar=Symbol('t'),
                 qs=None,
                 **kwargs):
        
        if G is not None: self.G = G
        if I is not None: self.I = I
        if Ms is not None: self.Ms = Ms
        if l_1 is not None: self.l_1 = l_1
        if l_2 is not None: self.l_2 = l_2
        if I_1 is not None: self.I_1 = I_1
        if I_2 is not None: self.I_2 = I_2
        if phi is not None: self.phi = phi
        if theta is not None: self.theta = theta

        self.qs = [self.phi]
        self.ivar = ivar
        self._init_from_components(**kwargs)
    
    @cached_property
    def components(self):
        components = {}
        
        self.k_1 = (self.G * self.I_1) / self.l_1
        self.k_2 = (self.G * self.I_2) / self.l_2

        self.disc_1 = Disk(self.I, pos1=self.phi, qs=self.qs)
        self.spring_2 = Spring(self.k_1 * self.k_2 / (self.k_2 + self.k_1),
                               pos1=self.phi,
                               pos2=self.theta,
                               qs=self.qs)  #right spring
        self.moment = Force(self.Ms, pos1=self.phi, qs=self.qs)
        
        components['moment'] = self.moment
        components['disc_1'] = self.disc_1
        components['spring_2'] = self.spring_2
        
        return components


    def symbols_description(self):
        self.sym_desc_dict = {
            self.I: r'Moment of Inertia',
            self.k_1: r'',
            self.k_2: r'',
        }
        return self.sym_desc_dict
    def get_default_data(self):

        m0, l0, G, l = symbols('m_0 l_0 G l', positive=True)
        theta0, Omega = symbols('theta_0, Omega', positive=True)

        default_data_dict = {
            self.I: [S.Half * m0 * (l0**2) * no for no in range(1, 3)],
            self.I_1: [S.Half**(no) * (l0**4) for no in range(1, 8)],
            self.I_2: [S.Half**no * (l0**4) for no in range(1, 8)],
            self.l_1: [S.Half**(no - 6) * l0 for no in range(1, 8)],
            self.l_2: [S.Half**(no - 6) * l0 for no in range(1, 8)],
            self.theta: [theta0 * cos(Omega * self.ivar)],
        }

        return default_data_dict

    def disc_force(self):
        t = self.ivar
        return self.I * self.steady_solution().diff(t, t)

    def max_static_force_pin(self):
        d = Symbol('d', positive=True)
        return 2 * self.Ms / d

    def max_dynamic_force_pin(self):
        d = Symbol('d', positive=True)
        return self.frequency_response_function(
            self.natural_frequencies()[0]) * self.stiffness_matrix()[0]

    def max_static_bearing_force(self):
        d = Symbol('d', positive=True)
        return abs(2 * self.static_load()[0] / d)

    def max_dynamic_bearing_force(self):
        d = Symbol('d', positive=True)
        acc_amp = self.frequency_response_function() * self.Omega**2

        return abs(
            2 * (self.I * acc_amp) /
            d) + self.max_static_bearing_force()  #.subs(self._given_data)

    def static_key_length(self):
        kd = Symbol('k_d', positive=True)
        h = Symbol('h', positive=True)
        return (2 * self.max_static_bearing_force()) / (kd * h)

    def dynamic_key_length(self):

        kd = Symbol('k_d', positive=True)
        h = Symbol('h', positive=True)
        return (2 * self.max_dynamic_bearing_force()) / (kd * h)            