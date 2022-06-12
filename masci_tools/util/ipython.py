"""
Import this module to activate useful ipython extensions
"""
from __future__ import annotations

from lxml import etree
from pygments import highlight
from pygments.lexers import XmlLexer  #pylint: disable=no-name-in-module
from pygments.formatters import HtmlFormatter  #pylint: disable=no-name-in-module

from masci_tools.util.typing import XMLLike
from typing import Any
import difflib
from IPython.display import HTML

def display_xml(data: XMLLike) -> str:
    """
    Display the given lxml XML tree as formatted HTML

    :param data: data to show

    :returns: HTML string for presentation in Jupyter notebooks
    """

    xmlstring = etree.tostring(data, encoding='unicode', pretty_print=True)
    return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True,nobackground=False, style='monokai'))

def compare_xml_diff(old: XMLLike, new: XMLLike):

    old_lines = etree.tostring(old, encoding='unicode', pretty_print=True).split('\n')
    new_lines = etree.tostring(new, encoding='unicode', pretty_print=True).split('\n')

    lines = list(difflib.unified_diff(old_lines, new_lines))

    for index, line in enumerate(lines):
        if line.startswith('@@'):
            first_block = index
            break

    lines = lines[first_block:]
    lines.reverse()

    diff_blocks = []
    current_block = None

    css = """\
    <style type="text/css">
        .diff .control {
            background-color: #eaf2f5;
            color: #999999;
        }

        .insert {
            background-color: hsla(102, 100%, 74%, 0.5);
            color: #000000;
        }
        .insert .detail {
            background-color: hsla(102, 100%, 50%, 0.5);
            color: #000000;
        }
        .delete {
            background-color: hsla(0, 100%, 74%, 0.5); //semi-transparent red
            color: #000000;
        }
        .delete .detail {
            background-color:  hsla(0, 100%, 50%, 0.5);
            color: #000000;
        }
    </style>
    """

    def highlight_xml(xmlstring):
        return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True, nowrap=True)).rstrip('\n')

    def _line_diff(a, b):

        a, b = highlight_xml(a), highlight_xml(b)
        aline = []
        bline = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
            if tag == "equal":
                aline.append(a[i1:i2])
                bline.append(b[j1:j2])
                continue
            aline.append(f'<span class="detail">{a[i1:i2]}</span>')
            bline.append(f'<span class="detail">{b[j1:j2]}</span>')
        return "".join(aline), "".join(bline)

    while lines:
        line = lines.pop()
        if line.startswith('@@') or not lines:
            line = line.strip('\n@- ').replace(',',' (')
            print(line)
            original, _, changed = line.partition('+')
            line = f'Original: line {original} lines)\n' \
                f' Changed line {changed} lines)'

            if current_block is None:
                current_block = [f'<span class="control"> {line}</span>']
            else:
                current_block.append('<span></span>')
                diff_blocks.append('\n'.join(current_block))
                current_block = [f'<span class="control"> {line}</span>']
        elif line.startswith('-'):
            if lines:
                _next = []
                while lines and len(_next) < 2:
                    _next.append(lines.pop())
                if _next[0].startswith("+") and (
                        len(_next) == 1 or _next[1][0] not in ("+", "-")):
                    aline, bline = _line_diff(line[1:], _next.pop(0)[1:])
                    current_block.append(f'<span class="delete"> {aline}</span>')
                    current_block.append(f'<span class="insert"> {bline}</span>')
                    if _next:
                        lines.append(_next.pop())
                    continue
                lines.extend(reversed(_next))
            current_block.append(f'<span class="delete"> {highlight_xml(line[1:])}</span>')
        elif line.startswith('+'):
            current_block.append(f'<span class="insert"> {highlight_xml(line[1:])}</span>')
        elif current_block is not None:
            current_block.append(highlight_xml(line))

    diff_blocks = '\n'.join(diff_blocks)
    
    return HTML(f"""
    {css}
    <pre style="line-height: 125%;"><span></span>
    {diff_blocks}
    </pre>
    """ )


def register_formatters(ipython: Any) -> None:

    html_formatter = ipython.display_formatter.formatters['text/html']
    html_formatter.for_type(etree._Element, display_xml)
    html_formatter.for_type(etree._ElementTree, display_xml)
