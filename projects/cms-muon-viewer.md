# CMS Muon Detector Viewer

**Context:** CERN A&M Chapter, muon alignment and electronics testing, May-August 2026.

## Problem

Alignment workflows produce many plots organized by detector identifiers. A 3D navigation interface makes it easier to find the plots associated with a wheel, station, and sector instead of navigating output directories manually.

## My Contribution

- Built an interactive muon detector interface using JavaScript, Three.js, JSROOT, and HTML/CSS.
- Connected detector selections to corresponding pre-generated alignment plots.
- Used Python, ROOT, and Linux to organize alignment outputs in support of Monte Carlo validation work.

## How the Pieces Fit

```text
Separate alignment/ROOT workflow -> plot files
Python packaging                 -> plot manifest and metadata
Browser geometry                 -> selected detector identifiers
JavaScript lookup                -> matching plot paths
Browser interface                -> displayed images or ROOT objects
```

Three.js renders the selectable geometry. A raycaster determines which mesh the pointer intersects, and that mesh carries wheel/station/sector metadata. JavaScript passes those identifiers to the plot interface. Providers resolve either packaged image paths or supported ROOT objects; JSROOT handles browser-side ROOT drawing where applicable.

The implementation separates these responsibilities into `detectorScene.js`, `viewerApp.js`, `sidebar.js`, `plotKeys.js`, and `plotProviders.js`. A Python importer prepares a browser-ready package from existing plot directories.

The model is a simplified navigation representation, not a detector simulation. Plot generation and alignment fitting remain in the separate analysis workflow; selecting a chamber displays existing results.

## Repository and Deployment

The team project uses CERN GitLab, separate from this GitHub portfolio. A [viewer merge request](https://gitlab.cern.ch/tamu-cms/MuonAlignment/-/merge_requests/20) was submitted there; access may require CERN credentials. The link is a source/review reference, not a public live demo.

Source control stores and reviews changes. Separately deployed web files serve the browser interface, and JavaScript runs in the user's browser.

## Evidence Here

The [standalone Python example](../examples/chamber_plot_index.py) demonstrates chamber lookup using synthetic filenames. It was prepared for this portfolio, not extracted from CERN production code. Original viewer source and research plots remain with the team project. My work supported Monte Carlo validation; this portfolio does not claim completion of the full validation campaign.
