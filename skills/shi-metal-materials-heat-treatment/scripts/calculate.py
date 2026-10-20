"""Small, dependency-free teaching calculations. Concentrations share one basis."""
import argparse
import json
import math
import sys


def finite(*values):
    if not all(math.isfinite(x) for x in values):
        raise ValueError("Inputs must be finite")


def lever(c0, left, right):
    finite(c0, left, right)
    if not 0 <= left < right <= 100:
        raise ValueError("Use percent concentrations with 0 <= left < right <= 100")
    if not left <= c0 <= right:
        raise ValueError("Overall composition lies outside the specified two-phase tie line")
    wleft = (right-c0)/(right-left)
    wright = (c0-left)/(right-left)
    return dict(left_fraction=wleft, right_fraction=wright,
                reconstructed_composition=wleft*left+wright*right,
                concentration_basis="percent; both endpoints at the same temperature")


def fcc_atoms(diameter_nm, volume_mm3=1.0):
    finite(diameter_nm, volume_mm3)
    if diameter_nm <= 0 or volume_mm3 <= 0:
        raise ValueError("Diameter and volume must be positive")
    a = math.sqrt(2)*diameter_nm
    return dict(lattice_parameter_nm=a, atoms=4*volume_mm3*1e18/a**3,
                assumptions="ideal FCC; 4 atoms per conventional cell; no porosity or expansion")


def recrystallization(melting_c, coefficient=0.4):
    finite(melting_c, coefficient)
    if melting_c <= -273.15 or not 0 < coefficient < 1:
        raise ValueError("Melting point must exceed absolute zero and 0 < coefficient < 1")
    return dict(estimate_c=coefficient*(melting_c+273.15)-273.15,
                status="rough estimate; not a furnace process instruction")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="operation", required=True)
    a=sub.add_parser("lever");a.add_argument("--c0",type=float,required=True);a.add_argument("--left",type=float,required=True);a.add_argument("--right",type=float,required=True)
    a=sub.add_parser("fcc");a.add_argument("--diameter-nm",type=float,required=True);a.add_argument("--volume-mm3",type=float,default=1)
    a=sub.add_parser("recrystallization");a.add_argument("--melting-c",type=float,required=True);a.add_argument("--coefficient",type=float,default=.4)
    args=p.parse_args()
    try:
        if args.operation=="lever":result=lever(args.c0,args.left,args.right)
        elif args.operation=="fcc":result=fcc_atoms(args.diameter_nm,args.volume_mm3)
        else:result=recrystallization(args.melting_c,args.coefficient)
    except ValueError as error:p.error(str(error))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":main()
