# Import required libraries
import simpy         # Used to simulate processes (customers, agents, queues)
import random        # Used to create random arrival and service times
import statistics    # Used to calculate averages like mean waiting time
import pandas as pd  # Used to display the final results in a neat table

# --- Basic Settings ---
RANDOM_SEED = 42             # Makes random numbers repeatable (so results are the same each run)
random.seed(RANDOM_SEED)     # Apply the random seed
SIM_TIME = 120               # Total simulation time = 120 minutes (2 hours)
SERVICE_TIME = 5             # Average service time per call = 5 minutes
WAIT_THRESHOLD = 5           # If a customer waits more than 5 minutes, they hang up (abandon)

# --- Customer Process ---
def customer(env, name, agents, service_rate, wait_times):
    """This function defines what happens to each customer — wait, get help, or hang up"""
    global handled, abandoned           # Use global counters to count total handled and abandoned calls
    arrival = env.now                   # Record the time the customer arrived

    # Try to get an available agent
    with agents.request() as req:       # Customer requests an agent
        result = yield req | env.timeout(WAIT_THRESHOLD)  # Wait for agent OR time out after WAIT_THRESHOLD

        # If the request is not successful within WAIT_THRESHOLD, customer hangs up
        if req not in result:
            abandoned += 1              # Increase abandoned call counter
            return                      # End the process for this customer

        # If customer got an agent before timeout
        wait = env.now - arrival        # Calculate how long they waited
        wait_times.append(wait)         # Save the wait time for later analysis

        # Generate a random service time (based on exponential distribution)
        service = random.expovariate(1.0 / service_rate)
        yield env.timeout(service)      # Simulate the time taken to complete the call
        handled += 1                    # Increase handled call counter

# --- Customer Arrivals ---
def arrivals(env, agents, rate, service_rate, wait_times):
    """This function continuously sends customers into the system at random intervals"""
    i = 0                               # Start with 0 customers
    while True:                         # Keep generating customers until the simulation ends
        i += 1                          # Increase customer number
        yield env.timeout(random.expovariate(rate))  # Wait for the next customer's arrival
        # Start a new customer process (they will wait, get served, or hang up)
        env.process(customer(env, f"Customer {i}", agents, service_rate, wait_times))

# --- Run One Scenario ---
def run_scenario(agents_count, arrival_rate, service_time):
    """Run the simulation for one set of parameters (agents, arrival rate, etc.)"""
    global handled, abandoned           # Use global counters
    handled = abandoned = 0             # Reset counters for this scenario
    wait_times = []                     # Create an empty list to record all waiting times

    # Create the simulation environment
    env = simpy.Environment()

    # Create the group of agents (like employees answering calls)
    agents = simpy.Resource(env, capacity=agents_count)

    # Start the customer arrival process
    env.process(arrivals(env, agents, arrival_rate, service_time, wait_times))

    # Run the simulation for SIM_TIME minutes
    env.run(until=SIM_TIME)

    # --- After simulation, calculate summary statistics ---
    avg_wait = statistics.mean(wait_times) if wait_times else 0   # Calculate average wait time
    utilization = (handled * service_time) / (SIM_TIME * agents_count)  # How busy the agents were
    avg_queue = arrival_rate * avg_wait                           # Estimate average queue length (Little’s Law)

    # Store results in a dictionary (used to build the final table)
    return {
        "Agents": agents_count,              # Number of available agents
        "Arrival Rate": arrival_rate,        # How often customers arrive
        "Avg Wait (min)": round(avg_wait, 2),# Average waiting time
        "Queue Length": round(avg_queue, 2), # Average number of waiting customers
        "Utilization (%)": round(utilization * 100, 1), # Percentage of time agents were busy
        "Calls Handled": handled,            # Total calls completed
        "Abandoned Calls": abandoned,        # Total calls where customers hung up
    }

# --- Define and Run 3 Scenarios ---
scenarios = [
    {"Agents": 3, "Arrival Rate": 0.3, "Label": "Scenario 1 – Base"},         # Normal case: 3 agents
    {"Agents": 5, "Arrival Rate": 0.3, "Label": "Scenario 2 – More Agents"},  # Add more agents
    {"Agents": 3, "Arrival Rate": 0.5, "Label": "Scenario 3 – Busy"},         # Busier system (more calls)
]

results = [] # List to store results for all scenarios

# Run each scenario one by one
for s in scenarios:
    print(f"\nRunning {s['Label']}...")  # Show which scenario is running
    result = run_scenario(s["Agents"], s["Arrival Rate"], SERVICE_TIME)  # Run it
    results.append(result)               # Add the results to the list

# --- Show Summary Table ---
df = pd.DataFrame(results)               # Convert all results to a table using pandas
print("\n=== Simulation Results Summary ===")
print(df.to_string(index=False))         # Display the table neatly (no index numbers)
