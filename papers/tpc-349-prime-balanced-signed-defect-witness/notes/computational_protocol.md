# TPC-349 computational protocol

* Parent producer: TPC-348 code SHA256
  `fe29f0adeea6234c637a479ba2447068a1e6b1c91731761ed2d2af73464d20b8`.
* Parent certificate SHA256
  `5f0b1cb66431f6a57fa97335808f30fdbe86ffc0b31ce074d7a1dbbdc692a294`.
* Origins: `40097, 48097`.
* Counts: `256, 512, 1024`.
* Shell anchors: `24, 36, 54, 80`.
* Exponents: `1, 2`; height: `66`.
* Source sign laws: `all_plus`, `alternating_index`, `mod4_character`,
  `half_split`.
* Rows: `2*3*4*2*4=192`.
* Balanced vector: all shell incidences with the declared zero-sum beta split.
* Baseline: TPC-348 best mask-hit coordinate column, used only for comparison.
* Independent replay reverses shell accumulation and uses relative tolerance for
  floating matrix norms; exact anchor arithmetic uses `Fraction`.
