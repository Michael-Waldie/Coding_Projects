# RR-Simulation
This was a homework for my operating systems class.

GanntChart.py creates a gannt chart for five premade processes.
Both charts use a quantum of 10 while the first uses a context switch of 0 while the second uses a context switch of 2.

RandomArrival.py generates x number of random numbers between 0 and 1 which then gets turned into arrival times and service times.
These times are between a minimum and maximum bounds.

RR_simulation.py simulates the round robin of an operating system given a list of processes with service and arrival times.
It also needs a given quantum and context switch.
GanntChart.py uses this to generate its chart.
RandomArrival.py can be used to generate a number of random processes for the simulation.
