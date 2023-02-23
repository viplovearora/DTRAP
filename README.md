# DTRAP
Python code for reproducing results in "[Optimal Resource Allocation to Minimize Errors When Detecting Human Trafficking][1]".

Follow [these][2] instructions to install Gurobi for Python. Data for GFW case study can be downloaded [here][3]. Synthetic data used for LJI case study can be shared upon reasonable request.

## Reproducing results
Follow the instructions in `GFW.ipynb` to reproduce the results in Table 5 and Figure 3.

Follow the instructions in `GFW-SC.ipynb` to reproduce the results in Table 5 and Figure 2.

Run file `solve_lji.py` for saving the data used for creating Figures 6-8.

Follow the instructions in `LJI-DIFFRES.ipynb` to reproduce the results in Figure 7(c).

Follow the instructions in `LJI-VT.ipynb` to reproduce the results in Figure 9.

[1]: https://www.tandfonline.com/doi/abs/10.1080/24725854.2023.2177364
[2]: https://www.gurobi.com/documentation/9.5/quickstart_mac/cs_python.html
[3]: https://www.pnas.org/doi/suppl/10.1073/pnas.2016238117/suppl_file/pnas.2016238117.sd04.csv
