#!/usr/bin/env python

# smoothing.py - Smoothing filter operations on pixel arrays in 2D
#
# Copyright (C) 2020 Martin Urschler <martin.urschler@auckland.ac.nz>
#
# Original concept by Martin Urschler.
#
# LICENCE (MIT)
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import imageProcessing.utilities as IPUtils
import imageProcessing.convolve2D as IPConv2D



def computeGaussianAveraging3x3(pixel_array, image_width, image_height):

    # sigma is 3 pixels
    smoothing_3tap = [0.27901, 0.44198, 0.27901]

    averaged = IPConv2D.computeSeparableConvolution2DOddNTapBorderZero(pixel_array, image_width, image_height, smoothing_3tap)

    return averaged

def computeGaussianAveraging5x5(pixel_array, image_width, image_height):

    # sigma is 3 pixels
    smoothing_3tap = [0.06136, 0.24477, 0.38774, 0.24477, 0.06136]

    averaged = IPConv2D.computeSeparableConvolution2DOddNTapBorderZero(pixel_array, image_width, image_height, smoothing_3tap)

    return averaged

def computeGaussianAveraging7x7(pixel_array, image_width, image_height):

    # sigma is 3 pixels
    smoothing_3tap = [0.00598,0.060626,0.241843,0.383103,0.241843,0.060626,0.00598]

    averaged = IPConv2D.computeSeparableConvolution2DOddNTapBorderZero(pixel_array, image_width, image_height, smoothing_3tap)

    return averaged

def computeGaussianAveraging9x9(pixel_array, image_width, image_height):

    # sigma is 3 pixels
    smoothing_3tap = [0.000229,0.005977,0.060598,0.241732,0.382928,0.241732,0.060598,0.005977,0.000229]

    averaged = IPConv2D.computeSeparableConvolution2DOddNTapBorderZero(pixel_array, image_width, image_height, smoothing_3tap)

    return averaged

def computeGaussianAveraging(pixel_array, image_width, image_height, filter_size):
    if filter_size == 3:
        return computeGaussianAveraging3x3(pixel_array, image_width, image_height)
    elif filter_size == 5:
        return computeGaussianAveraging5x5(pixel_array, image_width, image_height)
    elif filter_size == 7:
        return computeGaussianAveraging7x7(pixel_array, image_width, image_height)
    elif filter_size == 9:
        return computeGaussianAveraging9x9(pixel_array, image_width, image_height)
    
    return null