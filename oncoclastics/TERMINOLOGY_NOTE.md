# Oncoclastics: a terminology note

**Version 1.0.0 · 2026-10-12 · Cesar Marolla (ORCID 0000-0001-8498-7380)**

Status: definition note and reference mapping. Research framework, not validated, not a medical device (see `DISCLAIMER.md`).

---

## 1. The term

**Oncoclastics** (noun; adjective **oncoclastic**, as in "an oncoclastic event") is the application of hazard–exposure–vulnerability–resilience assessment, as developed in disaster-risk reduction, to the fragmentation of cancer-related trajectories. As a method, it is a disaster-risk-reduction–based approach to oncological surveillance cascades. It is implemented here through the Risk Mechanism Theory Index (RMTI; Marolla, 2018, 2025, 2026a, 2026b).

Two senses are distinguished and **must be named wherever the term is used**:

| Sense | What is fragmented | Patient-level carrier in the RMTI |
|---|---|---|
| **Biological oncoclastics** | The adaptive trajectory of one patient from chronic injury toward cancer (for example, chronic liver injury toward hepatocellular carcinoma, HCC, including noncirrhotic HCC) | L, E, V and the biological component of resilience, ρ_bio |
| **Care-system oncoclastics** | The continuity of surveillance and care along that same path | The care-system component of resilience, ρ_care, and the delivery series that drives it over time |

In the **allostatic reading** used in the accompanying manuscript, the continuity that is broken in the biological sense is adaptive continuity: the path from chronic injury toward cancer is read as a series of discontinuities in restoration and recalibration, ending where adaptive reserve can no longer sustain compensation (relinquishment). The definition above does not depend on that reading; it is one framework in which the biological sense can be stated.

The term organizes existing predictors and existing views of cancer. It does not replace them, it does not describe a therapy, and it does not imply destruction of tumor.

## 2. Etymology and closest terms

*Onco-* (Greek *onkos*, mass, tumor) + *-clastic* (Greek *klastos*, broken; as in *clastic*, composed of fragments). What is broken is **continuity**: of an adaptive trajectory (biological sense) or of a care pathway (care-system sense).

Established terms that a reader may confuse it with:

- **Oncolytic**: therapies, notably viruses, that infect and destroy tumor cells (Russell et al., 2012). An action on tumor tissue; oncoclastics is not.
- **Osteoclast / osteoclastic**: a bone cell that resorbs bone (Teitelbaum, 2000). An action on tissue by a cell; oncoclastics is not.
- **Clastogenic**: causing breaks in chromosomes. Relevant to carcinogenesis, but it names a property of an agent acting on DNA. Oncoclastics concerns the trajectory of a patient and of their care, not the integrity of the genome. *(Dictionary-level term; add a citation if the journal asks for one.)*

## 3. Two uses of the term: academic and oncological

**Academic use** (naming, scholarship, citation). The term labels a method and a way of dividing a problem. In text: give "Risk Mechanism Theory Index (RMTI)" in full at first use (the acronym has unrelated uses elsewhere); state the sense (biological or care-system) at every use; cite this note and the RMTI sources; and avoid it as a synonym for "cancer progression", "tumor destruction" or "screening failure". Suggested keywords: *oncoclastics; Risk Mechanism Theory Index; RMTI; disaster-risk reduction; surveillance; hepatocellular carcinoma*.

**Oncological use** (what is scored). Each RMTI domain is read at the level of the individual patient, rescored over successive assessments, and each domain is assigned to one sense. Table 1 below is the canonical statement of that assignment. In the reference code (`rmti_oncoclastics.py`) the biological sense is carried by L, E, V and ρ_bio, and the care-system sense by ρ_care; the existing time-indexed HCC layer already behaves this way, because its V*(t) is driven by an allostatic-load indicator (biological) and its ρ(t) by surveillance adherence (care-system).

## 4. The RMTI domains in the two senses

**Table 1 (of this note; Table S9 of the manuscript).** Use of the RMTI domains in the two senses of oncoclastics. Definitions are *adapted* from the disaster-risk definitions of the RMTI for use with an individual patient (the re-parametrization of E, V and ρ is described in the manuscript and in its Supplementary Material S5); they do not reproduce them.

| Term | Definition for an individual patient | Biological oncoclastics | Care-system oncoclastics (enters through ρ only) |
|---|---|---|---|
| **Unit** | Individual patient, rescored over successive assessments | Progression from chronic injury toward cancer (for example HCC) | The same patient's care pathway (surveillance and follow-up). Programme- or population-level scoring, as in the HCC-surveillance application, is a different unit and is not covered here |
| **L** | Likelihood of the outcome over a defined horizon, from a stage-anchored or validated model, rescaled to a bounded score | Probability of progression to cancer over the horizon | Unchanged by disruption of care; remains the outcome probability. The disruption itself is not given a hazard term: the probability that care is interrupted is not modeled |
| **E** | Cumulative burden imposed on the liver (magnitude, duration, frequency) | Burden of metabolic, inflammatory, toxic or hemodynamic insults on the liver | Unchanged by disruption of care. The programme-level E of the HCC-surveillance application (share of patients inside the surveillance footprint) is not used; coverage and continuity enter through ρ_care |
| **V** | Accumulated cost of prior injury and incomplete adaptation (allostatic load) | Allostatic load carried forward across cycles | Not a care-system term. Missed care can raise V only through biology, as unresolved injury accrues in later cycles (V*(t) in the time-indexed layer) |
| **ρ** | Adaptive capacity, expressed as the fraction of inherent risk that is absorbed; (1 − ρ) is the unabsorbed fraction | ρ_bio: biological adaptive reserve, scored on five provisional anchor levels (0.10, 0.25, 0.40, 0.55, 0.70, the span of the existing ρ ladders; `RHO_BIO_ANCHORS.md`) | ρ_care: delivery of surveillance, access to follow-up, continuity, adherence. A disruption of care is a fall in ρ_care |
| **C** | Ordinal severity if the outcome occurs (0.10–1.00); used only in EAL | Outcome-specific severity (for HCC, anchored to stage at detection) | Care capacity can shift stage at detection and so overlaps with ρ_care. Default: the effect of care enters through ρ_care only, and C is not re-scored when care changes; report EAL with C re-scored as a sensitivity analysis |

**Combining the two components of ρ.** If biological and care-system absorption act independently on the same inherent risk,

> ρ = 1 − (1 − ρ_bio) · (1 − ρ_care)

which is bounded in [0, 1), monotone in each component, and never double-counts capacity. Example: ρ_bio = 0.50 and ρ_care = 0.40 give ρ = 0.70, not 0.90. With ρ_bio = 0 it equals ρ_care, which is the ρ of the published HCC-surveillance application. Three conditions apply wherever the combined ρ is used: (1) independence is itself a proposition to be tested; (2) ρ_bio must be built from information that does not describe surveillance delivery, and ρ_care must not contain hepatic reserve; (3) the overlap between ρ_care and C is a stated limitation.

**Operational reading of "an oncoclastic event" (provisional, proposed for testing).**

- *Care-system event:* a missed or delayed surveillance cycle, or a fall in delivery between consecutive recorded cycles.
- *Biological event:* a rise in V*(t) beyond a pre-specified step (any rise, if no step is set).

These are descriptive flags, not alerts, diagnoses or recommendations; the step size is uncalibrated. They are implemented in `oncoclastic_events()`.

## 5. Relation to neighboring constructs

- **Cancer care under disaster conditions.** Natural disasters disrupt health-care infrastructure, workforce and continuity of care for patients with cancer (Man et al., 2018), and interrupted screening and diagnostics delay diagnosis, with modeled consequences (Maringe et al., 2020). Care-system oncoclastics differs in treating such disruption as a reduction of absorptive capacity (ρ_care) within an index whose other terms are scored separately. It does not replace outcome studies of disaster exposure.
- **Ecological and evolutionary views.** Cancer as an evolutionary and ecological process of competing cell populations (Merlo et al., 2006; Greaves and Maley, 2012) concerns the tumor as a population. Biological oncoclastics concerns the host's risk trajectory and treats cancer as the outcome toward which it may lead. The two are complementary.
- **Hallmarks of cancer.** The hallmarks describe capabilities acquired by cancer cells (Hanahan and Weinberg, 2011; Hanahan, 2022). Oncoclastics proposes no new hallmark; it concerns exposure, accumulated cost and absorptive capacity at the level of the patient.
- **Cancer systems biology.** Network and pathway models describe dysregulation within cells and tissues (Kreeger and Lauffenburger, 2010). Oncoclastics works at another level, with a bounded arithmetic index scored from stated anchors rather than a mechanistic network model.
- **Allostasis.** V is allostatic load (McEwen and Stellar, 1993; Sterling, 2012; Baffy, 2013), the main route by which oncoclastics connects to the allostatic framework.

## 6. Analogy and limits

The analogy to disaster risk is structural, not literal. It holds where the architecture does the work: hazard, exposure, vulnerability and absorptive capacity are separable terms with distinct directions of effect, accumulated cost carries forward, and the index is built for repeated reassessment. It fails elsewhere. A neoplastic process is not an exogenous hazard; L and E are partly intrinsic to the patient; the scores are relative and uncalibrated; and the vocabulary of disaster must not be read as a description of any patient's experience.

Specific limits of this version: tier cut-points are inherited from disaster-risk applications and are uncalibrated; the measures of V and ρ are immature proxies; rubric scoring involves analyst judgment; the independence assumption in the combined ρ is untested; the probability of a care disruption is not modeled; ρ_care and C overlap; and no clinical action is attached to any score or tier. Whether the approach identifies patients whose trajectories warrant closer follow-up is a proposition to be tested, not a finding.

## 7. Attribution, citation, archive

The RMTI, including its adaptation to oncology, was developed by Marolla (2018, 2025, 2026a, 2026b); the term *oncoclastics* is introduced in the accompanying manuscript and defined in this note. To cite this note:

> Marolla, C. (2026). *Oncoclastics: a terminology note* (Version 1.0.0) [Computer software and definition note]. Zenodo. https://doi.org/[DOI added at release]

## References

Baffy, G. (2013). Allostasis in nonalcoholic fatty liver disease: implications for risk assessment. Dig Dis Sci 58, 302–308.
Greaves, M., and Maley, C.C. (2012). Clonal evolution in cancer. Nature 481, 306–313.
Hanahan, D. (2022). Hallmarks of cancer: new dimensions. Cancer Discov 12, 31–46.
Hanahan, D., and Weinberg, R.A. (2011). Hallmarks of cancer: the next generation. Cell 144, 646–674.
Kreeger, P.K., and Lauffenburger, D.A. (2010). Cancer systems biology: a network modeling perspective. Carcinogenesis 31, 2–8.
Man, R.X., Lack, D.A., Wyatt, C.E., and Murray, V. (2018). The effect of natural disasters on cancer care: a systematic review. Lancet Oncol 19, e482–e499.
Maringe, C., Spicer, J., Morris, M., Purushotham, A., Nolte, E., Sullivan, R., Rachet, B., and Aggarwal, A. (2020). The impact of the COVID-19 pandemic on cancer deaths due to delays in diagnosis in England, UK: a national, population-based, modelling study. Lancet Oncol 21, 1023–1034.
Marolla, C. (2018). Information and Communication Technology for Sustainable Development (Boca Raton: CRC Press). https://doi.org/10.1201/9781351045230
Marolla, C. (2025). Enhancing urban resilience to California wildfires: a systemic risk mechanism design and theory framework for a comprehensive risk assessment. Int J Manag Data Anal 5, 60–77.
Marolla, C. (2026a). From Narrative to Algorithm: A Risk Mechanism Theory Index for Urban Infrastructure Investment in Sub-Saharan Africa. Int J Manag Data Anal 6, 354–388. https://doi.org/10.68485/ijmada.20266156
Marolla, C. (2026b). The Risk Mechanism Theory Index as a triage and evidence-grading layer for hepatocellular carcinoma surveillance. SSRN. https://doi.org/10.2139/ssrn.7427450 (preprint)
McEwen, B.S., and Stellar, E. (1993). Stress and the individual. Mechanisms leading to disease. Arch Intern Med 153, 2093–2101.
Merlo, L.M.F., Pepper, J.W., Reid, B.J., and Maley, C.C. (2006). Cancer as an evolutionary and ecological process. Nat Rev Cancer 6, 924–935.
Russell, S.J., Peng, K.W., and Bell, J.C. (2012). Oncolytic virotherapy. Nat Biotechnol 30, 658–670.
Sterling, P. (2012). Allostasis: A model of predictive regulation. Physiol Behav 106, 5–15.
Teitelbaum, S.L. (2000). Bone resorption by osteoclasts. Science 289, 1504–1508.
