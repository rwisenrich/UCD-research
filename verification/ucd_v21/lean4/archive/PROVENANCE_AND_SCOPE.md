# UCD recovered Lean proof source audit (read-only mathematical status)

Restored historic source, not new theorems. All original `.lean` code is stored as separate archive modules without rewriting declarations. GitHub `main` verification has not been changed.
The main v21 Lean library is compiled on its established workflow; the files in this archive are tested independently in a separate CI job.
Compiling a theorem proves only the actual type stated after the colon, not broader physics claims in the prose comment.

## Exact Google Drive source provenance
- `UCDYangMillsExistenceAndMassGap_v10_Master.lean`: https://docs.google.com/document/d/1f0rx_b0gD7MaOMI3MfCl8RTWwzFbm-_yILE2ia3TqgU/edit
- `UCDYangMillsExistenceAndMassGap_v9_Master.lean`: https://docs.google.com/document/d/1NkxUk6JbkgjSD7Ubqf7yOd93lqRAeT7e2LRW_EbRDUU/edit
- `UCDYangMillsExistenceAndMassGap_v7_Master.lean`: https://docs.google.com/document/d/1dgyl7FnO1Qo4Hq76A93o6R02WprzcCcWgtOmcPeV_YQ/edit
- `UCDYangMillsExistenceAndMassGap_v5_Master.lean`: https://docs.google.com/document/d/1GrAxa8j_GfG8Eq_L9NSaSj7aKkHjLT6QGzD2T4s_t9M/edit
- `UCDYangMillsExistenceAndMassGap_v4.lean`: https://docs.google.com/document/d/1vuoYTXepccQRMvprdGxKQkwuAN4ujxGMi3Idcu9KKr4/edit
- `UCDYangMillsExistenceAndMassGap_v3.lean`: https://docs.google.com/document/d/1zeIIM_U1_VCyNfgVziGxne0rPBx_eQZEZqd0t2obpow/edit
- `UCDYangMillsExistenceAndMassGap_Rebuilt.lean`: https://docs.google.com/document/d/1FkUFH9JnOWFsomD-ASxBldfbxZ2IkAuvixFismr2rCM/edit
- `UCDYangMillsExistenceAndMassGap.lean`: https://docs.google.com/document/d/1a4kzhjrt4rdczfMOlhEVGH8zYe4eRb0J-7_6N5uEIfY/edit
- `UCDUnifiedMasterAtlas180.lean`: https://docs.google.com/document/d/13lpQ4HDMH3oo-ixWQR5rmGYf0XnKqIkgxKffKU2ki80/edit
- `UCDCompleteTheoryOfEverything.lean`: https://drive.google.com/file/d/1x3aK9jCfd5_2VsFqAf8Ehc-0TpWvkXRJ/view
- `UCDVolumeVIIIToIXContinuation.lean`: https://drive.google.com/file/d/1wzQktlpmKexZ2VOZovm_om7Bo-6OAA0q/view
- `UCDCompleteTreatiseProofs.lean`: https://drive.google.com/file/d/1xW65nKTZC-o_yqHgUU-DwWDe9JlaWGNA/view
- `NoRedoContinuationClosureV46.lean`: https://docs.google.com/document/d/1TcvvBGGB60XWm7nC4GloSi5kZCRbrs7Lzs-I9BbqmK8/edit
- `FourStageVacuumMatrixRGAndCosmologyV47.lean`: https://docs.google.com/document/d/1C_Ee4s_k_LYYkoTB7odgEaXlM3F9_klGdBoNVvqxiOw/edit
- `UpstreamPolesBHYMTailAndQLDPCV48.lean`: https://docs.google.com/document/d/16z8hhHHSd7KaqdBrxg6ODPeTcjA2cD5JsFJeK3s4r-o/edit

## Scope warnings
- `bridge15_kelvin_parallelohedron_uniqueness` currently proves a predicate about a specified record, plus arithmetic; it does not prove uniqueness over all convex parallelohedra.
- `bridge104_qec_59_and_qldpc_144_36_12` proves arithmetic involving a record with assigned distance, not a computed proof of code distance 12 or all 59 Knill-Laflamme error conditions.
- The v48 file states a cumulative count of 225 theorems in 28 files, but this file itself contains only 10 theorems and arithmetic certifies the count without importing or verifying the other 27 files.
- Yang-Mills source versions include conditional algebraic and finite rational bounds. Their existence is not by itself a formalization of the infinite-volume 4D Yang-Mills mass gap.

## Duplicate handling
- `Gemini_v7_Master_Lean_export.txt` matches `UCDYangMillsExistenceAndMassGap_v7_Master.lean` and `Gemini_v9_Master_Lean_export.txt` matches `UCDYangMillsExistenceAndMassGap_v9_Master.lean`; only one canonical copy of each is restored.
- The archived Google Drive v21 finite certificate matches the existing GitHub `Finite.lean` and is not duplicated here.

