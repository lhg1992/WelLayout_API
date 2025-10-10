# WelLayout_API
This repository provides examples of using WelLayout API which provides the field layout optimization under various constraints with extreme efficiency.
Parametric trajectory design pattern let you say good-bye to manual trial-and-errors on the trajectory geometry to fulfill various constraints.


The basic technical methods/ideas are created during my PhD work in NTNU-SUBPRO research team, and published in a series of 3 journal papers:  

https://doi.org/10.1016/j.petrol.2021.109450

https://doi.org/10.1016/j.petrol.2021.109273

https://doi.org/10.1016/j.petrol.2021.109336

Many improvements have been made over the original papers' work.

Currently, this test server has very limited computing power, but it still just takes several seconds for a case (except the anticollision case which takes around 4 minutes).

=========================================================  
__Run the \*.ipynb under /Demos/... to see the examples of using WelLayout API.__

Here shows some examples of the optimization results, **click the figures for interactive 3D visualization**.
# 1-well (Single well trajectory design)
Avoiding dangerous area in the formation (at a specific depth): /Demos/get_1well/1well_ex1.ipynb   
[![get_1well_ex1 plotly figure](./Demos/get_1well/ex1/figure.png)](https://lhg1992.github.io/WelLayout_API/figure_1well_ex1.html)

Anticollision with user-defined safety distance functions: /Demos/get_1well/1well_ex2.ipynb   
[![get_1well_ex2 plotly figure](./Demos/get_1well/ex2/figure.png)](https://lhg1992.github.io/WelLayout_API/figure_1well_ex2.html)

# 1-site-N-wells (site-level layout design)
Without additional constraints, limited by DLS only: /Demos/get_1site/1site_ex1.ipynb   
[![get_1site_ex1 plotly figure](./Demos/get_1site/ex1/figure.png)](https://lhg1992.github.io/WelLayout_API/figure_1site_ex1.html)

Avoiding dangerous area + inclination control at a specific depth (for 2nd well ≤36°): /Demos/get_1site/1site_ex2.ipynb   
[![get_1site_ex2 plotly figure](./Demos/get_1site/ex2/figure.png)](https://lhg1992.github.io/WelLayout_API/figure_1site_ex2.html)

# K-site-N-wells (field-level layout design)
Without additional constraints, limited by DLS only: /Demos/get_ksites/ksites_ex1.ipynb   
(To be continued ...)