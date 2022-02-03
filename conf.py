import lsst_sphinx_bootstrap_theme

# -- Sphinx extensions -------------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "documenteer.sphinxext.jira",
    "documenteer.sphinxext.lsstdocushare"
]

# -- General configuration ------------------------------------------------

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The root toctree document.
root_doc = "index"

# General information about the project.
project = "PanDA User Guide"
copyright = (
    "Copyright 2022 Association of Universities for Research in "
    "Astronomy, Inc. (AURA)"
)
author = "Vera C. Rubin Observatory"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
version = "Current"
release = version

# Format for |today|
today_fmt = "%Y-%m-%d"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    "**/*.in.rst",  # rst files meant to be used for include directives
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# The reST default role cross-links Python (used for this markup: `text`)
default_role = "py:obj"

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pipelines": ("https://pipelines.lsst.io/", None),
}

# -- Options for linkcheck builder ----------------------------------------

# The linkcheck build often failed when trying to check the actual LSP
# URLs, so we need to ignore those URLs here.
linkcheck_ignore = [
    r"^https://lsst-lsp-stable\.ncsa\.illinois\.edu",
    r"^https://lsst-lsp-int\.ncsa\.illinois\.edu",
    r"^https://lsst-nts-k8s\.ncsa\.illinois\.edu",
    r"^https://base-lsp\.lsst\.codes",
    r"^https://summit-lsp\.lsst\.codes",
    r"^https://tucson-test-stand\.lsst\.codes",
    r"^https://data-dev\.lsst\.codes",
    r"^https://data-int\.lsst\.codes",
    r"^http(s)*://ls.st",
]
linkcheck_retries = 2

# -- Options for HTML output ----------------------------------------------

# Enables <link ref="canonical" href=<...>> canonical URL metadata
html_baseurl = "https://panda.lsst.io"

templates_path = [
    lsst_sphinx_bootstrap_theme.get_html_templates_path(),
]

html_theme = "lsst_sphinx_bootstrap_theme"
html_theme_path = [lsst_sphinx_bootstrap_theme.get_html_theme_path()]

html_context = {}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {"logotext": project}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = project

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "PanDA User Documentation"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%Y-%m-%d"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False
