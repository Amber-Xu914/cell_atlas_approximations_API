"""
.. _beginner-guide:

Beginner guide
==============

The `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_
API provides access to approximated single-cell data across 28 species, including
both animals and plants. You can explore data from species such as *Homo sapiens*
(humans), *Mus musculus* (mice), *Arabidopsis thaliana* (thale cress), and *Zea mays* (corn).
Follow this guide to get started with installation, basic usage, and example queries.
"""

# %%
# .. note::
#
#     To ensure consistent dependencies, setting up a virtual environment is recommended
#     before installing the package. Here's one way to do it:
#
#     Create a virtual environment:    ``python -m venv myenv``
#
#     Activate your environment (use the appropriate command for your OS)
#
#     For macOS/Linux users:    ``source myenv/bin/activate``
#
#     For Windows users:    ``myenv\\Scripts\\activate``


# %%
# Installation
# ------------
#
# Use *pip* to install the *atlasapprox* Python package:
#     ``pip install atlasapprox``

#%%
# Initialize the API
# ------------------
# Import the *atlasapprox* Python package and create an API object:

import atlasapprox
api = atlasapprox.API()

# %%
# Getting average gene expression
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The ``average`` function allows you to retrieve the average gene expression data fo
# selected genes within an organism's specific organ.
#
# The following example shows how to examine the average expression of five genes 
# (*COL13A1*, *COL14A1*, *TGFBI*, *PDGFRA*, *GZMA*) in the human lung:

# Call API function with params
avg_gene_expr_lung = api.average(
    organism = "h_sapiens", 
    organ = "lung", 
    features = ["COL13A1", "COL14A1", "TGFBI", "PDGFRA", "GZMA"], 
    measurement_type = "gene_expression"
)

# Display the result
avg_gene_expr_lung

# %%
# Understand the output
# ---------------------
# This method returns a *Pandas DataFrame* where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values indicate the average gene expression, measured in counts per ten thousand (cptt).

# %%
# Conclusion
# ^^^^^^^^^^
# This tutorial provided a quick start guide to use the *atlasapprox* Python package.
# For more detailed information, refer to the official
# `documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.