import os

reps = {x for x in os.listdir("./") if "Replicate" in x}
mpath = "python /Users/aadavin/Desktop/Brisbane/LGT_DATING/Scripts/MaxTiC2.py SpeciesTreeMapped.nwk REP"
for rep in reps:
    print(mpath.replace("REP", rep))


