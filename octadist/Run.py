# How to run OctaDist
# 1. Stay outside octadist directory
# 2. Execute following command:
#    $ python -m octadist.Run

import octadist.main

version = octadist.__version__
release = octadist.__release__

if __name__ == '__main__':
    print(f"\nProgram Starts >>>")
    print(f"... OctaDist {version} {release} ...")

    octadist.main.main()

    print(f"<<< Program Terminated")
