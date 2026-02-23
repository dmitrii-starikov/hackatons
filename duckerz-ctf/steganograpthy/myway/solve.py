import struct
from pathlib import Path
import tempfile
import jpeglib

def read_id3v23(mp3_path: Path):
    data = mp3_path.read_bytes()

    flags = data[5]

    tag_size = syncsafe_to_int(data[6:10])
    tag_data = data[10:10 + tag_size]

    frames = []
    pos = 0
    while pos + 10 <= len(tag_data):
        frame_id = tag_data[pos:pos + 4]
        if frame_id == b"\x00\x00\x00\x00":
            break
        size = struct.unpack(">I", tag_data[pos + 4:pos + 8])[0]
        if size == 0:
            break
        flags = tag_data[pos + 8:pos + 10]
        frame_data = tag_data[pos + 10:pos + 10 + size]
        frames.append((frame_id, flags, frame_data))
        pos += 10 + size

    return frames

def syncsafe_to_int(b: bytes) -> int:
    return ((b[0] & 0x7F) << 21) | ((b[1] & 0x7F) << 14) | ((b[2] & 0x7F) << 7) | (b[3] & 0x7F)

def parse_apic(frame_data: bytes):
    enc = frame_data[0]
    rest = frame_data[1:]
    mime_end = rest.find(b"\x00")
    mime = rest[:mime_end].decode("latin1")
    after_mime = rest[mime_end + 1:]
    pic_type = after_mime[0]
    desc_data = after_mime[1:]

    term = b"\x00"
    desc_end = desc_data.find(term)
    img = desc_data[desc_end + 1:]

    return mime, pic_type, img

def iter_coeff_bits(jpeg):
    for comp in (jpeg.Y, jpeg.Cb, jpeg.Cr):
        if comp is None:
            continue
        h, w, _, _ = comp.shape
        for by in range(h):
            for bx in range(w):
                block = comp[by, bx]
                for i in range(8):
                    for j in range(8):
                        if i == 0 and j == 0:
                            continue
                        yield abs(int(block[i, j])) & 1


def jpeg_capacity_bits(jpeg) -> int:
    capacity = 0
    for comp in (jpeg.Y, jpeg.Cb, jpeg.Cr):
        if comp is None:
            continue
        h, w, _, _ = comp.shape
        capacity += h * w * 63
    return capacity


def bits_to_int(bits):
    value = 0
    for b in bits:
        value = (value << 1) | b
    return value


def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i + 8]:
            byte = (byte << 1) | b
        out.append(byte)
    return bytes(out)

def extract_payload_from_jpeg_bytes(jpeg_bytes: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        in_path = Path(tmp) / "cover.jpg"
        in_path.write_bytes(jpeg_bytes)

        # Читаем DCT коэффициенты из JPEG
        dcts = jpeglib.read_dct(str(in_path))
        # Записываем LSB всех AC кэффициентов из всех блоков dct 
        bit_iter = iter_coeff_bits(dcts)
        payload_bits = [next(bit_iter) for _ in range(jpeg_capacity_bits(dcts))]
        return payload_bits


mp3_path = Path("My_way.mp3")
out_payload = Path("payload.png")

frames = read_id3v23(mp3_path)

apic_frame = None
for fid, flags, data in frames:
    if fid == b"APIC":
        apic_frame = data
        break

mime, pic_type, img = parse_apic(apic_frame)

payload = extract_payload_from_jpeg_bytes(img)

out_payload.write_bytes(bits_to_bytes(payload)[4:])