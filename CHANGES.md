# xcube-gen-bc changes

## Changes

* Fixed problem with an input bands valid_pixel_expression, the (SNAP) band maths expressions
  `nan(x)` and `x^y`are now correctly transpiled to `isnan(x)` and `x**y`. (#2)