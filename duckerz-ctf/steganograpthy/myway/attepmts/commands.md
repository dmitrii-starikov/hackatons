```bash
strings file.mp3 | less
exiftool file.mp3
file file.mp3
binwalk file.mp3
binwalk -e file.mp3
sox file.mp3 -n spectrogram -o spec.png
xxd file.mp3 | less
binwalk -e --dd='.*' My_way.mp3 
dd if=My_way.mp3 of=cover.jpg bs=1 skip=614  - достаем картинку
file cover.jpg
exiftool cover.jpg
strings cover.jpg | less
convert cover.jpg -channel R -separate r.png
convert cover.jpg -channel G -separate g.png
convert cover.jpg -channel B -separate b.png
convert cover.jpg -colorspace gray gray.png
convert gray.png -contrast-stretch 0 gray2.png
convert gray.png -normalize gray3.png
xxd cover.jpg | tail -n 50
convert cover.jpg -channel RGB -separate +channel \
\( r.png g.png -compose difference -composite \) diff_rg.png \
\( r.png b.png -compose difference -composite \) diff_rb.png \
\( g.png b.png -compose difference -composite \) diff_gb.png
convert fft.png -inverse-fft ifft.png
```

```
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ sox My_way.mp3 -n spectrogram -o spec.png
sox FAIL formats: no handler for file extension `mp3'
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ xxd My_way.mp3 | less
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ xxd My_way.mp3 >> xxd.txt
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ cat xxd.txt | grep flag
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ cat xxd.txt | grep DUCK
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ binwalk -e My_way.mp3

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
614           0x266           JPEG image data, JFIF standard 1.01

bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ file My_way.mp3
My_way.mp3: Audio file with ID3 version 2.3.0, contains: MPEG ADTS, layer III, v1, 224 kbps, 44.1 kHz, Stereo
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ exiftool My_way.mp3
ExifTool Version Number         : 12.40
File Name                       : My_way.mp3
Directory                       : .
File Size                       : 7.0 MiB
File Modification Date/Time     : 2026:02:07 12:13:28+03:00
File Access Date/Time           : 2026:02:07 12:35:37+03:00
File Inode Change Date/Time     : 2026:02:07 12:35:30+03:00
File Permissions                : -rw-rw-r--
File Type                       : MP3
File Type Extension             : mp3
MIME Type                       : audio/mpeg
MPEG Audio Version              : 1
Audio Layer                     : 3
Sample Rate                     : 44100
Channel Mode                    : Stereo
MS Stereo                       : Off
Intensity Stereo                : Off
Copyright Flag                  : False
Original Media                  : False
Emphasis                        : None
VBR Frames                      : 10480
VBR Bytes                       : 7133276
VBR Scale                       : 0
ID3 Size                        : 192852
Title                           : Donald Duck Sings My Way (NOT AI)
Year                            : 2024
User Defined Text               : (comment) omment
Encoder Settings                : Lavf58.76.100
Picture MIME Type               : image/jpeg
Picture Type                    : Front Cover
Picture Description             : Album cover
Picture                         : (Binary data 192029 bytes, use -b option to extract)
Album                           :
Comment                         : https://www.youtube.com/watch?
Artist                          : ExtraReadyDude
Genre                           : None
Date/Time Original              : 2024
Audio Bitrate                   : 208 kbps
Duration                        : 0:04:34 (approx)




bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ dd if=My_way.mp3 of=cover.jpg bs=1 skip=614
^C4226237+0 records in
4226237+0 records out
4226237 bytes (4,2 MB, 4,0 MiB) copied, 18,7758 s, 225 kB/s

bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ exiftool cover.jpg
ExifTool Version Number         : 12.40
File Name                       : cover.jpg
Directory                       : .
File Size                       : 4.0 MiB
File Modification Date/Time     : 2026:02:07 12:53:47+03:00
File Access Date/Time           : 2026:02:07 12:53:38+03:00
File Inode Change Date/Time     : 2026:02:07 12:53:47+03:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Width                     : 640
Image Height                    : 480
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 640x480
Megapixels                      : 0.307



bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ convert cover.jpg -colorspace gray gray.png
convert gray.png -contrast-stretch 0 gray2.png
convert gray.png -normalize gray3.png
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ grep "DUCK" My_way.mp3
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ grep "DUC^C My_way.mp3
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ grep "DUCK" xxd.txt
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/DUCK/{print "Found on line", NR; print $0}'
^C
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/DUCK/{print "Found on line", NR; print $0}' xxd.txt
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/escrip/{print "Found on line", NR; print $0}' xxd.txt
Found on line 12
000000b0: 7c00 0000 6465 7363 7269 7074 696f 6e00  |...description.
Found on line 13
000000c0: 6573 6372 6970 7469 6f6e 0000 0000 0000  escription......
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/flag/{print "Found on line", NR; print $0}' xxd.txt
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/duck/{print "Found on line", NR; print $0}' xxd.txt
bot@linux:~/PycharmProjects/hackatons/duckerz-ctf/steganograpthy/myway$ awk '/ctf/{print "Found on line", NR; print $0}' xxd.txt
```

