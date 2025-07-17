from pyflink.common import Duration, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode
from pyflink.datastream.connectors.file_system import FileSource, StreamFormat

env = StreamExecutionEnvironment.get_execution_environment()

env.set_runtime_mode(RuntimeExecutionMode.STREAMING)


# 设置并行度,一个并行度对应一个task
env.set_parallelism(1)


# 设置数据从上游发送到下游的延迟时间,默认200毫秒
# 设置为0,每一条数据发送一次
env.set_buffer_timeout(100)

# 2、监控目录,构建无界流
# for_record_stream_format: 指定读取数据的格式和路径
# monitor_continuously:每隔一段时间扫描目录下新的文件,构建无界流
file_source = (FileSource
               .for_record_stream_format(StreamFormat.text_line_format("UTF-8"),"../../data/words")
               .monitor_continuously(Duration.of_millis(5))
               .build())


# 基于source构建DataStream
lines_ds = env.from_source(file_source,WatermarkStrategy.no_watermarks(),"file_source")

# 3、统计单词的梳理
# 一行转换成多行
words_ds = lines_ds.flat_map(lambda line:line.split(","))

# 转换成kv
kv_ds = words_ds.map(lambda word: (word, 1))

# 安装单词分组
key_by_ds = kv_ds.key_by(lambda kv: kv[0])

# 统计数量
count_ds = key_by_ds.sum(1)

# 打印数据
count_ds.print()

# 启动flink任务
env.execute()
