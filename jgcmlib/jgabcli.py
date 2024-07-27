import jgcmlib as jcm

import os
import subprocess

def pto_post_just_an_abc_file(filepath,musescore_bin = "musescore3",abc2midiExecutable = "abc2midi"):
  
  filebase = os.path.basename(filepath)
  output_dir=os.path.dirname(filepath)
  res_midi_filepath=os.path.join(output_dir, filebase.replace(".abc",".mid"))
  res_audio_filepath=os.path.join(output_dir, filebase.replace(".abc",".mp3"))
  res_musicsheet_svg_filepath=os.path.join(output_dir, filebase.replace(".abc",".svg"))
  
  jcm._convert_abc_2_midi(filepath, res_midi_filepath,abc2midiExecutable=abc2midiExecutable)
  jcm._convert_midi_to_mp3(res_midi_filepath, res_audio_filepath,musescore_bin=musescore_bin)
  jcm._convert_midi_2_score(filepath, res_musicsheet_svg_filepath,musescore_bin=musescore_bin)
  return res_musicsheet_svg_filepath, res_audio_filepath, res_midi_filepath

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Convert an ABC file to a MIDI file, a MP3 file and a SVG file')
  parser.add_argument('abcfile', type=str, help='The ABC file to convert')
  parser.add_argument('--musescore-bin', type=str, default="musescore3", help='The path to the musescore binary')
  parser.add_argument('--abc2midi-bin', type=str, default="abc2midi", help='The path to the abc2midi binary')
  args = parser.parse_args()
  res_musicsheet_svg_filepath, res_audio_filepath, res_midi_filepath =  pto_post_just_an_abc_file(args.abcfile,musescore_bin=args.musescore_bin,abc2midiExecutable=args.abc2midi_bin)
  print("res_musicsheet_svg_filepath: ", res_musicsheet_svg_filepath)
  print("res_audio_filepath: ", res_audio_filepath)
  print("res_midi_filepath: ", res_midi_filepath)

if __name__ == "__main__":
  main()