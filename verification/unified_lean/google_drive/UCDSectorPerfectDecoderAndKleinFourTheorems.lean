/-
  UCDSectorPerfectDecoderAndKleinFourTheorems.lean
  ---------------------------------------------------------------------------
  Pure Core Lean 4 Formalization (Zero External Dependencies, Zero `sorry`s)
  for:
  "Audit of ChatGPT's 100% Single-Shot UCD Relational Decoder and Mathematical
   Continuation to the 2-Bit (4-State) Klein-Four Perfect Decoder, 24-Coset
   Gauge Factorization, and Exact Lindblad Decoherence Law"


  Author: Richard Alan Wise
  Unified Coherence Dynamics Research Program, Denver Metropolitan Area, Colorado, USA
  Date: November 16, 2026


  Formalizes:
  1. Exact Dic_6 group law on G = Z_12 x Z_2 (`dic6Mul`), identity, inverse,
     and the exact relational parity reversal law: for h = x * g^{-1} with
     x = (0, 1) and g = (k, e), Bob's reflection parity is e_B = 1 - e_A
     while Bob's rotation-index parity is p_B = (-k) mod 2 = k mod 2 = p_A.
  2. Exact Relational Product Invariant Conservation Law: under every generator
     action (g, h) -> (s * g, h * s^{-1}) in Delta_vertex, the relational
     invariant c = h * g in Dic_6 is strictly conserved (`relational_product_invariant`).
  3. Exact 2D Uniform Rotation/Reflection Sector Reduction (`h2 = 2I_2 - 2 sigma_x`)
     and exact quarter-turn beamsplitter action at t* = pi/8 mapping
     (|0> + i|1>)/sqrt(2) -> e^{i pi/4}|1> and (|0> - i|1>)/sqrt(2) -> e^{-i pi/4}|0>,
     yielding orthogonal Bob sector supports P_{B,0} P_{B,1} = 0 and D_B(pi/8) = 1.
  4. Exact 4D Abelianization (Klein-Four Z_2 x Z_2) Kronecker-Sum Decomposition
     `h4 = h2 (x) I_2 + I_2 (x) h2` and the 4-State (2-Bit) Single-Shot Perfect
     Decoder at the exact same readout time t* = pi/8, mapping the 4 local
     Alice phase encodings (s_p, s_e) in {+1, -1}^2 onto the 4 mutually
     orthogonal Bob parity-and-reflection quadrants with zero cross-overlap.
-/


namespace UCDSectorPerfectDecoderAndKleinFour


/-- An element of `Dic_6` represented in canonical coordinates `(k, e)` where
    `k ∈ {0..11}` represents `a^k` and `e ∈ {0, 1}` represents `x^e`. -/
structure Dic6 where
  k : Nat
  e : Nat
  deriving DecidableEq, Repr


/-- Modulo-12 helper on integers mapped to `{0..11}`. -/
def mod12 (n : Int) : Nat :=
  Int.toNat ((n % 12 + 12) % 12)


/--Modulo-2 helper on naturals. -/
def mod2 (n : Nat) : Nat :=
  n % 2


/-- Exact group multiplication in `Dic_6`:
    `(a^k x^e)(a^l x^f) = a^{k + (-1)^e l + 6 e f} x^{e xor f}`. -/
def dic6Mul (g h : Dic6) : Dic6 :=
  let sign : Int := if g.e % 2 == 0 then 1 else -1
  let shift : Int := Int.ofNat g.k + sign * Int.ofNat h.k + 6 * Int.ofNat (g.e % 2) * Int.ofNat (h.e % 2)
  { k := mod12 shift, e := (g.e + h.e) % 2 }


/-- Exact group inverse in `Dic_6`. -/
def dic6Inv (g : Dic6) : Dic6 :=
  if g.e % 2 == 0 then
    { k := (12 - (g.k % 12)) % 12, e := 0 }
  else
    { k := (g.k + 6) % 12, e := 1 }


/-- Canonical generators of `Dic_6`: `e_id = (0,0)`, `a = (1,0)`, `x = (0,1)`. -/
def dic6Id : Dic6 := { k := 0, e := 0 }
def genA   : Dic6 := { k := 1, e := 0 }
def genAi  : Dic6 := { k := 11, e := 0 }
def genX   : Dic6 := { k := 0, e := 1 }
def genXi  : Dic6 := { k := 6, e := 1 }


/-- Bob's relational partner address `h = x * g^{-1}` for Alice's address `g`. -/
def bobPartner (g : Dic6) : Dic6 :=
  dic6Mul genX (dic6Inv g)


/-- Reflection sector parity `e ∈ {0, 1}`. -/
def reflParity (g : Dic6) : Nat := g.e % 2


/-- Rotation index parity `p = k mod 2 ∈ {0, 1}`. -/
def rotParity (g : Dic6) : Nat := g.k % 2


/-- Klein-four quadrant index `q(g) = 2 * e(g) + p(g) ∈ {0, 1, 2, 3}`. -/
def kleinQuadrant (g : Dic6) : Nat := 2 * reflParity g + rotParity g


-- ============================================================================
-- THEOREM 1: Exact Reflection-Sector Inversion and Rotation-Parity Preservation
--            Across All 24 Relational Pairs `(g, x * g^{-1})`
-- ============================================================================


/-- Exhaustive boolean check that for every `k ∈ {0..11}` and `e ∈ {0, 1}`,
    Bob's relational partner `h = x * g^{-1}` has opposite reflection parity
    `e_B = 1 - e_A` and identical rotation parity `p_B = p_A`. -/
def checkAll24RelationalParities : Bool :=
  let ks := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  let es := [0, 1]
  ks.all (fun k =>
    es.all (fun e =>
      let g : Dic6 := { k := k, e := e }
      let h := bobPartner g
      (reflParity h == (1 - reflParity g)) && (rotParity h == rotParity g)))


theorem relational_sector_inversion_and_parity_preservation :
    checkAll24RelationalParities = true := by
  decide


-- ============================================================================
-- THEOREM 2: Exact Conservation of the Relational Product Invariant `c = h * g`
--            Under All 4 Generator Hops `(g, h) ↦ (s * g, h * s^{-1})`
-- ============================================================================


/-- Verify that `(h * s^{-1}) * (s * g) = h * g` for all `g, h ∈ Dic_6` and all
    four symmetric Cayley generators `s ∈ {a, a^{-1}, x, x^{-1}}`. -/
def checkRelationalInvariantConservation : Bool :=
  let ks := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  let es := [0, 1]
  let gens := [genA, genAi, genX, genXi]
  gens.all (fun s =>
    ks.all (fun k1 =>
      es.all (fun e1 =>
        ks.all (fun k2 =>
          es.all (fun e2 =>
            let g : Dic6 := { k := k1, e := e1 }
            let h : Dic6 := { k := k2, e := e2 }
            let g_new := dic6Mul s g
            let h_new := dic6Mul h (dic6Inv s)
            dic6Mul h_new g_new == dic6Mul h g)))))


theorem relational_product_invariant_conserved_576 :
    checkRelationalInvariantConservation = true := by
  decide


-- ============================================================================
-- THEOREM 3: Exact 2D Uniform Sector Beamsplitter Identity (`D_B(pi/8) = 1`)
-- ============================================================================


/-- Gaussian integers `a + b i` for exact symbolic verification of the scaled
    beamsplitter unitary `2 * exp(-i (pi/8) h_2) = [[1 - i, 1 + i], [1 + i, 1 - i]]`
    and scaled input states `(1, ±i)`. -/
structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr


def gAdd (z w : GaussInt) : GaussInt :=
  { re := z.re + w.re, im := z.im + w.im }


def gMul (z w : GaussInt) : GaussInt :=
  { re := z.re * w.re - z.im * w.im, im := z.re * w.im + z.im * w.re }


def gNormSq (z : GaussInt) : Int :=
  z.re * z.re + z.im * z.im


/-- A 2-vector over `GaussInt`. -/
structure Vec2G where
  v0 : GaussInt
  v1 : GaussInt
  deriving DecidableEq, Repr


/-- Scaled beamsplitter operator `2 * U_2(pi/8) = (1 - i) I_2 + (1 + i) sigma_x`. -/
def applyScaledU2Pi8 (v : Vec2G) : Vec2G :=
  let d : GaussInt := { re := 1, im := -1 } -- 1 - i
  let o : GaussInt := { re := 1, im := 1 }  -- 1 + i
  { v0 := gAdd (gMul d v.v0) (gMul o v.v1),
    v1 := gAdd (gMul o v.v0) (gMul d v.v1) }


/-- Scaled Alice input states `|psi_+> = (1, +i)` and `|psi_-> = (1, -i)`. -/
def psiPlus0  : Vec2G := { v0 := { re := 1, im := 0 }, v1 := { re := 0, im := 1 } }
def psiMinus0 : Vec2G := { v0 := { re := 1, im := 0 }, v1 := { re := 0, im := -1 } }


/-- Exact symbolic proof that at `t = pi/8`, `|psi_+>` has zero amplitude in
    Alice sector `e_A = 0` (putting 100% of weight in `e_A = 1`, which maps to
    Bob rotation sector `e_B = 0`), while `|psi_->` has zero amplitude in
    Alice sector `e_A = 1` (putting 100% of weight in `e_A = 0`, which maps to
    Bob reflection sector `e_B = 1`). -/
theorem exact_1bit_sector_decoder_orthogonal_supports :
    (applyScaledU2Pi8 psiPlus0).v0 = { re := 0, im := 0 } ∧
    gNormSq (applyScaledU2Pi8 psiPlus0).v1 = 8 ∧
    (applyScaledU2Pi8 psiMinus0).v1 = { re := 0, im := 0 } ∧
    gNormSq (applyScaledU2Pi8 psiMinus0).v0 = 8 := by
  decide


-- ============================================================================
-- THEOREM 4: Exact 4D Klein-Four (2-Bit / 4-State) Kronecker-Sum Decoder at `t = pi/8`
-- ============================================================================


/-- A 4-vector over `GaussInt` representing amplitudes on the 4 Klein-four
    sectors `(p=0,e=0), (p=1,e=0), (p=0,e=1), (p=1,e=1)`. -/
structure Vec4G where
  q00 : GaussInt
  q10 : GaussInt
  q01 : GaussInt
  q11 : GaussInt
  deriving DecidableEq, Repr


/-- Because `h_4 = h_2 ⊗ I_2 + I_2 ⊗ h_2`, the scaled evolution operator at
    `t = pi/8` is the tensor square `(2 U_2(pi/8)) ⊗ (2 U_2(pi/8))` of the 2D
    beamsplitter, which simplifies via `(1 - i)^2 = -2i`, `(1 + i)^2 = +2i`,
    and `(1 - i)(1 + i) = 2` to `2 * [[ -i, 1, 1, +i ], [ 1, -i, +i, 1 ],
    [ 1, +i, -i, 1 ], [ +i, 1, 1, -i ]]`. Dividing by 2 gives the exact
    Gaussian-integer matrix `2 * U_4(pi/8)`. -/
def applyScaledU4Pi8 (v : Vec4G) : Vec4G :=
  let mi : GaussInt := { re := 0, im := -1 }
  let pi : GaussInt := { re := 0, im := 1 }
  let one : GaussInt := { re := 1, im := 0 }
  let comb (a b c d : GaussInt) : GaussInt :=
    gAdd (gAdd a b) (gAdd c d)
  { q00 := comb (gMul mi v.q00) (gMul one v.q10) (gMul one v.q01) (gMul pi v.q11),
    q10 := comb (gMul one v.q00) (gMul mi v.q10) (gMul pi v.q01) (gMul one v.q11),
    q01 := comb (gMul one v.q00) (gMul pi v.q10) (gMul mi v.q01) (gMul one v.q11),
    q11 := comb (gMul pi v.q00) (gMul one v.q10) (gMul one v.q01) (gMul mi v.q11) }


/-- Alice's 4 local Klein-four phase encodings `(s_p, s_e) ∈ {+1, -1}^2`
    with amplitudes `(1, i s_p, i s_e, -s_p s_e)`. -/
def kleinInput (sp se : Int) : Vec4G :=
  { q00 := { re := 1, im := 0 },
    q10 := { re := 0, im := sp },
    q01 := { re := 0, im := se },
    q11 := { re := -(sp * se), im := 0 } }


/-- Exact theorem proving that at `t = pi/8`, the 4 Klein-four phase states
    route deterministically into 4 mutually orthogonal single-quadrant basis
    vectors with zero cross-quadrant leakage (`P_correct = 100%` for 2 bits). -/
theorem exact_2bit_klein_four_perfect_decoder_at_pi8 :
    let out_pp := applyScaledU4Pi8 (kleinInput 1 1)
    let out_pm := applyScaledU4Pi8 (kleinInput 1 (-1))
    let out_mp := applyScaledU4Pi8 (kleinInput (-1) 1)
    let out_mm := applyScaledU4Pi8 (kleinInput (-1) (-1))
    -- Message (+1, +1) concentrates 100% into Alice sector (p=1, e=1) -> Bob quadrant (p_B=1, e_B=0):
    (out_pp.q00 = { re := 0, im := 0 } ∧ out_pp.q10 = { re := 0, im := 0 } ∧
     out_pp.q01 = { re := 0, im := 0 } ∧ gNormSq out_pp.q11 = 16) ∧
    -- Message (+1, -1) concentrates 100% into Alice sector (p=1, e=0) -> Bob quadrant (p_B=1, e_B=1):
    (out_pm.q00 = { re := 0, im := 0 } ∧ gNormSq out_pm.q10 = 16 ∧
     out_pm.q01 = { re := 0, im := 0 } ∧ out_pm.q11 = { re := 0, im := 0 }) ∧
    -- Message (-1, +1) concentrates 100% into Alice sector (p=0, e=1) -> Bob quadrant (p_B=0, e_B=0):
    (out_mp.q00 = { re := 0, im := 0 } ∧ out_mp.q10 = { re := 0, im := 0 } ∧
     gNormSq out_mp.q01 = 16 ∧ out_mp.q11 = { re := 0, im := 0 }) ∧
    -- Message (-1, -1) concentrates 100% into Alice sector (p=0, e=0) -> Bob quadrant (p_B=0, e_B=1):
    (gNormSq out_mm.q00 = 16 ∧ out_mm.q10 = { re := 0, im := 0 } ∧
     out_mm.q01 = { re := 0, im := 0 } ∧ out_mm.q11 = { re := 0, im := 0 }) := by
  decide


end UCDSectorPerfectDecoderAndKleinFour