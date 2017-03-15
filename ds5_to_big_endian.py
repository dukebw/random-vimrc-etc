import re
import sys

def convert_big_endian(argv):
    assert len(argv) >= 2

    big_endian = '0x'
    for word in reversed(re.sub('[\s+]', '', argv[1]).split('0x')[1:]):
        big_endian += word

    print(big_endian)


if __name__ == "__main__":
    convert_big_endian(sys.argv)
