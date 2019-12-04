# xcube-gen-bc changes

## Changes

* Code adjustment to suit xarray 0.14.1. 
* Added new input processor `CMEMSInputProcessor` to read daily or hourly input data provided by CEMEMS.
* Added input processor parameter `xy_gcp_step` to configure the number of 
  ground control points when re-projecting from satellite coordinates to WGS 84. (#7)
  To use every 10th value in x and y direction of the `lon` and `lat` 2D coordinate 
  variables, specify:
  ```
    input_processor_params:
        xy_gcp_step: 10
  ```      
  For example, if `lon` and `lat` 2D coordinate variables are 2000 x 1000 pixels, 
  the total number of GCPs will be 200 x 100 = 20000.    
* Fixed problem with an input bands valid_pixel_expression, the (SNAP) band maths expressions
  `nan(x)` and `x^y`are now correctly transpiled to `isnan(x)` and `x**y`. (#2)