import json
import os
import time
import subprocess
import re
import tlid

def json_to_dict(json_str):
    return json.loads(json_str)

# IMPORT from CM app.py, by J.Guillaume Isabelle, 2024-06-20
def postprocess_abc(text, conversation_id="test",musescore_bin = "musescore3",use_tlider=True,workdir="tmp",prefix="",quiet=False,sc_namespace_suffix=None):
    abc2midiExecutable = "abc2midi"
    #check if musescore_bin is an executable, else use "musescore"
    #if not os.path.isfile(musescore_bin):
    #    musescore_bin = "musescore"
    
    os.makedirs(f"{workdir}/{conversation_id}", exist_ok=True)
    abc_pattern_extractor_str = r'(X:\d+\n(?:[^\n]*\n)+)'
    extracted_abc_notation_from_text = re.findall(abc_pattern_extractor_str, text+'\n')
    if not quiet:
      print(f'extract abc block: {extracted_abc_notation_from_text}')
    if extracted_abc_notation_from_text:
        
        
        sc_namespace_suffix = newsc_namespace_suffix(prefix,use_tlider=use_tlider) if not sc_namespace_suffix else sc_namespace_suffix # So we can define it in the function call
        
        # Write the ABC text to a temporary file
        res_abc_filepath = mkns_filepath(conversation_id, workdir, sc_namespace_suffix,"abc")
        with open(res_abc_filepath, "w") as abc_file:
            abc_file.write(extracted_abc_notation_from_text[0])
        
        # Convert abc notation to midi
        res_midi_filepath = mkns_filepath(conversation_id, workdir, sc_namespace_suffix,"mid")
        subprocess.run([abc2midiExecutable, str(res_abc_filepath), "-o", res_midi_filepath])
        
        # Convert abc notation to SVG
        res_musicsheet_svg_filepath = mkns_filepath(conversation_id, workdir, sc_namespace_suffix,"svg")
        res_audio_filepath = mkns_filepath(conversation_id, workdir, sc_namespace_suffix,"mp3")
        
        capture_output_of_command = True if not quiet else False
        
        subprocess.run([musescore_bin, "-o", res_musicsheet_svg_filepath, res_midi_filepath], capture_output=capture_output_of_command, text=True)
        subprocess.run([musescore_bin,"-o", res_audio_filepath, res_midi_filepath])
        
        # Fix the SVG file path (from ChatMusician, why do they do that ?)
        res_musicsheet_svg_filepath_fixed = mkns_filepath(conversation_id, workdir, sc_namespace_suffix,"svg","-1")
        
        if not quiet:
          print("-----------------------------")
          print(" FILES CREATED: ")
          print(res_musicsheet_svg_filepath_fixed)
          print(res_audio_filepath)
          print(res_abc_filepath)
          print(res_midi_filepath)
        #print_postprocess_abc_result_as_markdown(res_musicsheet_svg_filepath_fixed, res_audio_filepath,res_abc_filepath,render=False)
        return res_musicsheet_svg_filepath_fixed, res_audio_filepath,res_abc_filepath,res_midi_filepath
    else:
        return None, None 

def newsc_namespace_suffix(prefix, use_tlider=True):
  ts_or_tlid = _newts_suffix(use_tlider)
  _prefix = prefix + "_" if prefix else ""
  return _prefix + str(ts_or_tlid)

def _newts_suffix(use_tlider):
  return time.time() if not use_tlider else tlid.get_tlid()

def mkns_filepath(conversation_id, workdir, ts_namespace,ext,fn_suffix=""):
  return f"{workdir}/{conversation_id}/{ts_namespace}{fn_suffix}.{ext}"

def generate_markdown_output(res_musicsheet_svg_filepath_fixed, res_audio_filepath, res_abc_filepath,res_midi_filepath, line_prefix="* ",end_of_line_char = "\n",b4_musicscore="  "):
  if res_musicsheet_svg_filepath_fixed:
    abc_source = f"{line_prefix}[ABC source:]({res_abc_filepath})"
    midi_source=f"{line_prefix}[MIDI source:]({res_midi_filepath})"
    audio = f"{line_prefix}[Audio]({res_audio_filepath})"
    music_sheet = f"{b4_musicscore}![Music Sheet]({res_musicsheet_svg_filepath_fixed})"
    
    return abc_source + end_of_line_char+ midi_source + end_of_line_char+ audio + end_of_line_char +  music_sheet
  else:
    return "No ABC block found in the input text.",

def print_markdown_output(markdown_output):
  for line in markdown_output:
    print(line)

def print_postprocess_abc_result_as_markdown(res_musicsheet_svg_filepath_fixed, res_audio_filepath,res_abc_filepath,res_midi_filepath,line_prefix="* ",render=True):
  markdown_output = generate_markdown_output(res_musicsheet_svg_filepath_fixed, res_audio_filepath, res_abc_filepath,res_midi_filepath, line_prefix)
  print_markdown_output(markdown_output) if not render else print_markdown_output_in_jupyter(markdown_output)


def print_markdown_output_in_jupyter(markdown_output):
  from IPython.display import display, Markdown
  #markdown = "\n".join(markdown_output)
  display(Markdown(markdown_output))

def play_midi_in_notebook(res_mid_filepath):
  from music21 import midi
  mf = midi.MidiFile()
  path=res_mid_filepath
  mf.open(path) # path='abc.midi'
  mf.read()
  mf.close()
  s = midi.translate.midiFileToStream(mf)
  s.makeNotation(inPlace=True)
  s.secondsMap
  s.show('midi')


def play_mp3_in_notebook(res_audio_filepath):
  from IPython.display import Audio
  return Audio(res_audio_filepath,autoplay=True)


def get_generated_text_from_json(filepath):
  with open(filepath, 'r') as json_file:
    data = json.load(json_file)
    return data[0].get('generated_text', None)



# Get all json files in the directory './data/' + workdir
def get_json_files_list(workdir):
    json_files = []
    working_directory_path = './' + workdir
    print('Working directory path: ' + working_directory_path)
    for file in os.listdir(working_directory_path):
        if file.endswith('.json'):
            json_files.append(file)
    return json_files


def save_as_json(output,workdir,scprefix,sc_namespace_suffix,suffix=""):
  outdir=f"{workdir}"
  os.makedirs(outdir, exist_ok=True)
  filepath=f"{workdir}/{scprefix}{sc_namespace_suffix}{suffix}.json"
  with open(filepath, 'w') as f:
    json.dump(output, f, indent=4)
    print("written: ",filepath)
    return filepath
  return None




import requests
def run_inference_query(payload,api_url,headers = {
	"Accept" : "application/json",
	"Content-Type": "application/json" 
}):
  response = requests.post(api_url, headers=headers, json=payload)
  return response.json()
