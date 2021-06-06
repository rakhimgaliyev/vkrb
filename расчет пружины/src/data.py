array_of_delta_sp_inch = [
    0.363 / 2,
    0.251 / 2,
    0.363 / 2,
    0.256 / 2,
    0.355 / 2,
    0.344 / 2,
    0.284 / 2,
    0.414 / 2,
    0.332 / 2,
    0.360 / 2,
    0.382 / 2,
    0.312 / 2,
    0.532 / 2,
    0.442 / 2,
    0.483 / 2,
    0.424 / 2,
    0.456 / 2,
]

array_of_delta_sp = []

for delta_sp in array_of_delta_sp_inch:
    array_of_delta_sp.append(delta_sp * 25.4 * 10**(-3))

# число опорных витков
array_of_i_p_sp = [2, 3, 4, 5, 6, 7, 8]
