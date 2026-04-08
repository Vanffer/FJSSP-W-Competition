from util.benchmark_parser import WorkerBenchmarkParser

def main(): 
    # 示例：读取一个 FJSSP-W 实例文件，并展示解析后的核心接口。
    # 该脚本主要用于帮助理解 WorkerBenchmarkParser 返回对象的结构。

    path = r"instances\Example_Instances_FJSSP-WF\Fattahi20.fjs"
    parser = WorkerBenchmarkParser()
    result = parser.parse_benchmark(path)

    # durations 是三维张量：[工序][机器][工人] -> 加工时长。
    print(result.durations())

    # 下面分别输出实例规模信息与可行性查询接口结果。
    print(f"n_jobs: {result.n_jobs()}")
    print(f"n_machines: {result.n_machines()}")
    print(f"n_operations: {result.n_operations()}")
    print(f"get_workers_for_operation: {result.get_workers_for_operation(1)}")
    print(f"get_all_machines_for_all_operations: {result.get_all_machines_for_all_operations()}")
    print(f"get_workers_for_operation_on_machine: {result.get_workers_for_operation_on_machine(1, 1)}")
    print(f"is_possible: {result.is_possible(1,1,1)}")

if __name__ == "__main__":
    main()
