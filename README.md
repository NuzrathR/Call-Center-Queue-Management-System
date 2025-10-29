# Call-Center-Queue-Management-System
A customer-support call center is a service facility where customers contact the company to get help, ask questions, or report problems. The call center operates with a fixed number of agents who are responsible for answering incoming calls.
The main purpose of the system is to ensure that customers receive support as quickly and efficiently as possible. When a customer calls, if an agent is free, the call is answered immediately. If all agents are busy, the customer is placed in a queue and waits until someone becomes available.

## Installation
Install Python 3.14 on your computer

Install required extra libraries

Open the file call_center_sim.py

At the top of the file, change
        o	SIM_TIME → total simulation time (in minutes)
        o	SERVICE_TIME → average time to handle one call
        o	WAIT_THRESHOLD → max time a customer will wait before hanging up
        o	Change number of agents or arrival rates in the scenario section
        
To make the results the same each run, set:
     RANDOM_SEED = 42
     
The program will display:
        •	Number of agents
        •	Average waiting time
        •	Calls handled
        •	Calls abandoned
        •	Agent utilization (%)
        •	Average queue length
                                            
