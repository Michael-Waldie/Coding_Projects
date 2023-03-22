#  Michael Waldie
#  3/21/2023
#  CSC 440 02

import RR_simulation as RR

quantum = 10
context1 = 0
context2 = 2


service_times = [75, 40, 25, 20, 45]
arrival_times = [0, 10, 10, 80, 85]
processes = []
clock = 0

if __name__ == "__main__":
    for i in range(len(service_times)):
        processes.append(RR.Process(i + 1, service_times[i], arrival_times[i]))
    num_p = len(processes)
    print('Quantum of 10 and context switch of 0:')
    opp = RR.OperatingSystem(quantum, context1, num_p)
    opp.set_processes(processes)
    opp.dispatcher()
    opp.math()
    opp.output()
    print('---------------------------------------------------------------------------------------------------')
    print('Quantum of 10 and context switch of 2:')
    opp2 = RR.OperatingSystem(quantum, context2, num_p)
    opp2.set_processes(processes)
    opp2.dispatcher()
    opp2.math()
    opp2.output()
