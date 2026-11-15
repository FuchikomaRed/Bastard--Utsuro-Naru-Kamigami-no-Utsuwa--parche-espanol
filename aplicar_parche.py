#!/usr/bin/env python3
"""
aplicar_parche.py - Aplica un parche BPS sin instalar nada (solo Python 3).
Uso (sin argumentos, en la carpeta con los archivos):
  python3 aplicar_parche.py
Usa Bastard_ES_v0.62.bps + Bastard.bin (original) y crea Bastard_ES.bin. Tambien admite: parche.bps origen.bin salida.bin
Ademas crea el archivo .cue junto a la BIN de salida (necesario para emuladores y consolas).
Comprueba el CRC32 de la BIN original, del parche y del resultado antes de dar por bueno el archivo.
"""
import sys, os, re, zlib, struct, hashlib
if len(sys.argv) == 1: sys.argv += ["Bastard_ES_v0.62.bps", "Bastard.bin", "Bastard_ES.bin"]
if len(sys.argv) != 4: sys.exit(__doc__)
bps = open(sys.argv[1], "rb").read(); src = open(sys.argv[2], "rb").read()
if bps[:4] != b"BPS1": sys.exit("No es un parche BPS")
sc, tc, pc = struct.unpack("<III", bps[-12:])
if zlib.crc32(bps[:-4]) != pc: sys.exit("El parche esta corrupto (CRC del parche incorrecto)")
if zlib.crc32(src) != sc: sys.exit("La BIN de origen NO es la que espera el parche (CRC32 %08x, esperado %08x)" % (zlib.crc32(src), sc))
pos = 4
def vn():
    global pos
    n = 0; s = 1
    while True:
        x = bps[pos]; pos += 1; n += (x & 0x7f) * s
        if x & 0x80: break
        s <<= 7; n += s
    return n
ssz = vn(); tsz = vn(); msz = vn(); pos += msz
if ssz != len(src): sys.exit("Tamano de origen distinto")
out = bytearray(tsz); o = 0; sro = 0; tro = 0; end = len(bps) - 12
while pos < end:
    v = vn(); a = v & 3; l = (v >> 2) + 1
    if a == 0: out[o:o + l] = src[o:o + l]; o += l
    elif a == 1: out[o:o + l] = bps[pos:pos + l]; pos += l; o += l
    else:
        d = vn(); d = -(d >> 1) if d & 1 else d >> 1
        if a == 2:
            sro += d; out[o:o + l] = src[sro:sro + l]; sro += l; o += l
        else:
            tro += d
            for _ in range(l): out[o] = out[tro]; o += 1; tro += 1
if zlib.crc32(out) != tc: sys.exit("ERROR: el resultado no coincide con el CRC32 esperado")
open(sys.argv[3], "wb").write(out)
print("OK -> %s  CRC32 %08x  SHA-256 %s" % (sys.argv[3], zlib.crc32(out), hashlib.sha256(out).hexdigest()))
# ---- archivo .cue ----
salida = sys.argv[3]; carpeta = os.path.dirname(os.path.abspath(salida)); nombre_bin = os.path.basename(salida)
cue_out = os.path.join(carpeta, os.path.splitext(nombre_bin)[0] + ".cue")
orig = os.path.abspath(sys.argv[2]); cue_orig = os.path.splitext(orig)[0] + ".cue"
if os.path.exists(cue_orig):
    # Se reutiliza el .cue original (pistas incluidas) cambiando solo el nombre del archivo BIN
    txt = open(cue_orig, encoding="utf-8", errors="replace").read()
    txt2, n = re.subn(r'(?im)^(\s*FILE\s+)(?:"[^"]*"|\S+)(\s+BINARY)', lambda m: m.group(1) + '"' + nombre_bin + '"' + m.group(2), txt, count=1)
    if n == 0: txt2 = None
else: txt2 = None
if txt2 is None:
    txt2 = 'FILE "%s" BINARY\r\n  TRACK 01 MODE2/2352\r\n    INDEX 01 00:00:00\r\n' % nombre_bin
    origen_cue = "generado (una sola pista de datos MODE2/2352)"
else: origen_cue = "basado en tu .cue original (%s)" % os.path.basename(cue_orig)
open(cue_out, "w", encoding="utf-8", newline="").write(txt2)
print("CUE -> %s  [%s]" % (cue_out, origen_cue))
