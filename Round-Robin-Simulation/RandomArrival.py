#  Michael Waldie
#  3/14/2023
#  CSC 440 02
import random


#  Generates 100 random numbers between min and max.
def random_x(x):
    random_ints = [random.random() for _ in range(x)]
    return random_ints


#  Convert generated real numbers between 4 - 9 (inter-arrival times).
def convert_random(rand_list):
    inter_arrival = [round(4 + (9 - 4) * x) for x in rand_list]
    return inter_arrival


#  Convert inter-arrival times to arrival times.
def convert_inter_arrival(inter_list):
    arrival = [0]
    for i in range(len(inter_list)-1):
        l = arrival[i-1]
        p = inter_list[i]
        arrival.append(inter_list[i])
    return arrival


#  Convert generated real numbers to service times.
def convert_to_service(rand_list):
    service = [round(2 + (5 - 2) * x) for x in rand_list]
    return service


def output():
    #  Generate 100 random numbers between 0 and 1
    rand_x = random_x(100)
    #  Convert random numbers to inter-arrival times
    inter = convert_random(rand_x)
    #  Convert inter-arrival times to arrival times
    arrival_times = convert_inter_arrival(inter)
    #  Convert random numbers to service times
    service_times = convert_to_service(rand_x)

    #  Output (split into thirds to be able to screenshot it)
    a_first = arrival_times[:33]
    a_second = arrival_times[33:-33]
    a_third = arrival_times[-33:]
    print("The arrival times are: " + str(a_first)[1:-1])
    print("                       " + str(a_second)[1:-1])
    print("                       " + str(a_third)[1:-1])

    s_first = service_times[:33]
    s_second = service_times[33:-33]
    s_third = service_times[-33:]
    print("The service times are: " + str(s_first)[1:-1])
    print("                       " + str(s_second)[1:-1])
    print("                       " + str(s_third)[1:-1])


if __name__ == "__main__":
    output()
