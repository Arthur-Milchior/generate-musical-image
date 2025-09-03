import unittest
from lily.svg import *
from lily.svg import *


class TestSvg(unittest.TestCase):
    example_no_xlink = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.2" width="67.79mm" height="15.02mm" viewBox="8.5358 -0.0000 38.5749 8.5450">
<style text="style/css">
<![CDATA[
tspan { white-space: pre; }
]]>
</style>
<line transform="translate(8.5358, 6.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 5.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 4.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 3.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 2.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<rect transform="translate(0.0000, 7.0000)" x="27.0443" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="24.0421" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 8.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(33.6249, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.000h0" fill="currentColor"/>
<rect transform="translate(46.9208, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.0000" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(38.1640, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(38.2290, 4.0000)" x="-0.0650" y="-1.3139" width="0.1300" height="5.6472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(34.7149, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(35.9541, 4.0000)" x="-0.0650" y="-4.0000" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(34.7149, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(34.7149, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(44.2335, 4.0000)" x="-0.0650" y="-2.3139" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(44.1685, 1.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(41.2312, 4.0000)" x="-0.0650" y="-1.8139" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(41.1662, 2.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(34.7149, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 7.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(22.6051, 4.0000)" x="-0.0650" y="-2.5000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<path transform="translate(17.6659, 4.0000) scale(0.0040, -0.0040)" d="M359 27c-49 0 -75 42 -75 75c0 38 27 77 72 77c4 0 9 0 14 -1c-28 37 -72 59 -120 59c-106 0 -113 -73 -113 -186v-51v-51c0 -113 7 -187 113 -187c80 0 139 70 158 151c2 7 7 10 12 10c6 0 13 -4 13 -12c0 -94 -105 -174 -183 -174c-68 0 -137 21 -184 70
c-49 51 -66 122 -66 193s17 142 66 193c47 49 116 69 184 69c87 0 160 -63 175 -149c1 -5 1 -10 1 -14c0 -40 -30 -72 -67 -72z" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(12.9558, 4.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(13.8759, 2.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(14.7959, 4.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(15.7159, 3.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
</a>
<path transform="translate(9.3358, 5.0000) scale(0.0040, -0.0040)" d="M266 -635h-6c-108 0 -195 88 -195 197c0 58 53 103 112 103c54 0 95 -47 95 -103c0 -52 -43 -95 -95 -95c-11 0 -21 2 -31 6c26 -39 68 -65 117 -65h4zM461 -203c68 24 113 95 113 164c0 90 -66 179 -173 190c24 -116 46 -231 60 -354zM74 28c0 -135 129 -247 264 -247
c28 0 55 2 82 6c-14 127 -37 245 -63 364c-79 -8 -124 -61 -124 -119c0 -44 25 -91 81 -123c5 -5 7 -10 7 -15c0 -11 -10 -22 -22 -22c-3 0 -6 1 -9 2c-80 43 -117 115 -117 185c0 88 58 174 160 197c-14 58 -29 117 -46 175c-107 -121 -213 -243 -213 -403zM335 -262
c-188 0 -333 172 -333 374c0 177 131 306 248 441c-19 62 -37 125 -45 190c-6 52 -7 104 -7 156c0 115 55 224 149 292c6 5 14 5 20 0c71 -84 133 -245 133 -358c0 -143 -86 -255 -180 -364c21 -68 39 -138 56 -207c4 0 9 1 13 1c155 0 256 -128 256 -261
c0 -76 -33 -154 -107 -210c-22 -17 -47 -28 -73 -36c3 -35 5 -70 5 -105c0 -19 -1 -39 -2 -58c-7 -119 -88 -225 -202 -228l1 43c93 2 153 92 159 191c1 18 2 37 2 55c0 31 -1 61 -4 92c-29 -5 -58 -8 -89 -8zM428 916c0 55 -4 79 -20 129c-99 -48 -162 -149 -162 -259
c0 -74 18 -133 36 -194c80 97 146 198 146 324z" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(21.3659, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 8.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(25.6073, 4.0000)" x="-0.0650" y="-3.0000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<rect transform="translate(31.6119, 4.0000)" x="-0.0650" y="-3.6667" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(30.3726, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(28.6096, 4.0000)" x="-0.0650" y="-3.3333" width="0.1300" height="6.1472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(27.3704, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
</svg>"""

    example_input = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.2" width="67.79mm" height="15.02mm" viewBox="8.5358 -0.0000 38.5749 8.5450">
<style text="style/css">
<![CDATA[
tspan { white-space: pre; }
]]>
</style>
<line transform="translate(8.5358, 6.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 5.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 4.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 3.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 2.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<rect transform="translate(0.0000, 7.0000)" x="27.0443" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="24.0421" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 8.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(33.6249, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.000h0" fill="currentColor"/>
<rect transform="translate(46.9208, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.0000" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:37:6:7">
<path transform="translate(38.1640, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:38:6:7">
<path transform="translate(38.1640, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:39:6:7">
<path transform="translate(38.1640, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:40:6:7">
<path transform="translate(38.1640, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(38.2290, 4.0000)" x="-0.0650" y="-1.3139" width="0.1300" height="5.6472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:33:6:7">
<path transform="translate(34.7149, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(35.9541, 4.0000)" x="-0.0650" y="-4.0000" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:35:6:7">
<path transform="translate(34.7149, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:34:6:7">
<path transform="translate(34.7149, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(44.2335, 4.0000)" x="-0.0650" y="-2.3139" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:50:6:7">
<path transform="translate(44.1685, 1.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:49:6:7">
<path transform="translate(44.1685, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:48:6:7">
<path transform="translate(44.1685, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:47:6:7">
<path transform="translate(44.1685, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(41.2312, 4.0000)" x="-0.0650" y="-1.8139" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:45:6:7">
<path transform="translate(41.1662, 2.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:44:6:7">
<path transform="translate(41.1662, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:43:6:7">
<path transform="translate(41.1662, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:42:6:7">
<path transform="translate(41.1662, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:19:6:7">
<path transform="translate(24.3681, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:32:6:7">
<path transform="translate(34.7149, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:17:6:7">
<path transform="translate(24.3681, 7.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:18:6:7">
<path transform="translate(24.3681, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(22.6051, 4.0000)" x="-0.0650" y="-2.5000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<path transform="translate(17.6659, 4.0000) scale(0.0040, -0.0040)" d="M359 27c-49 0 -75 42 -75 75c0 38 27 77 72 77c4 0 9 0 14 -1c-28 37 -72 59 -120 59c-106 0 -113 -73 -113 -186v-51v-51c0 -113 7 -187 113 -187c80 0 139 70 158 151c2 7 7 10 12 10c6 0 13 -4 13 -12c0 -94 -105 -174 -183 -174c-68 0 -137 21 -184 70
c-49 51 -66 122 -66 193s17 142 66 193c47 49 116 69 184 69c87 0 160 -63 175 -149c1 -5 1 -10 1 -14c0 -40 -30 -72 -67 -72z" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:10:4:5">
<path transform="translate(12.9558, 4.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(13.8759, 2.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(14.7959, 4.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(15.7159, 3.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
</a>
<path transform="translate(9.3358, 5.0000) scale(0.0040, -0.0040)" d="M266 -635h-6c-108 0 -195 88 -195 197c0 58 53 103 112 103c54 0 95 -47 95 -103c0 -52 -43 -95 -95 -95c-11 0 -21 2 -31 6c26 -39 68 -65 117 -65h4zM461 -203c68 24 113 95 113 164c0 90 -66 179 -173 190c24 -116 46 -231 60 -354zM74 28c0 -135 129 -247 264 -247
c28 0 55 2 82 6c-14 127 -37 245 -63 364c-79 -8 -124 -61 -124 -119c0 -44 25 -91 81 -123c5 -5 7 -10 7 -15c0 -11 -10 -22 -22 -22c-3 0 -6 1 -9 2c-80 43 -117 115 -117 185c0 88 58 174 160 197c-14 58 -29 117 -46 175c-107 -121 -213 -243 -213 -403zM335 -262
c-188 0 -333 172 -333 374c0 177 131 306 248 441c-19 62 -37 125 -45 190c-6 52 -7 104 -7 156c0 115 55 224 149 292c6 5 14 5 20 0c71 -84 133 -245 133 -358c0 -143 -86 -255 -180 -364c21 -68 39 -138 56 -207c4 0 9 1 13 1c155 0 256 -128 256 -261
c0 -76 -33 -154 -107 -210c-22 -17 -47 -28 -73 -36c3 -35 5 -70 5 -105c0 -19 -1 -39 -2 -58c-7 -119 -88 -225 -202 -228l1 43c93 2 153 92 159 191c1 18 2 37 2 55c0 31 -1 61 -4 92c-29 -5 -58 -8 -89 -8zM428 916c0 55 -4 79 -20 129c-99 -48 -162 -149 -162 -259
c0 -74 18 -133 36 -194c80 97 146 198 146 324z" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:15:6:7">
<path transform="translate(21.3659, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:14:6:7">
<path transform="translate(21.3659, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:13:6:7">
<path transform="translate(21.3659, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:12:6:7">
<path transform="translate(21.3659, 8.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(25.6073, 4.0000)" x="-0.0650" y="-3.0000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<rect transform="translate(31.6119, 4.0000)" x="-0.0650" y="-3.6667" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:30:6:7">
<path transform="translate(30.3726, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:29:6:7">
<path transform="translate(30.3726, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:28:6:7">
<path transform="translate(30.3726, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:27:6:7">
<path transform="translate(30.3726, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(28.6096, 4.0000)" x="-0.0650" y="-3.3333" width="0.1300" height="6.1472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:24:6:7">
<path transform="translate(27.3704, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:20:6:7">
<path transform="translate(24.3681, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:22:6:7">
<path transform="translate(27.3704, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:23:6:7">
<path transform="translate(27.3704, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:25:6:7">
<path transform="translate(27.3704, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
</svg>"""

    expected = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.2" width="67.79mm" height="15.02mm" viewBox="8.5358 -0.0000 38.5749 8.5450">
<style text="style/css">
<![CDATA[
tspan { white-space: pre; }
]]>
</style>
<rect x="8.5358" width="38.5749" y="-0.0000" height="8.5450" fill="white"/>
<line transform="translate(8.5358, 6.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 5.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 4.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 3.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 2.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<rect transform="translate(0.0000, 7.0000)" x="27.0443" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="24.0421" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 8.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(33.6249, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.000h0" fill="currentColor"/>
<rect transform="translate(46.9208, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.0000" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:37:6:7">
<path transform="translate(38.1640, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:38:6:7">
<path transform="translate(38.1640, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:39:6:7">
<path transform="translate(38.1640, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:40:6:7">
<path transform="translate(38.1640, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(38.2290, 4.0000)" x="-0.0650" y="-1.3139" width="0.1300" height="5.6472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:33:6:7">
<path transform="translate(34.7149, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(35.9541, 4.0000)" x="-0.0650" y="-4.0000" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:35:6:7">
<path transform="translate(34.7149, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:34:6:7">
<path transform="translate(34.7149, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(44.2335, 4.0000)" x="-0.0650" y="-2.3139" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:50:6:7">
<path transform="translate(44.1685, 1.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:49:6:7">
<path transform="translate(44.1685, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:48:6:7">
<path transform="translate(44.1685, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:47:6:7">
<path transform="translate(44.1685, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(41.2312, 4.0000)" x="-0.0650" y="-1.8139" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:45:6:7">
<path transform="translate(41.1662, 2.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:44:6:7">
<path transform="translate(41.1662, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:43:6:7">
<path transform="translate(41.1662, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:42:6:7">
<path transform="translate(41.1662, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:19:6:7">
<path transform="translate(24.3681, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:32:6:7">
<path transform="translate(34.7149, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:17:6:7">
<path transform="translate(24.3681, 7.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:18:6:7">
<path transform="translate(24.3681, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(22.6051, 4.0000)" x="-0.0650" y="-2.5000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<path transform="translate(17.6659, 4.0000) scale(0.0040, -0.0040)" d="M359 27c-49 0 -75 42 -75 75c0 38 27 77 72 77c4 0 9 0 14 -1c-28 37 -72 59 -120 59c-106 0 -113 -73 -113 -186v-51v-51c0 -113 7 -187 113 -187c80 0 139 70 158 151c2 7 7 10 12 10c6 0 13 -4 13 -12c0 -94 -105 -174 -183 -174c-68 0 -137 21 -184 70
c-49 51 -66 122 -66 193s17 142 66 193c47 49 116 69 184 69c87 0 160 -63 175 -149c1 -5 1 -10 1 -14c0 -40 -30 -72 -67 -72z" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:10:4:5">
<path transform="translate(12.9558, 4.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(13.8759, 2.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(14.7959, 4.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(15.7159, 3.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
</a>
<path transform="translate(9.3358, 5.0000) scale(0.0040, -0.0040)" d="M266 -635h-6c-108 0 -195 88 -195 197c0 58 53 103 112 103c54 0 95 -47 95 -103c0 -52 -43 -95 -95 -95c-11 0 -21 2 -31 6c26 -39 68 -65 117 -65h4zM461 -203c68 24 113 95 113 164c0 90 -66 179 -173 190c24 -116 46 -231 60 -354zM74 28c0 -135 129 -247 264 -247
c28 0 55 2 82 6c-14 127 -37 245 -63 364c-79 -8 -124 -61 -124 -119c0 -44 25 -91 81 -123c5 -5 7 -10 7 -15c0 -11 -10 -22 -22 -22c-3 0 -6 1 -9 2c-80 43 -117 115 -117 185c0 88 58 174 160 197c-14 58 -29 117 -46 175c-107 -121 -213 -243 -213 -403zM335 -262
c-188 0 -333 172 -333 374c0 177 131 306 248 441c-19 62 -37 125 -45 190c-6 52 -7 104 -7 156c0 115 55 224 149 292c6 5 14 5 20 0c71 -84 133 -245 133 -358c0 -143 -86 -255 -180 -364c21 -68 39 -138 56 -207c4 0 9 1 13 1c155 0 256 -128 256 -261
c0 -76 -33 -154 -107 -210c-22 -17 -47 -28 -73 -36c3 -35 5 -70 5 -105c0 -19 -1 -39 -2 -58c-7 -119 -88 -225 -202 -228l1 43c93 2 153 92 159 191c1 18 2 37 2 55c0 31 -1 61 -4 92c-29 -5 -58 -8 -89 -8zM428 916c0 55 -4 79 -20 129c-99 -48 -162 -149 -162 -259
c0 -74 18 -133 36 -194c80 97 146 198 146 324z" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:15:6:7">
<path transform="translate(21.3659, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:14:6:7">
<path transform="translate(21.3659, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:13:6:7">
<path transform="translate(21.3659, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:12:6:7">
<path transform="translate(21.3659, 8.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(25.6073, 4.0000)" x="-0.0650" y="-3.0000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<rect transform="translate(31.6119, 4.0000)" x="-0.0650" y="-3.6667" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:30:6:7">
<path transform="translate(30.3726, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:29:6:7">
<path transform="translate(30.3726, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:28:6:7">
<path transform="translate(30.3726, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:27:6:7">
<path transform="translate(30.3726, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(28.6096, 4.0000)" x="-0.0650" y="-3.3333" width="0.1300" height="6.1472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:24:6:7">
<path transform="translate(27.3704, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:20:6:7">
<path transform="translate(24.3681, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:22:6:7">
<path transform="translate(27.3704, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:23:6:7">
<path transform="translate(27.3704, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;" xlink:href="textedit:{generate_root_folder}/piano/chord_successions/../{generate_root_folder}/piano/chord_successions/seventh_in_Aflat_.ly:25:6:7">
<path transform="translate(27.3704, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
</svg>"""

    expected_clean = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.2" width="67.79mm" height="15.02mm" viewBox="8.5358 -0.0000 38.5749 8.5450">
<style text="style/css">
<![CDATA[
tspan { white-space: pre; }
]]>
</style>
<rect x="8.5358" width="38.5749" y="-0.0000" height="8.5450" fill="white"/>
<line transform="translate(8.5358, 6.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 5.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 4.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 3.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<line transform="translate(8.5358, 2.0000)" stroke-linejoin="round" stroke-linecap="round" stroke-width="0.1000" stroke="currentColor" x1="0.0500" y1="-0.0000" x2="38.5249" y2="-0.0000"/>
<rect transform="translate(0.0000, 7.0000)" x="27.0443" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="24.0421" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 7.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(0.0000, 8.0000)" x="21.0398" y="-0.1000" width="1.9563" height="0.2000" ry="0.1000" fill="currentColor"/>
<rect transform="translate(33.6249, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.000h0" fill="currentColor"/>
<rect transform="translate(46.9208, 4.0000)" x="0.0000" y="-2.0000" width="0.1900" height="4.0000" ry="0.0000" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(38.1640, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(38.1640, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(38.2290, 4.0000)" x="-0.0650" y="-1.3139" width="0.1300" height="5.6472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(34.7149, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(35.9541, 4.0000)" x="-0.0650" y="-4.0000" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(34.7149, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(34.7149, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(44.2335, 4.0000)" x="-0.0650" y="-2.3139" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(44.1685, 1.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 2.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(44.1685, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(41.2312, 4.0000)" x="-0.0650" y="-1.8139" width="0.1300" height="5.8139" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(41.1662, 2.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 3.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(41.1662, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(34.7149, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 7.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(22.6051, 4.0000)" x="-0.0650" y="-2.5000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<path transform="translate(17.6659, 4.0000) scale(0.0040, -0.0040)" d="M359 27c-49 0 -75 42 -75 75c0 38 27 77 72 77c4 0 9 0 14 -1c-28 37 -72 59 -120 59c-106 0 -113 -73 -113 -186v-51v-51c0 -113 7 -187 113 -187c80 0 139 70 158 151c2 7 7 10 12 10c6 0 13 -4 13 -12c0 -94 -105 -174 -183 -174c-68 0 -137 21 -184 70
c-49 51 -66 122 -66 193s17 142 66 193c47 49 116 69 184 69c87 0 160 -63 175 -149c1 -5 1 -10 1 -14c0 -40 -30 -72 -67 -72z" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(12.9558, 4.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(13.8759, 2.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(14.7959, 4.5000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
<path transform="translate(15.7159, 3.0000) scale(0.0040, -0.0040)" d="M27 41l-1 -66v-11c0 -22 1 -44 4 -66c45 38 93 80 93 139c0 33 -14 67 -43 67c-31 0 -52 -30 -53 -63zM-15 -138l-12 595c8 5 18 8 27 8s19 -3 27 -8l-7 -345c25 21 58 34 91 34c52 0 89 -48 89 -102c0 -80 -86 -117 -147 -169c-15 -13 -24 -38 -45 -38
c-13 0 -23 11 -23 25z" fill="currentColor"/>
</a>
<path transform="translate(9.3358, 5.0000) scale(0.0040, -0.0040)" d="M266 -635h-6c-108 0 -195 88 -195 197c0 58 53 103 112 103c54 0 95 -47 95 -103c0 -52 -43 -95 -95 -95c-11 0 -21 2 -31 6c26 -39 68 -65 117 -65h4zM461 -203c68 24 113 95 113 164c0 90 -66 179 -173 190c24 -116 46 -231 60 -354zM74 28c0 -135 129 -247 264 -247
c28 0 55 2 82 6c-14 127 -37 245 -63 364c-79 -8 -124 -61 -124 -119c0 -44 25 -91 81 -123c5 -5 7 -10 7 -15c0 -11 -10 -22 -22 -22c-3 0 -6 1 -9 2c-80 43 -117 115 -117 185c0 88 58 174 160 197c-14 58 -29 117 -46 175c-107 -121 -213 -243 -213 -403zM335 -262
c-188 0 -333 172 -333 374c0 177 131 306 248 441c-19 62 -37 125 -45 190c-6 52 -7 104 -7 156c0 115 55 224 149 292c6 5 14 5 20 0c71 -84 133 -245 133 -358c0 -143 -86 -255 -180 -364c21 -68 39 -138 56 -207c4 0 9 1 13 1c155 0 256 -128 256 -261
c0 -76 -33 -154 -107 -210c-22 -17 -47 -28 -73 -36c3 -35 5 -70 5 -105c0 -19 -1 -39 -2 -58c-7 -119 -88 -225 -202 -228l1 43c93 2 153 92 159 191c1 18 2 37 2 55c0 31 -1 61 -4 92c-29 -5 -58 -8 -89 -8zM428 916c0 55 -4 79 -20 129c-99 -48 -162 -149 -162 -259
c0 -74 18 -133 36 -194c80 97 146 198 146 324z" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(21.3659, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(21.3659, 8.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(25.6073, 4.0000)" x="-0.0650" y="-3.0000" width="0.1300" height="6.3139" ry="0.0400" fill="currentColor"/>
<rect transform="translate(31.6119, 4.0000)" x="-0.0650" y="-3.6667" width="0.1300" height="5.9806" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(30.3726, 3.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 5.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(30.3726, 6.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<rect transform="translate(28.6096, 4.0000)" x="-0.0650" y="-3.3333" width="0.1300" height="6.1472" ry="0.0400" fill="currentColor"/>
<a style="color:inherit;">
<path transform="translate(27.3704, 5.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(24.3681, 4.5000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 7.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 6.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
<a style="color:inherit;">
<path transform="translate(27.3704, 4.0000) scale(0.0040, -0.0040)" d="M218 136c55 0 108 -28 108 -89c0 -71 -55 -121 -102 -149c-35 -21 -75 -34 -116 -34c-55 0 -108 28 -108 89c0 71 55 121 102 149c35 21 75 34 116 34z" fill="currentColor"/>
</a>
</svg>"""

    maxDiff = None

    def test_remove_xlink(self):
        self.assertEqual(remove_xlink(self.example_input), self.example_no_xlink)

    def test_rect(self):
        self.assertEqual(rect(self.example_input, "white"), """<rect x="8.5358" width="38.5749" y="-0.0000" height="8.5450" fill="white"/>""")

    def test_add_background(self):
        self.assertEqual(add_background(self.example_input, "white"), self.expected)

    example_input_path = "example.svg"
    example_output_path = "example_output.svg"

    def test_file(self):
        with open(self.example_input_path, "w") as f:
            f.write(self.example_input)
        clean_svg(self.example_input_path, self.example_output_path, "white")
        with open(self.example_output_path, "r") as f:
            self.assertEqual(f.read(), self.expected_clean)
        display_svg_file(self.example_output_path)
