# Chunking Strategy

Chunking should preserve SAS-native structure before falling back to generic size-based splitting.

Related stories:
- [CHUNK-001](../../safe/enabler/CHUNK-001-implement-heading-aware-documentation-chunking.md)
- [CHUNK-002](../../safe/enabler/CHUNK-002-implement-sas-aware-code-boundary-detection.md)
- [CHUNK-003](../../safe/feature/CHUNK-003-persist-chunk-ids-and-source-section-paths.md)

Notes:
- Documentation chunks should follow heading hierarchy.
- SAS examples should preserve `PROC`, `DATA`, and macro boundaries.
- Nearby explanatory comments should stay with the code block they explain.
