# Data Interface

This research-preview contract defines how multimodal cardiac inputs and ordinal task labels would enter AMTDAN. It contains no patient data or implementation.

## Examination record

| Field group | Required content |
|:---|:---|
| Identity | Non-identifying `patient_id` and `exam_id` |
| Visual input | Versioned ultrasound representation with view and quality metadata |
| Clinical input | Structured feature vector with units and missingness mask |
| Task labels | Seventeen condition-specific severity labels on the declared five-level scale |
| Modality state | Availability and quality mask for each input branch |
| Provenance | Site, device family, annotation version, and patient-level split |

## Label registry

For every condition, the registry defines severity order, permissible values, unknown-label handling, class support, and evaluation metrics. Registry versions must remain immutable once a test cohort is frozen.

## Validation checks

- Repeated studies from one patient share a split.
- Visual and clinical records refer to the same examination window.
- Missing modalities are explicit and never replaced by undocumented defaults.
- Test labels are unavailable to preprocessing, fusion, and threshold selection.
- Site and device metadata are retained for stratified evaluation but excluded from unintended prediction paths.

## Public boundary

Only schemas and synthetic fixtures may be released before governance review. Ultrasound, clinical records, identifiers, private manifests, and model artifacts remain excluded.
