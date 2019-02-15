(TeX-add-style-hook
 "3-implementation"
 (lambda ()
   (TeX-run-style-hooks
    "img/logo/logos")
   (LaTeX-add-labels
    "chap:implementation"
    "fig:modules"))
 :latex)

