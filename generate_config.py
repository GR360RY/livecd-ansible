#!/usr/bin/env python
import os
import sys
import argparse

from jinja2 import Environment, FileSystemLoader

cmdargs = str(sys.argv)

template_folder='templates'
default_template='centos6-mini.ks.j2'

config_file_name=str(sys.argv[1])

script_path, script_filename = os.path.split(os.path.abspath(__file__))
template_folder=os.path.join(script_path,template_folder)

config_name=os.path.splitext(config_file_name)[0]

# Variable dictionary for jinja2 template
template_dictionary = {}

template_dictionary['work_dir'] = script_path
template_dictionary['config_name'] = config_name

env = Environment(loader=FileSystemLoader(template_folder))
template = env.get_template(default_template)
output_from_parsed_template = template.render(template_dictionary)

config_name_kickstart = config_name + '.ks'

with open(config_name_kickstart,"wb") as fh:
  fh.write(output_from_parsed_template)