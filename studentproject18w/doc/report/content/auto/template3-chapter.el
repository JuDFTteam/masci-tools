(TeX-add-style-hook
 "template3-chapter"
 (lambda ()
   (TeX-run-style-hooks
    "fig/tikz_plot")
   (LaTeX-add-labels
    "sec:a-chapter"
    "fig:tikz-curve"))
 :latex)

