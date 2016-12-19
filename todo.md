# romkit todo

#### $ rom [file.bin ...]
If invoked with no options, implies --all.

#### $ rom -a, --all
Implies --type --meta --info --header --list 30 --error --deep_scan.

--

### General info

#### $ rom -t, --type
Detect ROM/disc type.

#### $ rom -H, --header
Output header, if available. Not sure about -H (can't use -h). In the short-term, need to support:

* Sega Mega Drive/CD/32X
* Sega Saturn
* Sega Dreamcast
* SNES?
* PSX?

In case -w is provided, ROM header fields need to be displayed in-line with their semantics, so this needs to work well with -i somehow. Maybe -w needs to handle this (from an immediate representation or something).

#### $ rom -i, --info
Output any information we can gather from the file, such as:

* Game name
* Checksum
* Build date
* Serial
* Developer

--

### Containers (discs, etc.)


#### $ rom -l, --list [number\_of_entries]
List contents, if the file is a container (e.g. a disc). Show no more than number\_of_entries.

* Output file icons when -w is specified
* Detect 2048 (.iso), 2352 (raw/.bin), split disc dumps (.cue/.gdi)
  * Consume individual tracks in split dumps (don't analyze the same file twice). Probably means looking for .cue/.gdi first.

#### $ rom -e, --error

Analyze the disc for bad sectors using error detection and correction codes (EDC/ECC) and sector data format (only possible for 2352 dumps).

Show which files are affected by bad sectors and at which locations.

#### $ rom -x, --extract

Extract the container contents.

#### $ rom --deep_scan

Scan empty space for leftover data.

#### Miscellaneous
* Analyze ISO 9660 for volume dates and time zones. This needs some kind of heuristics because these are often fake.


--

### Wiki utilities

#### $ rom -m, --meta
Output a listing of the input files, containing file name, file type, size, crc32, md5, and sha1.

#### $ rom -w, --wiki
Output HP wiki format instead of text.

#### $ rom --json
Maybe?