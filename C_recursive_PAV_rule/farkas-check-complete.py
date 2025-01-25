# Check that all Farkas certificates have been computed

import itertools
import sys
import os
import pickle
from collections import deque

from utility_functions import powerset, generate_wlog_partition, is_wlog

def get_continuations(k, history):
    """
    Parameters:
        num_alts: number of alternatives
        k: committee size
        history: list of tuples (committee, T) where T is a core objection to committee
            note that committee must contain all prior T's
    Returns:
        list of tuples (committee, T) where T might be a core objection to committee
    """
    past_deviations = set().union(*[set(T) for _, T in history])
    remaining_candidates = set(A) - past_deviations
    places_to_fill = k - len(past_deviations)
    assert places_to_fill >= 0
    # generate based on a list of all past committees and deviations
    wlog_partition = generate_wlog_partition(A, [T for _, T in history] + [committee for committee, _ in history])
    possible_new_committees = [tuple(past_deviations | set(newcomers)) for newcomers in itertools.combinations(remaining_candidates, places_to_fill) if is_wlog(newcomers, wlog_partition)]

    new_histories = []
    for new_committee in possible_new_committees:
        wlog_partition = generate_wlog_partition(A, [T for _, T in history] + [committee for committee, _ in history] + [new_committee])
        possible_deviations = [T 
            for ell in range(1, k+1)
            for T in itertools.combinations(A, ell)
            if is_wlog(T, wlog_partition) and not set(T) <= set(new_committee)]
        
        for T in possible_deviations:
            new_histories.append(history + ((new_committee, T),))

    return new_histories

def run(k, info):
    queue = deque()

    queue.append(()) # empty history

    while queue:
        history = queue.pop()
        assert history in info
        if "farkas" in info[history]:
            continue
        for new_history in get_continuations(k, history):
            assert new_history in info
            if info[new_history]["successful"]:
                queue.append(new_history)
            else:
                assert "farkas" in info[new_history]

if len(sys.argv) not in [2, 3]:
    print("Usage: python3 farkas-check-complete.py num_alts [k]")
    sys.exit()

num_alts = int(sys.argv[1])
A = range(num_alts)
ballots = sorted(powerset(A))

ks = range(8, num_alts-1) if len(sys.argv) == 2 else [int(sys.argv[2])]

for k in ks:
    if os.path.exists(f"results/{num_alts}/info-{num_alts}-{k}.pkl"):
        info = pickle.load(open(f"results/{num_alts}/info-{num_alts}-{k}.pkl", "rb"))
        print(f"Loaded info for num_alts = {num_alts}, k = {k}")
        run(k, info)
    else:
        print(f"No info for num_alts = {num_alts}, k = {k}")