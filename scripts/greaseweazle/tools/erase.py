# greaseweazle/tools/erase.py
#
# Greaseweazle control script: Erase a Disk.
#
# Written & released by Keir Fraser <keir.xen@gmail.com>
#
# This is free and unencumbered software released into the public domain.
# See the file COPYING for more details, or visit <http://unlicense.org>.

description = "Erase a disk."

import sys

from greaseweazle.tools import util
from greaseweazle import usb as USB

def erase(usb, args):

    # @drive_ticks is the time in Greaseweazle ticks between index pulses.
    # We will adjust the flux intervals per track to allow for this.
    flux = usb.read_track(2)
    drive_ticks = (flux.index_list[0] + flux.index_list[1]) / 2
    del flux

    for cyl in range(args.tracks.cyl[0], args.tracks.cyl[1]+1):
        for side in range(args.tracks.side[0], args.tracks.side[1]+1):
            print("\rErasing Track %u.%u..." % (cyl, side), end="")
            usb.seek((cyl, cyl*2)[args.tracks.double_step], side)
            usb.erase_track(drive_ticks * 1.1)

    print()


def main(argv):

    parser = util.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument("--device", help="greaseweazle device name")
    parser.add_argument("--drive", type=util.drive_letter, default='A',
                        help="drive to write (A,B,0,1,2)")
    parser.add_argument("--tracks", type=util.trackset,
                        default='c=0-81:s=0-1',
                        help="which tracks to read")
    parser.description = description
    parser.prog += ' ' + argv[1]
    args = parser.parse_args(argv[2:])

    try:
        usb = util.usb_open(args.device)
        print("Erasing %s" % (args.tracks))
        util.with_drive_selected(erase, usb, args)
    except USB.CmdError as error:
        print("Command Failed: %s" % error)


if __name__ == "__main__":
    main(sys.argv)

# Local variables:
# python-indent: 4
# End:
