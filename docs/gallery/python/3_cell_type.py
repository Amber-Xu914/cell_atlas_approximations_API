"""
.. _cell_types:

Exploring cell types
====================

Understanding the distribution of a cell type, its marker genes, and its relationships with other cell types is
essential in single-cell analysis. The `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API
provides access to cell atlas data across 30 species, including humans, mice, fish, plants, and worms.

This tutorial focuses on querying cell type related data across the available species, using human examples where
applicable.
"""

# %%
# Contents
# ^^^^^^^^
#   - `Retrieve cell type distributions across organs. <retrieve-distributions_>`__
#   - `Identify organs where a specific cell type occurs. <identify-organs_>`__
#   - `Find marker genes for a cell type in a specific organ. <markers_>`__
#   - `Visualize cell type abundance and relationships. <visualization_>`__

# %%
# Initialize the API
# ------------------
# To begin, import the *atlasapprox* Python package and create an API object:

import atlasapprox

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# Required packages
# -----------------
# To follow along with the data visualization in this tutorial, first install the following packages using `pip`:
#
# ``pip install matplotlib seaborn pandas``
#
# Then import them by running the following command in your terminal or Jupyter notebook:

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# %%
# Explore available organisms
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Let's start by retrieving all available organisms from the API to see which species you can work with:

# Get available organisms
organisms = api.organisms(measurement_type="gene_expression")

print("Available organisms:")
print(organisms)

# %%
# .. _retrieve-distributions:
# Retrieve cell type distribution across organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Now, let's use the ``celltypexorgan`` method to retrieve the distribution of cell types in the human cell atlas. This
# will provide a clear overview of cell abundances and help identify which cell types are most prevalent across tissues.

# Query cell types across all human organs
human_celltypes = api.celltypexorgan(
    organism="h_sapiens",
    measurement_type="gene_expression"
)

# Display the cell type x organ table
human_celltypes

# %%
# Understand the output
# ---------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a unique cell type.
# - Each column represents an organ.
# - The values are counts of sampled cells for that cell type in the organ. A value of 0 means the cell type was not detected.
#
# For example, in lung tissue, there are 1,307 T cells and 12,160 macrophages, while hepatocytes have a count of 0,
# indicating they were not detected.

# %%
# .. _identify-organs:
# Visualizing the data
# ^^^^^^^^^^^^^^^^^^^^
# Analyzing large datasets can feel challenging when just looking at numbers in a **pandas.DataFrame**, so let's take a
# visual approach. Since absolute counts don't always reflect true biological trends, try the following code to see the
# percentage of macrophages in each organ:

# Get total cells per organ (column sum)
total_cells_per_organ = human_celltypes.sum(axis=0)

# Get target cell type counts per organ
target_counts = human_celltypes.loc["macrophage"]

# Compute proportion (%) of that cell type in each organ
percentage = (target_counts / total_cells_per_organ) * 100

# Plot bar chart
percentage.sort_values(ascending=False).plot(kind='bar')
plt.xlabel('Organ')
plt.ylabel('Abundance (%)')
plt.title('Proportion of macrophage cells in each organ')

# Display bar chart
plt.tight_layout()
plt.show()

# %%
# It is also possible to compare two cell types in a single bar chart.
#
# T cells and macrophages are both immune cells, but their distribution varies significantly between organs. Organs such
# as the gut, lymph nodes, and skin typically have a higher proportion of T cells, whereas the lung and liver are more enriched with macrophages.

# Get total cells per organ (column sum)
total_cells_per_organ = human_celltypes.sum(axis=0)

# Get target cell type counts per organ
target_counts_1 = human_celltypes.loc["macrophage"]
target_counts_2 = human_celltypes.loc["T"]

# Compute proportions (%)
percentage_1 = (target_counts_1 / total_cells_per_organ) * 100
percentage_2 = (target_counts_2 / total_cells_per_organ) * 100

# Combine into a DataFrame
percentage_df = pd.DataFrame({
    'macrophage': percentage_1,
    'T': percentage_2
})

# Sort by macrophage proportion (or any order you prefer)
percentage_df = percentage_df.sort_values(by='macrophage', ascending=False)

# Plot side-by-side bars
percentage_df.plot(kind='bar')
plt.xlabel('Organ')
plt.ylabel('Abundance (%)')
plt.title('Proportion of macrophage and T cells in each organ')

# Display bar chart
plt.tight_layout()
plt.show()

# %%
# This bar chart shows that macrophages are highly abundant in the lung, making up nearly 35% of its sampled cells.

# %%
# Focus on a specific organ: lung
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Now, let's explore which other cell types are abundant in this organ using a bar chart, as shown in the code below:

# Get all cell types in the lung
lung_abundance = human_celltypes["lung"]
lung_abundance_nonzero = lung_abundance[lung_abundance > 0]

# Plot the abundance as a vertical bar chart
lung_abundance_nonzero.plot(kind="bar")
plt.title(f"Cell type distribution in human lung")
plt.xlabel("cell type")
plt.ylabel("number of sampled cells")

# Display bar chart
plt.tight_layout()
plt.show()

# %%
# The bar chart displays the abundance of various cell types in the human lung , with the x-axis showing different
# cell types and the y-axis indicating the number of sampled cells.
#
# Looking at the bar chart, macrophages are the most abundant, with 12,160 cells, followed by AT2 cells at around 8,000.
# In contrast, cell types such as NK cells, monocytes, and ciliated cells are much less common, each with fewer than 500
# cells.

# %%
# .. _markers:
# Identify marker genes for lung macrophages
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Building on the cell type abundance in the lung, you can now explore what makes lung macrophages unique by
# identifying their marker genes using the ``markers`` function. The code below retrieves the top 10 marker genes
# specific to lung macrophages:

human_lung_macrophage_markers = api.markers(
    organism="h_sapiens",
    organ="lung",
    cell_type="macrophage",
    number=10,
    measurement_type='gene_expression'
)

human_lung_macrophage_markers

# %%
# Next, let's analyze their expression across cell types. To view the expression levels of these marker genes across
# cell types, use the ``average`` method. This helps identify characteristic genes for specific cell populations:

# Next, let’s examine how these marker genes are expressed across different cell types. You can use the ``average``
# method to view their expression levels, which helps identify genes that are characteristic of specific cell
# populations:


human_lung_macrophage_markers_exp = api.average(
    organism="h_sapiens",
    organ="lung",
    features=human_lung_macrophage_markers,
    measurement_type='gene_expression'
)

human_lung_macrophage_markers_exp

# %%
# Understand the output
# ---------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values show the average gene expression.
#
# The table reveals expression in counts per ten thousand (cpt). Macrophages show the highest levels across all
# marker genes — or example, *PPARG* is expressed at 2.712 cpt, far above plasmacytoid cells (0.000823) and neutrophils
# (0.129112).

# %%
# .. _visualization:
# For a clearer view of these expression patterns, you can try to visualize the data with a heatmap using the code below.
# This will make the expression levels across the macrophage marker genes more obvious:

# To better visualize these expression patterns, you can use a heatmap to display the data. The code below will show you
# the expression levels of the macrophage marker genes across different cell types.


# Create the heatmap
heatmap = sns.heatmap(
    human_lung_macrophage_markers_exp,
    cbar_kws={"label": "Gene Expression Level"}
)

# Set labels
plt.title("Average expression of marker genes in human macrophage")
plt.xlabel("Organs")
plt.ylabel("Genes")
cbar = heatmap.collections[0].colorbar
cbar.set_label("Gene Expression Level (cptt)")

# Display heatmap
plt.tight_layout()
plt.show()

# %%
# The heatmap shows the expression of 10 marker genes for macrophages across various cell types in the human lung,
# with the y-axis listing genes and the x-axis showing cell types. The color intensity reflects gene expression
# levels in counts per ten thousand (cptt), where bright shades indicate higher expression.
#
# Macrophages exhibit the strong expression for some genes, for example *MARCO* at 12.84179 cptt, while other cell types,
# such as plasmacytoid cells and neutrophils, show much lower levels.

# %%
# Conclusion
# ^^^^^^^^^^
# Now that you have a general understanding of how to explore cell types, their distribution, and marker genes  within a
# single species' atlas, you're ready to explore further. In this tutorial, human lung was used as a simple example,
# but you can apply the same code to investigate any other species or cell type of interest from the approximated cell
# atlases. Try experimenting with different ``cell_type`` and ``organism`` parameters to uncover new insights!
#
# Thank you for using the *atlasapprox* API. For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# %%
# Page source
# -----------

# sphinx_gallery_thumbnail_path = '_static/cell_type.png'