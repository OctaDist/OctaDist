import octadist.main

version = octadist.__version__
release = octadist.__release__

if __name__ == '__main__':
    print(f"\nProgram Started >>>")
    print(f"... OctaDist {version} {release} ...")

    octadist.main.main()

    print(f"<<< Program Terminated")
