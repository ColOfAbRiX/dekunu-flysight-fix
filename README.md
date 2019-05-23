# Fix for dekunu export for Flysight

## Description

In the [Dekunu cloud portal](1) exported CSV file in [Flysight](2) format have some issues. One of
the problems I've found is that vertical speed is not real and other data is very noisy.

This script aims at fixing the problems and create a new CSV file

## Requirements and Installation

To work the script requires:

* Python 3.6 or higher
* Pandas library installed

Please google how to better install these requirements on your system

## Usage

From the Action View page on Dekunu export the data in Flysight format. Then to fix the file run:

```Shell
./flysight_fix.py <path_to_exported_csv>
```

[1]: http://my.dekunu.cloud/
[2]: http://www.flysight.ca/

## License

Apache License 2.0

## Author Information

[Fabrizio Colonna](mailto:colofabrix@tin.it)
