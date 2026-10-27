# William Gipson | Engineering Portfolio

Mechanical Engineering and Physics student at Texas A&M University, expected May 2029.
My work spans interactive scientific software, electronics troubleshooting, and mechanical design.

[LinkedIn](https://www.linkedin.com/in/william-clay-gipson/)

## Selected Work

| Project | My contribution | Tools |
| --- | --- | --- |
| [CMS Muon Detector Viewer](projects/cms-muon-viewer.md) | Connected interactive detector selections to alignment residual plots | JavaScript, Three.js, JSROOT, HTML/CSS, Python, ROOT, Linux, Git/GitLab |
| [Electronics Testing and Repair](projects/electronics-testing.md) | Diagnosed and repaired 12 shorted circuits; reprogrammed 30 power modules for KRIA compatibility | Thermal imaging, microscope inspection, resistance/continuity and voltage measurements |
| [12 lb Combat Robot](projects/combat-robot.md) | Designed chassis and motor mounts; improved service access and reduced assembled weight from 13.1 to 11.8 lb | Onshape, parametric modeling, assemblies, dimensioned drawings |

Each project page separates my contribution, the engineering approach, and the evidence currently available here.
These are student and team projects, not claims of sole ownership of the surrounding systems.

## Inspectable Code Example

[Chamber plot index](examples/chamber_plot_index.py) is a small, standalone Python example prepared for this portfolio with AI assistance. It illustrates the detector-identifier-to-file lookup used in the viewer workflow. It is **not** the original CERN importer or a physics analysis program.

The example validates wheel/station/sector identifiers, indexes synthetic paths, and retrieves only the plots matching a selected chamber. It has no external Python dependencies and requires Python 3.10 or newer.

Run from the repository root:

```bash
python examples/chamber_plot_index.py examples/synthetic_plot_paths.json --wheel -2 --station 1 --sector 5
python -m unittest discover -s tests -v
```

The first command prints:

```json
[
  "MB-2/1/05/dt_bellcurves.png",
  "MB-2/1/05/dt_polynomials.png"
]
```

The paths are illustrative only. No research images, detector measurements, credentials, or private storage paths are bundled. GitHub Actions is configured to run the tests on pushes and pull requests; a local test pass does not imply that a remote workflow has run.

## Engineering Background

- **TAMU BUILD:** supervise groups of 6-8 volunteers converting shipping containers into medical clinics, including material staging, framing/interior-panel tasks, and panel-fit checks.
- **Engineering Mechanics teaching assistant:** guide 25 students through free-body diagrams, equilibrium, and support reactions during weekly help sessions.
- **STEM tutoring:** explain mathematics and science through systematic problem solving and conceptual understanding.

## Scope and Sharing

This repository is a personal portfolio, not an official CERN or CMS publication. Project descriptions summarize my experience; original team software remains in its project repository. CERN source, unpublished plots, lab photographs, CAD exports, and test records are not redistributed here without permission. The full resume is also excluded by default to avoid publishing its phone number unintentionally.

Current evidence consists of the project write-ups and the runnable example. CAD files, repair records, screenshots, and a recording of the original viewer are not included yet. Ask me about those projects in an interview; the example is not a substitute for the original project artifacts.
