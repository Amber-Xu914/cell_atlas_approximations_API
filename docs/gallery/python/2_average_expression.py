"""
.. _average_expression:

Exploring average gene expression
=================================

Investigating cell atlases often involves exploring gene expression patterns across different
cell types and organs. This tutorial guides you through using the
`atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API to explore
gene expression data effectively. You will gain a general idea of how to query average expression,
discover patterns of similar genes, identify marker genes, and visualize the data.
"""

# %%
# Contents
# ^^^^^^^^
#     - Querying average expression data for a single organ
#     - Querying expression data for multiple organs
#     - Identifying expression patterns of similar genes
#     - Querying expression data for marker genes

# %%
# Initialize the API
# ------------------
#
# To begin, import the *atlasapprox* Python package and create an API object:

import atlasapprox

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# Required packages
# -----------------
# To follow along with the data visualization in this tutorial, first install the following packages using `pip`,
# then import them by running the following command in your terminal or Jupyter notebook:

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %%
# Querying average gene expression data
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The ``average`` method allows you to retrieve average gene expression of selected genes across cell types within a
# specific organ of a species.
#
# Use the following code to get the average gene expression data for four example genes (*PRDM1*, *PTPRC*, *ACTB*,
# *GAPDH*) in the human lung across cell types:

avg_gene_expr_lung = api.average(
    organism='h_sapiens',
    organ='lung',
    features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    measurement_type='gene_expression'
)

# display the result
avg_gene_expr_lung

# %%
# Understand the output
# ---------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values indicate the average gene expression, measured in counts per ten thousand (cptt).
#
# A glance at the **pandas.DataFrame** reveals that *ACTB* consistently exhibits higher gene expression across all cell types
# compared to the other genes. In contrast, *PRDM1* shows very low expression overall.
#
# However, analysing large sets of numerical data can be challenging. Visualizing the data in a graphical format makes the
# differences more apparent.

# %%
# Visualizing the data
# ^^^^^^^^^^^^^^^^^^^^
# To visualize the average expression data of the queried genes, a heatmap is an effective starting point. The Python
# visualization libraries `Seaborn <https://seaborn.pydata.org/>`_ and `Matplotlib <https://matplotlib.org/>`_ offer
# powerful tools for creating such heatmaps.
#
# Here is a way to create one using Seaborn's `heatmap` method with custom labels:

# fill in heatmap contents
plt.figure(figsize=(12, 6))
sns.heatmap(
    avg_gene_expr_lung, 
    # add label to colour bar
    cbar_kws={'label': 'Expression Level'}
)

# Customize labels
plt.title('Average gene expression across cell types in the human lung')
plt.xlabel('Cell types')
plt.ylabel('Genes')

plt.tight_layout()
plt.show()

# %%
# From the color gradient, it is easier to compare the expression levels across different cell types. By looking at the
# heatmap, it is clear that *ACTB* exhibits consistently high gene expression across all cell types compared to the
# other genes. In contrast, *PRDM1* shows very low expression overall.

# %%
# Querying average gene expression for multiple organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# The following example demonstrates the average gene expression of four genes (same as above) across three human organs
# (*bladder*, *blood*, and *colon*).
#
# *Atlasapprox* API doesn't have any method to explore multiple organs at the same time, you can use the following code
# to use a for loop. Additionally, plotting the data using Seaborn's `heatmap` makes patterns easier to see than looking
# at raw numbers.

# Define the target organs.
organ_list = ['bladder', 'blood', 'colon']

# Loop through organ_list and display the results
for organ in organ_list:
    avg_gene_expr = api.average(
        organism='h_sapiens',
        organ=organ,
        features=['PRDM1', 'PTPRC', 'ACTB', 'GAPDH'],
    )

    # Create a new figure for each organ
    plt.figure(figsize=(12, 6))

    # Set up figure and display heatmap
    plt.title(f'Average gene expression across cell types in the human {organ}')
    sns.heatmap(
        avg_gene_expr,
        cbar_kws={'label': 'Expression Level'}
    )

    plt.tight_layout()
    plt.show()


# %%
# By comparing these three heatmaps, *ACTB* exhibits consistently high expression across all the selected organs,
# indicating a shared expression pattern among them.

# %%
# Exploring genes with similar expression patterns
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# When you have a gene of interest, you might want to find genes with similar expression patterns. This example
# shows how to use the ``similar_features`` method to retrieve the top 10 genes with expression patterns similar
# to *TP53* in the human lung:

similar_features = api.similar_features(
organism='h_sapiens',
organ='lung',
feature='TP53',
method='correlation',
number=10
)

similar_features

# %%
# Understand the output
# ---------------------
# ``similar_features`` returns a *pandas.Series* where the **index** contains gene names, and the corresponding **data**
# represent their distance to *TP53*.
#
# In this series, the **Pearson correlation** method is used to calculate the distance. This method produces a value
# between -1 and 1, where -1 signifies a perfect negative linear relationship and 1 signifies a perfect positive linear
# relationship. From the resulting *pandas.Series*, the top 10 genes most similar to *TP53* all exhibit
# positive linear relationships, with *TRA2A* showing the highest similarity. These genes may potentially be
# co-regulated with *TP53*.
#
# Additionally, `similar_features` supports the following methods for distance calculation:
#     - **cosine**: Computes cosine similarity/distance based on the fraction detected.
#     - **euclidean**: Measures Euclidean distance based on average measurements (e.g., expression levels).
#     - **manhattan**: Calculates the taxicab/Manhattan/L1 distance of average measurements.
#     - **log-euclidean**: Applies a logarithmic transformation to the average measurement (with a pseudo count of 0.001)
#                          before calculating the Euclidean distance, highlighting sparsely measured features.

# %%
# Get average gene expression for similar features
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# You can then use the ``average`` method to retrieve the average gene expression of these similar genes. Use
# **similar_features.index** to extract the gene names returned by ``similar_features``, and pass them as the ``feature``
# parameter to the ``average`` method.
#
# You can either use ``print`` function to directly display the resulting **pandas.DataFrame** or, as shown in the example
# below, use Seaborn's ``heatmap`` method to present a more intuitive graphical representation:

# Get average gene expression
avg_similar_features = api.average(
    organism='h_sapiens',
    organ='lung',
    features=similar_features.index
)

# Display the heatmap
sns.heatmap(
    avg_similar_features, 
    cbar_kws={'label': 'Expression Level'}
)
plt.tight_layout()
plt.show()

# %%
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
# Retrieve and plot
# -----------------
# Next, use the ``average`` method to retrieve the average gene expression of these genes, then use Seaborn's
# ``heatmap`` to visualize your data:

# Getting average gene expression for marker genes
avg_gene_expr_markers = api.average(
    organism='h_sapiens',
    organ='lung',
    features=markers_in_human_lung_neu
)

sns.heatmap(
    avg_gene_expr_markers,
    cbar_kws={'label': 'Expression Level'}
)
plt.tight_layout()
plt.show()

# %%
# Understand the output
# ---------------------
# This heatmap displays the gene expression levels of five neutrophil marker genes across all cell types.
#
# A significant portion of the heatmap appears black, indicating that these genes have very low expression levels
# (between 0-20 cptt) in most cell types. Due to the wide range of gene expression values, the current scale is too
# broad to effectively show differences within the 0 - 20 range. In this case, applying a logarithmic transformation helps
# compress the range, making smaller expression differences more visible while minimizing the impact of extremely high
# values. You can use the following code:

# Call the log method in NumPy to get all numbers logged
# Add 1 to each value to avoid division by zero
avg_gene_expr_markers_log = np.log(avg_gene_expr_markers + 1)

sns.heatmap(
    avg_gene_expr_markers_log,
    cbar_kws={'label': 'Expression Level'}
)
plt.tight_layout()
plt.show()

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

# %%
# Page source
# -----------

# sphinx_gallery_thumbnail_path = '_static/average_expression.png'