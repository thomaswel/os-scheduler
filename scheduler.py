#!/usr/bin/env python3
# Name: Thomas Welborn
# Class: Operating Systems
# Prof: Dr. Smith
# Assignment: Operating System Scheduler Simulation
# Due: Feb 26, 2021
'''
This program implements a simple uni-processor scheduling simulator using
Preemptive-Priority and secondary Round Robin where the Quantum number is
input by the user.
The simulator will step through a sequence of time units, performing
the actions of a simple operating system scheduler.

The main input file will contain process information separated by
spaces in the form:

3
0 5 8
2 8 72
5 2 7

Where the first line indicates how many processes there are.
The remaining lines contain each process information.
The first number is the arrival time, the second is priority,
and the third is the CPU_Time.

This scheduler is a PREEMPTIVE PRIORITY SCHEDULER with ROUND-ROBIN
as a second scheduling criteria. The best solution allows for
the user to vary the time quantum but a default of 2 should be used.
'''

import sys
import copy

# class to represent each process
class Process:
    def __init__ (self, label, arrival, priority, cpuTime):
        self.label = label
        self.arrival = arrival
        self.priority = priority
        self.cpuTime = cpuTime
        self.cpuTimeLeft = cpuTime
        self.endTime = -1
        self.currBurst = 0
        

    def getLabel(self):
        return self.label
    def getArrival(self):
        return self.arrival
    def getPriority(self):
        return self.priority
    def getCpuTime(self):
        return self.cpuTime
    def getCpuTimeLeft(self):
        return self.cpuTimeLeft
    def getEndTime(self):
        return self.getEndTime
    def getCurrBurst(self):
        return self.currBurst

    def decrement(self):
        self.cpuTimeLeft -= 1

    def __str__(self):
        fin_str = '[' + str(self.label)
        fin_str += ' ' + str(self.arrival)
        fin_str += ' ' + str(self.priority)
        fin_str += ' ' + str(self.cpuTime) + ']'
        return fin_str


'''
@params none
@returns boolean
Function to check if conditions for the input file are met. If the conditions
are not met, then it will return False. Otherwise, True.
'''
#function to check that the input file is valid
def input_checks():
    inFile = open('input.txt', 'r')
    #check number of processes >=1 and <=100
    line = inFile.readline().strip("\n")
    num_of_processes = int(line)
    if (num_of_processes < 1) or (num_of_processes > 100):
        print("Invalid number of processes. Must be >=1 and <=100.")
        return False 
    
    #create 2-d list for holding processes information
    #each row is a new process
    #three columns per row, [arrival, priority, CPUtime]
    processes_2d = []
    for line in inFile:
        temp_line = line.strip("\n")
        temp_list = temp_line.split(" ")
        #convert from strings to ints
        for i in range (0, len(temp_list)):
            temp_list[i] = int(temp_list[i])
        processes_2d.append(temp_list)

    #close file
    inFile.close()

    #check arrival times strictly increasing
    for i in range(0, (len(processes_2d)-1)):
        if (processes_2d[i][0] > processes_2d[i+1][0]):
            print("Invalid input. Process arrival times are not strictly increasing.")
            return False
        
    #check priority numbers are strictly 0-9
    for i in range(0, len(processes_2d)):
        if ((processes_2d[i][1] < 0) or (processes_2d[i][1] > 9)):
            print("Invalid input. Process priority levels are not between 0-9.")
            return False
        
    #check the number of processes received == num_of_processes (as stated in input file)
    if (num_of_processes != len(processes_2d)):
        print("Invalid input. Number of processes found does not equal number of processes")
        print("stated in the first line of the input text file.")
        return False

    #check all numbers are positive integers
    for i in range(0, len(processes_2d)):
        for j in range(0, 3):
            if (processes_2d[i][j] < 0):
                print("Invalid input. A number was found to be less than 0 in the input file.")
                return False
    
    #if all checks pass, return true
    return True


'''
function to check the cpuTimeLeft of a list of processes
@param process_list, list of Process objects
@return boolean, True if there are processes left, False if done
'''
def checkIfProcessesLeft(process_list):
    none_left = True
    for i in range(0, len(process_list)):
        if (process_list[i].cpuTimeLeft != 0):
            none_left = False
    return (not none_left)


'''
@param processes is a list of Process objects, int q is the quantum number 
@return a string representation of the gantt chart
'''
def start(processes, q):

    num_processes = len(processes)
    time = 0
    ready_q = []
    curr = None
    done_q = []
    gantt_str = ""

    #print out the initial processes to be scheduled
    print('----------------------------------------')
    print("The processes to be scheduled are:")
    for i in range(0, len(processes)):
        print(processes[i])
    print("The user input quantum number is " + str(q) + '.')
    print('----------------------------------------')
    print('Time = ' + str(time) + ':')

    #search for first arriving process
    while(time != processes[0].getArrival()):
        gantt_str += "x"
        time += 1
        print('Nothing happened at time ' + str(time))
        print('----------------------------------------')
        print('Time = ' + str(time) + ':')
        print(gantt_str)

    #start the main loop
    while (len(done_q) < num_processes):
            
        #check if anything arrives to ready q
        for i in range(0, len(processes)):
            if (processes[i].arrival == time):
                ready_q.append(processes[i])
                print('Process [' + str(processes[i].label) + '] arrived to ready queue at time ' + str(time) + '.')

        #check if the thing on current CPU is done and remove if done
        if ((curr != None) and (curr.cpuTimeLeft == 0)):
            curr.endTime = time
            print('Process [' + str(curr.label) + '] finished at time ' + str(time) + '.')
            done_q.append(curr)
            curr = None

        #print out the current vitals before continuing iteration
        #for i in range(0, len(done_q)):
            #print(done_q[i])
        #for i in range(0, len(ready_q)):
            #print("READY Q" + str(ready_q[i]))    
            

        
        # Case 1 - Ready Q empty and CPU empty
        if ((len(ready_q) == 0) and (curr == None)):
            if (len(done_q) == num_processes):
                print('All processes complete at time ' + str(time) + '.')
                print('----------------------------------------')
                continue
            else:  
                time += 1
                gantt_str += "x"
                print('Nothing running on CPU at time ' + str(time) + '.')
                print('----------------------------------------')
                print('Time = ' + str(time) + ':')
                print(gantt_str)
                continue
        
        # Case 2 - Ready Q has something but CPU empty
        elif ((len(ready_q) > 0) and (curr == None)):
            #check for lowest priority in ready q and dispatch
            curr_lowest = ready_q[0]
            curr_lowest_index = 0
            if (len(ready_q) > 1):
                for i in range(1, len(ready_q)):
                    if (ready_q[i].priority < curr_lowest.priority):
                        curr_lowest = ready_q[i]
                        curr_lowest_index = i
            
            curr = ready_q[curr_lowest_index]
            del ready_q[curr_lowest_index]
            print('Process [' + str(curr.label) + '] moved from ready queue to CPU at time ' + str(time) + '.')
            #do rest of things for iteration
            time += 1
            curr.decrement()
            curr.currBurst = 0
            curr.currBurst += 1
            gantt_str += str(curr.label)
            print('----------------------------------------')
            print('Time = ' + str(time) + ':')
            print(gantt_str)
            continue
                
        # Case 3 - Ready Q empty but CPU has something
        elif ((len(ready_q) == 0) and (curr != None)):
            time += 1
            curr.decrement()
            curr.currBurst += 1
            gantt_str += str(curr.label)
            print('----------------------------------------')
            print('Time = ' + str(time) + ':')
            print(gantt_str)
            continue
                
        # Case 4 - Ready Q something and CPU something
        elif ((len(ready_q) > 0) and (curr != None)):
            lowest_priority = curr
            lowest_priority_index = -1
            #check for strictly more important processes (lower priority integer means more important)
            for i in range (len(ready_q)-1, -1, -1):
                if (ready_q[i].priority < lowest_priority.priority):
                    lowest_priority = ready_q[i]
                    lowest_priority_index = i
            if (lowest_priority != curr):
                print('Current process [' + str(curr.label)+ '] has been pre-empted and moved from CPU to ready queue because there is a higher priority in the ready queue.')
                curr.currBurst = 0
                ready_q.append(curr)
                curr = lowest_priority
                print('Process [' + str(curr.label)+ '] has been dispatched from ready queue to the CPU.')
                del ready_q[lowest_priority_index]
                #do rest of things for iteration
                curr.decrement()
                curr.currBurst += 1
                time+=1
                gantt_str += str(curr.label)
                print('----------------------------------------')
                print('Time = ' + str(time) + ':')
                print(gantt_str)
                continue
                
                
            #now need to check for equal in priority only if the current didnt change
            tie_count = 0
            if (lowest_priority == curr):
                for i in range (len(ready_q)-1, -1, -1):
                    if (ready_q[i].priority == lowest_priority.priority):
                        tie_count += 1

            #if no tie, then complete iteration
            if (tie_count ==0):
                curr.decrement()
                curr.currBurst += 1
                time+=1
                gantt_str += str(curr.label)
                print('----------------------------------------')
                print('Time = ' + str(time) + ':')
                print(gantt_str)
                continue
                
            #if there was a tie, check the quantum in case it needs to pre-empt
            if (tie_count > 0):
                if (curr.currBurst < q):
                    curr.decrement()
                    curr.currBurst += 1
                    time+=1
                    gantt_str += str(curr.label)
                    print('----------------------------------------')
                    print('Time = ' + str(time) + ':')
                    print(gantt_str)
                    continue
                else:
                    tie_process = None
                    tie_process_index = -1
                    for i in range(0, len(ready_q)):
                        if (ready_q[i].priority == curr.priority):
                            tie_process = ready_q[i]
                            tie_process_index = i
                            break
                    #curr to ready q, ready q to curr
                    print('Current process [' + str(curr.label)+ '] has reached its quantum limit and there is a process of equal priority in the ready queue. Pre-empting to ready queue.')
                    curr.currBurst = 0
                    ready_q.append(curr)
                    curr = tie_process
                    print('Process [' + str(curr.label)+ '] has been dispatched from ready queue to the CPU.')
                    del ready_q[tie_process_index]
                    #complete iteration
                    curr.decrement()
                    curr.currBurst = 0
                    curr.currBurst += 1
                    time+=1
                    gantt_str += str(curr.label)
                    print('----------------------------------------')
                    print('Time = ' + str(time) + ':')
                    print(gantt_str)
                    continue
        else:  
            count += 1
            print("Error, did not satisfy one of the 4 cases.")
    if (gantt_str[-1] == 'x'):
        gantt_str = gantt_str[0:len(gantt_str)-1]
    for i in range(0, len(done_q)):
        print(str(done_q[i]) + "-- Done at: " + str(done_q[i].endTime))
    turn_around_avg = 0
    for i in range(0, len(done_q)):
        print(str(done_q[i]) + "-- Turnaround Time: " + str(done_q[i].endTime - done_q[i].arrival))
        turn_around_avg += (done_q[i].endTime - done_q[i].arrival)
    print("The average Turnaround Time is " + str(turn_around_avg / len(done_q)))
    
    return gantt_str


# main function, start here
def main():
    if (input_checks()):
        inFile = open('./input.txt', 'r')
        line = inFile.readline().strip("\n")
        num_of_processes = int(line)

        #create 2-d list for holding processes information
        #each row is a new process
        #three columns per row, [arrival, priority, CPUtime]
        processes_2d = []
        for i in range (0, num_of_processes):   
            line = inFile.readline().strip("\n")
            temp_list = line.split(" ")
            #convert from strings to ints
            for i in range (0, len(temp_list)):
                temp_list[i] = int(temp_list[i])
            processes_2d.append(temp_list)

        # close file
        inFile.close()
        #print(processes_2d)

    else:
        print('Terminating program due to invalid input file. Goodbye!')
        sys.exit()


    # create list of Process objects from the information gathered
    process_list = []
    # assign each Process a unique label:
    # 1-26 = A-Z 
    # 27-52 = a-z
    # 53-78 = AA-ZZ
    # 79-100 = aa-vv
    LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL', 'MM',
              'NN', 'OO', 'PP', 'QQ', 'RR', 'SS', 'TT', 'UU', 'VV', 'WW', 'XX', 'YY', 'ZZ',
              'aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm',
              'nn', 'oo', 'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv']
   
    for i in range (0, len(processes_2d)):
        temp_object = Process(label = LABELS[i], arrival=processes_2d[i][0], priority=processes_2d[i][1], cpuTime=processes_2d[i][2])
        process_list.append(temp_object)

    # accept user input for their desired quantum level
    user_input = 0
    valid_flag = False
    while(not valid_flag):
        try:
            user_input = int(input("Enter the quantum number: "))
            if ((user_input >= 1) and (user_input <= 100)):
                valid_flag = True
                continue
            print("Invalid user input. Not within 1-100 inclusive range. Please try again.")
            continue
        except:
            print('User input was not an integer type. Please try again.')
            continue


    # start the scheduler simulation
    gantt_chart = start(process_list, user_input)
    print("------------------------------------------")
    print("The final Gantt Chart is:")
    for i in range (0, len(gantt_chart)):
        print('---Time = ' + str(i) + '---')
        print(gantt_chart[i])
    print('---Time = ' + str(len(gantt_chart)) + '---')


if __name__ == '__main__':
    main()
    
