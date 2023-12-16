# DiskFill
Zero fill a HDD without the risk of affecting other storage devices

Requires installation of psutil: pip install psutil

## Usage
python (filename).py --path pathname 

This will fill the specified path with zero filled *.tmp files until space is exhausted.