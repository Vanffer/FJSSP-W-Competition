import random

def create_uncertainty_vector(n_required, factor : float = 10.0, offset : float = 1.0):
    """生成不确定性参数向量。

    每个元素形如 [alpha, beta, offset]，用于后续模拟中的 beta 分布扰动参数。
    """

    uncertainty_parameters = []
    for _ in range(n_required):
        # alpha 取 (0,1) 的随机值；beta 与 alpha 成比例。
        alpha = random.random()
        beta = factor * alpha
        # offset 保留为统一偏移量，用于控制扰动中心位置。
        offset = offset
        uncertainty_parameters.append([alpha, beta, offset])
    return uncertainty_parameters
