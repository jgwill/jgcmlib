
import sys
import os
import argparse
from time import sleep
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
  import jgcmlib as jcm
except:
  import __init__ as jcm
import json
import subprocess

def pto__convert_midi_2_score(filepath, musescore_bin = "musescore3",ext="svg"):
  filebase = os.path.basename(filepath)
  output_dir=os.path.dirname(filepath)
  res_musicsheet_svg_filepath=os.path.join(output_dir, filebase.replace(".mid",".svg"))
  res_musicsheet_svg_filepath=res_musicsheet_svg_filepath+".svg"
  res_musicsheet_svg_filepath=res_musicsheet_svg_filepath.replace(".svg.svg",".svg")
  
  # Convert midi to musicsheet
    
  try:
    res_musicsheet_svg_filepath=jcm._convert_midi_2_score(filepath, res_musicsheet_svg_filepath,musescore_bin=musescore_bin,ext=ext)
  except subprocess.CalledProcessError as e:
    print("Error: Could not convert the midi file to musicsheet. ", e)
    return
  return res_musicsheet_svg_filepath
 
def pto_post_just_an_abc_file(filepath,musescore_bin = "musescore3",abc2midiExecutable = "abc2midi",score_ext="svg"):
  
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
    try:
      jcm._convert_midi_to_mp3(res_midi_filepath, res_audio_filepath,musescore_bin=musescore_bin)
    except:
      print("Error: Could not convert the midi file to mp3. Something with musescore is not right.")
      sleep(2)
      return
      #raise Exception("Error: Could not convert the midi file to mp3. Something with musescore is not right.")
  score_path=jcm._convert_midi_2_score(filepath, res_musicsheet_svg_filepath,musescore_bin=musescore_bin,ext=score_ext)
  return score_path, res_audio_filepath, res_midi_filepath


def main_mid2score():
  args = create_arg_parser(argparse)
  res_musicsheet_svg_filepath = pto__convert_midi_2_score(args.inputfile,musescore_bin=args.musescore_bin)
  print("res_musicsheet_svg_filepath: ", res_musicsheet_svg_filepath)

def main():
  args = create_arg_parser(argparse)
  
  abc_filename = args.inputfile
  #Check if we were given an .abc or a .json
  if not args.inputfile.endswith(".abc"):
    if args.inputfile.endswith(".json"):
      try:          
        abc_filename = extract_abc_from_json_to_abc_file(args.inputfile)
      except:
        print("Error: Could not read the json file.")
        return
          
           
    #print("Only .abc files are supported for now.")
    #return
  
  res_musicsheet_svg_filepath, res_audio_filepath, res_midi_filepath =  pto_post_just_an_abc_file(abc_filename,musescore_bin=args.musescore_bin,abc2midiExecutable=args.abc2midi_bin, score_ext=args.ext)
  print("res_musicsheet_svg_filepath: ", res_musicsheet_svg_filepath)
  print("res_audio_filepath: ", res_audio_filepath)
  print("res_midi_filepath: ", res_midi_filepath)

def extract_abc_from_json_to_abc_file(inputfile):
    with open(inputfile, 'r') as f:
      data = json.load(f)
      if isinstance(data, list):
        generated_text = data[0]['generated_text']
      else:
        generated_text = data['generated_text']
      print("generated_text: ", generated_text)
      txt_filename=inputfile.replace(".json",".txt")
      with open(txt_filename, "w") as txt_file:
        txt_file.write(generated_text)
          
      abc_extracted=jcm.extract_abc_from_text(generated_text)
          #if abc_extracted list is empty  exit program
      if len(abc_extracted) == 0 or not abc_extracted:
        print("Error: Could not extract the abc notation from the json file.")
        print(data)
        raise Exception("Error: Could not extract the abc notation from the json file.")
      print("abc extracted:",abc_extracted)
      abc_filename=inputfile.replace(".json",".abc")
      try:
        with open(abc_filename, "w") as abc_file:
          abc_file.write(abc_extracted[0])
      except:
        print("Error: Could not write the abc file.  There might just did not have any abc notation in the json.")
        raise Exception("Error: Could not write the abc file.  There might just did not have any abc notation in the json.")
    return abc_filename

def create_arg_parser(argparse):
    parser = argparse.ArgumentParser(description='Convert an ABC file to a MIDI file, a MP3 file and a SVG file.  Or convert a MIDI file to a SVG file.')
    parser.add_argument('inputfile', type=str, help='The ABC or JSON or MID file to convert')
    parser.add_argument('--musescore-bin', type=str, default="musescore3", help='The path to the musescore binary (default: musescore3)')
    parser.add_argument('--abc2midi-bin', type=str, default="abc2midi", help='The path to the abc2midi binary. (default: abc2midi)')
    #score extension convertion, default is svg, support for png,jpg using ImageMagick
    parser.add_argument('-X','--ext', type=str, default="svg", help='The extension of the score file to convert to. (default: svg)')
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
  main()