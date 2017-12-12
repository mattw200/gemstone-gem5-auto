#!/usr/bin/env python

# Matthew J. Walker
# Created: 11 August 2017

# Generates all the bootscripts and iridis scripts. 
# Not as flexible, to be adapted as needed in future
# Assumes a local copy workload list and xu3 results

import create_bootscript

# freq is a preset as it needs to be supported by checkpoints
freqs_dict = {
        '200-800' : {
            'a7_freq' : "0.2GHz",
            'a15_freq' : "0.8GHz",
            'checkpoint_path_bko' : 'm5out-bko-latmem-cpt-l200-b800/cpt.5820172170000/'
        },
        '200-1400' : {
             'a7_freq' : "0.2GHz",
             'a15_freq' : '1.4GHz',
             'checkpoint_path_bko' : 'm5out-bko-latmem-cpt-l200-b1400/cpt.5364631158852/',
             'checkpoint_path_bk2' : 'm5out-bk2-latmem-cpt-l200-b1400/cpt.5307905196888/',
             'checkpoint_path_t01' : 'm5out-t01-cpt-l200-b1400/cpt.5265894988410/'
        },
        '400-1400' : {
            'a7_freq' : "0.4GHz",
            'a15_freq' : "1.4GHz",
            'checkpoint_path_bko' : 'm5out-bko-latmem-cpt-l400-b1400/cpt.4613099606766/'
        },
        '600-600' : {
            'a7_freq' : "0.6GHz",
            'a15_freq' : "0.6GHz",
            'checkpoint_path_bko' : 'm5out-bko-l600-b600/cpt.4553141051121',
            'checkpoint_path_m01' : 'm5out-checkpoint-latmem-hack-m01-600-600/cpt.4793771320885',
            'checkpoint_path_bk2' : 'm5out-bk2-latmem-cpt-l600-b600/cpt.4267197177115/',
            'checkpoint_path_t01' : 'm5out-t01-cpt-l600-b600/cpt.4227685111282/'
         },
        '1000-1000' : {
            'a7_freq' : "1.0GHz",
            'a15_freq' : "1.0GHz",
            'checkpoint_path_bko' :  'm5out-bko-l1000-b1000/cpt.3861983892000',
            'checkpoint_path_m01' : 'm5out-checkpoint-latmem-hack-m01-1000-1000/cpt.3939287714000',
            'checkpoint_path_1tb' :  'm5out-1tb-latmem-cpt-l1000-b1000/cpt.3853967257000/',
            'checkpoint_path_2tb' :  'm5out-2tb-latmem-cpt-l1000-b1000/cpt.3938100914000/',
            'checkpoint_path_1bp' :  'm5out-1bp-latmem-cpt-l1000-b1000/cpt.3903256446000/',
            'checkpoint_path_bo0' :  'm5out-bo0-latmem-cpt-l1000-b1000/cpt.3856764500000/',
            'checkpoint_path_2t0' :  'm5out-2t0-latmem-cpt-l1000-b1000/cpt.3845778248000/',
            'checkpoint_path_2t1' :  'm5out-2t1-latmem-cpt-l1000-b1000/cpt.3913028754000/',
            'checkpoint_path_bk2' :  'm5out-bk2-latmem-cpt-l1000-b1000/cpt.3645225168000/',
            'checkpoint_path_bk3' :  'm5out-bk3-latmem-cpt-l1000-b1000/cpt.3660202577000/',
            'checkpoint_path_t01' :  'm5out-t01-cpt-l1000-b1000/cpt.3706859598000/'
        },
        '1400-1800' : {
            'a7_freq' : "1.4GHz",
            'a15_freq' : "1.8GHz",
            'checkpoint_path_bko' :  'm5out-bko-l1400-b1800/cpt.3566806185128',
            'checkpoint_path_m01' : 'm5out-checkpoint-latmem-hack-m01-1400-1800/cpt.3655027154814',
            'checkpoint_path_bk2' : 'm5out-bk2-latmem-cpt-l1400-b1800/cpt.3383146836888/',
            'checkpoint_path_t01' :  'm5out-t01-cpt-l1400-b1800/cpt.3373272000432/'
        }
}

models_list = ['bko','m01','1tb', '2tb', '1bp', 'bo0', '2t0','2t1','bk2','bk3']

def create_iridis_run_script(checkpoint_dir, little_clock, big_clock, bootscript_path, m5out_dir, wall_hours, run_script_filepath,gem5_dir):
    if int(wall_hours) >= 60:
        raise ValueError("Wall time ("+str(int(wall_hours))+" must be less than 60")
    script_text = "#!/bin/bash\n"
    if os.path.isfile('mjw-only.txt'): # custom - for a specific setup
        script_text += "#PBS -l walltime={0:0>2}".format(int(wall_hours))+":00:00\n"
        with open('mjw-only.txt', 'r') as f:
            script_text += f.read()
        f.closed
        script_text += "module load python\n"
        script_text += "module load gcc/4.9.1\n"
    script_text += "cd "+gem5_dir+"\n"
    script_text += "build/ARM/gem5.opt --outdir="+m5out_dir+"  configs/example/arm/fs_bigLITTLE.py --restore-from="+checkpoint_dir+" --caches --little-cpus 4 --big-cpus 4 --big-cpu-clock "+big_clock+" --little-cpu-clock "+little_clock+" --bootscript "+bootscript_path+" --cpu-type exynos\n"
    script_text += 'echo "Finished iridis run script"\n'
    with open(run_script_filepath, "w") as f:
        f.write(script_text)
    f.close

if __name__=='__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', dest='gem5_dir', required=True, \
               help="The gem5 directory")
    parser.add_argument('--hours', dest='hours', required=False, \
               help="Wall time (hours)")
    parser.add_argument('--clean', dest='clean',action='store_true', required=False, \
               help="Cleans")
    parser.add_argument('--preset-list', dest='preset_list', required=True, \
            help="List of which presets to use. Available presets: " \
            +str(create_bootscript.get_presets()))
    parser.add_argument('--model', dest='model', required=True, \
            help="Which gem5 mode to use (i.e. checkpoint). Avail.:" \
            +str(models_list))
    parser.add_argument('--freq', dest='freq', required=True, \
            help="Which freq to use (i.e. checkpoint). Avail.:" \
            +str(freqs_dict))
    args=parser.parse_args()

    if not args.hours:
        args.hours = 58

    gem5_auto_dir = os.path.join(args.gem5_dir, 'gem5-auto')
    bootscripts_dir = os.path.join(gem5_auto_dir, 'bootscripts')
    runscripts_dir = os.path.join(gem5_auto_dir, 'runscripts')

    if not os.path.exists(gem5_auto_dir):
        os.makedirs(gem5_auto_dir)    
    if not os.path.exists(bootscripts_dir):
        os.makedirs(bootscripts_dir)    
    if not os.path.exists(runscripts_dir):
        os.makedirs(runscripts_dir)    

    if args.clean:
        import shutil
        import sys
        print("Will remove: "+gem5_auto_dir)
        raw_input("Press Enter to continue...")
        shutil.rmtree(gem5_auto_dir) 
        run_all_files = [x for x in os.listdir(args.gem5_dir) if x.startswith('run-all-') and x.endswith('.sh')]
        print("About to delete the following files:")
        print(run_all_files)
        raw_input("Press Enter to continue...")
        for run_file in run_all_files:
            os.remove(os.path.join(args.gem5_dir, run_file))
        print("Nice and clean")
        sys.exit()
        
    args.preset_list = args.preset_list.split(',')

    if not args.model in models_list:
        print("Error: "+args.model+" not in models list")
        sys.exit()

    print("Checkpoint selection: "+freqs_dict[args.freq]['checkpoint_path_'+args.model]+".")

    '''
    python create_bootscript.py --list ../workloads-small.config.armv7 --mask 4,5,6,7 --xu3-results ../../powmon-experiment-060-high-f/pmc-events-log.out-analysed.csv  --preset "parmibench"
    '''
    this_file_dir = dir_path = os.path.dirname(os.path.realpath(__file__))
    workload_list_filepath = os.path.join(this_file_dir, '../workloads-small.config.armv7')
    xu3_results_filepath = os.path.join(this_file_dir, 'xu3-results.example.csv')

    experiment_label = '000'
    with open(os.path.join(this_file_dir, 'gem5-auto-counter'), 'r') as f:
        experiment_label = "{0:0>3}".format(int(f.read()))
    f.closed
    with open(os.path.join(this_file_dir, 'gem5-auto-counter'), 'w') as f:
        f.write(str(int(experiment_label)+1))
    f.closed

    run_all_script  = "#!/bin/bash\n"
    for preset in args.preset_list:
        #for big and for little
        preset = preset.strip()
        core_masks = ['0,1,2,3','4,5,6,7']
        for mask in core_masks:
            filename_prefixes = experiment_label+'-'+args.model+'-'+args.freq+'-'+mask.replace('-','_')+'-'+preset
            bootscript_filepath = os.path.join(bootscripts_dir,filename_prefixes+'.rcS')
            runscript_filepath = os.path.join(runscripts_dir, filename_prefixes+'.sh')
            m5out_dir_path = os.path.join(args.gem5_dir, 'gem5out-'+filename_prefixes)
            create_bootscript.create_rcs_from_preset(workload_list_filepath, xu3_results_filepath, mask, preset, bootscript_filepath)
            create_iridis_run_script(
                    freqs_dict[args.freq]['checkpoint_path_'+args.model],
                    freqs_dict[args.freq]['a7_freq'],
                    freqs_dict[args.freq]['a15_freq'],
                    bootscript_filepath,
                    m5out_dir_path,
                    args.hours,
                    runscript_filepath,
                    args.gem5_dir
                )
            run_all_script += "qsub "+runscript_filepath+"\n"
    with open(os.path.join(args.gem5_dir, 'run-all-'+experiment_label+'.sh'), 'w') as f:
        f.write(run_all_script)
    f.closed


