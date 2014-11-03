#!/usr/bin/python
import argparse
import sys
import os
import time
import traceback
import sys
import ctypes
import subprocess
from subprocess import Popen, PIPE
import shutil
from optparse import OptionParser
from biokbase.workspace.client import Workspace
import urllib
import urllib2
import re
import json

desc1 = '''
NAME
      trns_transform_KBaseGenomes.GBK-to-KBaseGenomes.Genome -- convert CSV format to Pair for Transform module (version 1.0)

SYNOPSIS      
      
'''

desc2 = '''
DESCRIPTION
  trns_transform_KBaseGenomes.GBK-to-KBaseGenomes.Genome convert input GBK (GenBank) format to KBaseGenomes.Genome
  json string file for KBaseGenomes module.

  TODO: It will support KBase log format.
'''

desc3 = '''
EXAMPLES
      CSV conversion case
      > trns_transform_KBaseGenomes.GBK-to-KBaseGenomes.Genome -i input_file.csv -o ouput_file.json
      
SEE ALSO
      trns_transform_hndlr

AUTHORS
First Last.
'''

impt = "$KB_TOP/lib/jars/kbase/genomes/kbase-genomes-20140411.jar:$KB_TOP/lib/jars/kbase/common/kbase-common-0.0.6.jar:$KB_TOP/lib/jars/jackson/jackson-annotations-2.2.3.jar:$KB_TOP/lib/jars/jackson/jackson-core-2.2.3.jar:$KB_TOP/lib/jars/jackson/jackson-databind-2.2.3.jar:$KB_TOP/lib/jars/kbase/transform/GenBankTransform.jar"

mc = 'us.kbase.genbank.test.CommandLineTest'

def transform (args) :
#    try:
      kb_top = os.environ.get('KB_TOP', '/kb/deployment')
      cp = impt.replace('$KB_TOP', kb_top);

      in_dir = re.sub(r'/[^/]*$','', args.in_file)
      out_fn = re.sub(r'^.*/','', args.in_file)
      out_fn = re.sub(r'.gbk$','.jsonp', out_fn)
      if not out_fn.endswith(".jsonp"): out_fn = "{}.jsonp".format(out_fn)

      tcmd_lst = ['java', '-cp', cp, mc, in_dir]


      print in_dir
      print out_fn

      p1 = Popen(tcmd_lst, stdout=PIPE)
      out_str = p1.communicate()

      # print output message for error tracking
      if out_str[0] is not None : print out_str[0]
      if out_str[1] is not None : print >> sys.stderr, out_str[1]
     
     
      if p1.returncode != 0: 
          exit(p1.returncode) 

      # success
      if(args.cs is not None) :
        with open(out_fn, 'r') as gif:
          f = json.loads(gif.read())
          f['contigset_ref'] = args.cs
          with open(args.out_file, 'w') as outfile:
            json.dump(f, outfile)
      else:
        with open(out_fn, 'r') as gif:
          f = json.loads(gif.read())
          del f['contigset_ref'] 
          with open(args.out_file, 'w') as outfile:
            json.dump(f, outfile)
        #shutil.move(out_fn, args.out_file)

#    except:
#      raise Exception("Error writing to {}".format(args.out_file))

if __name__ == "__main__":
    # Parse options.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, prog='trns_transform_KBaseGenomes.GBK-to-KBaseGenomes.Genome', epilog=desc3)
    parser.add_argument('-i', '--in_file', help='Input file', action='store', dest='in_file', default=None, required=True)
    parser.add_argument('-o', '--out_file', help='Output file', action='store', dest='out_file', default=None, required=True)
    parser.add_argument('-c', '--contigset_ref', help='Contigset reference', action='store', dest='cs', default=None, required=False)
    usage = parser.format_usage()
    parser.description = desc1 + '      ' + usage + desc2
    parser.usage = argparse.SUPPRESS
    args = parser.parse_args()

    # main loop
    transform(args)
    exit(0);