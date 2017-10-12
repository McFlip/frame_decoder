# frame_decoder
A Data Comm project to practice decoding frames received from an interface.
As each frame is processed, the CRC is calculated for the data payload and compared to the provided CRC.
Correct frames are decoded from the byte-stuffed form and written to a file.
Frame number, data size (in bytes), and whether the frame is valid or invalid is reported to stdout.

Usage:
chmod ugo+x frame_decoder
./frame_decoder dumpFile decodedFile
or
python frame_decoder

Arguments:
dumpFile - A dumpfile of raw bytes recieved over the link.
decodedFile - The final output in plain text.

Dependencies: bitstrings
install with sudo -H pip install bitstrings
