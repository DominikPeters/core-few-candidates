# Verify Remark 4.2 that for k <= 7, every epsilon-local-swap
# PAV committee is in the core.

from gurobipy import Env, Model, GRB, quicksum
import itertools
from functools import cache
from utility_functions import powerset, show, generate_wlog_partition, is_wlog, harmonic_number, utility, committees_obtained_by_swap

##############################################
########### Core functions ###################
##############################################

num_alts = 14
k = 7
A = tuple(range(num_alts))
ballots = sorted(powerset(A))
committee = tuple(A[:k])

m = Model()

freq = {ballot: m.addVar(ub=1) for ballot in ballots}
m.addConstr(quicksum(freq[ballot] for ballot in ballots) == 1)

MARGIN = 0.1 / (k * k)

for bad_committee in committees_obtained_by_swap(A, committee):
    m.addConstr(
        quicksum(
            freq[ballot] * \
            (harmonic_number(utility(ballot, committee))) 
            for ballot in ballots)
        >= quicksum(
            freq[ballot] * \
            (harmonic_number(utility(ballot, bad_committee)))
            for ballot in ballots) - MARGIN
    )

# Enforce there is successful deviation
wlog_partition = generate_wlog_partition(A, [committee])
possible_deviations = [T 
    for ell in range(1, k+1)
    for T in itertools.combinations(A, ell)
    if is_wlog(T, wlog_partition) and not set(T) <= set(committee)]
binary_variables = []
for new_T in possible_deviations:
    ballots_preferring_T = set(ballot for ballot in ballots if utility(ballot, new_T) > utility(ballot, committee))
    binary_variable = m.addVar(vtype=GRB.BINARY)
    binary_variables.append(binary_variable)
    m.addConstr(quicksum(freq[ballot] for ballot in ballots_preferring_T) >= (len(new_T) / k) * binary_variable)
m.addConstr(quicksum(binary_variables) >= 1)

m.optimize()

if m.SolCount > 0:
    for ballot in ballots:
        if freq[ballot].x > 0.001:
            print(f"{round(freq[ballot].x,3)} {show(ballot)}")