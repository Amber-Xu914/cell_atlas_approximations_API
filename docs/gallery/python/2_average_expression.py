"""
.. _average_expression:

Exploring average gene expression
=================================

This tutorial demonstrates how to explore average gene expression across cell types using the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API, with examples based on human data.

If you haven't already completed the installation and API setup, please refer to the :ref:`beginner-guide` before continuing.
"""

# %%
# Contents
# ^^^^^^^^
#   - `Querying average gene expression for a single organ <average-expression_>`__
#   - `Querying average gene expression for multiple organs <multi-organs_>`__
#   - `Exploring genes with similar expression patterns <similar-features_>`__
#   - `Finding cell-type-specific markers in an organ <marker-genes_>`__

# %%
# Installing packages and initializing the API
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First, use *pip* to install the ``atlasapprox`` package along with the libraries needed for data visualization in this
# tutorial. Run the following command in your terminal:
#
#     ``pip install atlasapprox matplotlib seaborn numpy``
#
# Then, import them and instantiate the ``API``:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

api = atlasapprox.API()

# %%
# .. _average-expression:
#
# Querying average gene expression for a single organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The ``average`` method retrieves the average gene expression of selected genes across cell types within a specific organ.
# Let's explore this with four genes (*PRDM1*, *PTPRC*, *ACTB*, *GAPDH*) in the human lung:

avg_gene_expr_lung = api.average(
    organism='h_sapiens',
    organ='lung',
    features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    measurement_type='gene_expression'
)

# Display the result
avg_gene_expr_lung

# %%
# Understanding the output
# ------------------------
# The ``average`` function returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - Values show average gene expression in counts per ten thousand (cptt).
#
# Notice that *ACTB* consistently shows higher gene expression across all cell types compared to the other genes, while *PRDM1* exhibits very low expression overall.
#
# Interpreting large sets of numerical data can be challenging, but visualizing it graphically highlights differences and improves understanding.

# %%
# Visualizing the data
# --------------------
# To visualize the average expression data of queried genes, a heatmap is a recommended approach.
# Python's visualization libraries `Seaborn <https://seaborn.pydata.org/>`_ and `Matplotlib <https://matplotlib.org/>`_ offer powerful tools for creating heatmaps. Run the following code to create one with custom labels.

fig, ax = plt.subplots(figsize=(7, 5))
heatmap = sns.heatmap(avg_gene_expr_lung, ax=ax)

# Customize labels
plt.title('Average gene expression across cell types in the human lung')
plt.xlabel('Cell type')
plt.ylabel('Gene')

# Display heatmap
fig.tight_layout()

# %%
# The color gradient in the heatmap makes it easier to compare expression levels across cell types than viewing raw data in a **pandas.DataFrame**.
# This visualization works by mapping expression values to colors, where brighter shades indicate higher expression and darker shades show lower levels. The heatmap reveals that *ACTB* consistently shows high expression across all cell types, while *PRDM1* exhibits very low expression.

# %%
# .. _multi-organs:
#
# Querying average gene expression for multiple organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# This example shows the average gene expression of four genes across three human organs: blood, lung, and liver. The `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API does not support querying multiple organs simultaneously, so a for loop is used instead.

# Define the target organs.
organ_list = ['blood', 'lung', 'liver']

# Iterate through the organ list
for organ in organ_list:
    avg_gene_expr = api.average(
        organism='h_sapiens',
        organ=organ,
        features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    heatmap = sns.heatmap(avg_gene_expr, ax=ax)

    # Customize labels
    plt.title(f'Average gene expression across cell types in the human {organ}')
    plt.xlabel("Cell type")
    plt.ylabel("Gene")

    fig.tight_layout()

# %%
# These three heatmaps show that *ACTB* consistently exhibits high expression across the selected organs. This reflects the typical high and stable expression of housekeeping genes, essential for basic cellular functions across various organs and cell types.
# Adapt this code to explore gene expression with the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API using your genes and organs of interest.

# %%
# .. _similar-features:
#
# Exploring genes with similar expression patterns
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Building on the analysis of average gene expression across organs, this section introduces the ``similar_features`` method to explore related gene expression, using *ACTB* as an example for a gene of interest.
# This method helps answer questions like "Which genes exhibit similar expression patterns to a chosen gene in this organ?" and retrieves the top 10 similar genes, as shown below.

similar_features = api.similar_features(
    organism='h_sapiens',
    organ='lung',
    feature='ACTB',
    method='correlation',
    number=10
)

#Display result
similar_features

# %%
# The ``similar_features`` method returns a **pandas.Series** with gene names as the index and their Pearson correlation distances to the gene of interest (e.g., *ACTB*) as values.
# This correlation, ranging from -1 (perfect negative relationship) to 1 (perfect positive relationship), measures the similarity of expression trends. For example, *LASP1* shows the highest similarity (0.483309), suggesting potential co-regulation.

# %%
# Additionally, other than correlation, methods like **euclidean** and **manhattan** are also available; refer to the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API documentation for details.

# %%
# Visualise the expression profile of these genes
# -----------------------------------------------
# To visualize the expression profiles of these genes, use a heatmap by extracting gene names from ``similar_features.index`` and including the gene of interest (e.g., *ACTB*) for comparison.
# Pass these as the ``features`` parameter to the ``average`` method, then plot the results:

# Combine ACTB and its similar features into a single list for better comparison
gene_list = ['ACTB'] + list(similar_features.index)

# Get average gene expression
avg_similar_features = api.average(
    organism='h_sapiens',
    organ='lung',
    features=gene_list
)

# Display the heatmap
fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(avg_similar_features,ax=ax)

# Customize labels
plt.title(f'Average gene expression across ACTB and its similar features')
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# .. _marker-genes:
#
# Finding cell-type-specific markers in an organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# When unsure which genes to explore, marker genes serve as a useful starting point. This section demonstrates retrieving marker genes for a specific organ and cell type, followed by querying their average expression.
#
# For example, use the ``markers`` method to get the top 10 marker genes for neutrophils in the human lung:

markers_in_lung_neutrophil = api.markers(
    organism='h_sapiens',
    organ='lung',
    cell_type='neutrophil',
    number=10
)

markers_in_lung_neutrophil

# %%
# Visualize expression profiles using a heatmap
# ---------------------------------------------

avg_gene_expr_markers = api.average(
    organism='h_sapiens',
    organ='lung',
    features=markers_in_lung_neutrophil
)

fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(avg_gene_expr_markers, ax=ax)

# Set labels
plt.title("Average expression of marker genes in lung neutrophil")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# The heatmap displays average expression levels of five neutrophil marker genes across cell types. Most areas appear dark, indicating low expression (0-20 cptt) in non-neutrophil cells, highlighting these genes' specificity.

# %%
# Applying log transformation
# ---------------------------
# The heatmap's dark regions suggest a wide expression range, with low values (0-20 cptt) obscured by higher values. A logarithmic transformation compresses this range, enhancing visibility of small differences. The following code applies this adjustment:

# Apply log transformation with a pseudo-count to avoid division by zero
avg_gene_expr_markers_log = np.log(avg_gene_expr_markers + 1)

fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(avg_gene_expr_markers_log, ax=ax)

# Set labels
plt.title("Log-transformed expression of markers in lung neutrophils")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# The log-transformed heatmap reveals cell type-specific expression patterns for neutrophil marker genes. *CXCR2*, *FCGR3B*, and *VNN2* exhibit notably high expression (bright colors) in neutrophils, confirming their specificity.
# *G0S2* also shows high levels in neutrophils, with some expression in monocytes, dendritic cells, alveolar fibroblasts, and vascular smooth muscle, possibly indicating a role in related immune or tissue functions.
# Dark regions across other cell types indicate minimal or no expression, emphasizing the markers' neutrophil dominance.

# %%
# Conclusion
# ^^^^^^^^^^
# This tutorial demonstrated how to retrieve average gene expression using atlasapprox API functions and visualize the data using Python libraries such as `Seaborn <https://seaborn.pydata.org/>`_ and `Matplotlib <https://matplotlib.org/>`_.
# For further details, consult the `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/average_expression.png'