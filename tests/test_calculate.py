import importlib.util
import math
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"skills/shi-metal-materials-heat-treatment/scripts/calculate.py"
spec=importlib.util.spec_from_file_location("calculate",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Calculations(unittest.TestCase):
    def test_lever_conservation(self):
        for a,b in [(0,100),(.02,.77),(15,95),(.77,6.69)]:
            for t in [0,.1,.5,.9,1]:
                c=a+(b-a)*t;r=m.lever(c,a,b)
                self.assertAlmostEqual(r["left_fraction"]+r["right_fraction"],1)
                self.assertAlmostEqual(r["reconstructed_composition"],c)
                self.assertAlmostEqual(r["right_fraction"],t)
    def test_invalid_tie_lines(self):
        for vals in [(30,40,50),(50,15,15),(20,90,10),(math.nan,0,100)]:
            with self.assertRaises(ValueError):m.lever(*vals)
    def test_eutectic_book_example(self):
        overall=m.lever(50,15,95)
        initial=m.lever(50,15,75)
        eut=m.lever(75,15,95)
        self.assertAlmostEqual(overall["left_fraction"],.5625)
        self.assertAlmostEqual(initial["left_fraction"]+initial["right_fraction"]*eut["left_fraction"],.5625)
    def test_fcc_units_and_volume_scaling(self):
        r=m.fcc_atoms(.256)
        self.assertAlmostEqual(r["lattice_parameter_nm"],.36203867196751236)
        self.assertAlmostEqual(m.fcc_atoms(.256,2)["atoms"]/r["atoms"],2)
        self.assertTrue(8e19<r["atoms"]<9e19)
        with self.assertRaises(ValueError):m.fcc_atoms(0)
    def test_kelvin_conversion(self):
        self.assertAlmostEqual(m.recrystallization(1083)["estimate_c"],269.31)
        self.assertNotAlmostEqual(m.recrystallization(1083)["estimate_c"],.4*1083)
        with self.assertRaises(ValueError):m.recrystallization(-274)

if __name__=="__main__":unittest.main()
