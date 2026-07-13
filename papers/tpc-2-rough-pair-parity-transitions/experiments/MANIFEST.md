# Production experiment manifest

This manifest records the finite data used in the paper. These calculations are descriptive diagnostics and do not support an asymptotic twin-prime claim.

## Environment

- Date: 2026-07-13
- Platform: Windows x64
- Compiler: Microsoft C/C++ Optimizing Compiler 19.38.33134
- C++ mode: C++17, `/O2`
- Python: standard library only for testing and plotting
- SVG-to-PNG renderer: Google Chrome 150.0.7871.114, headless mode

The published C++ source is also compatible with GCC and Clang. An independent small regression test was run after compilation:

```text
smoke test passed: independent counts and histograms, exact inversion, and block invariance
```

## Production commands

For each `h` in `2,6,10,30`:

```text
rough_pair_diagnostics.exe --x 100000000 --h H \
  --theta 0.34,0.36,0.38,0.40,0.42,0.44,0.46,0.48,0.49 \
  --block 4194304 --factor-bins 40 \
  --output data/rough_pair_x1e8_hH
```

The retained `h=2` SVG was generated with:

```text
python plot_diagnostics.py \
  --summary data/rough_pair_x1e8_h2_summary.csv \
  --bins data/rough_pair_x1e8_h2_factor_bins.csv \
  --theta 0.34,0.38,0.42,0.46,0.49 \
  --output ../figures/rough-pair-x1e8-h2.svg
```

The PNG embedded by LaTeX was rendered from that SVG with:

```text
chrome --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1220,1060 \
  --screenshot=../figures/rough-pair-x1e8-h2.png \
  file:///ABSOLUTE/PATH/figures/rough-pair-x1e8-h2.svg
```

All 36 production rows have exact `inversion_error=0` and `sector_sum_error=0`. The count and factor-bin fields are deterministic. The summary files also contain `elapsed_seconds`, so their whole-file hashes are machine-specific even though every mathematical field is reproducible.

## SHA-256

```text
rough_pair_x1e8_h2_factor_bins.csv   726d874325db90ec8463e1706f728fb32d9bc4b77c280bb7e7041f97792eb424
rough_pair_x1e8_h2_summary.csv       84394d315cc5c9ae68551eea092d8f1ed59590c74befba33370d7d840bca94b0
rough_pair_x1e8_h6_factor_bins.csv   43a0c742013dad141e77c73deffb5e0215284a9ce8c5b14068f9a32463c5a3d4
rough_pair_x1e8_h6_summary.csv       20ce34cb9076bdb3a9593a453177c36423472fd6736be48214ee9d2fb1d5d211
rough_pair_x1e8_h10_factor_bins.csv  a7569ea549824f64d839185c5eaf97b9a7e2369c5a84836e32b42fb3b0c397c9
rough_pair_x1e8_h10_summary.csv      0de60f9abda72a33422dc767e5abd1dd22a184548797c5f7d47c7b1ffd7c9995
rough_pair_x1e8_h30_factor_bins.csv  dcc65a91c8bd0d804728b226db003afe7d956d8c31f3065e672586e89cb8ca62
rough_pair_x1e8_h30_summary.csv      f3e6aee0b670b7832dbf34d5d86183e2e24e661447a88a7fa986c5b6362d6c79
rough-pair-x1e8-h2.svg               7e23e6940236b2c24d8e1f3a00f996f2f029bb264b08208449fb5b5da6dbb3cd
rough-pair-x1e8-h2.png               4b08ff1892a5067948b6a8a410d295b6f20372ab106a593cf5a78f21d270bcf5
rough_pair_diagnostics.cpp           eb06514bce92026474fd22743372fd56d3bad20371e3a5f77d2073ba712da8e5
plot_diagnostics.py                  9cb016db51c838e08447302979d717dc59a258039a2ad615b62cca2f6e466c50
smoke_test.py                        7aa6e8f95aeeda49591f9bd31ea3836114b29bd3fe1dce28bb0cd46978ac83b6
```
