# Bastard!! (PlayStation) — Traducción al español de España

Parche de traducción **japonés → español (España)** para *Bastard!! ~Ankoku no Hakai-shin~* (PlayStation, 1996, Shueisha / Seta), tratamiento de **«tú»**.

> **Estado: beta jugable (v0.62).** Historia, diálogos, menús, combate, nombres, epílogos, tarjeta de memoria y botones del título están traducidos. Aproximadamente el 90–95 % del texto está localizado y la prueba completa del juego sigue en curso. Consulta *Limitaciones conocidas*.

## Aviso legal
Este repositorio **no contiene el juego ni ninguna ROM/ISO**. Solo incluye un parche diferencial (BPS) que modifica **únicamente** una copia que ya poseas legítimamente. No se ofrece ni se da soporte para obtener la imagen original.

## Qué necesitas
- La imagen original del juego: `Bastard.bin` (la imagen de CD en formato BIN de 2352 bytes por sector, con su `.cue`).
- **Datos para comprobar que es la imagen correcta:**

| | SHA-256 | CRC32 | Tamaño |
|---|---|---|---|
| **Original (sin parchear)** | `326de98cfc9254c6f954e9fa1b3f68fe1cb8bf9c8c14310e33b1efee3f87349f` | `baef7ab1` | 565 989 984 bytes |
| **Resultado (parcheada)** | `5e9a671ec9d651832e91954cf17ee6081465873d3b63ee1420d811d9d7007147` | `60f723da` | 565 989 984 bytes |

Si el hash de tu `Bastard.bin` no coincide con el original, el parche no se aplicará (o se aplicará mal): usa otra copia.

## Contenido del repositorio
- `Bastard_ES_v0.62.bps` — el parche (formato BPS, acumulativo: incluye todos los cambios, no hace falta aplicar nada anterior).
- `aplicar_parche.py` — aplicador en Python 3 sin dependencias (opcional); además genera el `.cue`.
- `README.md` — este documento.

## Cómo aplicar el parche

**Antes de empezar:** haz una copia de seguridad de `Bastard.bin`. El parche **no modifica** el archivo original: genera uno nuevo.

### Opción A — Con el script incluido (macOS, Linux y Windows con Python 3)
1. Pon en la misma carpeta: `Bastard.bin`, `Bastard_ES_v0.62.bps` y `aplicar_parche.py`.
2. Abre una terminal en esa carpeta y ejecuta:
   ```
   python3 aplicar_parche.py
   ```
   (En Windows, `py aplicar_parche.py`.)
3. Se creará `Bastard_ES.bin` **y también `Bastard_ES.cue`**. El script comprueba el CRC32 del original, del parche y del resultado, y muestra el SHA-256 final, que debe ser el de la tabla de arriba.
   - Si junto a `Bastard.bin` hay un `Bastard.cue`, se reutiliza (con sus pistas) cambiando solo el nombre del archivo BIN.
   - Si no lo hay, se genera uno de una sola pista de datos (`MODE2/2352`).

También admite nombres propios: `python3 aplicar_parche.py parche.bps origen.bin salida.bin`.
Necesita unos 1,2 GB de memoria libre y tarda un par de minutos.

### Opción B — Con Floating IPS (Flips)
- **Interfaz gráfica:** *Apply Patch* → elige `Bastard_ES_v0.62.bps` → elige `Bastard.bin` → guarda como `Bastard_ES.bin`.
- **Terminal (macOS, con Homebrew):** `brew install flips` y después
  ```
  flips --apply Bastard_ES_v0.62.bps Bastard.bin Bastard_ES.bin
  ```

### Opción C — Otros parcheadores BPS
Cualquier parcheador compatible con BPS (por ejemplo MultiPatch en macOS, beat/Rom Patcher JS en navegador si tu equipo tiene memoria suficiente) vale. Elige el parche, la imagen original y un nombre de salida.

### Comprobar el resultado
```
shasum -a 256 Bastard_ES.bin        # macOS / Linux
certutil -hashfile Bastard_ES.bin SHA256   # Windows
```
Debe salir `5e9a671ec9d651832e91954cf17ee6081465873d3b63ee1420d811d9d7007147`.

### Jugar
- Carga `Bastard_ES.cue` (generado por el script) en el emulador o en tu consola con lector de BIN/CUE. Si usas Flips u otro parcheador, crea el `.cue` a mano: `FILE "Bastard_ES.bin" BINARY` / `TRACK 01 MODE2/2352` / `INDEX 01 00:00:00`, o copia tu `.cue` original cambiando el nombre del BIN.
- Funciona con emuladores como **DuckStation** o **RetroArch (Beetle PSX / PCSX ReARMed)**. Tras parchear, la imagen no necesita más cambios.
- Si cambias el nombre del `.bin`, actualiza la línea `FILE` del `.cue`.

## Limitaciones conocidas
- La prueba completa del juego **todavía no está terminada**: puede haber textos cortados o poco naturales, sobre todo en combates largos, tienda y epílogos.
- Siguen sin traducir (por estar generados por el juego/BIOS): la **«H» y la «M»** de las barras de PV/PM y el texto `ファイル1/2` de la tarjeta de memoria.
- Algunas etiquetas dudosas por confirmar en pantalla: VIEW, SPELLBOUND, DISCORDED, WARNING, SQUARE.
- En las etiquetas de menú y combate no se usan tildes (el juego no las admite en esas cadenas).

## Cómo informar de errores
Abre un *issue* con: captura de pantalla (o *save state*), el momento del juego y, si puedes, el texto que ves. Con eso se prepara una nueva versión del parche.

## Créditos
Localización, ingeniería inversa y parche: *(tu nombre / alias)*.
Material original © Kazushi Hagiwara / Shueisha / Seta. Proyecto de aficionados, sin ánimo de lucro y sin relación con los titulares de derechos.
