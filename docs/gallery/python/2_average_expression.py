"""
.. _average_expression:

Exploring average gene expression
=================================

Investigating cell atlases often involves exploring gene expression patterns across different cell types and organs.
This tutorial guides you through using the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API
to explore gene expression data effectively. You will gain a general idea of how to query average expression, discover
patterns of similar genes, identify marker genes, and visualize the data.
"""

# %%
# Contents
# ^^^^^^^^
#   - `Querying average gene expression for single organ <average-expression_>`__
#   - `Querying average gene expression for multiple organs <multi-organs_>`__
#   - `Exploring genes with similar expression patterns <similar-features_>`__
#   - `Finding marker genes for a specific cell type in organ <marker-genes_>`__

# %%
# Installing packages and initializing the API
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First, use pip to install the `atlasapprox` package along with the libraries needed for data visualization in this
# tutorial. Run the following command in your terminal:
#
#     ``pip install atlasapprox matplotlib seaborn numpy``
#
# Next, import them:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %%
# Now, instantiate the ``API`` project:

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# Exploring available organisms
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Let's start by retrieving all available organisms from the API to see which species you can work with:

# Get available organisms
organisms = api.organisms(measurement_type="gene_expression")

print("Available organisms:")
print(organisms)

# %%
# .. _average-expression:
# Querying average gene expression for single organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The ``average`` method can be used to retrieve the average gene expression of selected genes across cell types within
# a specific organ of a species.
#
# Try the code below to retrieve average gene expression data for four example genes (*PRDM1*, *PTPRC*, *ACTB*, and
# *GAPDH*) across cell types in the human lung:


avg_gene_expr_lung = api.average(
    organism='h_sapiens',
    organ='lung',
    features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    measurement_type='gene_expression'
)
# display the result
avg_gene_expr_lung

# %%
# Understanding the output
# ------------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values indicate the average gene expression, measured in counts per ten thousand (cptt).
#
# A glance at the **pandas.DataFrame** reveals that *ACTB* consistently exhibits higher gene expression across all cell
# types compared to the other genes. In contrast, *PRDM1* shows very low expression overall.
#
# However, interpreting large sets of numerical data can be difficult. Visualizing the data graphically  helps make the
# differences more obvious and easier to understand.

# %%
# Visualizing the data
# ^^^^^^^^^^^^^^^^^^^^
# To visualize the average expression data of the queried genes, a heatmap is a great place to start. Python's
# visualization libraries `Seaborn <https://seaborn.pydata.org/>`_ and `Matplotlib <https://matplotlib.org/>`_ provide
# powerful tools for creating heatmaps. Here is how to create one using Seaborn's ``heatmap`` method with custom labels:

# fill in heatmap contents
fig, ax = plt.subplots(figsize=(7, 5))
heatmap = sns.heatmap(avg_gene_expr_lung, ax=ax)

# Customize labels
plt.title('Average gene expression across cell types in the human lung')
plt.xlabel('Cell type')
plt.ylabel('Gene')

# Display heatmap
fig.tight_layout()

# %%
# The color gradient makes it much easier to compare expression levels across different cell types than by inspecting
# the raw **pandas.DataFrame**. From the heatmap, it's clear that *ACTB* consistently shows high expression across all
# cell types, while *PRDM1* has very low expression overall.

# %%
# .. _multi-organs:
# Querying average gene expression for multiple organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The following example demonstrates the average gene expression of four genes (same as above) across three human organs
# blood, lung and liver.
#
# The *atlasapprox* API doesn't currently support querying multiple organs at once, but you can use a for loop instead.
# Try the following code:

# Define the target organs.
organ_list = ['blood', 'lung', 'liver']

# Loop through organ list
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
# By comparing these three heatmaps, you can see that the housekeeping gene *ACTB* consistently shows high expression
# across all the selected organs. This makes sense, as housekeeping genes typically have high and stable expression
# across various organs or cell types due to their essential roles in basic cellular functions.

# %%
# .. _similar-features:
# Exploring genes with similar expression patterns
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Take *ACTB* as an example — you might be interested in finding genes with similar expression patterns. The example
# below demonstrates how to use the ``similar_features`` method to retrieve the top 10 genes with expression patterns
# similar to *ACTB* in the human lung:

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
# Understanding the output
# ------------------------
# ``similar_features`` returns a **pandas.Series** where the index contains gene names, and the corresponding data
# represent their distance to *ACTB*.
#
# In this series, the **Pearson correlation** method is used to calculate the distance. This method produces a value between
# -1 and 1, where -1 signifies a perfect negative linear relationship and 1 signifies a perfect positive linear
# relationship.
#
# From the resulting **pandas.Series**, the top 10 genes most similar to *ACTB* all exhibit
# positive linear relationships, with *LASP1* showing the highest similarity. These genes may potentially be
# co-regulated with *ACTB*.

# %%
# Additionally, `similar_features` supports the following methods for distance calculation:
#   - **cosine**: Computes cosine similarity/distance based on the fraction detected.
#   - **euclidean**: Measures Euclidean distance based on average measurements (e.g., expression levels).
#   - **manhattan**: Calculates the taxicab/Manhattan/L1 distance of average measurements.
#   - **log-euclidean**: Applies a logarithmic transformation to the average measurement (with a pseudo count of 0.001) before calculating the Euclidean distance, highlighting sparsely measured features.

# %%
# Getting average gene expression for similar features
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# You can then use the ``average`` method to retrieve the average gene expression of these similar genes. Use
# **similar_features.index** to extract the gene names returned by ``similar_features``, and pass them as the ``feature``
# parameter to the ``average`` method.
#
# You can either use ``print`` function to directly display the resulting **pandas.DataFrame** or, as shown in the
# example below, use Seaborn's ``heatmap`` method to present a more intuitive graphical representation:

# Combine ACTB and its similar features into a single list for better comparison.
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
# Finding marker genes for a specific cell type in organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# If you're unsure which genes to explore, marker genes can be a helpful starting point. The following example
# demonstrates how to retrieve marker genes for your organ and cell type of interest, followed by querying the average
# expression of these genes.
#
# First, use the ``markers`` method to obtain the top 5 marker genes for neutrophils in the human lung:

markers_in_human_lung_neu = api.markers(
    organism='h_sapiens',
    organ='lung',
    cell_type='neutrophil',
    number=5
)

markers_in_human_lung_neu

# %%
# Next, use the ``average`` method to retrieve the average gene expression of these genes, then use Seaborn's
# ``heatmap`` to visualize your data:

# Getting average gene expression marker genes
avg_gene_expr_markers = api.average(
    organism='h_sapiens',
    organ='lung',
    features=markers_in_human_lung_neu
)

fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(avg_gene_expr_markers, ax=ax)

# Set labels
plt.title("Average expression of marker genes in lung neutrophil")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# Understanding the output
# ------------------------
# This heatmap displays the gene expression levels of five neutrophil marker genes across all cell types.

# %%
# Applying log transformation
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# A significant portion of the heatmap appears black, indicating that these genes have very low expression levels
# (between 0-20 cptt) in most cell types. Due to the wide range of gene expression values, the current scale is too
# broad to effectively show differences within the 0 - 20 range. In this case, applying a logarithmic transformation
# helps compress the range, making smaller expression differences more visible while minimizing the impact of extremely
# high values. You can use the following code:

# Call the log method in NumPy to get all numbers logged
# Add 1 to each value to avoid division by zero
avg_gene_expr_markers_log = np.log(avg_gene_expr_markers + 1)

fig, ax = plt.subplots(figsize=(8, 6))
heatmap = sns.heatmap(avg_gene_expr_markers_log, ax=ax)

# Set labels
plt.title("Average expression of marker genes in lung macrophage")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# To avoid division by zero, this example uses avg_gene_expr_markers + 1 instead of avg_gene_expr_markers. This
# prevents any potential blank cell issues while keeping the log scale consistent.
#
# Comparing this heatmap with the original one, all blank cells represent areas with no gene expression, while the other
# genes show low levels of expression across most cell types. It can be observed that *G0S2*
# is also expressed in *monocytes*, *dendritic cells*, *alveolar fibroblasts*, and *vascular smooth muscle*.
# Additionally, *IL1R2* shows expression in two other cell types as well.

# %%
# Conclusion
# ^^^^^^^^^^
# This tutorial introduced several functions for retrieving average gene expression using different API functions and
# how to use different packages for visualizing the data.
#
# Thank you for using the *atlasapprox* API. For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/average_expression.png'