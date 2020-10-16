from builtins import range
import datetime
import numpy as np
import time
# Todo: polish docstrings


def list_del_indices(mylist,indices):
    """
    iteratively remove elements of a list by indices
    Parameters
    ----------
    mylist : list
        the list of elements of interest

    indices : list
        the list of indices of elements that should be removed

    Returns
    -------
    list
        the reduced mylist entry

    """
    for index in sorted(indices, reverse=True):
        del mylist[index]
    return mylist


def std_datetime_str(mode='datetime'):
    """ human readable data and time
        This function gives out the formatted time as a standard string, i.e., YYYY-MM-DD hh:mm:ss.
    """
    if mode == 'datetime':
        return str(datetime.datetime.now())[:19]
    elif mode == 'date':
        return str(datetime.datetime.now())[:10]
    elif mode == 'time':
        return str(datetime.datetime.now())[11:19]
    elif mode == 'datetime_ms':
        return str(datetime.datetime.now())
    elif mode == 'time_ms':
        return str(datetime.datetime.now())[11:]
    else:
        msg = 'The mode value must be one of datetime, date, time, datetime_ms, or time_ms.'
        raise ValueError(msg)


def tot_exec_time_str(time_start):
    """ execution time
        This function gives out the formatted time string.
    """
    time_end = time.time()
    exec_time = time_end-time_start
    tmp_str = "execution time: %0.2fs (%dh %dm %0.2fs)" %(exec_time, exec_time/3600, (exec_time%3600)/60,(exec_time%3600)%60)
    return tmp_str


# def slurm_script_exclusive(pyscript_file,nnodes=1,input_slurm_script=None,output_slurm_script='script.slurm'):
#     """(slurmjob)
#     make the slurm script based on exclusive selection of cores per nodes.
#
#     Parameters
#     ----------
#     pyscript_file: string
#         This is the python script that includes nn_dsgd functions and you are
#         going to run on the cluster. If you are using the cheml python script
#         maker this parameter is going to be the name of the final output file.
#
#     nnodes: int, optional(default = 1)
#         number of available empty nodes in the cluster.
#
#     input_slurm_script: string, optional(default = None)
#         The file path to the prepared slurm script. We also locate place of
#         --nodes and -np in the script and make sure that provided numbers are
#         equal to number of nodes(nnodes). Also, the exclusive option must be
#         included in the script to have access to an entire node.
#
#     output_slurm_script: string, optional(default = 'script.slurm')
#         The path and name of the slurm script file that will be saved after
#         changes by this function.
#
#     Returns
#     -------
#     The function will write a slurm script file with the filename passed by
#     output_slurm_script.
#     """
#     if not input_slurm_script:
#         file = ['#!/bin/sh\n', '#SBATCH --time=99:00:00\n', '#SBATCH --job-name="nn"\n', '#SBATCH --output=nn.out\n', '#SBATCH --clusters=chemistry\n', '#SBATCH --partition=beta\n', '#SBATCH --account=pi-hachmann\n', '#SBATCH --exclusive\n', '#SBATCH --nodes=1\n', '\n', '# ====================================================\n', '# For 16-core nodes\n', '# ====================================================\n', '#SBATCH --constraint=CPU-E5-2630v3\n', '#SBATCH --tasks-per-node=1\n', '#SBATCH --mem=64000\n', '\n', '\n', 'echo "SLURM job ID         = "$SLURM_JOB_ID\n', 'echo "Working Dir          = "$SLURM_SUBMIT_DIR\n', 'echo "Temporary scratch    = "$SLURMTMPDIR\n', 'echo "Compute Nodes        = "$SLURM_NODELIST\n', 'echo "Number of Processors = "$SLURM_NPROCS\n', 'echo "Number of Nodes      = "$SLURM_NNODES\n', 'echo "Tasks per Node       = "$TPN\n', 'echo "Memory per Node      = "$SLURM_MEM_PER_NODE\n', '\n', 'ulimit -s unlimited\n', 'module load intel-mpi\n', 'module load python\n', 'module list\n', 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/projects/hachmann/packages/Anaconda:/projects/hachmann/packages/rdkit-Release_2015_03_1:/user/m27/pkg/openbabel/2.3.2/lib\n', 'date\n', '\n', '\n', 'echo "Launch job"\n', 'export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so\n', 'export I_MPI_FABRICS=shm:tcp\n', '\n', 'mpirun -np 2 python test.py\n']
#         file[8] = '#SBATCH --nodes=%i\n'%nnodes
#         file[-1] = 'mpirun -np %i python %s\n' %(nnodes,pyscript_file)
#     else:
#         file = open(input_slurm_script,'r')
#         file = file.readlines()
#         exclusive_flag = False
#         nodes_flag = False
#         np_flag = False
#         for i,line in enumerate(file):
#             if '--exclusive' in line:
#                 exclusive_flag = True
#             elif '--nodes' in line:
#                 nodes_flag = True
#                 ind = line.index('--nodes')
#                 file[i] = line[:ind]+'--nodes=%i\n'%nnodes
#             elif '-np' in line:
#                 np_flag = True
#                 ind = line.index('--nodes')
#                 file[i] = line[:ind]+'--nodes=%i\n'%nnodes
#         if not exclusive_flag:
#             file = file[0] + ['#SBATCH --exclusive\n'] + file[1:]
#             msg = "The --exclusive option is not available in the slurm script. We added '#SBATCH --exclusive' to the first of file."
#             warnings.warn(msg,UserWarning)
#         if not nodes_flag:
#             file = file[0] + ['#SBATCH --nodes=%i\n'%nnodes] + file[1:]
#             msg = "The --nodes option is not available in the slurm script. We added '#SBATCH --nodes=%i' to the first of file."%nnodes
#             warnings.warn(msg,UserWarning)
#         if not np_flag:
#             file.append('mpirun -np %i python %s\n'%(nnodes,pyscript_file))
#             msg = "The -np option is not available in the slurm script. We added 'mpirun -np %i python %s'to the end of file."%(nnodes,pyscript_file)
#             warnings.warn(msg,UserWarning)
#
#     script = open(output_slurm_script,'w')
#     for line in file:
#         script.write(line)
#     script.close()


def chunk(xs, n, X=None, Y=None):
    """
    X and Y must be numpy array
    n is the number of chunks (#total_batch).

    Examples
    --------
    it = chunk ( range(len(X), n, X, Y)
    X_chunk, y_chunk = next(it)

    """
    ys = list(xs)
    # random.shuffle(ys)
    size = len(ys) // n
    leftovers= ys[size*n:]
    for c in range(n):
        if leftovers:
           extra = [ leftovers.pop() ]
        else:
           extra = []
        if isinstance(X,np.ndarray):
            if isinstance(Y, np.ndarray):
                yield X[ys[c*size:(c+1)*size] + extra], Y[ys[c*size:(c+1)*size] + extra]
            else:
                yield X[ys[c * size:(c + 1) * size] + extra]
        else:
            yield ys[c*size:(c+1)*size] + extra


# def choice(X, Y=None, n=0.1, replace=False):
#     """
#     Generates a random sample from a given 1-D array. Bassicaly same as np.random.choice with pre- and post-processing
#      steps. Sampling without replacement.
#     :param X: 1-D array-like
#         A random sample will be generated from its elements.
#     :param Y: 1-D array-like, optional (default = None)
#         A random sample will be generated from its elements.
#     :param n: int or float between zero and one, optional (default = 0.1)
#         size of sample
#     :param replace: boolean, default=False
#         whether the sample is with or without replacement
#     :return: a_out: 1-D array-like
#                 the array of out of sample elements
#     :return: a_sample: 1-D array-like, shape (size,)
#                 the sample array
#     """
#     if not isinstance(n,int):
#             n = int(n*len(X))
#     ind_sample = np.random.choice(len(X),n,replace=replace)
#     ind_out = np.array([i for i in xrange(len(X)) if i not in ind_sample])
#     X_sample = X[ind_sample]
#     X_out = X[ind_out]
#     if isinstance(Y,np.ndarray):
#         if len(Y) != len(X):
#             raise Exception('X and Y must be same size')
#         Y_sample = Y[ind_sample]
#         Y_out = Y[ind_out]
#     else:
#         Y_sample = None
#         Y_out = None
#     return X_out, X_sample, Y_out, Y_sample
#
# def return2Dshape(shape):
#     if len(shape) == 2:
#         return shape
#     elif len(shape) == 1:
#         return (shape[0],None)
#     else:
#         raise Exception('input dimension is greater than 2')


def bool_formatter(bool_value):
    """
    convert Python boolean to json/xml format of boolean

    Parameters
    ----------
    bool_value: bool
        the boolean value that needs to be converted

    Returns
    -------
    str
        either "true" or "false"

    """
    if isinstance(bool_value, bool):
        if bool_value:
            return("true")
        else:
            return("false")
    else:
        msg = "bool_value must be a boolean"
        raise ValueError(msg)


def padaxis(array, new_size, axis, pad_value=0, pad_right=True):
    """
    Padds one axis of an array to a new size

    This is just a wrapper for np.pad, more usefull when only padding a single axis

    Parameters
    ----------
    array: array
        the array to pad

    new_size: int
        the new size of the specified axis

    axis: int
        axis along which to pad

    pad_value: float or int, optional(default=0)
        pad value

    pad_right: bool, optional(default=True)
        if True pad on the right side, otherwise pad on left side

    Returns
    -------
        padded_array: np.array

    """
    add_size = new_size - array.shape[axis]
    assert add_size >= 0, 'Cannot pad dimension {0} of size {1} to smaller size {2}'.format(axis, array.shape[axis], new_size)
    pad_width = [(0,0)]*len(array.shape)

    #pad after if int is provided
    if pad_right:
        pad_width[axis] = (0, add_size)
    else:
        pad_width[axis] = (add_size, 0)

    return np.pad(array, pad_width=pad_width, mode='constant', constant_values=pad_value)

def mol_shapes_to_dims(mol_tensors=None, mol_shapes=None):
    ''' Helper function, returns dim sizes for molecule tensors given tensors or
    tensor shapes
    '''

    if not mol_shapes:
        mol_shapes = [t.shape for t in mol_tensors]

    num_molecules0, max_atoms0, num_atom_features = mol_shapes[0]
    num_molecules1, max_atoms1, max_degree1, num_bond_features = mol_shapes[1]
    num_molecules2, max_atoms2, max_degree2 = mol_shapes[2]

    num_molecules_vals = [num_molecules0, num_molecules1, num_molecules2]
    max_atoms_vals = [max_atoms0, max_atoms1, max_atoms2]
    max_degree_vals = [max_degree1, max_degree2]

    assert len(set(num_molecules_vals))==1, 'num_molecules does not match within tensors (found: {})'.format(num_molecules_vals)
    assert len(set(max_atoms_vals))==1, 'max_atoms does not match within tensors (found: {})'.format(max_atoms_vals)
    assert len(set(max_degree_vals))==1, 'max_degree does not match within tensors (found: {})'.format(max_degree_vals)

    return max_atoms1, max_degree1, num_atom_features, num_bond_features, num_molecules1