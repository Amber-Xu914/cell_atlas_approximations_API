"""
.. _markers:

Exploring marker genes
======================
Understanding which genes define a specific cell type is crucial for
interpreting cell identity and tracking developmental trajectories. The
`atlasapprox <https://atlasapprox.readthedocs.io/en/latest/index.html>`_  API
provides access to cell atlas data across 30 species, including humans, mice,
fish, plants, and worms.

This tutorial will guide you through the process of retrieving and visualizing
marker genes, identifying their expression patterns across tissues, and
comparing their specificity across cell types. By the end, you'll be able to:
"""
# %%
#   - `Find marker genes for a specific cell type in an organ (e.g., T cells in the human lung) <marker_>`__
#   - `Check marker genes' expression and fraction detected across cell types <expression-fraction_>`__
#   - `Querying the gene sequence <sequence_>`__

# %%
# Installing packages and initializing the API
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First, use pip to install the `atlasapprox` package along with the libraries needed for data visualization in this
# tutorial. Run the following command in your terminal:
#
#     ``pip install atlasapprox matplotlib seaborn pandas``
#
# Next, import them:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# %%
# Now, instantiate the ``API`` project:

api = atlasapprox.API()

# %%
# For complete setup instructions, check out :ref:`beginner-guide`.

# %%
# .. _marker:
# Finding marker genes for a cell type
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Marker genes help identify specific cell types by showing unique expression
# patterns. You can use the ``markers`` method to find the top 10 marker genes
# for T cells in the human lung. These genes will be highly expressed in T cells
# compared to other cell types in the lung.

human_lung_T_markers = api.markers(
    organism='h_sapiens',
    organ='lung',
    cell_type='T',
    number=10,
    measurement_type='gene_expression')

human_lung_T_markers

# %%
# .. _expression-fraction:
# Analyzing marker gene expression and fraction
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# To check how these marker genes are expressed across different cell types in
# the human lung, you can use the ``average`` method:

human_lung_T_markers_exp = api.average(
    organism='h_sapiens',
    organ='lung',
    features=human_lung_T_markers,
    measurement_type='gene_expression')

human_lung_T_markers_exp

# %%
# Understanding the output
# ------------------------
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - The values indicate the average gene expression, measured in counts per ten thousand (cptt).

# %%
# The resulting DataFrame displays expression levels in counts per ten thousand
# (cptt) across cell types. For instance, CD3D shows an expression of 8.6169 in
# T cells, indicating strong activity, compared to 0.058188 in neutrophils and
# 0.051887 in macrophages, where its expression is minimal. This contrast
# highlights CD3D's specificity as a T cell marker in the lung.

# %%
# Next, to determine the proportion of cells expressing these genes in each cell
# type, apply the ``fraction_detected`` method:

human_lung_fraction = api.fraction_detected(
    organism='h_sapiens',
    organ='lung',
    features=human_lung_T_markers,
    measurement_type='gene_expression')

human_lung_fraction

# %%
# The resulting DataFrame shows values from 0 to 1, representing the fraction of
# cells in each cell type expressing a gene. A value of 1 means 100% of cells
# express the gene, while 0 means none do. For instance, CD3D has a fraction of
# 0.868401 in T cells (86.84% express it) but only 0.011494 in neutrophils
# (1.15%). Similarly, CD3E is expressed in 82.79% of T cells (0.827850) and
# 5.75% of neutrophils (0.05747). This pattern confirms the specificity of these
# markers for T cells.

# %%
# Creating a dot plot using the data
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Reshape and prepare data
data = pd.melt(
    human_lung_T_markers_exp.reset_index(),
    id_vars='index',
    var_name='Cell types',
    value_name='Expression').rename(columns={'index': 'Genes'})
data['Fraction'] = pd.melt(
    human_lung_fraction.reset_index(),
    id_vars='index')['value'].clip(0, 1)

# Plot the data
plt.figure(figsize=(9, 4))
sns.scatterplot(
    data=data,
    x='Cell types',
    y='Genes',
    size='Fraction',
    hue='Expression',
    sizes=(30, 200))

plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1, 1))

# %%
# Understanding the output
# ------------------------
# The dot plot displays the expression of the 10 marker genes for T cell across
# various cell types in the human lung. The y-axis lists the genes, and the
# x-axis shows the cell types.
#
# Each dot in the dot plot contains two pieces of information:
#
# - The size of dot indicates the fraction of cells within that cell type that express the gene.
# - The color of the dot reflects the average gene expression level, measured in counts per ten thousand (cptt), with darker colors representing higher expression.
#
# For example, T cells show strong expression of CD3D, with an expression level
# of 8.62 cptt and a fraction of 0.87, meaning 87% of T cells express this gene.


# %%
# .. _sequence:
# Querying gene sequences
# ^^^^^^^^^^^^^^^^^^^^^^^
# To learn more about a rare marker gene, for example, compare your marker gene
# against already characterized genes — such as by running a BLAST search —
# you first need to retrieve its sequence. Try the following code to get the raw
# sequence of your marker genes:

sequence = api.sequences(organism='h_sapiens', features=human_lung_T_markers, measurement_type='gene_expression')

print(f"sequence type: {sequence['type']}")

for item, seq in zip(human_lung_T_markers, sequence['sequences']):
    print(f'{item}:')
    print(seq)

# %%
# Conclusion
# ^^^^^^^^^^
#
# Now that you have a general understanding of how to explore marker genes, how
# to get their expression and fraction, and how to retrieve their sequences,
# you're ready to explore further. In this tutorial, human lung was used as a
# simple example, but you can apply the same code to investigate any other
# species or cell type of interest from the approximated cell atlases. Try
# experimenting with different `gene` and ``organism`` parameters to uncover new
# insights!
#
# Thank you for using the *atlasapprox* API. For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.

# sphinx_gallery_thumbnail_path = '_static/markers.png'
