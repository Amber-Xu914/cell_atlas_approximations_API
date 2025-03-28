REST
====
Cell atlas approximations are designed to be readable by machines independent of programming language. For this purpose, a RESTful API is provided.

The current version of the RESTful API is **v1**.

Quick start
-----------
.. tabs::

   .. tab:: **Python**

      .. code-block:: python
      
        import requests
        response = requests.get(
            'http://api.atlasapprox.org/v1/organs',
            params=dict(organism='h_sapiens'),
        )
        print(response.json())


   .. tab:: **R**

      .. code-block:: R
      
        response <- httr::GET('http://api.atlasapprox.org/v1/organs')
        print(reponse)

   .. tab:: **JavaScript**

      .. code-block:: javascript

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                console.log(xmlHttp.responseText);
        }
        xmlHttp.open("GET", 'http://api.atlasapprox.org/v1/organisms', true);
        xmlHttp.send(null);

Getting started
---------------
- The API generally accepts **GET** requests only.
- The API returns **JSON** data except for the ``approximation`` endpoint, which returns an HDF5 file.
- For data involving gene expression, only 50 features at a time are supported to reduce egress throughput.
- No aliases for names (e.g. organisms, genes) are supported yet: please double check your spelling.
- If you can use one of the languge-dedicated APIs (e.g. the Python API), please do so instead of using the REST API. Language-specific packages use caching to reduce load on our servers and also give you faster answers, so it's a win-win.

.. note::
   Mouse genes are generally spelled with only the first letter capitalised, while human genes
   are spelled ALL CAPS.

If you are starting to explore the API from scratch, you can start by asking:

1. What organisms are available.
2. What organs are covered in your organism of choice.
3. What cell types are found in your organism and organ of interest.

After that you can query gene expression in specific cell types, organs, and organisms.

Reference API
-------------
The complete API is described below. Endpoints refer to the end of the URL only. For
instance, to query a list of available organisms, the **endpoint** description is ``/organisms`` so the full URL is ``http://api.atlasapprox.org/v1/organisms``.

Measurement types
+++++++++++++++++
**Endpoint**: ``/measurement_types``

**Parameters**: None

**Returns**: A dict with the following key-value pairs:
  - ``measurement_types``: The types of measurements (e.g. gene expression, chromatin accessibility). Not all organisms and organs are available for all measurement types, of course.

Organisms
+++++++++
**Endpoint**: ``/organisms``

**Parameters**:
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organisms``: The organisms available.


Organs
++++++
**Endpoint**: ``/organs``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organism``: The organism chosen.
  - ``organs``: The available organs for that measurement type and organism.

Features
++++++++
**Endpoint**: ``/features``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features available for that organism and measurement type.

   
.. note::
   All organs within one organism use the same features, in the same order.

Check features
++++++++++++++
**Endpoint**: ``/has_features``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features chosen, spell-corrected if necessary.
  - ``found``: A boolean list of the same length as ``features``, with each element specifying if that feature
    was found in this organism and measurement type.

Cell types
++++++++++
**Endpoint**: ``/celltypes``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.
  - ``include_abundance`` (optional, default ``false``): Whether to include cell numbers for each type.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen (same comment).
  - ``celltypes``: The list of cell types for that organism and organ.

If the ``include_abundance`` parameter was specified as true, the dict also has the following key-value pairs:
  - ``abundance``: The number of cells for each cell type.

Cell type location
++++++++++++++++++
**Endpoint**: ``/celltype_location``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``celltype``: The cell type to find organs/locations for.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``celltype``: The cell type chosen.
  - ``organs``: A list of organs in which that cell type was detected.

Table of cell types x organ
+++++++++++++++++++++++++++
**Endpoint**: ``/celltypexorgan``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organs`` (optional): A list of organs of interest. If not specified, all organs from the chosen organism will be used. If specified, must be a subset of the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.
  - ``boolean`` (optional, default ``false``): Whether to return a boolean presence/absence matrix
        (if ``true``) or the number of cells/nuclei sampled for each type and organ (if ``false``).

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organs``: A list of organs chosen.
  - ``celltypes``: A list containing all celltypes from any of the chosen organs or, if no organs were specified, from the whole organism. They are ordered from celltypes detected in most organs to the ones found in only one organ.
  - ``detected``: A table (list of lists) of numeric values. If ``boolean`` was set to ``true``, ``1`` or ``true`` means that cell type was detected in that organ. Otherwise, this is the number of samples cells/nuclei from that cell type and organ, without any normalisation. Order of rows and columns as in the ``organs`` and ``celltypes`` part of the returned object.

Table of organ x organism for a cell type
+++++++++++++++++++++++++++++++++++++++++
**Endpoint**: ``/organxorganism``

**Parameters**:
  - ``celltype``: The cell type chosen.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organs``: A list of organs containing that cell type in at least one organism.
  - ``organisms``: The list of organisms that contain that cell type.
  - ``celltype``: The chosen cell type, spell corrected if necessary.
  - ``detected``: A table (list of lists) of boolean values, with 1 indicating presence and 0 indicating absence of the chosen cell type in that organ and organism. Order of rows and columns as in the ``organs`` and ``organisms`` part of the returned object.

Table of cell types x organism
++++++++++++++++++++++++++++++
**Endpoint**: ``/celltypexorganism``

**Parameters**:
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``celltypes``: A list containing all celltypes across the entire database.
  - ``organisms``: The list of organisms across the entire database.
  - ``detected``: A table (list of lists) of boolean values, with 1 indicating presence and 0 indicating absence of the chosen cell type in that organism. Order of rows and columns as in the ``celltypes`` and ``organisms`` part of the returned object.

Averages
++++++++
**Endpoint**: ``/average``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. Either this or the ``celltype`` parameter are required and you cannot specify both.
  - ``celltype``: The cell type of interest. Must be present in at least one organ. Either this or the ``organ`` parameter are required and you cannot specify both.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``features``: The features requested. Any spelling correction is included here.
  - ``average``: The average measurement (e.g. gene expression) for each cell type and feature.
  - ``unit``: The unit of measurement for this measurement type.

If the ``organ`` parameter was specified, the dict also has the following key-value pairs:
  - ``organ``: The organ chosen.
  - ``celltypes``: A list containing all celltypes from any of the chosen organ.

If the ``celltype`` parameter was specified instead, the dict also has the following key-value pairs:
  - ``celltype``: The cell type chosen.
  - ``organs``: The organs containing the chosen cell type.

Fraction of cells with signal
+++++++++++++++++++++++++++++
**Endpoint**: ``/fraction_detected``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. Either this or the ``celltype`` parameter are required and you cannot specify both.
  - ``celltype``: The cell type of interest. Must be present in at least one organ. Either this or the ``organ`` parameter are required and you cannot specify both.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about. 

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``features``: The features requested. Any spelling correction is included here.
  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell type and feature.

If the ``organ`` parameter was specified, the dict also has the following key-value pairs:
  - ``organ``: The organ chosen.
  - ``celltypes``: A list containing all celltypes from any of the chosen organ.

If the ``celltype`` parameter was specified instead, the dict also has the following key-value pairs:
  - ``celltype``: The cell type chosen.
  - ``organs``: The organs containing the chosen cell type.

.. note::
   For some measurement types (e.g. chromatin accessibility), fraction of cells with signal is currently defined as exactly equal the average measurement, so the two API calls are equivalent except for the keys of the output dictionary.

Dotplot data (average and fraction detected at once)
++++++++++++++++++++++++++++++++++++++++++++++++++++
**Endpoint**: ``/dotplot``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. Either this or the ``celltype`` parameter are required and you cannot specify both.
  - ``celltype``: The cell type of interest. Must be present in at least one organ. Either this or the ``organ`` parameter are required and you cannot specify both.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about. 

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``features``: The features requested. Any spelling correction is included here.
  - ``average``: The average measurement (e.g. gene expression) for each cell type and feature.
  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell type and feature.

If the ``organ`` parameter was specified, the dict also has the following key-value pairs:
  - ``organ``: The organ chosen.
  - ``celltypes``: A list containing all celltypes from any of the chosen organ.

If the ``celltype`` parameter was specified instead, the dict also has the following key-value pairs:
  - ``celltype``: The cell type chosen.
  - ``organs``: The organs containing the chosen cell type.

.. note::
   For some measurement types (e.g. chromatin accessibility), fraction of cells with signal is currently defined as exactly equal the average measurement, so the two API calls are equivalent except for the keys of the output dictionary.

Neighborhoods (cell states)
+++++++++++++++++++++++++++
**Endpoint**: ``/neighborhood``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.
  - ``include_embedding`` (optional, default ``false``): Whether to include embedding coordinates for each neighborhood.
  - ``features``: A list of features (e.g. genes) for which cell state-level average and fraction detected are requested.


**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen.
  - ``celltypes``: A list of cell types in the tissue.
  - ``ncells``: A table (list of lists) with the number of cells for each cell type in each neighborhood (cell state).

If the ``features`` parameter was specified and at least one feature was found, the dict also has the following key-value pairs:

  - ``features``: The features requested (optional). Any spelling correction is included here. 
  - ``average``: A list of average measurements for each cell state.
  - ``unit``: The unit of measurement for this measurement type.

If ``features`` was requested for a measurement type that has both averages and fraction detected (e.g. gene expression), the dict also has the following key-value pair:

  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell state and feature.

If ``include_embedding`` was true, the dict also has the following key-value pairs:

  - ``centroids``: The x and y coordinates of the centroid of each cell state in a tissue-level embedding (e.g. UMAP).
  - ``boundaries``: A list of convex hulls. Each hull is a list of (x, y) coordinates with the perimeter of that cell state in the same embedding as the centroids.

.. note::
   If no features are selected but ``include_embedding`` is true, this endpoint call can be used to gain *only* the cell state embedding.

Marker features
+++++++++++++++
**Endpoint**: ``/markers``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. If ``versus`` is set to ``other_organs``, the special string ``all`` can be used to request markers for each organ.
  - ``celltype``: The cell type of interest. If ``versus`` is set to ``other_celltypes`` (the default), the special string ``all`` can be used to request markers for each cell type in the tissue.
  - ``number``: The number of marker features to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.
  - ``versus``: Either ``other_celltypes`` (default) or ``other_organs``. The default is to compare the chosen cell type with other cell types from the same organ. The alternative option is to compare against the same cell type in other organs.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen.
  - ``celltype``: The cell type chosen.
  - ``markers``: The markers (e.g. genes, peaks) that are measured at higher level in the chosen cell type compared to other cell types within the same organ.

If either ``celltype`` or ``organ`` was set to ``all``, the dict also has the following key-value pair:

  - ``targets``: A list of cell types/organs of the same length as ``markers``. For each marker in the list, this specified what cell type/organ it is marking.

.. note::
   There are multiple methods to determine marker features (e.g. genes). Future versions of the API will allow the user to choose between methods.

Interactions
++++++++++++
**Endpoint**: ``/interaction_partners``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features to look for interaction partners with.

**Returns**: A dictionary with the following key-value pairs:
  - ``queries``: A list of features queried.
  - ``targets``: A list of interaction partners.

The two lists have equal length and are paired. Each pair of entries (e.g. the first entry of each list) indicates an interaction. Because each feature can be part of multiple interactions, queried features might (and typically do) appear multiple times.

Homologous features
+++++++++++++++++++
**Endpoint**: ``/homologs``

**Parameters**:
  - ``source_organism``: The source organism of interest, for which the features are known. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features to look for.
  - ``target_organism``: The target organism of interest, for which the features are unknown. Must be one of the available ones as returned by ``organisms`` and, of course, must be different from ``source_organism``.
  - ``max_distance_over_min``: This argument sets the threshold for additional homologs beyond the closest match. If set to zero, only the closest match across speces will be returned. Setting this parameter above around 50 is pointless as there is a hard cutoff on the absolute distance at 60.

**Returns**: A dictionary with the following key-value pairs:
  - ``queries``: A list of features queried in ``source_organism``.
  - ``targets``: A list of homologous features in ``target_organism``.
  - ``distances``: A list of distances between each query and its homolog. Lower values indicate stronger homology.

The three lists have equal length and are paired. Each triplet of entries indicates a homology relationship. Because each feature can have multiple homologs (i.e. paralogs), queried features might (and typically do) appear multiple times.

Currently, homology is estimated using `PROST <https://doi.org/10.1073/pnas.2211823120>`_. Therefore, only gene expression for protein-coding genes is supported.

.. note::
   Setting the source and target organisms to the same species can be used to search for paralogs within that species. Increasing ``max_distance_over_min``
   might be necessary in that case since the closest match is by definition the query itself, which is at distance zero. Values of 20-30 are usually
   reasonable for this purpose.

Homology distance between pairs of features
+++++++++++++++++++++++++++++++++++++++++++
**ENDPOINT**: ``/homology_distances``

**Parameters**:
  - ``source_organism``: The source organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``source_features``: The features to look for in the source organism.
  - ``target_organism``: The target organism of interest. Must be one of the available ones as returned by ``organisms``. It can be the same as the source organism.
  - ``target_features``: The features to look for in the target organism. Must be the same number as ``source_features``.

  **Returns**: A dictionary with the following key-value pairs:
  - ``queries``: A list of features queried in ``source_organism``.
  - ``targets``: A list of features queried in ``target_organism``.
  - ``distances``: A list of distances between each pair of features. Lower values indicate stronger homology.

See ``/homologs`` for more information on the distance metric used.

Highest-measurement
++++++++++++++++++++++++++++++
**Endpoint**: ``/highest_measurement``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``feature``: The feature to look for.
  - ``number``: The number of cell types to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen.
  - ``feature``: The feature chosen, autocorrected for capitalisation and such.
  - ``celltypes``: A list of cell types with the highest measurement (e.g. expression) for that feature
  - ``organs``: A list of corresponding organs. This parameter and ``celltypes`` should be interpreted together as pairs that fully specify cell types.
  - ``average``: average measurement (e.g. expression) in those cell types and organs.
  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell type and organ.
  - ``unit``: The unit of measurement for the average measurement returned.

Highest-measurement across multiple features
++++++++++++++++++++++++++++++++++++++++++++
**Endpoint**: ``/highest_measurement_multiple``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features to look for.
  - ``number``: The number of cell types to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen.
  - ``features``: The features chosen, autocorrected for capitalisation and such.
  - ``celltypes``: A list of cell types with the highest measurement (e.g. expression) for that feature
  - ``organs``: A list of corresponding organs. This parameter and ``celltypes`` should be interpreted together as pairs that fully specify cell types.
  - ``average``: Average measurement (e.g. expression) in those cell types and organs for the chosen features.
  - ``score``: A list of "scores" used to rank cell type-organ pairs to determine the highest combined measurement (higher is better). The exact meaning of the score is to be considered immaterial and is subject to change.
  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell type, organ and feature.
  - ``unit``: The unit of measurement for the average measurement returned.

.. note::
   If not all features requested can be found, the server will respond with the ones that could be found and ignore the other ones. This should be fine in most casesbut
   but could lead to unexpected ranking if key features were missing (e.g. misspelled beyond our autocorrection ability). If no features were found at all, an error
   is returned.

Similar features
++++++++++++++++
**Endpoint**: ``/similar_features``

**Parameters**:
  - ``organism``: The organism of interest.
  - ``organ``: The organ of interest.
  - ``feature``: The original feature to look for similar features of.
  - ``number``: How many similar features to return.
  - ``method``: Method to use to compute distance between features. Available methods are:
    - ``correlation`` (default): Pearson correlation of the ``fraction_detected``.
    - ``cosine``: Cosine similarity/distance of the ``fraction_detected``.
    - ``euclidean``: Euclidean distance of average measurement (e.g. expression).
    - ``manhattan``: Taxicab/Manhattan/L1 distance of average measurement.
    - ``log-euclidean``: Log the average measurement with a pseudocount of 0.001, then compute euclidean distance. This tends to highlight sparsely measured features.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``method``: The method used.
  - ``feature``: The requested feature.
  - ``similar_features``: A list of similar features (e.g. genes) to the one requested.
  - ``distances``: Distances of the listed feature in the method chosen. For correlation/cosine methods, the distance is 1 - correlation.

Similar cell types
++++++++++++++++++
**Endpoint**: ``/similar_celltypes``

**Parameters**:
  - ``organism``: The organism of interest.
  - ``organ``: The organ of the cell type of interest. This parameter, together with the ``celltype`` parameter, constitute a full specification of the type of cells you are focusing on. Note that the similar cell types will *not* be restricted to this organ.
  - ``celltype``: The cell type of interest, to find similar types to. This parameter works jointly with the ``organ`` parameter, see above.
  - ``number``: How many similar cell types are requested.
  - ``features``: What features (genes, chromatin peaks, etc.) to use to determine similarity. Because many measurement spaces are high-dimensional, similarities are not meaningful without a feature selection (https://en.wikipedia.org/wiki/Curse_of_dimensionality). The same does *not* apply to the ``/similar_features`` endpoint, because there are only a few dozens cell types within an organ, so the space is relatively low-dimensional.
  - ``method`` (optional, default ``correlation``): What method to use to compute similarity. Currently available methods are:
    - ``correlation``: Pearson correlation of fraction detected.
    - ``euclidean``: Euclidean (L2) distance of average measurement.
    - ``manhattan``: Manhattan (L1) distance of average measurement.
    - ``log-euclidean``: Take the log of the measurement, then Euclidean distance. This emphasizes low-detected features, but also amplifies noise if the features are not selected carefully.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``celltype``: The cell type of interest.
  - ``method``: The method used.
  - ``features``: The requested features.
  - ``similar_celltypes``: A list of similar cell types. This should be interpreted in tandem with the ``similar_organs`` key below.
  - ``similar_organs``: A list of the organs for the similar cell types. This should be interpreted together with the ``similar_celltypes`` key above. Each pair of ``(organ, celltype)`` fully specifies a similar cell type.
  - ``distances``: Distances of the listed cell types in the method chosen. For correlation/cosine methods, the distance is 1 - correlation.

Approximation file
++++++++++++++++++
**Endpoint**: ``/approximation``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.

**Returns**: A binary (HDF5) file containing the approximation of the cell atlas for the chosen organism. You probably want to name the file something like ``approximation.h5``.

Data Sources
++++++++++++
**Endpoint**: ``/data_sources``

**Returns**: A dict with a key per organism listing the cell atlases (data sources) used for the approximations.

Full atlas data files
+++++++++++++++++++++
**Endpoint**: ``/full_atlas_files``

**Returns**: A URL to a public cloud folder where you can download the full atlas data files for each organism. Read the README.md file. Some organisms are missing because their atlases are very large and already shared on FigShare.
