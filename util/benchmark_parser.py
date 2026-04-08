from .encoding import Encoding, WorkerEncoding
import numpy as np

class BenchmarkParser: 
    """FJSSP 解析器（不含工人维度）。

    输入是 `.fjs` 文本实例，输出 Encoding：
    - durations[operation, machine] = duration
    - job_sequence[operation] = job_id
    """

    def __init__(self):
        pass

    def parse_benchmark(self, path: str):
        # 读取原始文件内容。
        file_content = []

        try:
            file = open(path, 'r')
            file_content = file.readlines()
        except Exception as exception: print(exception) 

        # 第一行包含全局规模信息：作业数、机器数等。
        info = file_content[0].split(' ')
        n_machines = int(info[1])
        n_overall_operations = 0

        # 从第二行开始，每一行对应一个 job。
        lines = [line.split() for line in file_content[1:]]
        for i in range(1, len(file_content)):
            line = file_content[i].split(' ')
            lines[i - 1] = line
            n_overall_operations += int(line[0])
        
        # durations 初始化为 0，0 表示该机器不可用于该工序。
        durations = np.zeros((n_overall_operations, n_machines), dtype=int)
        operation_index = 0
        # job_sequence 记录“全局工序索引 -> 属于哪个 job”。
        job_sequence = [0] * n_overall_operations

        for i in range(1, len(lines)):
            line = lines[i-1]
            n_operations = int(line[0])
            index = 1
            for j in range(0, n_operations):
                job_sequence[operation_index] = i-1
                # 当前工序可选机器数量。
                n_options = int(line[index])
                index +=1
                for k in range(0, n_options):
                    # 文件内机器编号从 1 开始，内部转为 0 开始。
                    machine = int(line[index])
                    index += 1
                    duration = int(line[index])
                    index += 1
                    durations[operation_index, machine - 1] = duration
                operation_index += 1
                
        return Encoding(durations, job_sequence)

class WorkerBenchmarkParser: 
    """FJSSP-W 解析器（包含工人维度）。

    输出 WorkerEncoding：
    - durations[operation, machine, worker] = duration
    - 值为 0 代表该 machine-worker 组合不可行。
    """

    def __init__(self):
        pass

    def parse_benchmark(self, path: str):
        # 读取原始文件。
        file_content = []

        try:
            file = open(path, 'r')
            file_content = file.readlines()
        except Exception as exception: print(exception) 

        # 第一行：作业规模、机器数、工人数。
        info = file_content[0].split(' ')
        n_machines = int(info[1])
        n_workers = int(round(float(info[2])))
        n_overall_operations = 0
        lines = [line.split() for line in file_content[1:]]

        for i in range(1, len(file_content)):
            line = file_content[i].split(' ')
            lines[i - 1] = line
            n_overall_operations += int(line[0])
        
        # 三维时长张量：工序 x 机器 x 工人。
        durations = np.zeros((n_overall_operations, n_machines, n_workers), dtype=int)
        operation_index = 0
        job_sequence = [0] * n_overall_operations

        for i in range(1, len(lines)+1):
            line = lines[i-1]
            n_operations = int(line[0])
            index = 1
            for j in range(0, n_operations):
                job_sequence[operation_index] = i-1
                n_machine_options = int(line[index])
                index +=1
                for k in range(0, n_machine_options):
                    # 先读机器，再读该机器下可选工人数。
                    machine = int(line[index])
                    index += 1
                    n_worker_options = int(line[index])
                    index += 1

                    for l in range(0, n_worker_options):
                        # 文件内 worker 编号同样是从 1 开始。
                        worker = int(line[index])
                        index += 1
                        duration = int(line[index])
                        index += 1
                        durations[operation_index, machine - 1, worker - 1] = duration
                
                operation_index += 1
                
        return WorkerEncoding(durations, job_sequence)

