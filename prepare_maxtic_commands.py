import os
import sys


def prepare_maxtic_commands():

    reps = {x for x in os.listdir("./") if "Replicate" in x}
    mpath = "python /Users/davin/Desktop/GitHub/Public/DatingTools/MaxTiCRelated/MaxTiC2.py /Users/davin/Desktop/GitHub/Private/GTDBClocks/Files/MaxTiC.nwk REP"
    for rep in reps:
        print(mpath.replace("REP", rep))



if __name__ == "__main__":

    if len(sys.argv) != 1:
        print("usage: python prepare_maxtic_commands.py")
        exit(0)

    scr = sys.argv
    prepare_maxtic_commands()
