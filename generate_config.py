#!/usr/bin/env python
import argparse
import os
import sys
import yaml

from jinja2 import Environment, FileSystemLoader

cmdargs = str(sys.argv)
config_file_name=str(sys.argv[1])

template_folder='templates'
default_template='centos6-mini.ks.j2'

script_path, script_filename = os.path.split(os.path.abspath(__file__))
template_folder=os.path.join(script_path,template_folder)

config_name=os.path.splitext(config_file_name)[0]

with open(config_file_name) as config_file_name_fh:
  dataMap = yaml.load(config_file_name_fh)
  template_dictionary = dataMap[0]['vars']

template_dictionary['work_dir'] = script_path
template_dictionary['config_name'] = config_name

env = Environment(loader=FileSystemLoader(template_folder))
template = env.get_template(default_template)
output_from_parsed_template = template.render(template_dictionary)

config_name_kickstart = config_name + '.ks'

with open(config_name_kickstart,"wb") as fh:
  fh.write(output_from_parsed_template)
