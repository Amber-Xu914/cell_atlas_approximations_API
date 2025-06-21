"""
.. _beginner-guide:

Beginner guide
==============

The `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API provides access to approximated
single-cell data across 30 species, including both animals and plants. You can explore data from species such as *Homo sapiens* (humans), *Mus musculus* (mice), *Arabidopsis thaliana* (thale cress), and *Zea mays* (corn).
This guide walks through installing the package, setting up the API, and running basic queries using simple examples.
"""

# %%
# Setting up a virtual environment (optional)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# It's recommended to use a virtual environment to manage dependencies. Run the following command:
#
#     ``python -m venv venv``
#
# Activate the environment using the appropriate command for your operating system:
#
# For macOS/Linux users:
#     ``source venv/bin/activate``
#
# For Windows users:
#     ``venv\Scripts\activate``

# %%
# Installation
# ^^^^^^^^^^^^
# Install the ``atlasapprox`` Python package using *pip*:
#
# ``pip install atlasapprox``

# %%
# Then, import the package and instantiate the ``API`` object:

import atlasapprox

api = atlasapprox.API()

# %%
# Querying available data
# ^^^^^^^^^^^^^^^^^^^^^^^
# Explore available organisms, organs, and cell types using the following methods:

# %%

# List available organisms
available_organisms = api.organisms()
print(available_organisms)

# %%

# List available organs for humans
available_organs = api.organs(organism="h_sapiens")
print(available_organs)

# %%

# List available cell types in the human lung
available_celltypes = api.celltypes(organism="h_sapiens", organ="lung")
print(available_celltypes)


# %%
# Exploring average gene expression
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The ``average`` method allows you to retrieve gene expression levels for selected genes in a specific organ of an
# organism.
#
# The following example shows how to examine the average expression of five genes
# (*COL13A1*, *COL14A1*, *TGFBI*, *PDGFRA*, *GZMA*) in the human lung:

avg_gene_expr_lung = api.average(
    organism = "h_sapiens",
    organ = "lung",
    features = ["COL13A1", "COL14A1", "TGFBI", "PDGFRA", "GZMA"],
    measurement_type = "gene_expression"
)

# Display the result
avg_gene_expr_lung

# %%
# Understanding the output
# ------------------------
# The ``average`` method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values indicate the average gene expression, measured in counts per ten thousand (cptt).

# %%
# Conclusion
# ^^^^^^^^^^
# This guide covers setup and data querying with a basic example. For more detailed
# information, refer to the official `documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/beginner_guide.png'