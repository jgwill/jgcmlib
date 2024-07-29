
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import jgcmlib as jcm
import json
import subprocess

def pto_post_just_an_abc_file(filepath,musescore_bin = "musescore3",abc2midiExecutable = "abc2midi"):
  
  filebase = os.path.basename(filepath)
  output_dir=os.path.dirname(filepath)
  res_midi_filepath=os.path.join(output_dir, filebase.replace(".abc",".mid"))
  res_audio_filepath=os.path.join(output_dir, filebase.replace(".abc",".mp3"))
  res_musicsheet_svg_filepath=os.path.join(output_dir, filebase.replace(".abc",".svg"))
  
  jcm._convert_abc_2_midi(filepath, res_midi_filepath,abc2midiExecutable=abc2midiExecutable)
  try:
    jcm._convert_midi_to_mp3(res_midi_filepath, res_audio_filepath,musescore_bin=musescore_bin)
  except:
    musescore_bin="musescore"
    jcm._convert_midi_to_mp3(res_midi_filepath, res_audio_filepath,musescore_bin=musescore_bin)
  jcm._convert_midi_2_score(filepath, res_musicsheet_svg_filepath,musescore_bin=musescore_bin)
  return res_musicsheet_svg_filepath, res_audio_filepath, res_midi_filepath

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Convert an ABC file to a MIDI file, a MP3 file and a SVG file')
  parser.add_argument('inputfile', type=str, help='The ABC or JSON file to convert')
  parser.add_argument('--musescore-bin', type=str, default="musescore3", help='The path to the musescore binary (default: musescore3)')
  parser.add_argument('--abc2midi-bin', type=str, default="abc2midi", help='The path to the abc2midi binary. (default: abc2midi)')
  args = parser.parse_args()
  
  abc_filename = args.inputfile
  #Check if we were given an .abc or a .json
  if not args.inputfile.endswith(".abc"):
    if args.inputfile.endswith(".json"):
      with open(args.inputfile, 'r') as f:
        data = json.load(f)
        if isinstance(data, list):
          generated_text = data[0]['generated_text']
        else:
          generated_text = data['generated_text']
        print("generated_text: ", generated_text)
        abc_extracted=jcm.extract_abc_from_text(generated_text)
        print("abc extracted:",abc_extracted)
        abc_filename=args.inputfile.replace(".json",".abc")
        with open(abc_filename, "w") as abc_file:
          abc_file.write(abc_extracted[0])
          
           
    #print("Only .abc files are supported for now.")
    #return
  
  res_musicsheet_svg_filepath, res_audio_filepath, res_midi_filepath =  pto_post_just_an_abc_file(abc_filename,musescore_bin=args.musescore_bin,abc2midiExecutable=args.abc2midi_bin)
  print("res_musicsheet_svg_filepath: ", res_musicsheet_svg_filepath)
  print("res_audio_filepath: ", res_audio_filepath)
  print("res_midi_filepath: ", res_midi_filepath)

if __name__ == "__main__":
  main()