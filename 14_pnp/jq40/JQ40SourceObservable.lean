import Lean

/-! UCD JQ40: finite source-observable pairing and character cancellation.
No sorry, admit, or auxiliary axioms. -/

namespace UCDJQ40
def sign (b : Bool) : Int := if b then -1 else 1
def zeroIndicator (b : Bool) : Nat := if b then 0 else 1
def oneIndicator (b : Bool) : Nat := if b then 1 else 0

theorem sign_pair_cancels (b : Bool) : sign b + sign (!b) = 0 := by
  cases b <;> decide

theorem complementary_zero_count (b : Bool) :
    zeroIndicator b + zeroIndicator (!b) = 1 := by
  cases b <;> decide

theorem complementary_one_count (b : Bool) :
    oneIndicator b + oneIndicator (!b) = 1 := by
  cases b <;> decide

def pairedSign {alpha : Type} (xs : List alpha)
    (observe : alpha -> Bool) (shift : alpha -> alpha) : Int :=
  match xs with
  | [] => 0
  | x :: more => sign (observe x) + sign (observe (shift x)) +
      pairedSign more observe shift

def pairedZeros {alpha : Type} (xs : List alpha)
    (observe : alpha -> Bool) (shift : alpha -> alpha) : Nat :=
  match xs with
  | [] => 0
  | x :: more => zeroIndicator (observe x) +
      zeroIndicator (observe (shift x)) + pairedZeros more observe shift

def pairedOnes {alpha : Type} (xs : List alpha)
    (observe : alpha -> Bool) (shift : alpha -> alpha) : Nat :=
  match xs with
  | [] => 0
  | x :: more => oneIndicator (observe x) +
      oneIndicator (observe (shift x)) + pairedOnes more observe shift

theorem signed_fiber_cancellation {alpha : Type} (xs : List alpha)
    (observe : alpha -> Bool) (shift : alpha -> alpha)
    (hflip : forall x, observe (shift x) = !(observe x)) :
    pairedSign xs observe shift = 0 := by
  induction xs with
  | nil => rfl
  | cons x more ih =>
      simp [pairedSign, hflip x, sign_pair_cancels, ih]

theorem paired_zero_one_counts {alpha : Type} (xs : List alpha)
    (observe : alpha -> Bool) (shift : alpha -> alpha)
    (hflip : forall x, observe (shift x) = !(observe x)) :
    pairedZeros xs observe shift = pairedOnes xs observe shift := by
  induction xs with
  | nil => rfl
  | cons x more ih =>
      simp [pairedZeros, pairedOnes, hflip x,
        complementary_zero_count, complementary_one_count, ih]

theorem bit_translation_involution (x k : Bool) :
    Bool.xor (Bool.xor x k) k = x := by
  cases x <;> cases k <;> decide

theorem bit_observation_transport (x k : Bool) :
    Bool.xor x k = (if k then !x else x) := by
  cases x <;> cases k <;> decide

end UCDJQ40
