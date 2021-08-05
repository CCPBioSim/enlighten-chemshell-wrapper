import os
import shutil
import subprocess
import os


def check_file(name, message=None):
    if not os.path.isfile(name):
        raise FileNotFoundError(message or "File " + name + " not found.")


def dump_to_file(file, contents):
    with open(file, 'w') as f:
        f.write(contents)


def parse_template(template, params):
    with open(template) as f:
        return f.read().format(**params)


def set_working_directory(working_directory):
    if os.path.exists(working_directory):
        shutil.rmtree(working_directory)
    os.makedirs(working_directory)
    os.chdir(working_directory)


def file_in_paths(filename, path_list):
    for path in path_list:
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            return full_path
    return None


def merge_dicts_of_dicts(dict1, dict2):
    return {key: {**dict1.get(key, {}), **dict2.get(key, {})}
            for key in set(dict1.keys()) | set(dict2.keys())}


def run_in_shell(command, output):
    """
    Runs given command in the shell, redirecting both STDOUT and STDERR to
    the output file. Waits for the command to finish.
    """
    with open(output, 'w') as f:
        proc = subprocess.Popen(command, shell=True, stdout=f,
                                stderr=subprocess.STDOUT)
        proc.wait()


def run_at_path(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    exit_code = run(command)
    os.chdir(cwd)
    return exit_code


def run(command):
    out = open('out', 'w')
    err = open('err', 'w')
    try:
        subprocess.run(command.split(), stdout=out, stderr=err, check=True)
        exit_code = 0
    except subprocess.CalledProcessError as e:
        exit_code = e.returncode
    out.close()
    err.close()
    return exit_code

def get_amber_charges(parmtop):
    # This function is to parse an AMBER top file to get a list of partial charges for all the atoms.
    infile = open(parmtop)

    copy = False
    charges = []
    for line in infile:
       if line.startswith("%FLAG CHARGE"):
          copy = True

       elif line.startswith("%FLAG ATOMIC_NUMBER"):
          copy = False

       elif copy:
          if line.startswith("%FORMAT"):
            print("not printing")
          else:
            charge_list = str.split(line)
          # AMBER charges need to be divided by 18.2223 to get the right units for ChemShell
            linecharges = [(float(i) / 18.2223) for i in charge_list]
            charges.extend(linecharges)

    infile.close()
    return charges
