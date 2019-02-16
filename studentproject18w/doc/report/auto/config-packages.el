(TeX-add-style-hook
 "config-packages"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("babel" "english") ("biblatex" "backend=biber" "autolang=hyphen" "style=alphabetic" "citestyle=alphabetic" "giveninits=false") ("hyperref" "pdftex") ("acronym" "footnote")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "babel"
    "biblatex"
    "a4wide"
    "graphicx"
    "subfig"
    "tikz"
    "pgfplots"
    "ifthen"
    "ifpdf"
    "hyperref"
    "color"
    "fancyhdr"
    "colortbl"
    "amsthm"
    "amssymb"
    "amsmath"
    "bbm"
    "array"
    "bm"
    "multirow"
    "acronym"
    "fontawesome"
    "dashrule")
   (TeX-add-symbols
    "headruleORIG"
    "cleardoublepage")
   (LaTeX-add-bibliographies
    "references")
   (LaTeX-add-lengths
    "figureheight"
    "figurewidth"))
 :latex)

