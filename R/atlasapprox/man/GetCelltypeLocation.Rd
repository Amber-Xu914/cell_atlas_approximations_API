% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/atlasapprox.R
\name{GetCelltypeLocation}
\alias{GetCelltypeLocation}
\title{GetCelltypeLocation}
\usage{
GetCelltypeLocation(organism, cell_type)
}
\arguments{
\item{organism}{The organism you would like to query}

\item{cell_type}{The cell type you would like to query}
}
\value{
An array of organs in which that cell type is found
}
\description{
Get the organs where a specified cell type is found in a given organism.
}
\examples{
GetCelltypeLocation("h_sapiens", "fibroblast")
}
