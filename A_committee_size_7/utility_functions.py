import itertools
from functools import lru_cache

##############################################
########### Utility functions ################
##############################################

def powerset(iterable):
  xs = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(xs,n) for n in range(1,len(xs)))

def show(ballot):
    return "".join(str(a) for a in ballot)

def generate_wlog_partition(A, identifiable_sets):
    partition = []
    for inclusions in itertools.product([True, False], repeat=len(identifiable_sets)):
        partition_block = []
        for x in A:
            if all((x in identifiable_set) == inclusion for inclusion, identifiable_set in zip(inclusions, identifiable_sets)):
                partition_block.append(x)
        if partition_block:
            partition.append(partition_block)
    return partition

def is_wlog(xs, partition):
    # given a partition of a ground set such that in each block of the partition, the elements are indistinguishable,
    # check that xs is a wlog selection of elements from the ground set
    sorted_partition = [sorted(block) for block in partition]
    assert all(not set(block1) & set(block2) for block1, block2 in itertools.combinations(sorted_partition, 2)) # disjoint
    number_from_block = [len(set(block) & set(xs)) for block in sorted_partition]
    assert sum(number_from_block) == len(xs) # partition covers xs
    wlog_selections = [block[:num] for block, num in zip(sorted_partition, number_from_block)]
    wlog_selection = sorted(itertools.chain(*wlog_selections))
    return wlog_selection == sorted(xs)

@lru_cache(maxsize=10000)
def harmonic_number(r):
    return sum(1/i for i in range(1,r+1))

@lru_cache(maxsize=10000)
def utility(ballot, committee):
    # return len(set(ballot) & set(committee))
    utility = 0
    ballot_set = set(ballot)
    for x in committee:
        if x in ballot_set:
            utility += 1
    return utility

@lru_cache(maxsize=10000)
def symmetric_difference(com1, com2):
    return len(set(com1) ^ set(com2))

@lru_cache(maxsize=10000)
def committees_obtained_by_swap(A, committee):
    obtained_committees = []
    for x in committee:
        for y in A:
            if y not in committee:
                obtained_committee = set(committee) - {x} | {y}
                obtained_committees.append(tuple(sorted(obtained_committee)))
    return obtained_committees

@lru_cache(maxsize=10000)
def swaps(A, committee):
    all_swaps = []
    for x in committee:
        for y in A:
            if y not in committee:
                all_swaps.append((x,y))
    return all_swaps