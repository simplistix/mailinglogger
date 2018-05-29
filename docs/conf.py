# -*- coding: utf-8 -*-
import os, pkginfo, datetime, time

pkg_info = pkginfo.Develop(os.path.join(os.path.dirname(__file__),'..'))
build_date = datetime.datetime.utcfromtimestamp(int(os.environ.get('SOURCE_DATE_EPOCH', time.time())))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
    ]

intersphinx_mapping = dict(
    python=('http://docs.python.org', None)
    )

# General
source_suffix = '.txt'
master_doc = 'index'
project = pkg_info.name
copyright = '2001-2003 New Information Paradigms Ltd, 2003-2015 Simplistix Ltd, 2015-%s Chris Withers' % build_date.year
version = release = pkg_info.version
exclude_trees = ['_build']
exclude_patterns = ['description.txt']
pygments_style = 'sphinx'

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
htmlhelp_basename = project+'doc'

# Options for LaTeX output
latex_documents = [
  ('index',project+'.tex', project+u' Documentation',
   'Simplistix Ltd', 'manual'),
]

