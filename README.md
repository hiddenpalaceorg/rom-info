## ROM info

 [![Travis](https://img.shields.io/travis/drx/rom-info.svg)](https://travis-ci.org/drx/rom-info)
 [![Coveralls](https://img.shields.io/coveralls/drx/rom-info.svg)](https://coveralls.io/github/drx/rom-info)

 ROM info is a utility for extracting information from ROMs and disc images. It is primarily meant to supplement the [Hidden palace video game prototype wiki](http://hiddenpalace.org/Main_Page).

 Some examples of information extracted: headers, file systems, file lists, files, disc sector errors.

#### Supported formats
 
 * CDs &mdash; EDC and ECC (P and Q) error checking
   * ISO 9660 file system tracks &mdash; volumes, files
   * GDI Dreamcast images
   
#### Requirements

 * Python 3.3 (64-bit recommended) or PyPy3 5.5.0

#### Example output

##### Sonic Adventure 2 GD-R
```
$ ./discinfo "Sonic Adventure 2 Review/disc.gdi"
Tracks:
  Track 1:
    Header:
      Hardware ID: SEGA SEGAKATANA 
      Maker ID: SEGA ENTERPRISES
      CRC: 0FA6
      Device: GD-ROM
      Disc: 1/1
      Region: E
      Peripherals: 0799A10 
      Product number: MK-5111750
      Product version: V1.002
      Release date: 20010521        
      Boot file: 1ST_READ.BIN    
      Company name: SEGA ENTERPRISES
      Software name: SONIC ADVENTURE 

    Volume:
      System: SEGA SEGAKATANA
      Name: SONIC2
      Set: SONIC2
      Publisher: SEGA ENTERPRISES,LTD.
      Data preparer: CRI CD CRAFT VER.2.30
      Application: 
      Creation date: 2001-05-21 14:15:00
      Modification date: 2001-05-21 14:15:00
      Start date: 
      Expiration date: 

    Files:
      /ABSTRACT.TXT              (2001-05-21 14:15:00, crc32: f60acaa4, 46 bytes, sector: 22)
      /BIBLIOGR.TXT              (2001-05-21 14:15:00, crc32: 57aaf9b9, 350 bytes, sector: 23)
      /COPYRIGH.TXT              (2001-05-21 14:15:00, crc32: 73dba4df, 75 bytes, sector: 21)
      /WALLP_CHAO1280X1024.BMP   (2001-05-21 14:15:00, crc32: 970b65a2, 2621494 bytes, sector: 24)
      /WALLP_CHAO800X600.BMP     (2001-05-21 14:15:00, crc32: acf631ae, 960054 bytes, sector: 1305)
      /WALLP_SHADOW1280X1024.BMP (2001-05-21 14:15:00, crc32: 5de80d7c, 2621494 bytes, sector: 1774)
      /WALLP_SHADOW800X600.BMP   (2001-05-21 14:15:00, crc32: 2d170ad0, 960054 bytes, sector: 3055)
      /WALLP_SONIC1280X1024.BMP  (2001-05-21 14:15:00, crc32: 8d4c24b2, 2621494 bytes, sector: 3524)
      /WALLP_SONIC800X600.BMP    (2001-05-21 14:15:00, crc32: 4a754f62, 960054 bytes, sector: 4805)


  Track 2: Audio track
  Track 3:
    Header:
      Hardware ID: SEGA SEGAKATANA 
      Maker ID: SEGA ENTERPRISES
      CRC: 0FA6
      Device: GD-ROM
      Disc: 1/1
      Region: E
      Peripherals: 0799A10 
      Product number: MK-5111750
      Product version: V1.002
      Release date: 20010521        
      Boot file: 1ST_READ.BIN    
      Company name: SEGA ENTERPRISES
      Software name: SONIC ADVENTURE 

    Volume:
      System: SEGA SEGAKATANA
      Name: SONIC2
      Set: SONIC2
      Publisher: SEGA ENTERPRISES,LTD.
      Data preparer: CRI CD CRAFT VER.2.30
      Application: 
      Creation date: 2001-05-21 14:15:00
      Modification date: 2001-05-21 14:15:00
      Start date: 
      Expiration date: 

    Files:
      /0GDTEX.PVR                        (2001-05-21 14:15:00, crc32: c32744d3, 131104 bytes, sector: 5817)
      /1ST_READ.BIN                      (2001-05-21 14:15:00, crc32: 465fa358, 1577860 bytes, sector: 503229)
      /2_DP.BIN                          (2001-05-21 14:15:00, crc32: f5612dd3, 2845860 bytes, sector: 12520)
      /DP2.INI                           (2001-05-21 14:15:00, crc32: 3f51b9ab, 7039 bytes, sector: 13910)
      /DPETC                             (2001-05-21 14:15:00, crc32: b0f4a62f, 2048 bytes, sector: 21)
      /DPETC/DP2.DPS                     (2001-05-21 14:15:00, crc32: 506e18a8, 58099 bytes, sector: 5882)
      /DPETC/DP2SOUND.MLT                (2001-05-21 14:15:00, crc32: 4a16f966, 1781696 bytes, sector: 5911)
      /DPETC/MANATEE.DRV                 (2001-05-21 14:15:00, crc32: 7c217c2a, 36160 bytes, sector: 6781)
      /DPETC/MESSAGE.INI                 (2001-05-21 14:15:00, crc32: 638bb369, 16513 bytes, sector: 6799)
      /DPETC/SOFTKEY.DPS                 (2001-05-21 14:15:00, crc32: 94688309, 67829 bytes, sector: 6808)
      /DPETC/START.ADX                   (2001-05-21 14:15:00, crc32: 89cfc3b1, 599094 bytes, sector: 6842)
      /DPETC/VMS.DPS                     (2001-05-21 14:15:00, crc32: 660929d1, 7151 bytes, sector: 7135)
      /DPETC/VOICE.AFS                   (2001-05-21 14:15:00, crc32: 516bb95a, 3661824 bytes, sector: 7139)
      /DPFONT                            (2001-05-21 14:15:00, crc32: 90762bcf, 2048 bytes, sector: 22)
      /DPFONT/S16EU04P.DAT               (2001-05-21 14:15:00, crc32: a0456f92, 16384 bytes, sector: 8927)
      /DPFONT/S18EU04P.DAT               (2001-05-21 14:15:00, crc32: 7fb8e7ad, 23040 bytes, sector: 8935)
      /DPFONT/S20EU04P.DAT               (2001-05-21 14:15:00, crc32: ca559c42, 25600 bytes, sector: 8947)
      /DPFONT/S24EU04P.DAT               (2001-05-21 14:15:00, crc32: 35a0250f, 36864 bytes, sector: 8960)
      /DPFONT/S26EU04P.DAT               (2001-05-21 14:15:00, crc32: e28953bc, 46592 bytes, sector: 8978)
      /DPMODEL                           (2001-05-21 14:15:00, crc32: 7ba00a62, 2048 bytes, sector: 23)
      /DPSS                              (2001-05-21 14:15:00, crc32: fd52a375, 2048 bytes, sector: 24)
      /DPSS/L_ADV2LOGO_EU.GIF            (2001-05-21 14:15:00, crc32: 00633343, 4343 bytes, sector: 9001)
      /DPSS/L_AMY_EU.GIF                 (2001-05-21 14:15:00, crc32: 3acba81b, 8043 bytes, sector: 9004)
      /DPSS/L_CHAO2_EU.GIF               (2001-05-21 14:15:00, crc32: 67af4a75, 6770 bytes, sector: 9008)
      /DPSS/L_EGGMAN_EU.GIF              (2001-05-21 14:15:00, crc32: 0ecfedb5, 6941 bytes, sector: 9012)
      /DPSS/L_KNUCKLES_EU.GIF            (2001-05-21 14:15:00, crc32: 7dd4042a, 8713 bytes, sector: 9016)
      /DPSS/L_NCHAO_EU.GIF               (2001-05-21 14:15:00, crc32: 557c3903, 6108 bytes, sector: 9021)
      /DPSS/L_ROUGE_EU.GIF               (2001-05-21 14:15:00, crc32: 49e920e3, 7839 bytes, sector: 9024)
      /DPSS/L_SHADOW_EU.GIF              (2001-05-21 14:15:00, crc32: bdd531ce, 7818 bytes, sector: 9028)
      /DPSS/L_SONIC_EU.GIF               (2001-05-21 14:15:00, crc32: aa8635cf, 7780 bytes, sector: 9032)
      /DPSS/L_TAILS_EU.GIF               (2001-05-21 14:15:00, crc32: 4f9b1de1, 8729 bytes, sector: 9036)
      /DPTEX                             (2001-05-21 14:15:00, crc32: e5aa4d03, 2048 bytes, sector: 25)
      /DPTEX/ASF_ADX0.PVR                (2001-05-21 14:15:00, crc32: d380f301, 524320 bytes, sector: 9041)
      /DPTEX/ASF_ADX1.PVR                (2001-05-21 14:15:00, crc32: 80f94fff, 524320 bytes, sector: 9298)
      /DPTEX/C_M_S.PVR                   (2001-05-21 14:15:00, crc32: 73b4d2cf, 524320 bytes, sector: 9555)
      /DPTEX/C_NAME.PVR                  (2001-05-21 14:15:00, crc32: ad5d495f, 67616 bytes, sector: 9812)
      /DPTEX/FLAGTEX001.PVR              (2001-05-21 14:15:00, crc32: 251700c3, 524320 bytes, sector: 9914)
      /DPTEX/FLAGTEX002.PVR              (2001-05-21 14:15:00, crc32: b4156200, 524320 bytes, sector: 10171)
      /DPTEX/F_BGTEX01.PVR               (2001-05-21 14:15:00, crc32: 9e5b980c, 67616 bytes, sector: 9846)
      /DPTEX/F_BGTEX02.PVR               (2001-05-21 14:15:00, crc32: 9e5b980c, 67616 bytes, sector: 9880)
      /DPTEX/JYOUCYU0.PVR                (2001-05-21 14:15:00, crc32: a3ec2650, 524320 bytes, sector: 10428)
      /DPTEX/JYOUCYU1.PVR                (2001-05-21 14:15:00, crc32: 237053a0, 67616 bytes, sector: 10685)
      /DPTEX/OPFILE.PVR                  (2001-05-21 14:15:00, crc32: 8f111b84, 524320 bytes, sector: 11233)
      /DPTEX/OPTION01.PVR                (2001-05-21 14:15:00, crc32: d6c6f9a8, 67616 bytes, sector: 11490)
      /DPTEX/OPTION02.PVR                (2001-05-21 14:15:00, crc32: 953bdc8c, 67616 bytes, sector: 11524)
      /DPTEX/OP_BACK1.PVR                (2001-05-21 14:15:00, crc32: 3f4c85c7, 524320 bytes, sector: 10719)
      /DPTEX/OP_BACK2.PVR                (2001-05-21 14:15:00, crc32: 976253e8, 524320 bytes, sector: 10976)
      /DPTEX/SKB_BASE.PVR                (2001-05-21 14:15:00, crc32: e2d8395a, 67616 bytes, sector: 11558)
      /DPTEX/SKB_EISU.PVR                (2001-05-21 14:15:00, crc32: b716f10b, 67616 bytes, sector: 11592)
      /DPTEX/SKB_KANA.PVR                (2001-05-21 14:15:00, crc32: 11614203, 67616 bytes, sector: 11626)
      /DPTEX/SKB_V102.PVR                (2001-05-21 14:15:00, crc32: f1b49921, 67616 bytes, sector: 11660)
      /DPTEX/SU_ICON.PVR                 (2001-05-21 14:15:00, crc32: be8669b5, 67616 bytes, sector: 11694)
      /DPTEX/TAG_SU.PVR                  (2001-05-21 14:15:00, crc32: 031582d7, 67616 bytes, sector: 11728)
      /DPTEX/VMSPART2.PVR                (2001-05-21 14:15:00, crc32: 78298c35, 524320 bytes, sector: 11762)
      /DPTEX/VMSPARTS.PVR                (2001-05-21 14:15:00, crc32: c4aa64e2, 524320 bytes, sector: 12019)
      /DPTEX/WALLPAPER.PVR               (2001-05-21 14:15:00, crc32: 448b9dea, 174796 bytes, sector: 12276)
      /DPWWW                             (2001-05-21 14:15:00, crc32: cff0f35b, 2048 bytes, sector: 26)
      /DPWWW/BT_DREAMARENA.GIF           (2001-05-21 14:15:00, crc32: 432edae1, 2216 bytes, sector: 12458)
      /DPWWW/BT_SEGA_EU.GIF              (2001-05-21 14:15:00, crc32: 81441743, 2068 bytes, sector: 12460)
      /DPWWW/BT_SONICTEAM_EU.GIF         (2001-05-21 14:15:00, crc32: 273ddd86, 2231 bytes, sector: 12462)
      /DPWWW/CONSTR2.GIF                 (2001-05-21 14:15:00, crc32: 4b1823ba, 2438 bytes, sector: 12464)
      /DPWWW/COPYRIGHT.GIF               (2001-05-21 14:15:00, crc32: 6c1ccaf6, 1939 bytes, sector: 12466)
      /DPWWW/ENGLISH.HTM                 (2001-05-21 14:15:00, crc32: 8cbd2c34, 1173 bytes, sector: 12467)
      /DPWWW/FRENCH.HTM                  (2001-05-21 14:15:00, crc32: c1a30d73, 1172 bytes, sector: 12468)
      /DPWWW/GERMAN.HTM                  (2001-05-21 14:15:00, crc32: 6401dfe2, 1173 bytes, sector: 12469)
      /DPWWW/INDEX.HTM                   (2001-05-21 14:15:00, crc32: 6d3c8a78, 968 bytes, sector: 12470)
      /DPWWW/INDEX_BG.JPG                (2001-05-21 14:15:00, crc32: 5540a40e, 66692 bytes, sector: 12471)
      /DPWWW/INDEX_TITLE_EU.GIF          (2001-05-21 14:15:00, crc32: 18d4b4a3, 27969 bytes, sector: 12504)
      /DPWWW/ITALIAN.HTM                 (2001-05-21 14:15:00, crc32: 775428d2, 1174 bytes, sector: 12518)
      /DPWWW/MODEL                       (2001-05-21 14:15:00, crc32: fb324413, 2048 bytes, sector: 27)
      /DPWWW/MODEL/CARA1_KAMI3.PVR       (2001-05-21 14:15:00, crc32: 1a47c50f, 7552 bytes, sector: 12362)
      /DPWWW/MODEL/CARA_DOU.PVR          (2001-05-21 14:15:00, crc32: d93f902c, 3456 bytes, sector: 12366)
      /DPWWW/MODEL/FACE_MASK4.PVR        (2001-05-21 14:15:00, crc32: f17b08d8, 23936 bytes, sector: 12368)
      /DPWWW/MODEL/HIFU.PVR              (2001-05-21 14:15:00, crc32: 97a25ebe, 896 bytes, sector: 12380)
      /DPWWW/MODEL/HITOMI.PVR            (2001-05-21 14:15:00, crc32: 97ddac60, 4128 bytes, sector: 12383)
      /DPWWW/MODEL/HITO_KAGE.PVR         (2001-05-21 14:15:00, crc32: 46f20213, 3456 bytes, sector: 12381)
      /DPWWW/MODEL/KUTI16.PVR            (2001-05-21 14:15:00, crc32: f583ec39, 1056 bytes, sector: 12386)
      /DPWWW/MODEL/KUTUSITA_1.PVR        (2001-05-21 14:15:00, crc32: 0b73664b, 3456 bytes, sector: 12387)
      /DPWWW/MODEL/MAYU.PVR              (2001-05-21 14:15:00, crc32: 374b07da, 1056 bytes, sector: 12389)
      /DPWWW/MODEL/NAOSI_NULL3_3.NJ      (2001-05-21 14:15:00, crc32: c811c9c0, 31032 bytes, sector: 12390)
      /DPWWW/MODEL/NAOSI_NULL3_3.NJM     (2001-05-21 14:15:00, crc32: 277ccda2, 25596 bytes, sector: 12406)
      /DPWWW/MODEL/SOKO2_64.PVR          (2001-05-21 14:15:00, crc32: 48b7271d, 3456 bytes, sector: 12419)
      /DPWWW/SPANISH.HTM                 (2001-05-21 14:15:00, crc32: 3165ec1f, 1173 bytes, sector: 12519)
      /DPWWW/WARNING                     (2001-05-21 14:15:00, crc32: 01c3f1d4, 2048 bytes, sector: 28)
      /DPWWW/WARNING/BGFAIL.JPG          (2001-05-21 14:15:00, crc32: 7e8ed48d, 9901 bytes, sector: 12421)
      /DPWWW/WARNING/DALOGO1.GIF         (2001-05-21 14:15:00, crc32: 085ef8e6, 2861 bytes, sector: 12426)
      /DPWWW/WARNING/LOCAL_AUTH01_FR.HTM (2001-05-21 14:15:00, crc32: bbe2aa2b, 1199 bytes, sector: 12428)
      /DPWWW/WARNING/LOCAL_AUTH01_GD.HTM (2001-05-21 14:15:00, crc32: 61f72404, 1241 bytes, sector: 12429)
      /DPWWW/WARNING/LOCAL_AUTH01_IT.HTM (2001-05-21 14:15:00, crc32: cb109362, 1255 bytes, sector: 12430)
      /DPWWW/WARNING/LOCAL_AUTH01_SP.HTM (2001-05-21 14:15:00, crc32: b94f2f54, 1222 bytes, sector: 12431)
      /DPWWW/WARNING/LOCAL_AUTH01_UK.HTM (2001-05-21 14:15:00, crc32: 10125ee6, 1190 bytes, sector: 12432)
      /DPWWW/WARNING/LOCAL_REG01_FR.HTM  (2001-05-21 14:15:00, crc32: 1d78affa, 1417 bytes, sector: 12433)
      /DPWWW/WARNING/LOCAL_REG01_GD.HTM  (2001-05-21 14:15:00, crc32: 357abc04, 1491 bytes, sector: 12434)
      /DPWWW/WARNING/LOCAL_REG01_IT.HTM  (2001-05-21 14:15:00, crc32: aabe03aa, 1479 bytes, sector: 12435)
      /DPWWW/WARNING/LOCAL_REG01_SP.HTM  (2001-05-21 14:15:00, crc32: 20600269, 1441 bytes, sector: 12436)
      /DPWWW/WARNING/LOCAL_REG01_UK.HTM  (2001-05-21 14:15:00, crc32: e08fbf06, 1388 bytes, sector: 12437)
      /DPWWW/WARNING/LOGONFAIL_FR.GIF    (2001-05-21 14:15:00, crc32: deb73742, 1417 bytes, sector: 12438)
      /DPWWW/WARNING/LOGONFAIL_GD.GIF    (2001-05-21 14:15:00, crc32: bc0ed35a, 936 bytes, sector: 12439)
      /DPWWW/WARNING/LOGONFAIL_IT.GIF    (2001-05-21 14:15:00, crc32: 7b99ef92, 1400 bytes, sector: 12440)
      /DPWWW/WARNING/LOGONFAIL_SP.GIF    (2001-05-21 14:15:00, crc32: b7986d5c, 1473 bytes, sector: 12441)
      /DPWWW/WARNING/LOGONFAIL_UK.GIF    (2001-05-21 14:15:00, crc32: 1613f970, 1016 bytes, sector: 12442)
      /DPWWW/WARNING/RECONFAIL_FR.GIF    (2001-05-21 14:15:00, crc32: de52b192, 488 bytes, sector: 12443)
      /DPWWW/WARNING/RECONFAIL_GD.GIF    (2001-05-21 14:15:00, crc32: e1c1ceb5, 1207 bytes, sector: 12444)
      /DPWWW/WARNING/RECONFAIL_IT.GIF    (2001-05-21 14:15:00, crc32: ef53e7dd, 664 bytes, sector: 12445)
      /DPWWW/WARNING/RECONFAIL_SP.GIF    (2001-05-21 14:15:00, crc32: 137fd096, 605 bytes, sector: 12446)
      /DPWWW/WARNING/RECONFAIL_UK.GIF    (2001-05-21 14:15:00, crc32: a9ea20cb, 546 bytes, sector: 12447)
      /DPWWW/WARNING/REGFAIL_FR.GIF      (2001-05-21 14:15:00, crc32: 965246c4, 1511 bytes, sector: 12448)
      /DPWWW/WARNING/REGFAIL_GD.GIF      (2001-05-21 14:15:00, crc32: 3e40e892, 1299 bytes, sector: 12449)
      /DPWWW/WARNING/REGFAIL_IT.GIF      (2001-05-21 14:15:00, crc32: 67c80a96, 1401 bytes, sector: 12450)
      /DPWWW/WARNING/REGFAIL_SP.GIF      (2001-05-21 14:15:00, crc32: dfe1cdf7, 1271 bytes, sector: 12451)
      /DPWWW/WARNING/REGFAIL_UK.GIF      (2001-05-21 14:15:00, crc32: 076267d5, 1252 bytes, sector: 12452)
      /DPWWW/WARNING/RESETFAIL_FR.GIF    (2001-05-21 14:15:00, crc32: 36c37383, 318 bytes, sector: 12453)
      /DPWWW/WARNING/RESETFAIL_GD.GIF    (2001-05-21 14:15:00, crc32: 2c51d395, 306 bytes, sector: 12454)
      /DPWWW/WARNING/RESETFAIL_IT.GIF    (2001-05-21 14:15:00, crc32: 914846ad, 305 bytes, sector: 12455)
      /DPWWW/WARNING/RESETFAIL_SP.GIF    (2001-05-21 14:15:00, crc32: e40c2b20, 459 bytes, sector: 12456)
      /DPWWW/WARNING/RESETFAIL_UK.GIF    (2001-05-21 14:15:00, crc32: 8708ef6c, 323 bytes, sector: 12457)
      /MAIGO.BIN                         (2001-05-21 14:15:00, crc32: 0ced9986, 14856 bytes, sector: 13914)
      /SG_DPLDR.BIN                      (2001-05-21 14:15:00, crc32: 0c2470a3, 14856 bytes, sector: 13922)
      /SONIC2                            (2001-05-21 14:15:00, crc32: d21dea19, 86016 bytes, sector: 29)
      /SONIC2/ADVERTISE.PRS              (2001-05-21 14:15:00, crc32: 6fbad2f5, 486425 bytes, sector: 151561)
      /SONIC2/ADVSHAREDATA.PRS           (2001-05-21 14:15:00, crc32: 2e2205ca, 5440 bytes, sector: 151799)
      /SONIC2/ADVSNG_1.ADX               (2001-05-21 14:15:00, crc32: 8e400d2b, 237568 bytes, sector: 151802)
      /SONIC2/ADVSNG_2.ADX               (2001-05-21 14:15:00, crc32: ab476256, 2451456 bytes, sector: 151918)
      /SONIC2/ADVSNG_3.ADX               (2001-05-21 14:15:00, crc32: def5e731, 2293760 bytes, sector: 153115)
      /SONIC2/ADVSNG_4.ADX               (2001-05-21 14:15:00, crc32: ca2cb1bc, 434176 bytes, sector: 154235)
      /SONIC2/ADVSNG_5.ADX               (2001-05-21 14:15:00, crc32: a7d865db, 2607104 bytes, sector: 154447)
      /SONIC2/ALERTTITLE.PRS             (2001-05-21 14:15:00, crc32: da48cae1, 130974 bytes, sector: 160553)
      /SONIC2/ALPHATITLE.PRS             (2001-05-21 14:15:00, crc32: bd8b9459, 288895 bytes, sector: 160617)
      /SONIC2/AL_BODY.PRS                (2001-05-21 14:15:00, crc32: faf4ae33, 48431 bytes, sector: 155720)
      /SONIC2/AL_CHILD02.PVP             (2001-05-21 14:15:00, crc32: a870f7be, 112 bytes, sector: 155744)
      /SONIC2/AL_COMMON_TEX.PRS          (2001-05-21 14:15:00, crc32: 3d3bb8fd, 28271 bytes, sector: 155745)
      /SONIC2/AL_DARK_OBJ_TEX.PRS        (2001-05-21 14:15:00, crc32: 5f70ecd9, 122319 bytes, sector: 155759)
      /SONIC2/AL_DC.PVP                  (2001-05-21 14:15:00, crc32: a7d8f3e2, 112 bytes, sector: 155819)
      /SONIC2/AL_ENTRANCE_OBJ.PRS        (2001-05-21 14:15:00, crc32: bf6fe084, 93401 bytes, sector: 155926)
      /SONIC2/AL_ENTRANCE_TEX.PRS        (2001-05-21 14:15:00, crc32: 4b5d338c, 195829 bytes, sector: 155972)
      /SONIC2/AL_ENT_CHAR_E_TEX.PRS      (2001-05-21 14:15:00, crc32: f42f8710, 35827 bytes, sector: 155820)
      /SONIC2/AL_ENT_CHAR_J_TEX.PRS      (2001-05-21 14:15:00, crc32: 5421f294, 32025 bytes, sector: 155838)
      /SONIC2/AL_ENT_COMMON_TEX.PRS      (2001-05-21 14:15:00, crc32: 042d808d, 45341 bytes, sector: 155854)
      /SONIC2/AL_ENT_RIVAL_TEX.PRS       (2001-05-21 14:15:00, crc32: 1f88c090, 42090 bytes, sector: 155877)
      /SONIC2/AL_ENT_TITLE_E_TEX.PRS     (2001-05-21 14:15:00, crc32: 059c587b, 24396 bytes, sector: 155898)
      /SONIC2/AL_ENT_TITLE_J_TEX.PRS     (2001-05-21 14:15:00, crc32: aaf4d8bf, 22797 bytes, sector: 155910)
      /SONIC2/AL_ENT_VMS_TEX.PRS         (2001-05-21 14:15:00, crc32: 88d6e78c, 7582 bytes, sector: 155922)
      /SONIC2/AL_ENV_TEX.PRS             (2001-05-21 14:15:00, crc32: 056b77b0, 16363 bytes, sector: 156068)
      /SONIC2/AL_EYE.PRS                 (2001-05-21 14:15:00, crc32: 21a5989a, 7593 bytes, sector: 156076)
      /SONIC2/AL_HC.PVP                  (2001-05-21 14:15:00, crc32: ab0bb3f8, 112 bytes, sector: 156080)
      /SONIC2/AL_HCF.PVP                 (2001-05-21 14:15:00, crc32: 56bc3eae, 112 bytes, sector: 156081)
      /SONIC2/AL_HCN.PVP                 (2001-05-21 14:15:00, crc32: 0271d234, 112 bytes, sector: 156082)
      /SONIC2/AL_HCP.PVP                 (2001-05-21 14:15:00, crc32: 7338c442, 112 bytes, sector: 156083)
      /SONIC2/AL_HCR.PVP                 (2001-05-21 14:15:00, crc32: 7448dbb2, 112 bytes, sector: 156084)
      /SONIC2/AL_HCS.PVP                 (2001-05-21 14:15:00, crc32: bf009008, 112 bytes, sector: 156085)
      /SONIC2/AL_HCZ.PVP                 (2001-05-21 14:15:00, crc32: 3ebf8cee, 112 bytes, sector: 156086)
      /SONIC2/AL_HERO_OBJ_TEX.PRS        (2001-05-21 14:15:00, crc32: b848d2dd, 75904 bytes, sector: 156087)
      /SONIC2/AL_HFF.PVP                 (2001-05-21 14:15:00, crc32: 54beec43, 112 bytes, sector: 156125)
      /SONIC2/AL_HFN.PVP                 (2001-05-21 14:15:00, crc32: 5424346f, 112 bytes, sector: 156126)
      /SONIC2/AL_HFP.PVP                 (2001-05-21 14:15:00, crc32: 54beec43, 112 bytes, sector: 156127)
      /SONIC2/AL_HFR.PVP                 (2001-05-21 14:15:00, crc32: 54beec43, 112 bytes, sector: 156128)
      /SONIC2/AL_HFS.PVP                 (2001-05-21 14:15:00, crc32: b761817d, 112 bytes, sector: 156129)
      /SONIC2/AL_HFZ.PVP                 (2001-05-21 14:15:00, crc32: 54beec43, 112 bytes, sector: 156130)

```
