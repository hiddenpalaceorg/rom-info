##### namco_museum.gdi

This test gdi is based on `Namco Museum v1.010 (2000)(Namco)(NTSC)(US)[!]`, chosen for its relatively small size. The gdi is edited to significantly reduce the file size. 

Track 3 is shortened from 1.1GB to 49KB by deleting empty sectors from 45021 to 544914. Sectors 544915 to 545497 are artificially moved to track 5. The resulting image is just 7MB (instead of 1.1GB). It's not strictly valid, but it's still very useful as a test case.

The original gdi is:

```
5
1 0 4 2352 track01.bin 0
2 756 0 2352 track02.raw 0
3 45000 4 2352 track03.bin 0
4 545647 0 2352 track04.raw 0
5 546248 4 2352 track05.bin 0
```

The modified version is (note that the starting sector is smaller than the one for sector 4):

```
5
1 0 4 2352 track01.bin 0
2 756 0 2352 track02.raw 0
3 45000 4 2352 track03.bin 0
4 545647 0 2352 track04.raw 0
5 544915 4 2352 track05.bin 0
```

