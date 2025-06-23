"""
.. _explore_markers:

Exploring marker genes
======================
Marker genes are essential for defining cell identity and distinguishing one
cell type from another. This tutorial demonstrates how to retrieve marker genes
for a specific cell type, analyze their expression and detection across tissues,
and visualize their specificity using dot plots—all using the
`atlasapprox API <https://atlasapprox.readthedocs.io/en/latest/index.html>`_.

Examples are based on human data for clarity, but the same approach applies to
other species in the atlasapprox api. Before getting started, make sure you've
completed the setup in the :ref:`beginner-guide`.
"""

# %%
# Contents
# ^^^^^^^^
#
#   - `Find marker genes for a specific cell type in an organ (e.g., T cells in the human lung) <marker_>`__
#   - `Check expression levels and detection fractions of marker genes across cell types <expression-fraction_>`__
#   - `Querying the gene sequence <sequence_>`__


# %%
# Importing required libraries
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Import the necessary libraries and instantiate the ``API`` object:

import atlasapprox
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

api = atlasapprox.API()


# %%
# .. _marker:
#
# Finding marker genes for a cell type
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Marker genes help identify cell types by exhibiting enriched or exclusive
# expression. Use the ``markers`` method to retrieve the top 10 marker genes for
# T cells in the human lung.

human_lung_T_markers = api.markers(
    organism='h_sapiens',
    organ='lung',
    cell_type='T',
    number=10,
    measurement_type='gene_expression')

human_lung_T_markers

# %%
# .. _expression-fraction:
#
# Analyzing marker gene expression and fraction
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Use the ``average`` method to examine how these marker genes are expressed
# across different lung cell types.

human_lung_T_markers_exp = api.average(
    organism='h_sapiens',
    organ='lung',
    features=human_lung_T_markers,
    measurement_type='gene_expression')

human_lung_T_markers_exp

# %%
# Understanding the output
# ------------------------
#
# This method returns a **pandas.DataFrame** where:
#
# - Each row represents a gene.
# - Each column corresponds to a cell type.
# - Values indicate the average gene expression, measured in counts per ten thousand (cptt).

# %%
# For example, *CD3D* shows an expression of 8.62 cptt in T cells, but only 0.06
# in neutrophils and 0.045 in basophil, highlighting its specificity to T cells
# in the lung.

# %%
# To explore how broadly these genes are expressed, use the ``fraction_detected`` method:

human_lung_fraction = api.fraction_detected(
    organism='h_sapiens',
    organ='lung',
    features=human_lung_T_markers,
    measurement_type='gene_expression')

human_lung_fraction

# %%
# This output shows the fraction of cells expressing each gene, ranging from 0
# to 1. A value of 1 means the gene is expressed in 100% of the cells of that
# type, while 0 means none do. For example, *CD3E* has a detection rate of 0.828
# in T cells (82.8% of T cells express it), but only 0.0057 in neutrophils.
# *CD3D* is expressed in 86.8% of T cells and only 1.1% of neutrophils. These
# patterns reinforce the specificity of these genes as T cell markers.

# %%
# Dot plot visualization
# ----------------------

# Reshape and prepare data
data = pd.melt(
    human_lung_T_markers_exp.reset_index(),
    id_vars='index',
    var_name='Cell types',
    value_name='Expression').rename(columns={'index': 'Genes'})

data['Fraction'] = pd.melt(
    human_lung_fraction.reset_index(),
    id_vars='index')['value'].clip(0, 1)

# Plot dot plot
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
# In this visualization, each dot corresponds to a gene-cell type pair. Both the
# size and color of the dot convey biological meaning: The dot size represents
# the fraction of cells within the cell type that express the gene, while the
# color indicates the average expression level. Larger, darker dots therefore
# represent genes that are both highly expressed and broadly detected.
#
# For instance, *CD3E* and *CD3D* stand out in T cells as large, dark circles,
# indicating strong expression and widespread detection. In contrast, the same
# genes appear as small, pale dots in other cell types, emphasizing their
# specificity to T cells.


# %%
# .. _sequence:
#
# Querying protein sequences of marker genes
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# Marker genes can also be analyzed at the protein sequence level to support
# tasks such as structural analysis, or similarity searches (e.g., BLASTp). To
# retrieve these amino acid sequences efficiently, utilize the ``sequences``
# method as demonstrated below.

sequence = api.sequences(
    organism='h_sapiens',
    features=human_lung_T_markers,
    measurement_type='gene_expression')

# Display retrieved sequences in a readable format
print(f"Sequence type: {sequence['type']}")

for gene, seq in zip(human_lung_T_markers, sequence['sequences']):
    print(f"\n{gene}:\n{seq}")

# %%
# Conclusion
# ^^^^^^^^^^
#
# This tutorial demonstrated how to retrieve marker genes for a specific cell
# type, assess their expression levels and detection frequency, visualize their
# specificity using dot plots, and extract protein sequences for further analysis.
#
# For more detailed information, please refer to the
# `official documentation <https://atlasapprox.readthedocs.io/en/latest/python/index.html>`_.
