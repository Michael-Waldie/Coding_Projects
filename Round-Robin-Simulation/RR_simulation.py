#  Michael Waldie
#  3/14/23
#  CSC 440 02
import RandomArrival as RandArr
import copy


class OperatingSystem:
    clock = 0
    start = []
    end = []
    initial_wait = []
    total_wait = []
    turn_around = []
    quantum = 0
    context_switch = 0
    process_list = []

    def __init__(self, quant, context, num_processes):
        self.quantum = quant
        self.context_switch = context
        self.clock = 0
        self.start = [None] * num_processes
        self.end = [None] * num_processes
        self.initial_wait = []
        self.total_wait = []
        self.turn_around = []
        #  Generate arrival and service times
        rand_x = RandArr.random_x(num_processes)
        inter = RandArr.convert_random(rand_x)
        arrival_times = RandArr.convert_inter_arrival(inter)
        service_times = RandArr.convert_to_service(rand_x)
        #  Generate x processes
        self.process_list = []
        for i in range(num_processes):
            self.process_list.append(Process(i + 1, service_times[i], arrival_times[i]))

    def set_processes(self, p_list):
        self.process_list = p_list

    #  Simulates a dispatcher for RR scheduling.
    def dispatcher(self):
        disp_process = copy.deepcopy(self.process_list)
        #  If all processes have been completed end the loop
        l = len(disp_process)
        while len(disp_process) > 0:
            current_process = disp_process.pop(0)
            #  If the current process needs service and has arrived
            p = current_process.service_time
            o = current_process.arrival_time
            c = self.clock
            if current_process.service_time > 0 and current_process.arrival_time <= self.clock:
                #  If the current process is just now starting add it to the start list
                if current_process.service_time == self.process_list[current_process.p_id - 1].service_time:
                    self.start[current_process.p_id - 1] = self.clock
                #  If the current process needs less time the a quantum only use that time
                # print(current_process.p_id, self.clock, end=' ')  #  USED FOR TESTING UNCOMMENT TO USE
                if current_process.service_time < self.quantum:
                    self.clock += current_process.service_time + self.context_switch  # Add time used and CS
                    current_process.service_time = 0
                else:
                    current_process.service_time -= self.quantum
                    self.clock += self.quantum + self.context_switch
                # print(self.clock, end='| ')  #  USED FOR TESTING UNCOMMENT TO USE
                #  If the service has ended add it to the end list
                if current_process.service_time == 0:
                    self.end[current_process.p_id - 1] = self.clock
                #  If service is still needed add it back to the queue
                else:
                    disp_process.append(current_process)
            #  If the process has not arrived yet add it back to the queue
            else:
                disp_process.append(current_process)

    #  Does the math for initial wait time, turn around time, and total wait time.
    def math(self):
        for i in range(len(self.process_list)):
            #  Time spent waiting after arrival
            self.initial_wait.append(self.start[i] - self.process_list[i].arrival_time)
            #  completion - arrival
            self.turn_around.append(self.end[i] - self.process_list[i].arrival_time)
            #  turn around - burst
            self.total_wait.append(self.turn_around[i] - self.process_list[i].service_time)

    #  Prints important information about each program after the round robin
    def output(self):
        print("ID | Arrival Time | Service Time| Start Time | End Time | Initial Wait | Total Wait | Turn Around |")
        for i in range(len(self.process_list)):
            print("{:^3}|{:^14}|{:^13}|{:^12}|{:^10}|{:^14}|{:^12}|{:^13}|".format(
                self.process_list[i].p_id, self.process_list[i].arrival_time,
                self.process_list[i].service_time, self.start[i], self.end[i],
                self.initial_wait[i], self.total_wait[i], self.turn_around[i]))


class Process:
    p_id = 0
    service_time = 0
    arrival_time = 0

    def __init__(self, pid, s_time, a_time):
        self.p_id = pid
        self.service_time = s_time
        self.arrival_time = a_time

    def output(self):
        print(self.p_id, self.service_time, self.arrival_time)


if __name__ == "__main__":
    opp = OperatingSystem(1, 0, 10)
    opp.dispatcher()
    opp.math()
    opp.output()
