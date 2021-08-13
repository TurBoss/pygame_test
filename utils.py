# p=Pid(3.0,0.4,1.2)
# p.setPoint(5.0)
# while True:
#     pid = p.update(measurement_value)


class Pid:
    """ Discrete PID control """

    def __init__(self,
                 p=2.0,
                 i=0.0,
                 d=1.0,
                 derivator=0,
                 integrator=0,
                 integrator_max=500,
                 integrator_min=-500):

        self.p_value = 0
        self.i_value = 00
        self.d_value = 0

        self.kp = p
        self.ki = i
        self.kd = d
        self.derivator = derivator
        self.integrator = integrator
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min

        self.set_point = 0.0
        self.error = 0.0

    def update(self, current_value):
        """ Calculate PID output value for given reference input and feedback """

        self.error = self.set_point - current_value

        self.p_value = self.kp * self.error
        self.d_value = self.kd * (self.error - self.derivator)
        self.derivator = self.error

        self.integrator = self.integrator + self.error

        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max
        elif self.integrator < self.integrator_min:
            self.integrator = self.integrator_min

        self.i_value = self.integrator * self.ki

        pid = self.p_value + self.i_value + self.d_value

        return pid

    def set_setpoint(self, value):
        """ Initilize the setpoint of PID """

        self.set_point = value
        self.integrator = 0
        self.derivator = 0

    def set_integrator(self, value):
        self.integrator = value

    def set_derivator(self, value):
        self.derivator = value

    def set_kp(self, value):
        self.kp = value

    def set_ki(self, value):
        self.ki = value

    def set_kd(self, value):
        self.kd = value

    def get_point(self):
        return self.set_point

    def get_error(self):
        return self.error

    def get_integrator(self):
        return self.integrator

    def get_derivator(self):
        return self.derivator
