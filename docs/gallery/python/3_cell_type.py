"""
.. _cell_types:

Exploring cell types
====================

Investigating cell atlases often involves exploring gene expression patterns across different cell types and organs.
This tutorial guides you through using the `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API
to explore gene expression data effectively. You will gain a general idea of how to query average expression, discover
patterns among similar genes, identify marker genes, and visualize the data.

Understanding the distribution of a cell type, its marker genes, and its relationships with other cell types is
essential in single-cell analysis. The `atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API
provides access to cell atlas data across 30 species, including humans, mice, fish, plants, and worms.

This tutorial focuses on querying cell type related data across the available species, using human examples where
applicable.
"""

# %%
# Contents
# ^^^^^^^^
#     - Retrieve cell type distributions across organs.
#     - Identify organs where a specific cell type occurs.
#     - Find marker genes for a cell type in a specific organ.
#     - Visualize cell type abundance and relationships.


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

# %%
# Explore available organisms
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Let's start by retrieving all available organisms from the API to see which species you can work with:

# Get available organisms
organisms = api.organisms(measurement_type="gene_expression")
print("Available organisms:")
print(organisms)

# %%
# Retrieve cell type distribution across organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Now, let's use the ``celltypexorgan`` method to retrieve the distribution of cell types in the human cell atlas.
# This will provide a clear overview of cell abundances and help identify which cell types are most prevalent across
# tissues.

# Query cell types across all human organs
human_celltypes = api.celltypexorgan(
    organism="h_sapiens",
    measurement_type="gene_expression"
)

# Display the cell type x organ table
print(human_celltypes)

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
# Visualizing the data
# ^^^^^^^^^^^^^^^^^^^^
# Analyzing large datasets can feel challenging when just looking at numbers in a **pandas.DataFrame**, so let's take a visual
# approach. Since macrophages are abundant in the lung (12,160 cells), a bar chart can help reveal their
# abundance across other tissues and highlight where else they may be highly represented, as shown in the code below:

# Filter for macrophages
macrophage_dist = human_celltypes.loc["macrophage"]

# Plot the distribution as a bar chart
macrophage_dist.plot(kind="bar")
plt.title("macrophage distribution across human organs")
plt.xlabel("organ")
plt.ylabel("number of sampled cells")
plt.tight_layout()
plt.show()

# %%
# The bar chart shows macrophage abundance across human organs, with the x-axis representing different organs and the
# y-axis showing the number of sampled cells. The lung stands out with 12,160 macrophages - much higher than the bladder,
# fat, and muscle, which also show notable counts. In contrast, organs like the eye, heart, and marrow have far fewer
# macrophages.
#
# However, absolute counts don't always reflect true biological trends. Try the following code to see the percentage
# of macrophages in each organ:

# Get total cells per organ (column sum)
total_cells_per_organ = human_celltypes.sum(axis=0)
# Get target cell type counts per organ
target_counts = human_celltypes.loc["macrophage"]
# Compute proportion (%) of that cell type in each organ
percentage = (target_counts / total_cells_per_organ) * 100

# Plot bar chart
percentage.sort_values(ascending=False).plot(kind='bar')
plt.ylabel('Abundance (%)')
plt.title(f'Proportion of macrophage cells in each organ')
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
plt.tight_layout()
plt.show()

# %%
# The bar chart displays the abundance of various cell types in the lung of h_sapiens, with the x-axis showing different
# cell types and the y-axis indicating the number of sampled cells. Macrophages are the most abundant at 12,160 cells,
# followed by AT2 cells with around 8,000 cells, while fibroblasts and T cells show moderate counts at about 2,000
# and 1,500 cells, respectively. On the lower end, cell types like NK cells, monocytes, and ciliated cells are much less
# common, with counts below 500 cells.

# %%
# Identify marker genes for lung macrophages
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Building on the lung's cell type abundance, you can now explore what makes lung macrophages unique by identifying their
# marker genes using the ``markers`` function. The code below retrieves the top 10 marker genes for lung macrophages:

human_lung_macrophage_markers = api.markers(
    organism="h_sapiens",
    organ="lung",
    cell_type="macrophage",
    number=10,
    measurement_type='gene_expression'
)

print(human_lung_macrophage_markers)

# %%
# Next, let's analyze their expression across cell types. To view the expression levels of these marker genes across
# cell types, use the ``average`` method. This helps identify characteristic genes for specific cell populations:

human_lung_macrophage_markers_exp = api.average(
        organism="h_sapiens",
        organ="lung",
        features=human_lung_macrophage_markers,
        measurement_type='gene_expression')

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
# For a clearer view of these expression patterns, visualize the data with a heatmap using the code below. This will
# highlight how macrophages dominate expression levels across the marker genes:

# Create the heatmap
plt.figure(figsize=(15, 4))
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

# Show the plot
plt.tight_layout()
plt.show()

# %%
# The heatmap displays the expression of 10 marker genes for macrophages across various cell types in the human lung,
# with the y-axis listing genes and the x-axis showing cell types. The color intensity reflects gene expression
# levels in counts per ten thousand (cptt), where darker shades indicate higher expression. Macrophages exhibit the
# strongest expression for most genes, especially *MARCO* at 12.84179 cptt, while other cell types, such as plasmacytoid
# cells and neutrophils, show much lower levels, often below 2 cptt.

# %%
# Conclusion
# ^^^^^^^^^^
# Now that you've learned how to explore cell types, their distribution, and marker genes in a single species' atlas —
# focusing on lung macrophages in human — you can apply this code to investigate any other species or cell type of
# interest from the approximated cell atlases. Experiment with different cell_type and organism parameters to uncover
# new insights!
#
# Thank you for using the *atlasapprox* API. For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# %%
# Page source
# -----------

# sphinx_gallery_thumbnail_path = '_static/cell_type.png'