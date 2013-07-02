#!/usr/bin/python
from subprocess import *
import os
import sys, getopt
from os import chdir
def main(argv):
  opts, args = getopt.getopt(argv,"ht:v:",["type=","version="])
  for opt, arg in opts:
      if opt == '-h':
         print 'kerenelcompile.py -type <stable|mainline|lts> -v <version>'
         sys.exit()
      elif opt in ("-t", "--type"):
         kernel_type = arg
      elif opt in ("-v", "--version"):
         version = arg
  call("apt-get install git-core kernel-package fakeroot build-essential libncurses5-dev python-pip wget",shell=True)
  call("pip install feedparser sh",shell=True)
  from functions.functions import *
  from sh import cp,make,uname
  BUILD_DIR="/usr/src"
  if kernel_type == 'mainline':
    kernel_version=GetReleaseCandidateVersion()
  else:
    kernel_version=GetStableVersion()
  cpuCount=getCpuCount()
  print("cpu count:%s\n" % cpuCount)
  print("compiling kernel %s\n" % kernel_version)

  chdir(BUILD_DIR)
  call("wget --continue http://kernel.org/pub/linux/kernel/v3.x/linux-%s.tar.bz2" % kernel_version,shell=True)
  call("tar -jxf linux-%s.tar.bz2" % kernel_version,shell=True)
  chdir("linux-%s" % kernel_version)
  current_kernel=uname("-r").rstrip('\n')
  cp("/boot/config-%s"%current_kernel,"./.config")
  call("make nconfig",shell=True)
  call("make-kpkg clean",shell=True)
  new_env = os.environ.copy()
  os.environ["CONCURENCY_LEVEL"] = "%s"% cpuCount
  call("fakeroot make-kpkg --initrd --append-to-version=-vanillaice kernel_image kernel_headers" ,shell=True)
  call("make clean",shell=True)
  Install(kernel_version)

if __name__ =="__main__":
  main(sys.argv[1:])
