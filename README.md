# Code for the paper "The Core of Approval-Based Committee Elections with Few Candidates"

This repository contains code and data for verifying the results presented in the paper.

Several files are Jupyter notebooks, which are also converted to PDF for easier reading. The folders also contain a file `utility_functions.py` which is imported by other scripts. In particular, it contains functions related to checking whether a given set is "wlog" (without loss of generality), i.e. canonical, with respect to a collection of sets that have become distinguishable. This logic is used to break symmetries and to reduce the number of cases to check.

Python dependencies:
```bash
pip install tqdm gurobipy gmpy2 jupyterlab
# or
pip install -r requirements.txt
```

## A: Committee size 7

The folder `A_committee_size_7` contains material for Section 4.1 of the paper. It contains:

* a Jupyter notebook `check-inequality.ipynb` that checks if inequality (3) in the paper holds for all T and all ballots. Running it finds that the inequality holds when k <= 7, but fails for k = 8 exactly when T contains two committee members and two non-committee members (as claimed in Lemma 4.4)
* a Python script `pav-almost-swap-stable.py` that runs an integer linear program to find an example of a profile where some committee for k = 7 is PAV local swap stable up to a given margin, but fails the core. The program is infeasible with the provided margin of 0.1/k^2. This proves the claims of Remark 4.2. Gurobi is required to run the script; if you don't have a Gurobi license, the unlicensed size-limited version works if using `num_alts = 10`.

## B: Committee size 8

The folder `B_committee_size_8` contains material for Section 4.2 of the paper. It contains:

* a Jupyter notebook `primals-counterexample-k8-structure.ipynb` that directly computes the optimal values of the linear programs from the proof of Lemma 4.4, using Gurobi (unlicensed version works). It stores the corresponding dual solutions in a file, after interpreting them as exact fractions. Running this notebook is not necessary to *verify* the results (since that can be done by checking the duals), but is useful to reproduce the results.
* the dual solutions stored in a Python pickle file `dual_values_k8.pkl`, as produced by the above notebook. The same data is stored in a human-readable JSON file `dual_values_k8.json`.
* a Jupyter notebook `duals-counterexample-k8-structure.ipynb` that verifies that the dual solutions in the file `dual_values_k8.pkl` are correct, using fractional arithmetic. 

## C: Recursive PAV rule for at most 15 candidates

The folder `C_recursive_PAV_rule` contains material for Section 5 of the paper. It contains:

* a subfolder `results/15` which contains files listing for different potential histories either an example profile establishing that it is a history, or a Farkas witness establishing that it is not a history. There is a file for each committee size k between 8 and 13 (though core existence for k = 8 can also be deduced using the method from Section 4.2). For each k, there is a `json` file and a `pkl` file, with the same content. The `json` file is intended for human inspection, while the `pkl` (python pickle) files are used by the verification scripts.
* a Python script `farkas-check-complete.py` that checks that there are Farkas witnesses present in the results files for all potential histories, establishing that the rule works. It does not check that the Farkas witnesses are correct.
* a Python script `farkas-verify-multiprocessing.py` that checks that every Farkas witness in the results files is correct, using fractional arithmetic. It uses multiprocessing to verify several witnesses in parallel.
* a file `counterexample-m16-k10.json` containing an example that the recursive PAV rule fails for m = 16 and k = 10.

The python scripts can be called using `python filename.py 15` to check the results for all k, or with `python filename.py 15 11` to check the results for a specific k (here 11). Run the scripts from inside the `C_recursive_PAV_rule` folder so that they can find the results files.

To perform a complete verification (which will take several hours), run the following commands:

```
cd C_recursive_PAV_rule
python farkas-check-complete.py 15
python farkas-verify-multiprocessing.py 15
```