import Mathlib

/-!
UCD four-frontier arithmetic companion.  These declarations encode exact
integer consequences of the binary matrix ranks and enumerated witnesses.
The Python programs carry the full 144/1296-bit matrix certificates.
-/
namespace UCDFourFrontiers

theorem kelvin_faces_per_site : 8 * 7 / 2 = 28 := by norm_num
theorem bcc_sites_nt8 : 8 * 2 * 3^3 = 432 := by norm_num
theorem bcc_links_nt8 : 432 * 8 = 3456 := by norm_num
theorem bcc_faces_nt8 : 432 * 28 = 12096 := by norm_num
theorem q72_order : 3 * 24 = 72 := by norm_num
theorem q72_a3_orbit_rank : (72 / 4) * 3 = 54 := by norm_num
theorem css_native_dimension : 144 - 54 - 54 = 36 := by norm_num
theorem shor_nine_code : 9 - 2 - 6 = 1 := by norm_num
theorem concat_length : 144 * 9 = 1296 := by norm_num
theorem concat_x_rank : 2 * 144 + 54 = 342 := by norm_num
theorem concat_z_rank : 6 * 144 + 54 = 918 := by norm_num
theorem concat_encoded_dimension : 1296 - 342 - 918 = 36 := by norm_num
theorem concat_distance_product : 4 * 3 = 12 := by norm_num
theorem low_weight_search_count : 144 + 10296 + 487344 = 497784 := by norm_num
end UCDFourFrontiers
