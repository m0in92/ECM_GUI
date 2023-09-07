# ECM-GUI

This Python package is the lithium-ion simulator using the equivalent-circuit
model.

## Installation and setup

The following repository can be installed by cloning it or downloading the tar.gz file in the dist directory.

Use the following repository link when cloning this repository: 
[git@github.com:m0in92/ECM_GUI.git](git@github.com:m0in92/ECM_GUI.git). Furthermore, the project python library 
dependencies, numpy and matplotlib, should be installed in your project.

When using the tar.gz file, first extract the contents from the file. Then, `cd` into the extracted content's root 
file path (where the setup.py file resides) and run the following into the command line:
```
python setup.py install
```

## Example Usage

The simulation involves first defining the parameters of the battery cell and creating a BatteryCell instance using
the defined parameters as such:
```
param = src.ParameterSet(R0=R0, R1=R1, C1=C1, Q=Q, func_SOC_OCV=func_SOC_OCV, func_eta=func_eta)
b_cell = src.BatteryCell(param=param, soc_init=soc_init)
```
Next, the `cycler` instance is defined which dictates the cycling protocol. In the following the `DischargeCycler`
object is used that performs one discharge cycling step:
```
cycler_instance = src.DischargeCycler(discharge_current=discharge_current, V_min=V_min,
                                      SOC_LIB_min=SOC_LIB_min, SOC_LIB=SOC_LIB)
```
This is followed by the simulation and visualization. First, the solver object is defined and then its `solver` method
is used, as illustrated below:
```
solver = src.DTSolver(battery_cell_instance=b_cell)
sol = solver.solve(cycler_instance=cycler_instance, dt=0.1)
```
The `solve` method creates a `Solution` object. It's plot `comprehensive_plot` method can be used to generate a visual
plot of the simulation results.
