# sound

WAV generators using only the standard library (`wave`, `struct`, `math`).

- `tones.py` — sine/square/saw/triangle tone to a WAV file.
- `melody.py` — render note-name scores (`C4 E4 G4:2 R`) to audio; plays Twinkle Twinkle.
- `chord.py` — mix major, minor and dominant-7th chords into one file.
- `envelope.py` — ADSR amplitude envelopes: a plucked note and a slow pad note.
- `noise.py` — white, brown (random walk) and rain-like noise.
- `arpeggio.py` — plucked minor-pentatonic arpeggio up and down.
- `vibrato.py` — sine tone with LFO pitch vibrato.
- `sweep.py` — exponential chirp from low to high frequency.
- `drum_beat.py` — synthesized kick/snare/hi-hat loop.
- `fm_bell.py` — FM synthesis bell with a decaying modulator.
- `stereo_pan.py` — stereo tone that pans left and right with equal-power gain.
- `bitcrush.py` — bit-depth and sample-rate reduction of a sweeping saw.
- `square_pwm.py` — square wave with a sweeping pulse-width (duty cycle).
- `karplus_strong.py` — plucked-string synthesis with a delay-line average.
- `tremolo.py` — LFO amplitude modulation of a C major chord.
- `flanger.py` — LFO-swept short delay mixed with a saw wave, with interpolated delay reads.
- `echo.py` — feedback echo with decaying repeats on a plucked note.
- `beating.py` — two close frequencies make audible amplitude beats.
- `reverse_reverb.py` — time-reversed plucks that swell into their attack.
- `ring_mod.py` — ring modulation of a tone by two carriers for metallic sidebands.
- `shepard_tone.py` — endlessly rising Shepard-tone illusion from octave-spaced sines.
