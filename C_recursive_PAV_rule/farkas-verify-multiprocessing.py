# check Farkas certificates are correct for unsuccessful histories

import itertools
import sys
import os
from functools import lru_cache
import pickle
from tqdm import tqdm
from multiprocessing import Pool

# from fractions import Fraction
from gmpy2 import mpq as Fraction

from utility_functions import powerset, utility, swaps

##############################################
########### Core functions ###################
##############################################

def check_farkas_for_history(A, ballots, k, history, farkas):

    alpha = farkas["alpha"]
    beta = farkas["beta"]
    gamma = farkas["gamma"]

    for ballot in ballots:
        ballot_set = set(ballot)

        lhs = alpha
        for history_time in range(len(history)):
            committee, T = history[history_time]

            # beta terms
            for x, y in swaps(A, committee):
                if beta[history_time, x, y] != 0:
                    if x in ballot_set and y not in ballot_set:
                        # utility went down, lost 1/utility
                        lhs += -beta[history_time, x, y] * Fraction(1, utility(ballot, committee))
                    if x not in ballot_set and y in ballot_set:
                        # utility went up, gained 1/(utility + 1)
                        lhs += beta[history_time, x, y] * Fraction(1, utility(ballot, committee) + 1)

            # gamma terms
            if utility(ballot, T) > utility(ballot, committee):
                lhs -= gamma[history_time]
                break # ballot becomes inactive
            
        assert lhs >= 0

    assert alpha - sum(Fraction(len(T), k) * gamma[history_time] for history_time, (_, T) in enumerate(history)) <= -1

def worker(args):
    A, ballots, k, history, farkas = args
    
    check_farkas_for_history(A, ballots, k, history, farkas)
    return True

def run(num_alts, k, info):
    A = range(num_alts)
    ballots = sorted(powerset(A))

    unsuccessful_histories = [history for history in info if not info[history]["successful"]]
    
    with Pool(8) as pool:
        args = [(A, ballots, k, history, info[history]["farkas"]) for history in unsuccessful_histories]
        results = list(tqdm(
            pool.imap_unordered(worker, args),
            total=len(args),
            desc=f"    m={num_alts}, k={k}"
        ))
    return all(results)

if __name__ == "__main__":

    if len(sys.argv) not in [2, 3]:
        print("Usage: python3 farkas-verify-multiprocessing.py num_alts [k]")
        sys.exit()

    num_alts = int(sys.argv[1])

    ks = range(9, num_alts-1) if len(sys.argv) == 2 else [int(sys.argv[2])]

    for k in ks:
        info = {tuple() : {"successful": True}}
        if os.path.exists(f"results/{num_alts}/info-{num_alts}-{k}.pkl"):
            info = pickle.load(open(f"results/{num_alts}/info-{num_alts}-{k}.pkl", "rb"))
            print(f"Loaded info for num_alts = {num_alts}, k = {k}")

        run(num_alts, k, info)
