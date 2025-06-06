"""
.. _data:

Exploring available data
========================
This tutorial introduces basic functions for retrieving all available data from
the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API,
including organisms, organs, and cell types.

By the end, you'll be able to:
"""
# %%
#   - `Retrieve available measurement types <measurement-types_>`__
#   - `Retrieve available organisms <organisms_>`__
#   - `Retrieve available organs <organs_>`__
#   - `Retrieve available cell types <cell-types_>`__

# %%
# Installing packages and initializing the API
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First, use pip to install the `atlasapprox` package.
# Run the following command in your terminal:
#
#     ``pip install atlasapprox``
#
# Next, import it:

import atlasapprox

# %%
# Now, instantiate the API project:

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# .. _measurement-types:
# Get available measurement types
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# *Atlasapprox* API currently supports two measurement types. Try
# ``measurement_types`` method to get available measurement types:

available_measurement_types = api.measurement_types()

print(available_measurement_types)

# %%
# By default, all other functions use **gene expression** as the measurement type.
# For chromatin accessibility, the only available organism is Homo sapiens
# (*h_sapiens*) currently.

# %%
# .. _organisms:
# Get available organisms
# ^^^^^^^^^^^^^^^^^^^^^^^
# The *atlasapprox* API currently provides access to approximated single-cell
# data across 30 species using **gene expression** as the measurement type. Use the
# ``organisms`` method below to retrieve a list of all available data under a
# specified measurement type:

available_organisms = api.organisms(measurement_type='gene_expression')

print(available_organisms)

# %%
# .. _organs:
# Get available organs
# ^^^^^^^^^^^^^^^^^^^^
# Try the ``organs`` method to get the list of available organs for your chosen
# organism:

available_human_organs = api.organs(organism="h_sapiens", measurement_type='gene_expression')

print(available_human_organs)
# %%
# .. _cell-types:
# Get available cell types
# ^^^^^^^^^^^^^^^^^^^^^^^^
# Try the ``celltypes`` method to retrieve the list of available cell types for
# your chosen organism and organ:

available_human_lung_celltypes = api.celltypes(organism="h_sapiens", organ="lung", measurement_type="gene_expression")

print(available_human_lung_celltypes)

# %%
# If you already have a cell type of interest, you can try the
# ``celltype_location`` method which retrieve a list of organs where a cell type
# is detected:

T_location = api.celltype_location(
    organism='h_sapiens',
    cell_type='T',
    measurement_type='gene_expression'
)

print(T_location)

# %%
# Also, you can use the ``celltypexorgan`` method to get a **Pandas.DataFrame**,
# which display all the distribution of cell types in the human cell atlas. This
# will provide a clear overview of cell abundances and help identify which cell
# types are most prevalent across tissues.

human_celltypes = api.celltypexorgan(organism="h_sapiens")

human_celltypes

# %%
# Understanding the output
# ------------------------
# This method returns a **pandas.DataFrame** where:
#
#   - Each row represents a unique cell type.
#   - Each column represents an organ.
#   - Each cell indicates whether the cell type was detected in the sampled organ. A value of True means the cell type was present.

# %%
# Get available features
# ^^^^^^^^^^^^^^^^^^^^^^
# You can try the ``features`` method to query all available features for your
# specified organism:

available_human_features = api.features(organism='h_sapiens', measurement_type='gene_expression')

print(available_human_features)

# %%
# Conclusion
# ^^^^^^^^^^
#
# Now that you have a general understanding of how to fetch available organisms,
# organs, cell types and features, you're ready to explore further. It's always
# a good idea to revisit this tutorial whenever you're starting from scratch or
# want to check whether your cell type or feature of interest is available in
# the *atlasapprox* API.
#
# Thank you for using the *atlasapprox* API. For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/data.png'
