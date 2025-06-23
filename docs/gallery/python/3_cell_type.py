"""
.. _cell_types:

Exploring cell types
====================

Understanding how cell types are distributed across organs is a key aspect of analyzing single-cell data.
This tutorial covers how to retrieve cell type distributions, visualize abundance across tissues, and identify dominant cell populations in specific organs using the `atlasapprox API <https://atlasapprox.readthedocs.io/en/latest/index.html>`_.

Examples are based on human data for clarity, but the same approach applies to other species in the atlasapprox API.
Before getting started, make sure you've completed the setup in the :ref:`beginner-guide`.

"""

# %%
# Contents
# ^^^^^^^^
#   - `Retrieving cell type distribution across organs <retrieve-distributions_>`__
#   - `Zooming into a specific organ <specific-organ_>`__
#   - `Identifying marker genes for a cell type <markers_>`__


# %%
# Importing required libraries
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Import the necessary libraries and instantiate the ``API`` object:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns

api = atlasapprox.API()

# %%
# .. _retrieve-distributions:
#
# Retrieving cell type distribution across organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# To obtain the distribution of cell types in the human cell atlas, use the ``celltypexorgan`` method.
# This provides a comprehensive overview of cell abundances and helps identify the most prevalent cell types across different tissues.

# Query cell types across human organs
human_celltypes = api.celltypexorgan(
    organism="h_sapiens",
    measurement_type="gene_expression"
)

# Display the cell type distribution matrix
human_celltypes

# %%
# Understanding the output
# ------------------------
# The ``celltypexorgan`` method returns a **pandas.DataFrame** where:
#
# - Each row represents a unique cell type.
# - Each column represents an organ.
# - The values represent counts of sampled cells for that cell type in each organ (a value of 0 means the cell type was not detected)
#
# For example, in the lung, there are 1,307 T cells and 12,160 macrophages, while hepatocytes have a count of 0,
# indicating they were not detected.
#
# At first glance, some cell type such as macrophages, T cell, and B cells are found across multiple tissue, while others
# like schwann and thymocytes are much rarer. However, looking at these numbers alone can make it hard to spot trends
# across many organs and cell types, especially in a large dataset like this one.

# %%
# Visualizing the data
# --------------------
# Visualization reveals patterns hidden by raw numbers. Organs vary in sampled cell totals, so raw counts can be misleading—those with more samples may appear to have higher cell type numbers, even if the type is rare.
# Proportions normalize the data to reflect true distribution within organs. Using macrophages as an example, their proportion is visualized to assess their role as key immune cells across tissues.

# Compute proportion of macrophages in each organ
proportions = (human_celltypes.loc["macrophage"] / human_celltypes.sum(axis=0)) * 100

# Plot bar chart
proportions.sort_values(ascending=False).plot(kind='bar')
plt.xlabel('Organ')
plt.ylabel('Percentage(%)')
plt.title('Proportion of macrophage across organs')

# Display bar chart
plt.tight_layout()

# %%
# The bar chart indicates macrophages are highly abundant in the lung, comprising
# nearly 35% of sampled cells. This suggests the lung is a primary site for
# macrophage activity, while other organs like liver and bladder show moderate
# proportions, and many, such as pancreas and colon, exhibit minimal presence.
# The variation highlights the diverse roles macrophages play across the body's tissues.

# %%
# Comparing cell type proportions
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# To explore further, one can focus on the proportions of specific cell types
# across organs and compare multiple types to reveal differences in their distributions.
# For example, consider macrophages alongside T cells—both are immune cells, but
# their roles and abundances vary across the body.

# Select cell types to compare
cell_types = ["T", "macrophage"]

# Calculate percentage of each cell type in each organ
proportions = (human_celltypes.loc[cell_types] / human_celltypes.sum(axis=0)) * 100

# Plot bars for each cell type
proportions.T.plot(kind="bar")
plt.xlabel("Organ")
plt.ylabel("Percentage(%)")
plt.title("Proportion of macrophage and T cells across organs")

plt.tight_layout()

# %%
# The plot shows how macrophages and T cells are spread across different organs.
# For example, the lung and liver have more macrophages, while the gut, lymph
# nodes, and skin have more T cells.
# The atlasapprox API enables further investigation, and to explore other
# cell types or species of interest, the code can be adapted by changing the parameters.

# %%
# .. _specific-organ:
#
# Zooming into a specific organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# After examining cell type distributions across multiple organs, the next step is to focus on a specific organ
# to better understand its tissue-specific cell composition.
#
# This example selects the lung and identifies the most abundant cell types beyond macrophages.
# Only cell types with non-zero proportions are included in the plot to simplify the visualization.

# Plot lung cell type proportions
lung_pct = (human_celltypes["lung"] / human_celltypes["lung"].sum() * 100).sort_values(ascending=False)
lung_pct[lung_pct > 0].plot(kind="bar")

plt.title("Cell type proportions in lung")
plt.xlabel("Cell type")
plt.ylabel("Percentage(%)")
plt.tight_layout()

# %%
# The bar chart shows that macrophages represent the largest proportion (~34%)
# of lung cells, followed by AT2 cells (~25%) and monocytes (~7%). In contrast,
# rare cell types such as NK cells, lymphatic endothelial cells, and ionocytes
# account for less than 2%.

# %%
# .. _markers:
#
# Identifying marker genes for a cell type within an organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# To further characterize a specific cell type within a tissue, marker genes can
# be retrieved using the ``markers`` method.
#
# The following example identifies the top 10 marker genes for macrophages in the lung:

human_lung_macrophage_markers = api.markers(
    organism="h_sapiens",
    organ="lung",
    cell_type="macrophage",
    number=10,
    measurement_type='gene_expression'
)

human_lung_macrophage_markers

# %%
# To analyze how these marker genes are expressed across different lung cell
# types, use the ``average`` method:

human_lung_macrophage_markers_exp = api.average(
    organism="h_sapiens",
    organ="lung",
    features=human_lung_macrophage_markers,
    measurement_type='gene_expression'
)

human_lung_macrophage_markers_exp

# %%
# Understanding the output
# ------------------------
# The ``average`` function returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values represent average expression in counts per ten thousand (cptt).
#
# Marker gene expression is generally higher in macrophages than in other lung
# cell types. For example, *MARCO* shows an average expression of 12.84 cptt in
# macrophages, compared to just 0.12 in neutrophils and 0.18 in B cells. This
# confirms *MARCO* as a highly specific marker for macrophages in the lung.

# %%
# Visualizing marker gene expression with a heatmap
# -------------------------------------------------
# While the table provides a detailed quantitative view, visualizing the
# expression data as a heatmap can help highlight global patterns and make
# comparisons across cell types more intuitive.

# Create the heatmap
fig, ax = plt.subplots(figsize=(7, 5))
heatmap = sns.heatmap(human_lung_macrophage_markers_exp, ax=ax)

# Set labels
plt.title("Average expression of marker genes in lung macrophage")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# The heatmap displays the average expression of selected marker genes across
# lung cell types, with color intensity representing expression levels in counts
# per ten thousand (cptt). Darker colors indicate lower expression, while
# lighter shades (e.g., pink and white) reflect higher expression. Genes such as
# *MARCO* and *MSR1* exhibit strong, macrophage-specific expression, confirming
# their relevance as marker genes for this cell type.

# %%
# Conclusion
# ^^^^^^^^^^
# This tutorial introduced how to explore cell types, their distribution, and
# marker genes using a single species' atlas. The human lung served as an
# example, but the same approach can be applied to any other species or cell
# type available in the approximated cell atlases. Try adjusting the cell_type
# and organism parameters to explore new biological insights.
#
# For more detailed information, please refer to the `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/cell_type.png'