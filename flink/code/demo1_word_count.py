from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode

# 创建环境
env = StreamExecutionEnvironment.get_execution_environment()

# 设置任务的并行度,一个并行度对应一个task
env.set_parallelism(1)

env.set_runtime_mode(RuntimeExecutionMode.BATCH)

# 2、读取数据
# 有界流
lines_ds = env.read_text_file("../../data/words.txt")

# 3、统计单词的梳理
# 一行转多行
words_ds = lines_ds.flat_map(lambda line: line.split(","))

# 转换成kv
kv_ds = words_ds.map(lambda word: (word,1))

# 按照单词分组
key_by_ds = kv_ds.key_by(lambda kv:kv[0])

# 统计数量
count_ds = key_by_ds.sum(1)

# 打印数据
count_ds.print()

# 启动flink任务
env.execute()
