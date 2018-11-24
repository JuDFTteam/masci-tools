import os

from studenproject18ws.model.reader import Reader
from studenproject18ws.control.plotter import Plotter


def main():
    print("Hiiiiiiiiiiiiiiiiiiiii hdf!!!")

    # filename = 'banddos_4x4.hdf'
    filename = 'banddos.hdf'
    # filename = 'banddos_Co.hdf'
    filepath = os.path.join("input", filename)
    data = Reader(filepath)

    with data as h5file:
        data.read()
        plotter = Plotter(data)
        output_dir = os.path.join(os.getcwd(), "output")
        print(f"Saving plots to {output_dir}")
        plotter.plot_to_files(output_dir)


if __name__ == '__main__':
    main() # if run as script
else:
    main() # if run as module
