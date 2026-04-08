import random

def to_index(job, operation, job_sequence):
    # 将 (job, job内第k道工序) 映射到全局工序索引。
    counter = -1
    index = 0
    for i in job_sequence:
        if i == job:
            counter += 1
        if counter == operation:
            return index
        index += 1
    return None

class GreedyFJSSPSolver:
    """FJSSP 贪心基线。

    核心思想：在每一步从所有 job 的“下一道待排工序”中，
    选择最短可加工时间的工序（含随机平局打破）。
    """

    def __init__(self, durations, job_sequence):
        self.durations = durations
        self.job_sequence = job_sequence
        jobs = set(job_sequence)
        self.counts = [job_sequence.count(job) for job in jobs]

    def determine_next(self, next_operation):
        # 为每个 job 找到其下一道工序在可选机器上的最短时长。
        next_durations = [0] * len(next_operation)
        min_index = float('inf')
        min_duration = float('inf')
        machine = [float('inf')] * len(next_operation)
        min_machine = float('inf')
        for i in range(len(next_operation)):
            if next_operation[i] >= self.counts[i]:
                continue
            index = to_index(i, next_operation[i], self.job_sequence)
            operation_durations = self.durations[index]
            # for FJSSP, use this, for FJSSP-W, extract workers
            next_durations[i] = float('inf')
            for j in range(len(operation_durations)):
                if operation_durations[j] > 0 and operation_durations[j] < next_durations[i]:
                    next_durations[i] = operation_durations[j]
                    machine[i] = j
                elif operation_durations[j] > 0 and operation_durations[j] == next_durations[i] and random.random() < 0.5:
                    next_durations[i] = operation_durations[j]
                    machine[i] = j
        for i in range(len(next_durations)):
            if next_durations[i] > 0:
                if next_durations[i] < min_duration:
                    min_duration = next_durations[i]
                    min_machine = machine[i]
                    min_index = i
                elif next_durations[i] == min_duration and random.random() < 0.5:
                    min_duration = next_durations[i]
                    min_machine = machine[i]
                    min_index = i
        return min_index, min_duration, min_machine
    
    def solve(self):
        # 依次构建作业选择序列 sequence 与机器分配 machines。
        next_operation = []
        jobs = set(self.job_sequence)
        for i in jobs:
            next_operation.append(0)

        sequence = [float('inf')] * len(self.durations)
        machines = [float('inf')] * len(self.durations)
        counts = [self.job_sequence.count(job) for job in jobs]
        for i in range(len(self.job_sequence)):
            index, duration, machine = self.determine_next(next_operation)
            machines[to_index(index, next_operation[index], self.job_sequence)] = machine
            next_operation[index] += 1
            sequence[i] = index
        return sequence, machines


class GreedyFJSSPWSolver:
    """FJSSP-W 贪心基线。

    与 FJSSP 版本类似，但在机器和工人组合上联合选择最短时长。
    """

    def __init__(self, durations, job_sequence):
        self.durations = durations
        self.job_sequence = job_sequence
        jobs = set(job_sequence)
        self.counts = [job_sequence.count(job) for job in jobs]

    def determine_next(self, next_operation):
        # 对每个候选 job，遍历 (machine, worker) 可行组合找最短时长。
        next_durations = [0] * len(next_operation)
        machine = [float('inf')] * len(next_operation)
        worker = [float('inf')] * len(next_operation)
        min_index = float('inf')
        min_duration = float('inf')

        for i in range(len(next_operation)):
            if next_operation[i] >= self.counts[i]:
                continue
            index = to_index(i, next_operation[i], self.job_sequence)
            operation_durations = self.durations[index]

            next_durations[i] = float('inf')
            for j in range(len(operation_durations)):
                for k in range(len(operation_durations[j])):
                    if operation_durations[j][k] > 0 and operation_durations[j][k] < next_durations[i]:
                        next_durations[i] = operation_durations[j][k]
                        machine[i] = j
                        worker[i] = k
                    elif operation_durations[j][k] > 0 and operation_durations[j][k] == next_durations[i] and random.random() < 0.5:
                        next_durations[i] = operation_durations[j][k]
                        machine[i] = j
                        worker[i] = k
        for i in range(len(next_durations)):
            if next_durations[i] > 0:
                if next_durations[i] < min_duration:
                    min_duration = next_durations[i]
                    min_index = i
                elif next_durations[i] == min_duration and random.random() < 0.5:
                    min_duration = next_durations[i]
                    min_index = i
        return min_index, min_duration, machine[min_index], worker[min_index]
    
    def solve(self):
        # 输出：作业执行顺序、机器分配、工人分配。
        next_operation = []
        jobs = set(self.job_sequence)
        for i in jobs:
            next_operation.append(0)

        sequence = [float('inf')] * len(self.durations)
        machines = [float('inf')] * len(self.durations)
        workers = [float('inf')] * len(self.durations)
        counts = [self.job_sequence.count(job) for job in jobs]
        for i in range(len(self.job_sequence)):
            index, duration, machine, worker = self.determine_next(next_operation)
            machines[to_index(index, next_operation[index], self.job_sequence)] = machine
            workers[to_index(index, next_operation[index], self.job_sequence)] = worker
            sequence[i] = index
            next_operation[index] += 1
        return sequence, machines, workers
