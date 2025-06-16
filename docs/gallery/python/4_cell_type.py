"""
.. _cell_types:

Exploring cell types
====================

Understanding cell type distribution across organs and identifying their marker genes are key skills in analyzing a
species' cell atlas. This tutorial shows how to access this data more easily using the
`atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_ API, which provides cell atlas data for 30
species, including humans, mice, fish, plants, and worms, with practical human examples to guide you.
"""

# %%
# Contents
# ^^^^^^^^
#   - `Retrieving cell type distribution across organs <retrieve-distributions_>`__
#   - `Zooming into a specific organ <specific-organ_>`__
#   - `Identifying marker genes for a cell type within an organ <markers_>`__

# %%
# Installing packages and initializing the API
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First, use pip to install the `atlasapprox` package along with the libraries needed for data visualization in this
# tutorial. Run the following command in your terminal:
#
#     ``pip install atlasapprox matplotlib seaborn``
#
# Next, import them:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Now, instantiate the ``API`` project:

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# Exploring available organisms
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Let's start by retrieving all available organisms from the API to see which
# species you can work with:

# Get available organisms
organisms = api.organisms(measurement_type="gene_expression")

print("Available organisms:")
print(organisms)

# %%
# .. _retrieve-distributions:
# Retrieving cell type distribution across organs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Now, let's use the ``celltypexorgan`` method to retrieve the distribution of
# cell types in the human cell atlas. This will provide a clear overview of cell
# abundances and help identify which cell types are most prevalent across tissues.

# Query cell types across all human organs
human_celltypes = api.celltypexorgan(
    organism="h_sapiens",
    measurement_type="gene_expression"
)

# Display the cell type x organ table
human_celltypes

# %%
# Understanding the output
# ------------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a unique cell type.
# - Each column represents an organ.
# - The values are counts of sampled cells for that cell type in the organ. A value of 0 means the cell type was not
# detected.
#
# For example, in the lung, there are 1,307 T cells and 12,160 macrophages, while hepatocytes have a count of 0,
# indicating they were not detected.
# At a glance, some cell type such as macrophages, T cell and B cells are found across multiple tissue, while others
# like schwann and thymocytes are more rare. However, looking at these numbers alone can make it hard to spot trends
# across many organs and cell types, especially in a large dataset like this one.

# %%
# Visualizing the data
# ^^^^^^^^^^^^^^^^^^^^
# To better understand the data, a visual approach helps reveal patterns that numbers alone can obscure.
# For example, raw cell counts can be unrepresentative because organs vary in the total number of sampled cells—an organ
# with more sampled cells may appear to have more of a specific cell type, even if that cell type is relatively rare—so
# using proportions normalizes the data to better reflect the actual distribution of a cell type within each organ.
#
# Let's start by visualizing the proportion of macrophages across organs, since they are often abundant and play a key
# role in immune responses across tissues:

# Compute proportion of macrophages in each organ
proportions = (human_celltypes.loc["macrophage"] / human_celltypes.sum(axis=0)) * 100

# Plot bar chart
proportions.sort_values(ascending=False).plot(kind='bar')
plt.xlabel('Organ')
plt.ylabel('Percentage(%)')
plt.title('Proportion of macrophage cells across organs')

# Display bar chart
plt.tight_layout()

# %%
# This bar chart shows that macrophages are highly abundant in the lung, making up nearly 35% of its sampled cells.
#
# To dive deeper, we can zoom into the proportions of specific cell types across organs and even compare multiple cell
# types to uncover differences in their distributions. Let's examine macrophages alongside T cells—both are immune
# cells, but their roles and abundances vary across the body.

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
# The plot shows that macrophages and T cells are distributed differently across organs. For example, the lung and liver
# have a higher percentage of macrophages, while the gut, lymph nodes, and skin have a higher percentage of T cells.
#
# This shows how you can use the API to explore cell type distributions, and the code can be applied to any other
# available cell type or species, like B cells in mice, by simply changing the parameters.

# %%
# .. _specific-organ:
# Zooming into a specific organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# After exploring cell type distributions across all organs, you might want to dive deeper into a specific organ to see
# its unique cell type composition.
#
# In this example, we focus on the lung to identify the most abundant cell types besides macrophages. To improve
# clarity, we only include cell types with non-zero proportions to simplify the visualization.

# Plot lung cell type proportions
lung_pct = (human_celltypes["lung"] / human_celltypes["lung"].sum() * 100).sort_values(ascending=False)
lung_pct[lung_pct > 0].plot(kind="bar")

plt.title("Cell type proportions in lung")
plt.xlabel("Cell type")
plt.ylabel("Percentage(%)")
plt.tight_layout()

# %%
# As seen in the chart, macrophages make up the largest proportion (~34%), followed by AT2 cells (~25%) and monocytes (~7%).
# In contrast, rare cell types such as NK cells, lymphatic, and ionocyte each represent less than 2% of lung cells.

# %%
# .. _markers:
# Identifying marker genes for a cell type within an organ
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Now that you've seen the cell type composition in the lung, you can use the API to find marker genes for a specific
# cell type. Here, we'll look at lung macrophages as an example, starting with the ``markers`` function to retrieve the
# top 10 marker genes:

human_lung_macrophage_markers = api.markers(
    organism="h_sapiens",
    organ="lung",
    cell_type="macrophage",
    number=10,
    measurement_type='gene_expression'
)

human_lung_macrophage_markers

# %%
# To see how these marker genes are expressed across different cell types in the lung, you can use the ``average``
# method:

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
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values show the average gene expression in counts per ten thousand (cptt).
#
# The table shows how much higher the expression of these marker genes is in macrophages compared to other cell types in
# the lung. For example, the gene *PPARG* has an expression of 2.712 cpt in macrophages, while it's only 0.000823 in
# plasmacytoid cells and 0.129112 in neutrophils.

# %%
# You can visualize these expression patterns with a heatmap to make the differences clearer, as shown in the code
# below:

# Create the heatmap
fig, ax = plt.subplots(figsize=(7, 5))
heatmap = sns.heatmap(human_lung_macrophage_markers_exp, ax=ax)

# Set labels
plt.title("Average expression of marker genes in lung macrophage")
plt.xlabel("Cell type")
plt.ylabel("Gene")

fig.tight_layout()

# %%
# The heatmap displays the expression of the 10 marker genes for macrophages across various cell types in the human lung.
# The y-axis lists the genes, and the x-axis shows the cell types.
# The color intensity reflects gene expression levels in counts per ten thousand (cpt), with brighter shades indicating
# higher expression.
#
# For example, macrophages show strong expression for genes like *MARCO* at 12.84179 cpt, while other cell types, such
# as plasmacytoid cells and neutrophils, have much lower levels.

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

# sphinx_gallery_thumbnail_path = '_static/cell_type.png'