import argparse
from pyrosetta import *
from pyrosetta.rosetta.core.scoring.sasa import SasaCalc

def parse_arguments():
    parser = argparse.ArgumentParser(description="Find NxT and NxS motifs in a protein structure.")
    parser.add_argument("pdb_file", type=str, help="Path to the input PDB file.")
    return parser.parse_args()

init()

args = parse_arguments()

pose = pose_from_pdb(args.pdb_file)

sasa_calculator = SasaCalc()
sasa_calculator.calculate(pose)
sasa_values = sasa_calculator.get_residue_sasa()

sasa_cutoff = 10.0 #! Adjust as needed
surface_residues = [i for i, sasa in enumerate(sasa_values, start=1) if sasa > sasa_cutoff]

asn_residues = [i for i in range(1, pose.size() + 1) if pose.residue(i).name1() == "N"]

nxt_surface_motifs = []
nxs_surface_motifs = []
nxt_non_surface_motifs = []
nxs_non_surface_motifs = []

for res in asn_residues:
    if res < pose.size() - 1:
        if pose.residue(res + 2).name1() == "T":
            if res in surface_residues:
                nxt_surface_motifs.append(res)
            else:
                nxt_non_surface_motifs.append(res)

        if pose.residue(res + 2).name1() == "S":
            if res in surface_residues:
                nxs_surface_motifs.append(res)
            else:
                nxs_non_surface_motifs.append(res)

print("Surface-accessible NxT motif residues:", nxt_surface_motifs)
print("Non-surface-accessible NxT motif residues:", nxt_non_surface_motifs)
print("Surface-accessible NxS motif residues:", nxs_surface_motifs)
print("Non-surface-accessible NxS motif residues:", nxs_non_surface_motifs)

# __author__ = "Franz Dietzmeyer"
# __contact__ = "franz.dietzmeyer@medizin.uni-leipzig.de"