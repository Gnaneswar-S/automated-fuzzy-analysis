# Baseline Audit

Audit date: 2026-11-11 (Asia/Kolkata)

## Scope and source

The audit used the repository archive already present at `Automated_fuzzy_analysis/`, including its Git metadata and `origin` remote. The live GitHub repository is `Gnaneswar-S/automated-fuzzy-analysis`, with `main` as its default branch. The archive's `main` commit is `a5947728df6a96ba6d6c6f9e1c0a00bee335d940`, matching the latest commit returned by GitHub. No repository files were modified during the audit until this document was added.

## Git state and protected history

- Starting branch: `main`.
- Starting commit: `a5947728df6a96ba6d6c6f9e1c0a00bee335d940` (`Merge pull request #1 from Gnaneswar-S/frontend-v1`).
- Starting working tree: clean (`main...origin/main`).
- Frozen tag: `v1.0-research-complete` exists locally at commit `a5fa1ec3fbaf68b5f0da97ffa3e63849cee596fa` (tag object `62169c3c6447b6f73cab5a353ef49d3e7840290f`), dated 2026-09-21. It is an ancestor of `main`; `main` adds frontend and deployment work. The tag and its history were not changed.
- `frontend-v1` is not a current local or remote branch, and the GitHub branch search returned only `main`. Its work is preserved in the merge commit's first-parent ancestry and feature commits, including the Streamlit dashboard and custom rule-base editor.
- A new branch, `research/novelty`, was created from the clean `main` commit for continuation. It was subsequently pushed with the Day 1 audit commits.
- No new backup reference was needed because the frozen release tag already provides a recoverable reference and no baseline history is being rewritten.

## Repository structure and architecture

The repository has 51 tracked paths at the current `main` tip. The core is plain Python with NumPy; the interface uses Streamlit.

- `main.py`: command-line demonstration of verification, diagnosis, repair, behavior comparison, controlled benchmark evaluation, localization, and activation analysis.
- `frontend/app.py`: Streamlit research interface, including custom rule-base JSON editing, inspection, verification, diagnosis, repair, and re-verification.
- `core/rules/`: `FuzzyRule` representation and rule utilities.
- `core/fuzzy/`: fuzzy-set definitions and similarity calculations.
- `core/verification/`: consistency and completeness analysis.
- `core/diagnosis/`: rule and conflict diagnosis, localization, and activation-overlap analysis.
- `core/repair/`: candidate generation, ranking, application, behavioral validation, and selection support.
- `core/experiments/`: benchmark construction/runners, mutation and localization experiments, multi-defect experiments, external model adapters, and JFML comparison scripts and CSV fixtures.
- `data/sample_rules.py`: sample rule base.
- `data/external_validation/InvertedPendulumMamdani1.xml`: the model-specific external validation input.
- `results/`: output directory (no committed benchmark output files were present in the tracked file list).

There is no `docs/` directory, no checked-in `tests/` directory, and no standalone test/benchmark configuration in the root. `requirements.txt` pins only `numpy==1.26.4` and `streamlit==1.64.0`.

## Baseline execution

Commands were run with the repository's included Windows virtual environment on 2026-11-11. The environment is not portable as committed and lacks pytest.

| Check | Command | Result |
|---|---|---|
| Main demonstration | `venv\\Scripts\\python.exe main.py` | Passed; exited 0 and printed the existing 4-rule example, including one detected conflict, 100% completeness, repair ranking, controlled defect benchmark, sensitivity/severity analysis, and activation-aware diagnosis. |
| Test discovery/run | `venv\\Scripts\\python.exe -m pytest -q` | Not run to completion: `pytest` is not installed (`No module named pytest`). No tests directory or test files are tracked. |
| JFML systematic comparison | `venv\\Scripts\\python.exe core\\experiments\\compare_jfml_validation.py` | Passed: 289/289 within `1e-5`; maximum absolute error `4.92178742206e-10`; zero NaN mismatches. |
| JFML boundary/transition comparison | `venv\\Scripts\\python.exe core\\experiments\\compare_jfml_boundary.py` | Passed: 49/49 within `1e-5`; maximum absolute error `3.67180064131e-10`; zero NaN mismatches. |

The first attempt to invoke the JFML scripts as Python modules failed because their imports are written for direct script execution; rerunning the documented script files directly succeeded. This is an invocation/import-path limitation, not a failed numerical comparison. JFML source/JAR is not part of this project repository; a separate workspace archive contains the JFML project, but it is not a tracked dependency.

## Historical research claims and reproducibility

The README reports controlled localization, multi-defect, and JFML results. The JFML figures above were reproduced from committed CSV fixtures and the independent implementation. The user's specified 12-rule benchmark (mutations A2/B2/C2; 3 initial conflicts; 100% completeness; 108 sampled conflict-grid points; 3 diagnostic groups; 12 repair candidates) and its six-way `0.7333` repair tie could not be matched to a corresponding checked-in result artifact or an exact summary in the README during this audit.

The closest matching three-region constructor, `create_three_region_interacting_experiment_case()` in `core/experiments/multi_defect_experiment.py`, builds 14 rules (six region rules plus eight coverage rules). Its API returns a `verification` object rather than a serialized report of the specified 108 sampled points and ranking tie. Therefore the 12-rule results are recorded as user-supplied historical baseline claims pending identification of their source script/output; they are not independently verified by this audit. The README's MD-6 description separately reports 9 conflicts and 100% completeness for its stated configuration. These are distinct reported experiment descriptions and should not be conflated.

The README also documents the 4-rule demonstration. Its first listed repair candidates and ranking values differ in scope from the supplied 12-rule controlled benchmark; neither should be used as a substitute for the other. Structural conflict reduction, completeness, and semantic correctness remain separate measurements. In particular, the README acknowledges tie-aware ambiguity and the need to interpret finite-grid results within their configuration.

## Dependency and reproducibility gaps

- `pytest` is absent from the included environment and requirements file; no test suite is committed.
- The included `venv/` is machine-specific and should not be considered an install artifact. A clean setup command is not documented as a verified process.
- No lock file, Python version declaration, lint configuration, CI workflow, benchmark manifest, or machine-readable run metadata was found.
- Existing JFML comparison fixtures preserve numerical outputs, but the independent implementation reproduces only the selected Inverted Pendulum Mamdani M1 semantics. The README correctly limits the claim to that model and those points; it does not establish universal JFML or IEEE 1855 compatibility.
- The root README says to run `python main.py` and gives `python -m streamlit run frontend/app.py` as the frontend command. This audit confirmed the main script only; Streamlit was not launched.

## Initial implementation boundary

The repository is on branch `research/novelty` with the Day 1 audit commits pushed. No algorithm, benchmark protocol, frozen tag, application module, external validation fixture, or existing result was changed. The GitHub integration rejected PR creation with HTTP 403, the local GitHub CLI is unavailable, and the available browser session was signed out; therefore no PR is open yet. The scheduled workflow is not configured or active. The next step is literature review and research-gap documentation, followed by a reviewable plan before any substantial algorithm change.
