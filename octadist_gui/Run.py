import octadist_gui.main

version = octadist_gui.__version__
revision = octadist_gui.__release__

if __name__ == '__main__':
    print(f"\nProgram Started >>>")
    print(f"... OctaDist {version} {revision} ...")

    octadist_gui.main.main()

    print(f"<<< Program Terminated")
