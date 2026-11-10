# Literature Review: Fuzzy Rule-Base Verification, Diagnosis, and Repair

**Search date:** 2026-11-11
**Status:** Preliminary structured review; not an exhaustive systematic review.

## Scope and search method

Searched scholarly records and publisher/institutional pages from IEEE Xplore, Elsevier/ScienceDirect, Springer, ACM/IEEE conference records, arXiv, university research repositories, and Google Scholar-indexed results where accessible. Terms covered fuzzy rule-base integrity, consistency/completeness, conflict detection and resolution, diagnosis, repair/simplification, mutation testing, counterfactual explanations, semantic preservation, and JFML validation. Publisher or author-institution records were preferred.

This pass identifies direct precedents and rejects broad novelty claims. It does not establish that no similar method exists. When full texts or experimental tables were unavailable, details are marked unverified rather than inferred.

## Paper comparison matrix

### 1. A high-level net approach for discovering potential inconsistencies in fuzzy knowledge bases

- **Authors/year/venue:** H. Scarpelli and F. Gomide, 1994, *Fuzzy Sets and Systems*, 64(2), 175–193.
- **DOI/link:** [10.1016/0165-0114(94)90332-8](https://doi.org/10.1016/0165-0114(94)90332-8); [bibliographic record](https://www2.informatik.uni-hamburg.de/tgi/pnbib/s/scarpelli_h1.html).
- **Problem/method:** Integrity checking for fuzzy knowledge bases using High Level Fuzzy Petri Nets to locate potential local and global inconsistencies.
- **Evaluation:** The accessible record describes simple and chained rule examples; it does not identify a standardized benchmark or quantitative metrics.
- **Limitations/relation/gap:** Foundational structural verification, distinct from numerical activation-grid diagnosis and repair ranking. A new claim must define its conflict semantics and measurable distinction.

### 2. Completeness and consistency conditions for learning fuzzy rules

- **Authors/year/venue:** Antonio Gonzalez and Raúl Pérez, 1998, *Fuzzy Sets and Systems*, 96(1), 37–51.
- **DOI/link:** [10.1016/S0165-0114(96)00280-1](https://doi.org/10.1016/S0165-0114(96)00280-1); [author manuscript](https://sci2s.ugr.es/keel/pdf/specific/articulo/gonzalez_perez_98_completenessandconsistency.pdf).
- **Problem/method:** Learns concept-recognition rules using soft completeness and consistency conditions, combining rule and feature selection and treating consistency as graded under partial matches.
- **Evaluation:** Abstract reports tests on multiple databases; indexed text mentions the Sonar example base. Full list and metric values not verified in this pass.
- **Limitations/relation/gap:** Learning-focused, not post-hoc repair. It shows completeness/consistency are definition-dependent graded objectives; our project must state its own sampled and structural definitions.

### 3. Fuzzy rule-base systems verification using high-level Petri nets

- **Authors/year/venue:** Stephen J. H. Yang, Jeffrey J. P. Tsai, and Chyun Chyi Chen, 2003, *IEEE Transactions on Knowledge and Data Engineering*, 15(2), 457–473.
- **DOI/link:** [10.1109/TKDE.2003.1185845](https://doi.org/10.1109/TKDE.2003.1185845); [institutional record](https://scholars.ncu.edu.tw/en/publications/fuzzy-rule-base-systems-verification-using-high-level-petri-nets/).
- **Problem/method:** Detects redundancy, inconsistency, incompleteness, and circularity by normalizing rules to Horn clauses, transforming them into high-level Petri nets, and verifying the result; reports an implemented tool.
- **Evaluation:** The accessible abstract describes the mechanism/tool but omits benchmark sizes and metrics.
- **Limitations/relation/gap:** Formal representation and truth-factor semantics differ from this repository's Mamdani-style numerical memberships and finite-grid analyses. Integration alone is not novelty.

### 4. Handling of inconsistent rules with an extended model of fuzzy reasoning

- **Authors/year/venue:** Nikhil R. Pal and Kuhu Pal, 1999, *Journal of Intelligent & Fuzzy Systems*, 7(1), 55–73.
- **DOI/link:** [10.3233/IFS-1999-047](https://doi.org/10.3233/IFS-1999-047); [publisher record](https://journals.sagepub.com/doi/pdf/10.3233/IFS-1999-047).
- **Problem/method:** Handles incompatible rules by adding rule-importance factors to fuzzy reasoning, allowing rule-level tuning alongside membership-function tuning.
- **Evaluation:** Abstract reports extensive simulation for a control application; accessible metadata omits model details and metrics.
- **Limitations/relation/gap:** Importance-weighted inference is not identification of the originally corrupted rule or validation of a repair. Compare explicit repair assistance with inference-time conflict handling where semantics align.

### 5. Rule-base simplification in fuzzy systems by aggregation of inconsistent rules

- **Authors/year/venue:** Alexander Gegov, Farzad Arabikhan, and David Sanders, 2015, *Journal of Intelligent & Fuzzy Systems*, 28, 1331–1343.
- **DOI/link:** [10.3233/IFS-141418](https://doi.org/10.3233/IFS-141418); [author manuscript](https://pure.port.ac.uk/ws/portalfiles/portal/2120842/Rule_based_symplification_in_fuzzy_systems_by_aggregation_of_inconsistent_rules_IFS1418.pdf).
- **Problem/method:** Resolves inconsistent rules with identical antecedents by aggregating consequents into one equivalent rule.
- **Evaluation:** Simulation on a transportation-demand-management case study; reports approximation/performance observations. Exact metric values were not extracted.
- **Limitations/relation/gap:** Assumes aggregation is appropriate; it may not recover intended semantics after an injected defect. This is a direct repair/simplification comparator.

### 6. Aggregation of inconsistent rules for fuzzy rule-base simplification

- **Authors/year/venue:** Alexander Gegov, David Sanders, and Boriana Vatchova, 2017, *International Journal of Knowledge-Based and Intelligent Engineering Systems*, 21(3), 135–145.
- **DOI/link:** [10.3233/KES-170358](https://doi.org/10.3233/KES-170358); [institutional record and postprint](https://researchportal.port.ac.uk/en/publications/aggregation-of-inconsistent-rules-for-fuzzy-rule-base-simplificat/).
- **Problem/method:** Replaces groups with identical antecedent permutations but different linguistic consequents by one aggregated rule; motivated where additional data or expertise is unavailable.
- **Evaluation:** Simulation is reported; accessible record omits datasets and metrics.
- **Limitations/relation/gap:** Abstract targets same-antecedent inconsistency, not localization of known injected defects among overlapping nonidentical antecedents.

### 7. Fuzzy Rule Base Simplification via Conflict Resolution by Aggregating Rule Consequents

- **Authors/year/venue:** Ruilin Xu, Changjing Shang, Jinle Lin, Mou Zhou, Yanjie Chen, and Qiang Shen, 2024, *Proceedings of the 2024 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE)*, pp. 1–6.
- **DOI/link:** [10.1109/FUZZ-IEEE60900.2024.10611849](https://doi.org/10.1109/FUZZ-IEEE60900.2024.10611849); [Aberystwyth University record](https://research.aber.ac.uk/en/publications/fuzzy-rule-base-simplification-via-conflict-resolution-by-aggrega/).
- **Problem/method:** Resolves same-antecedent inconsistent rules by linearly combining consequent fuzzy sets, drawing on fuzzy rule interpolation; also targets simplification of learned rule bases.
- **Evaluation:** Record reports better performance in experiments on learned rule bases; dataset names and metric values were not exposed. Full text needed for fair comparison.
- **Limitations/relation/gap:** Aggregation differs from recovering known ground-truth semantics after a mutation. This recent direct precedent rules out broad novelty claims for conflict resolution itself.

### 8. Fuzzy Petri Nets for Human Behavior Verification and Validation

- **Authors/year/venue:** M. Kouzehgar, M. A. Badamchizadeh, and S. Khanmohammadi, 2011, *International Journal of Advanced Computer Science and Applications*, 2(12); arXiv version 2013.
- **Stable links:** [arXiv:1303.1247](https://arxiv.org/abs/1303.1247); [journal PDF](https://thesai.org/Downloads/Volume2No12/Paper%2016-Fuzzy%20Petri%20Nets%20for%20Human%20Behavior%20Verification%20and%20Validation.pdf).
- **Problem/method:** Builds a hierarchical rule base from a questionnaire, maps it to a fuzzy Petri net, and uses reachability/reasoning to search for structural and semantic errors.
- **Evaluation:** Professor–student interaction case study; no standardized multi-system metrics in accessible record.
- **Limitations/relation/gap:** Application-specific construction and Petri-net reachability differ from numerical Mamdani inference and repair ranking. Semantic validation has precedent, but not necessarily the same behavioral checks.

### 9. Computing repair trees for resolving inconsistencies in design models

- **Authors/year/venue:** Alexander Reder and Alexander Egyed, 2012, *Proceedings of the 27th IEEE/ACM International Conference on Automated Software Engineering*.
- **DOI/link:** [10.1145/2351676.2351707](https://doi.org/10.1145/2351676.2351707); [IEEE record](https://ieeexplore.ieee.org/document/6494921/).
- **Problem/method:** Computes inconsistency causes and represents alternative/sequential model changes as repair trees to control repair-space growth.
- **Evaluation:** Reports 29 UML models and 18 OCL design rules; repairs were computed in milliseconds on average.
- **Limitations/relation/gap:** Concerns UML/OCL rather than fuzzy membership semantics. It motivates explicit alternatives and complexity measures but does not establish a fuzzy-specific method.

### 14. Similarity measures in fuzzy rule base simplification

- **Authors/year/venue:** Magne Setnes, Robert Babuška, Uzay Kaymak, and Hans R. van Nauta Lemke, 1998, *IEEE Transactions on Systems, Man, and Cybernetics—Part B*, 28(3), 376–386.
- **DOI/link:** [10.1109/3477.678632](https://doi.org/10.1109/3477.678632); [author manuscript](https://alexandria.tue.nl/openaccess/Metis238686.pdf).
- **Problem/method:** Simplifies learned fuzzy models by merging similar fuzzy sets and rules when they become equivalent.
- **Evaluation:** Reports application to a real-world model; the accessible abstract does not provide standardized benchmark metrics.
- **Limitations/relation/gap:** Targets redundancy and interpretability, not recovery of an intended consequent. Similarity in this project is a heuristic signal, not proof of a defect.

### 15. Fuzzy rule-base simplification using multidimensional scaling and constrained optimization

- **Authors/year/venue:** George E. Tsekouras, 2016, *Fuzzy Sets and Systems*, 297, 46–72.
- **DOI/link:** [10.1016/j.fss.2015.10.009](https://doi.org/10.1016/j.fss.2015.10.009); [publisher record](https://www.sciencedirect.com/science/article/pii/S0165011415005163).
- **Problem/method:** Simplifies accurate Gaussian-set models using fuzzy-set similarity, multidimensional scaling of antecedents, fuzzy clustering/merging, and constrained optimization to balance interpretability and model performance.
- **Evaluation:** Simulation experiments include low- and high-dimensional datasets; dataset identities and metric values require full-text extraction.
- **Limitations/relation/gap:** Assumes an accurate initial model and targets complexity, not diagnosis of injected faults. Accuracy and edit complexity are established objectives, not novel by themselves.

### 10. Model-based mutation testing—Approach and case studies

- **Authors/year/venue:** Fevzi Belli, Christof J. Budnik, Axel Hollmann, Tugkan Tuglular, and W. Eric Wong, 2016, *Science of Computer Programming*, 120, 25–48.
- **DOI/link:** [10.1016/j.scico.2016.01.003](https://doi.org/10.1016/j.scico.2016.01.003); [ScienceDirect record](https://www.sciencedirect.com/science/article/pii/S0167642316000137).
- **Problem/method:** Defines insertion and omission operators over graph models, event-sequence graphs, finite-state machines, and statecharts to assess tests and expose faults.
- **Evaluation:** Three industrial/commercial case studies; abstract reports insertion-based test sets were more effective than omission-based sets.
- **Limitations/relation/gap:** Not fuzzy-rule-specific; mutation score differs from semantic repair correctness. It is a methodological precedent for operator definitions and controls.

### 11. Targeting the Right Situations: Mutation Testing of Fuzzy-Powered Situation Hyperspace

- **Authors/year/venue:** Nawshin Mannan Proma, 2026, arXiv preprint arXiv:2610.15122, submitted 2026-10-10; not peer reviewed as of this search.
- **Stable link:** [arXiv:2610.15122](https://arxiv.org/abs/2610.15122).
- **Problem/method:** Compares uniformly random and fuzzy-guided situation generation for UAV mine-flight testing in SCALOFT, using software mutants.
- **Evaluation:** Abstract reports higher mutation score for fuzzy guidance but does not state the numeric score or mutant count; no secondary-source numbers are used here.
- **Limitations/relation/gap:** Tests a fuzzy-guided input strategy, not fuzzy rule-base defect diagnosis or repair. Recheck peer-review status later.

### 12. Counterfactuals in fuzzy relational models

- **Authors/year/venue:** Rami Al-Hmouz, Witold Pedrycz, and Ahmed Chiheb Ammari, 2024, *Artificial Intelligence Review*, 57(12), article 343.
- **DOI/link:** [10.1007/s10462-024-10996-9](https://doi.org/10.1007/s10462-024-10996-9); [Springer record](https://link.springer.com/article/10.1007/s10462-024-10996-9).
- **Problem/method:** Formulates counterfactual explanations for fuzzy relational equations as optimization and represents nonunique solutions using type-2 or interval-valued fuzzy sets.
- **Evaluation:** Illustrative examples; accessible record has no benchmark or comparative metric table.
- **Limitations/relation/gap:** Counterfactual explanations in fuzzy relations are not counterfactual repair of rule-base defects. Nonuniqueness is already an explainability topic; project claims must stay narrower.

### 13. JFML: A Java Library to Design Fuzzy Logic Systems According to the IEEE Std 1855-2016

- **Authors/year/venue:** José M. Soto-Hidalgo, José M. Alonso, Giovanni Acampora, and Jesús Alcalá-Fdez, 2018, *IEEE Access*, 6, 54952–54964.
- **DOI/link:** [10.1109/ACCESS.2018.2872777](https://doi.org/10.1109/ACCESS.2018.2872777); [IEEE record](https://ieeexplore.ieee.org/abstract/document/8476558/).
- **Problem/method:** Open-source Java implementation of IEEE 1855-2016 Fuzzy Markup Language for interoperability among fuzzy-system tools.
- **Evaluation:** Three case studies demonstrate library functionality and exchange, not universal numerical conformance for every model/operator.
- **Limitations/relation/gap:** The project's comparison against one JFML example is system-specific validation, not general IEEE conformance.

## Synthesis and evidence gaps

- **Verification/conflict/completeness:** Structural Petri-net checking and learning-oriented graded consistency/completeness are established. Definitions differ by representation, so comparisons must align inference operators and assumptions.
- **Localization/diagnosis:** This pass did not establish that activation-grid localization or region-level ambiguity is new. Broader fuzzy diagnosis and model-based diagnosis searches remain necessary.
- **Repair/ranking:** Consequent aggregation is directly studied in 2015, 2017, and 2024; general repair trees exist for design models. Ranking edits by structural change and sampled behavior is not novel without direct comparisons.
- **Mutation testing:** General model-based mutation is mature. The 2026 preprint is adjacent, but it mutates software and changes test inputs rather than fuzzy rule bases. A fuzzy-rule suite needs formal operators, invalid/equivalent mutant handling, and known ground truth.
- **Semantic preservation:** Simplification work evaluates approximation/accuracy and fuzzy counterfactual work treats nonunique explanations. These do not show that this project's sampled outside-region behavior is semantically preserved.
- **Benchmarks/scalability:** This pass did not identify a shared benchmark spanning injected rule defects, ambiguity, candidate repairs, and behavioral impact. Absence in this search is not proof none exists.
- **External validation:** JFML implements IEEE 1855; one-model comparison supports only the selected model and tested points.

Still required: full-text extraction for 2015/2017/2024 aggregation methods; citation-chain searches for fuzzy diagnosis/localization/semantics-preserving repair; mapping this repository's predicates and metrics to comparator definitions; and recovery of the 12-rule benchmark source and raw outputs.
