import numpy as np

class Encoding:
    """FJSSP 编码容器。

    - durations: shape = (N, M)
    - job_sequence: 长度 N，按固定顺序标记每道工序所属 job
    """

    def __init__(self, durations: list, job_sequence: list) -> None:
        self.__durations = durations
        self.__job_sequence = job_sequence
        # 通过相邻 job id 的变化次数估计 job 数（假设同一 job 工序连续存放）。
        self.__n_jobs = 1
        for i in range(1, len(self.__job_sequence)):
            if self.__job_sequence[i] != self.__job_sequence[i - 1]: 
                self.__n_jobs += 1

    def job_sequence(self):
        return self.__job_sequence
    
    def n_operations(self):
        return self.__durations.shape[0]
    
    def n_machines(self):
        return self.__durations.shape[1]
    
    def n_jobs(self):
        return self.__n_jobs
    
    def durations(self):
        return self.__durations
    
    def get_machines_for_operation(self, operation_index: int):
        # 返回当前工序所有可行机器（duration > 0）。
        machines = []
        for i in range(0, self.__durations.shape[1]): 
            if self.__durations[operation_index, i] > 0:
                machines.append(i)
        return machines
    
    def get_machines_for_all_operations(self):
        # 批量返回每道工序的可行机器集合。
        machines = []
        for i in range (0, self.__durations.shape[0]):
            machines.append([])
            for j in range(0, self.__durations.shape[1]):
                if self.__durations[i, j] > 0: 
                    machines[i].append(j)
        return machines
    
    def copy(self):
        # 浅拷贝：底层数组/列表仍共享引用。
        return Encoding(self.__durations, self.__job_sequence)
    
    def deep_copy(self):
        # 深拷贝：显式复制 durations 与 job_sequence。
        duration_copy = np.zeros((self.__durations.shape[0], self.__durations.shape[1]), dtype=int)
        for i in range(0, self.__durations.shape[0]):
            for j in range(0, self.__durations.shape[1]):
                duration_copy[i, j] = self.__durations[i, j]
        
        job_sequence_copy = [None] * len(self.__job_sequence)
        for i in range(0, len(self.__job_sequence)):
            job_sequence_copy[i] = self.__job_sequence[i]

        return Encoding(duration_copy, job_sequence_copy)

class WorkerEncoding:
    """FJSSP-W 编码容器。

    - durations: shape = (N, M, W)
    - 0 表示 machine-worker 组合不可行
    """

    def __init__(self, durations: list, job_sequence: list) -> None:
        self.__durations = durations
        self.__job_sequence = job_sequence
        self.__n_jobs = 1
        for i in range(1, len(self.__job_sequence)):
            if self.__job_sequence[i] != self.__job_sequence[i - 1]: 
                self.__n_jobs += 1

    def job_sequence(self):
        return self.__job_sequence
    
    def n_operations(self):
        return self.__durations.shape[0]
    
    def n_machines(self):
        return self.__durations.shape[1]
    
    def n_jobs(self):
        return self.__n_jobs
    
    def durations(self):
        return self.__durations

    def get_workers_for_operation(self, operation_index: int):
        # 汇总该工序在所有机器上的可行工人。
        workers = []
        for i in range(0, self.__durations.shape[1]): 
            for j in range(0, self.__durations.shape[2]):
                if self.__durations[operation_index, i, j] > 0:
                    workers.append(j)

        return workers
    
    def get_all_machines_for_all_operations(self):
        # 对每道工序返回存在可行工人的机器集合。
        operations = []
        for i in range (0, self.__durations.shape[0]):
            machines = []
            for j in range(0, self.__durations.shape[1]):
                for k in range(0, self.__durations.shape[2]):
                    if self.__durations[i, j, k] > 0: 
                        machines.append(j)
                        break
                    
            operations.append(machines)

        return operations
    
    def get_workers_for_operation_on_machine(self, operation: int, machine: int):
        # 固定工序与机器后，返回可用工人集合。
        workers = []
        for j in range(0, self.__durations.shape[2]):
            if self.__durations[operation, machine, j] > 0:
                workers.append(j)

        return workers
    
    def is_possible(self, operation: int, machine: int, worker: int):
        # 直接判定三元组合是否可行。
        return self.__durations[operation, machine, worker] > 0

    def copy(self):
        # 浅拷贝。
        return WorkerEncoding(self.__durations, self.__job_sequence)
    
    def deep_copy(self):
        # 深拷贝。
        duration_copy = np.zeros((self.__durations.shape[0], self.__durations.shape[1], self.__durations.shape[2]), dtype=int)
        for i in range(0, self.__durations.shape[0]):
            for j in range(0, self.__durations.shape[1]):
                for k in range(0, self.__durations.shape[2]):
                    duration_copy[i, j, k] = self.__durations[i, j, k]
        
        job_sequence_copy = [None] * len(self.__job_sequence)
        for i in range(0, len(self.__job_sequence)):
            job_sequence_copy[i] = self.__job_sequence[i]

        return WorkerEncoding(duration_copy, job_sequence_copy)
