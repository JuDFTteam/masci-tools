(TeX-add-style-hook
 "4-manuals"
 (lambda ()
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (LaTeX-add-labels
    "cha:manuals"
    "sec:user-manual"
    "sec:system-requirements"
    "sec:input-data-formats"
    "sec:gui-usage"
    "sec:troubleshooting"
    "sec:developer-manual"
    "sec:extend-prepr"
    "sec:extend-visu-"))
 :latex)

