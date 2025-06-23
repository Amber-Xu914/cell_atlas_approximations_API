# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# Configuration file for the Sphinx documentation builder.
# Early import forfeits the credit warning for atlasapprox

import os

os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Cell Atlas Approximations API"
copyright = "2023, Fabio Zanini"
author = "Fabio Zanini"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_tabs.tabs",
    "sphinx.ext.napoleon",
    "sphinx_gallery.gen_gallery",
]
sphinx_tabs_disable_tab_closing = True
show_source = True

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for sphinx-gallery ----------------------------------------------

def file_name_sort_key(example):
    return os.path.basename(example)

sphinx_gallery_conf = {
    "filename_pattern": r".*\.py",
    "examples_dirs": ["../gallery/python"],
    "gallery_dirs": ["python/gallery"],
    'within_subsection_order': file_name_sort_key,
    "remove_config_comments": True, # hides config-style comments like thumbnail_path
    'download_all_examples': False, # hide zip downloading tab
    'show_memory': False,            # hide memory source
    'show_signature': False,
    'show_api_usage': False,
    'min_reported_time': float('inf'), # hide running time
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = ['css/custom.css']

extensions += ["sphinx_new_tab_link"]

# optional tweaks
new_tab_link_show_external_link_icon = False   # add an icon after each link
new_tab_link_enable_referrer        = True   # keep the HTTP referrer if you need it

