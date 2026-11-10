import Mathlib

/-!
UCD v21 / Volume IX / Layer XI. Finite exact arithmetic companion.
These proof statements cover the numerical identities derived from the 28-face
Kelvin geometry, internal sector dimensions, and CSS rank arithmetic.
The 72x144 binary-matrix verification is provided by the Python finite gate.
-/
namespace UCDv21

theorem temporal_faces : (11 : Rat) / 6 + 17 / 6 = 14 / 3 := by norm_num
theorem spatial_fourth_moment : (1 : Rat) / 4 = 3 * (1 / 12) := by norm_num
theorem spatial_anisotropy_zero : (1 : Rat) / 4 - 3 * (1 / 12) = 0 := by norm_num
theorem internal_h504_split : 84 + 420 = 504 := by norm_num
theorem internal_bright_dark_split : 84 + 84 + 336 = 504 := by norm_num
theorem group_order : 24 * 3 = 72 := by norm_num
theorem css_length : 2 * 72 = 144 := by norm_num
theorem css_k : 144 - 66 - 66 = 12 := by norm_num
theorem link_modes : 7 * 8 = 56 := by norm_num
theorem four_bond_weights : 4 * ((1 : Rat) / 3) = 4 / 3 := by norm_num
theorem low_weight_syndrome_cardinality : 1 + 1 + 1 + 1 + 1 = 5 := by norm_num
theorem scale_58 : 2 ^ 58 = 288230376151711744 := by norm_num
theorem scale_66 : 2 ^ 66 = 73786976294838206464 := by norm_num
theorem qec_inner_outer : 12 * 12 = 144 := by norm_num

end UCDv21
