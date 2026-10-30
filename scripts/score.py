"""Original music for the reels, made here note by note, so there are no rights to clear.

Quiet, classic jewelry-house feel: a soft string pad, a piano that plays one note each time the
board changes, a celesta shimmer over the opening piece, a breath of air as it shrinks into the
board, and a last open chord under the seal. 100 bpm, so one beat = one change of the board (0.6 s).

    from score import score
    wav = score(duration=14.0, opening=1.5, landing=2.3, cues=[2.65, 3.25, ...], outro=11.0)
"""
import wave

import numpy as np

SR = 44100
A4 = 440.0
NOTE = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}

# Bm(add9) - Gmaj7 - D/F# - A(sus2), one chord every four beats; ends on Dmaj9 under the seal
CHORDS = [["B2", "F#3", "D4", "C#5"], ["G2", "D3", "B3", "F#4"], ["F#2", "D3", "A3", "E4"], ["A2", "E3", "B3", "C#4"]]
ARP = [["B4", "D5", "F#5", "C#6"], ["G4", "B4", "D5", "F#5"], ["F#4", "A4", "D5", "E5"], ["A4", "C#5", "E5", "B5"]]
LAST = ["D2", "A2", "F#3", "C#4", "E4", "A4"]


def hz(name):
    return A4 * 2 ** ((NOTE[name[:-1]] + 12 * (int(name[-1]) - 4)) / 12)


def env(n, attack, release, total=None):
    """Linear attack, flat, raised-cosine release; n samples long."""
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    if a:
        e[:a] = np.linspace(0, 1, a)
    if r:
        e[-r:] *= 0.5 * (1 + np.cos(np.linspace(0, np.pi, r)))
    return e


def pad_voice(f, dur, rng):
    """String-like: a few detuned voices, harmonics falling off, a slow vibrato."""
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    for det in (-0.004, 0.0, 0.0045):
        vib = 1 + 0.0025 * np.sin(2 * np.pi * (4.6 + rng.random()) * t + rng.random() * 6)
        ph = 2 * np.pi * np.cumsum(f * (1 + det) * vib) / SR
        for k in range(1, 9):
            out += np.sin(k * ph + rng.random() * 6) / k ** 1.6
    return out / 6


def piano(f, dur=2.6, vel=1.0):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)      # a touch of string stiffness
        out += np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.6 + 0.9 * k)) / k ** 1.3
    hammer = np.random.default_rng(int(f)).standard_normal(len(t)) * np.exp(-t * 300) * 0.04
    att = np.minimum(1, t / 0.004)
    return (out + hammer) * att * vel


def bell(f, dur=3.0, vel=1.0):
    """Celesta: a pure tone with the bright, slightly out-of-tune partials of a struck bar."""
    t = np.arange(int(dur * SR)) / SR
    out = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.8)
           + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4.5)
           + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 8))
    return out * np.minimum(1, t / 0.002) * vel


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):  # one-pole; only used on short noise
        acc = (1 - a) * v + a * acc; y[i] = acc
    return y


def reverb(x, seconds=2.4, seed=3):
    """Stereo hall: convolution with two decaying noise tails, darker as they fade."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-t * 6.9 / seconds)
        ir = np.convolve(ir, np.ones(6) / 6, mode="same")  # soften the top
        ir[: int(0.012 * SR)] = 0                           # pre-delay
        m = len(x) + n
        size = 1 << (m - 1).bit_length()
        y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
        out.append(y / np.sqrt(np.sum(ir ** 2)) * 0.5)
    return np.stack(out, 1)


def eq(mix):
    """Clean low end for phone speakers: high-pass under 90 Hz, a little less of the 150-350 Hz mud."""
    f = np.fft.rfftfreq(len(mix), 1 / SR)
    g = (f / 90) ** 4 / (1 + (f / 90) ** 4)
    g *= 1 - 0.3 * np.exp(-((np.log2(np.maximum(f, 1) / 230)) ** 2) / 0.5)
    return np.stack([np.fft.irfft(np.fft.rfft(mix[:, c]) * g, len(mix)) for c in range(2)], 1)


def place(buf, sig, at, pan=0.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    buf[i:i + len(sig), 0] += sig * np.sqrt(0.5 * (1 - pan))
    buf[i:i + len(sig), 1] += sig * np.sqrt(0.5 * (1 + pan))


def score(duration, opening, landing, cues, outro, beat=0.6):
    rng = np.random.default_rng(11)
    dry = np.zeros((int(duration * SR), 2))

    # string pad: swells in under the opening piece, one chord every four beats from the landing
    starts = [0.0] + [landing + i * 4 * beat for i in range(64) if landing + i * 4 * beat < outro]
    for i, s in enumerate(starts):
        chord = CHORDS[0] if i == 0 else CHORDS[(i - 1) % 4]
        end = starts[i + 1] if i + 1 < len(starts) else outro
        dur = end - s + 0.9
        for j, note in enumerate(chord):
            v = pad_voice(hz(note), dur, rng) * env(int(dur * SR), 1.2 if i == 0 else 0.35, 0.9)
            place(dry, v * (0.16 if j else 0.2), s, pan=(-0.5, -0.15, 0.2, 0.5)[j])
    last = duration - outro
    for j, note in enumerate(LAST):  # the open chord under the seal
        v = pad_voice(hz(note), last, rng) * env(int(last * SR), 0.5, last * 0.6)
        place(dry, v * 0.15, outro, pan=(j / (len(LAST) - 1)) * 1.2 - 0.6)

    # celesta shimmer over the opening piece
    for k, (note, at) in enumerate((("F#6", 0.15), ("C#6", 0.45), ("D6", 0.75), ("B5", 1.05), ("F#5", 1.3))):
        place(dry, bell(hz(note), vel=0.34), at, pan=(-0.4, 0.4, -0.2, 0.3, 0.0)[k])

    # a breath of air as the piece shrinks into the board, settling on the landing
    n = int((landing - opening + 0.6) * SR)
    air = lowpass(rng.standard_normal(n), 2200)
    shape = np.concatenate([np.linspace(0, 1, int((landing - opening) * SR)) ** 2,
                            np.exp(-np.linspace(0, 5, n - int((landing - opening) * SR)))])
    place(dry, air * shape * 0.09, opening)
    place(dry, piano(hz("B2"), 3.0, 0.5) + piano(hz("B3"), 3.0, 0.35), landing)

    # piano: one note on every change of the board, rising through the chord
    for k, at in enumerate(cues):
        bar = int((at - landing + 1e-6) // (4 * beat)) % 4
        note = ARP[bar][k % 4]
        place(dry, piano(hz(note), vel=0.42 if k % 4 else 0.5), at, pan=0.3 if k % 2 else -0.3)
        if k % 4 == 0:  # the bass of the chord on its first beat
            place(dry, piano(hz(CHORDS[bar][0]), 3.0, 0.32), at)

    # the seal: low note and a celesta
    place(dry, piano(hz("D2"), 4.0, 0.5) + piano(hz("A3"), 4.0, 0.3), outro)
    place(dry, bell(hz("A5"), 4.0, 0.25), outro + 0.8, pan=0.2)
    place(dry, bell(hz("D6"), 4.0, 0.2), outro + 1.1, pan=-0.2)

    mix = eq(dry * 0.75 + reverb(dry.mean(1)) * 0.6)
    fade = int(0.8 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    mix = np.tanh(mix / np.abs(mix).max() * 1.1) * 0.89  # gentle limit, about -1 dB
    return mix


def write(path, mix):
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
