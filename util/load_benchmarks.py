import csv
import os
from .benchmark_parser import BenchmarkParser, WorkerBenchmarkParser

def filter(data, bounds : dict[str, tuple[float,float]]) -> list[str]:
    # data 第一行为表头，后续行为实例特征。
    header = data[0]
    data = data[1:]
    # count 用于统计每个实例满足了多少个过滤条件。
    count = dict()
    for bound in bounds:
        index = header.index(bound)
        lb = bounds[bound][0]
        ub = bounds[bound][1]
        for instance in data:
            if float(instance[index]) >= lb and float(instance[index]) <= ub:
                if instance[0] not in count:
                    count[instance[0]] = 0
                count[instance[0]] += 1
    # 仅保留满足全部 bounds 的实例。
    result = [instance for instance in count if count[instance] == len(bounds)]
    return result

def _load(path : str, bounds : dict[str, tuple[float,float]], worker : bool =False) -> dict:
    # 根据 CSV 特征筛选实例名；若不筛选则直接枚举目录。
    if filter:
        data = []
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        selected_instances = filter(data, bounds)
    else:
        selected_instances = os.listdir('instances/Instances_FJSSP') if not worker else os.listdir('instances/Example_Instances_FJSSP-WF')

    # 逐实例解析并返回 encoding 字典：{instance_name: Encoding}。
    result = dict()
    for instance in selected_instances:
        if worker:
            parser = WorkerBenchmarkParser()
            instance_path = r'instances/Example_Instances_FJSSP-WF'
            instance_path = instance_path + f'/{instance}.fjs'
        else:
            parser = BenchmarkParser()
            instance_path = r'instances/Instances_FJSSP'
            # 按实例名前缀映射到对应数据源子目录。
            if instance.lower().startswith('be'):
                instance_path += f'/0_BehnkeGeiger/{instance}.fjs'
            elif instance.lower().startswith('br'):
                instance_path += f'/1_Brandimarte/{instance}.fjs'
            elif instance.lower().startswith('hurink_s'):
                instance_path += f'/2a_Hurink_sdata/{instance}.fjs'
            elif instance.lower().startswith('hurink_e'):
                instance_path += f'/2b_Hurink_edata/{instance}.fjs'
            elif instance.lower().startswith('hurink_r'):
                instance_path += f'/2c_Hurink_rdata/{instance}.fjs'
            elif instance.lower().startswith('hurink_v'):
                instance_path += f'/2d_Hurink_vdata/{instance}.fjs'
            elif instance.lower().startswith('dp'):
                instance_path += f'/3_DPpaulli/{instance}.fjs'
            elif instance.lower().startswith('ch'):
                instance_path += f'/4_ChambersBarnes/{instance}.fjs'
            elif instance.lower().startswith('ka'):
                instance_path += f'/5_Kacem/{instance}.fjs'
            elif instance.lower().startswith('fa'):
                instance_path += f'/6_Fattahi/{instance}.fjs'        
        encoding = parser.parse_benchmark(instance_path)
        result[instance] = encoding
    return result

def load_fjssp_w(bounds : dict[str, tuple[float,float]]) -> dict:
    # 加载 FJSSP-W（含工人维度）实例。
    fjssp_w = r'instances/InstanceData/FJSSP-W/data.csv'
    return _load(fjssp_w, bounds, True)

def load_fjssp(bounds : dict[str, tuple[float,float]]) -> dict:
    # 加载 FJSSP（无工人维度）实例。
    fjssp = r'instances/InstanceData/FJSSP/data.csv'
    return _load(fjssp, bounds)
