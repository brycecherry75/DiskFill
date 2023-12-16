# Requires installation of psutil: pip install psutil

import argparse, struct, sys, os, ctypes, psutil

FillBlockSize = 256 # MB - takes about 30-60 seconds to generate at first and is an optimal size to start off with

if __name__ == "__main__":
  parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
  parser.add_argument("--path", help="Path to fill with *.tmp files filled with zeros")
  args = parser.parse_args()
  diskpath = args.path
  if args.path:
    FileCount = 0
    CurrentFillSize = int(FillBlockSize * 1048576)
    print("Generating fill buffer of", FillBlockSize, "MB")
    while True:
      CurrentFreeSpace = psutil.disk_usage(diskpath)[2]
      if CurrentFreeSpace == 0:
        print("Disk fill complete")
        break
      if CurrentFreeSpace < CurrentFillSize:
        CurrentFillSize = CurrentFreeSpace
      FillBuffer = (ctypes.c_byte * CurrentFillSize)()
      for ByteToClear in range (CurrentFillSize):
        FillBuffer[ByteToClear] = 0x00
      while True:
        CurrentFreeSpace = psutil.disk_usage(diskpath)[2]
        if CurrentFreeSpace >= CurrentFillSize:
          CurrentFile = diskpath + str(FileCount) + ".tmp"
          FillFile = open(CurrentFile, 'wb')
          FillFile.write(FillBuffer)
          FillFile.close()
          FileCount += 1
          if (CurrentFreeSpace - CurrentFillSize) > 0:
            GigabytesRemaining = int(((CurrentFreeSpace - CurrentFillSize) * 100) / 1073741824)
            GigabytesRemaining /= 100
            print(GigabytesRemaining, "gigabytes remaining to be zeroed")
        else:
          break
  else:
    print("Path to fill not specified")