import numpy as np
from scipy.integrate import odeint

class HarmonicDrive():
    """
    HarmonicDrive Base Class model
    Ref:

    """
    def __init__(self,Tinput,Vinput,N = 100) -> None:
        self.reductionRatio = N
        self.inputTorque    = Tinput
        self.inputVelocity  = Vinput
        self.c1 = 1
        self.c2 = 2
        
    
    def getOutputVelocity(self):
        """ """
        V=1
        return V
    
    def getOutputTorque(self):
        """ """
        T=1
        return T
    
    def computeCompliance(self, inputSpeed):
        """Compute the  """
        return 
    
    
    
    
    
    
"""
 


def HarmonicDrive(reductionRatio, inputTorque, inputVelocity, samplingRate, **kwargs):
    # Default parameters
    default_kinematicErrorParams = np.array([[0.57, 0.765, 0.72], [0.21, 0.31, 0.82]])
    default_complianceParams = np.array([0.32, 0.52])
    default_frictionParams = np.array([0.2, 0.15, 0.23, 0.19, 0.9])
    timeStep = 1 / samplingRate
    
    # Parse optional arguments
    kinematicErrorParams = kwargs.get('kinematicErrorParams', default_kinematicErrorParams)
    complianceParams = kwargs.get('complianceParams', default_complianceParams)
    frictionParams = kwargs.get('frictionParams', default_frictionParams)
    
    assert kinematicErrorParams.shape == (2, 3), "Invalid dimensions: 'kinematicErrorParams' must be a 2x3 matrix."
    assert len(frictionParams) == 5, "Invalid length: 'frictionParams' must be a vector of length 5."
    assert len(complianceParams) == 2, "Invalid length: 'complianceParams' must be a vector of length 2."
    assert inputTorque.shape == inputVelocity.shape, "Size mismatch: 'inputTorque' and 'inputVelocity' must have the same dimensions."
    
    timeSpan = (len(inputVelocity) - 1) / samplingRate
    time = np.arange(0, timeSpan + timeStep, timeStep)
    
    inputTorqueDerivative = np.diff(inputTorque) / timeStep
    inputVelocityDerivative = np.diff(inputVelocity) / timeStep
    inputVelocity = inputVelocity[:, np.newaxis]
    inputTorque = inputTorque[:, np.newaxis]
    
    def f(x, t):
        return (inputVelocity + reductionRatio * x) / inputTorque - \
               computeCompliance(reductionRatio, inputVelocity, x, complianceParams[0], complianceParams[1]) * \
               inputTorqueDerivative / inputTorque - \
               inputVelocityDerivative * (kinematicErrorParams[0, 0] + 3 * kinematicErrorParams[0, 1] * inputVelocity ** 2) / \
               (reductionRatio * (kinematicErrorParams[0, 0] + 3 * kinematicErrorParams[0, 1] * x ** 2))
    
    x0 = 0.0001 * np.ones_like(inputVelocity)
    flexSplineVelocity = odeint(f, x0, time, rtol=1e-3, atol=1e-2, hmax=0.1)
    maxInputVelocity = np.max(inputVelocity)
    
    flexSplineVelocity = np.minimum(np.squeeze(flexSplineVelocity), maxInputVelocity)
    compliance = computeCompliance(reductionRatio, inputVelocity, flexSplineVelocity, complianceParams[0], complianceParams[1])
    
    outputVelocity = flexSplineVelocity + \
                     kinematicErrorParams[0, 0] * np.sin(inputVelocity + kinematicErrorParams[1, 0]) + \
                     kinematicErrorParams[0, 1] * np.sin(2 * inputVelocity + kinematicErrorParams[1, 1]) + \
                     kinematicErrorParams[0, 2] * np.sin(4 * inputVelocity + kinematicErrorParams[1, 2]) + \
                     (1 / reductionRatio) * inputVelocity
    
    flexplineVelocityDerivative = np.diff(flexSplineVelocity) / timeStep
    
    frictionTorque = frictionParams[0] + frictionParams[1] * flexplineVelocityDerivative + \
                     frictionParams[2] * flexplineVelocityDerivative ** 3 + \
                     frictionParams[3] * np.cos(flexplineVelocityDerivative) + \
                     frictionParams[4] * np.sin(flexplineVelocityDerivative)
    
    maxInputTorque = np.max(np.abs(inputTorque))
    frictionTorque = np.where(np.abs(frictionTorque) > maxInputTorque,
                              np.sign(frictionTorque) * maxInputTorque,
                              frictionTorque)
    
    outputTorque = reductionRatio * inputTorque + frictionTorque
    efficacity = np.abs(outputTorque * outputVelocity / (inputTorque * inputVelocity))
    
    return outputTorque.squeeze(), outputVelocity.squeeze(), frictionTorque.squeeze(), efficacity.squeeze(), compliance

def computeCompliance(reductionRatio, inputSpeed, outputSpeed, c1, c2):
    assert c1 != 0, 'Compliance coefficient 1 should be non-null!'
    assert inputSpeed.shape == outputSpeed.shape, "Input speed vectors must be same size"
    
    outputSpeed[inputSpeed >= outputSpeed] = inputSpeed[inputSpeed >= outputSpeed]
    compliance = c1 * (inputSpeed + reductionRatio * outputSpeed) + c2 * (inputSpeed + reductionRatio * outputSpeed) ** 3
    compliance[compliance <= 0] = np.abs(compliance[compliance <= 0])
    
    return compliance.squeeze()



"""