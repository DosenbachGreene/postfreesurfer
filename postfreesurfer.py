#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess

def run(settings):
    # Pull subject name from freesurfer import basename
    Subject = os.path.basename(settings['freesurfer_import_dir'])
    FinalTemplateSpace = os.path.join(settings['mpr_import_dir'],'{}{}.nii.gz'.format(Subject,settings['t1_suffix']))

    # Image locations and names
    T1wFolder = os.path.join(settings['output'],Subject,settings['input_atlas_name'])
    AtlasSpaceFolder = os.path.join(settings['output'],Subject,settings['input_atlas_name'])
    NativeFolder = "Native"
    FreeSurferFolder = os.path.join(settings['freesurfer_import_dir'])
    FreeSurferInput = '{}{}'.format(Subject,settings['t1_suffix'])
    T1wRestoreImage = '{}{}'.format(Subject,settings['t1_suffix'])
    T2wRestoreImage = '{}{}'.format(Subject,settings['t1_suffix'])
    AtlasTransform = os.path.join(settings['freesurfer_import_dir'],settings['input_atlas_name'],'zero')
    InverseAtlasTransform = os.path.join(settings['freesurfer_import_dir'],settings['input_atlas_name'],'zero')
    AtlasSpaceT1wImage = '{}{}'.format(Subject,settings['t1_suffix'])
    AtlasSpaceT2wImage = '{}{}'.format(Subject,settings['t1_suffix'])
    T1wImageBrainMask = "brainmask_fs"

    # Make directories and copy over relevant data (freesurfer output and mpr)
    print('Make directories and copy relevant files...')
    shutil.copytree(settings['freesurfer_import_dir'],os.path.join(settings['output'],Subject,settings['input_atlas_name']))
    shutil.copyfile(FinalTemplateSpace,os.path.join(settings['output'],Subject,'{}{}.nii.gz'.format(Subject,settings['t1_suffix'])))

    # Make some more folders
    try:
        os.mkdir(os.path.join(T1wFolder,NativeFolder))
    except FileExistsError:
        print('T1w Native directory already exists.')
    try:
        os.mkdir(os.path.join(AtlasSpaceFolder,'ROIs'))
    except FileExistsError:
        print('Atlas ROIs directory already exists.')
    try:
        os.mkdir(os.path.join(AtlasSpaceFolder,'Results'))
    except FileExistsError:
        print('Atlas Results directory already exists.')
    try:
        os.mkdir(os.path.join(AtlasSpaceFolder,NativeFolder))
    except FileExistsError:
        print('Atlas Native directory already exists.')
    try:
        os.mkdir(os.path.join(AtlasSpaceFolder,'fsaverage'))
    except FileExistsError:
        print('Atlas fsaverage directory already exists.')
    try:
        os.mkdir(os.path.join(AtlasSpaceFolder,'fsaverage_LR{}k'.format(settings['downsample'])))
    except FileExistsError:
        print('Atlas fsaverage downsample directory already exists.')

# Find c_ras offset between FreeSurfer surface/volume and genearte matrix to transform surfaces


if __name__ == '__main__':
    # parse arguments to command
    parser = argparse.ArgumentParser(description='This script runs the post freesurfer processing on a freesurfer dataset')
    parser.add_argument('--input_atlas_name', default='7112b_fs_LR', help='e.g., 7112b, DLBS268, MNI152 (will be used to name folder in output)')
    parser.add_argument('--freesurfer_import_dir', required=True, help='Input freesurfer path')
    parser.add_argument('--mpr_import_dir', required=True, help='Input MPR path')
    parser.add_argument('--output', required=True, help='Path to output directory')
    parser.add_argument('--downsample', default=32000, help='Downsampled mesh; default is 32000 (same as HCP)')
    parser.add_argument('--t1_suffix', default='_mpr_debias_avgT_111_t88', help='suffix for freesurfer T1w image')

    # parse argumaents into dict
    settings = vars(parser.parse_args())

    # Run main function
    run(settings)
