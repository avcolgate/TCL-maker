from logic import Liberty
import copy
import os

def get_net_transition(lib_dir):
    data_files = []
    lib = []
    tran_arr = []
    index_1 = ''
    data = os.listdir(lib_dir)
    for count, file in enumerate(data):
        lib = copy.deepcopy(Liberty.load(lib_dir + '/' + data[count]))
    data_files.append(lib)

    for item in data_files:
        index_1 = lib.lu_table_template['delay_cell'].index_1  # type: ignore

    for tran in index_1.split(','):
        tran_arr.append(float(tran))

    return tran_arr
