import os

import deprecated  # pip install deprecated

from studenproject18ws.tmp.plotter import Plotter
from studenproject18ws.tmp.reader import Reader


@deprecated
def main():
    print("Hiiiiiiiiiiiiiiiiiiiii hdf!!!")

    # filename = 'banddos_4x4.hdf'
    filename = 'banddos.hdf'
    # filename = 'banddos_Co.hdf'

    filepath = ['data','input', filename]
    filepath = os.path.join(*filepath)
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
