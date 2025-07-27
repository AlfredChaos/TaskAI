"""雪花ID生成器模块"""

import time
import threading
from typing import Optional


class SnowflakeGenerator:
    """雪花ID生成器
    
    雪花ID结构（64位）：
    - 1位符号位（固定为0）
    - 41位时间戳（毫秒级，可使用约69年）
    - 10位机器ID（支持1024台机器）
    - 12位序列号（每毫秒可生成4096个ID）
    """
    
    def __init__(self, machine_id: int = 1, datacenter_id: int = 1):
        """初始化雪花ID生成器
        
        Args:
            machine_id (int): 机器ID（0-31）
            datacenter_id (int): 数据中心ID（0-31）
        """
        # 各部分位数
        self.TIMESTAMP_BITS = 41
        self.DATACENTER_BITS = 5
        self.MACHINE_BITS = 5
        self.SEQUENCE_BITS = 12
        
        # 最大值
        self.MAX_DATACENTER_ID = (1 << self.DATACENTER_BITS) - 1
        self.MAX_MACHINE_ID = (1 << self.MACHINE_BITS) - 1
        self.MAX_SEQUENCE = (1 << self.SEQUENCE_BITS) - 1
        
        # 位移量
        self.MACHINE_SHIFT = self.SEQUENCE_BITS
        self.DATACENTER_SHIFT = self.SEQUENCE_BITS + self.MACHINE_BITS
        self.TIMESTAMP_SHIFT = self.SEQUENCE_BITS + self.MACHINE_BITS + self.DATACENTER_BITS
        
        # 起始时间戳（2023-01-01 00:00:00 UTC）
        self.EPOCH = 1672531200000
        
        # 验证参数
        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"数据中心ID必须在0-{self.MAX_DATACENTER_ID}之间")
        if machine_id > self.MAX_MACHINE_ID or machine_id < 0:
            raise ValueError(f"机器ID必须在0-{self.MAX_MACHINE_ID}之间")
        
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        
        # 线程锁
        self._lock = threading.Lock()
    
    def _current_timestamp(self) -> int:
        """获取当前时间戳（毫秒）
        
        Returns:
            int: 当前时间戳
        """
        return int(time.time() * 1000)
    
    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待下一毫秒
        
        Args:
            last_timestamp (int): 上次时间戳
            
        Returns:
            int: 下一毫秒时间戳
        """
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp
    
    def generate_id(self) -> int:
        """生成雪花ID
        
        Returns:
            int: 雪花ID
            
        Raises:
            RuntimeError: 时钟回拨异常
        """
        with self._lock:
            timestamp = self._current_timestamp()
            
            # 时钟回拨检查
            if timestamp < self.last_timestamp:
                raise RuntimeError(
                    f"时钟回拨异常，拒绝生成ID。当前时间戳: {timestamp}, "
                    f"上次时间戳: {self.last_timestamp}"
                )
            
            # 同一毫秒内
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号溢出，等待下一毫秒
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 新的毫秒，序列号重置
                self.sequence = 0
            
            self.last_timestamp = timestamp
            
            # 组装雪花ID
            snowflake_id = (
                ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) |
                (self.datacenter_id << self.DATACENTER_SHIFT) |
                (self.machine_id << self.MACHINE_SHIFT) |
                self.sequence
            )
            
            return snowflake_id
    
    def parse_id(self, snowflake_id: int) -> dict:
        """解析雪花ID
        
        Args:
            snowflake_id (int): 雪花ID
            
        Returns:
            dict: 解析结果
        """
        timestamp = ((snowflake_id >> self.TIMESTAMP_SHIFT) + self.EPOCH)
        datacenter_id = (snowflake_id >> self.DATACENTER_SHIFT) & self.MAX_DATACENTER_ID
        machine_id = (snowflake_id >> self.MACHINE_SHIFT) & self.MAX_MACHINE_ID
        sequence = snowflake_id & self.MAX_SEQUENCE
        
        return {
            'timestamp': timestamp,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000)),
            'datacenter_id': datacenter_id,
            'machine_id': machine_id,
            'sequence': sequence
        }


# 全局雪花ID生成器实例
_snowflake_generator: Optional[SnowflakeGenerator] = None


def init_snowflake_generator(machine_id: int = 1, datacenter_id: int = 1) -> None:
    """初始化全局雪花ID生成器
    
    Args:
        machine_id (int): 机器ID
        datacenter_id (int): 数据中心ID
    """
    global _snowflake_generator
    _snowflake_generator = SnowflakeGenerator(machine_id, datacenter_id)


def generate_snowflake_id() -> int:
    """生成雪花ID
    
    Returns:
        int: 雪花ID
        
    Raises:
        RuntimeError: 生成器未初始化
    """
    global _snowflake_generator
    if _snowflake_generator is None:
        # 使用默认配置初始化
        init_snowflake_generator()
    return _snowflake_generator.generate_id()


def parse_snowflake_id(snowflake_id: int) -> dict:
    """解析雪花ID
    
    Args:
        snowflake_id (int): 雪花ID
        
    Returns:
        dict: 解析结果
    """
    global _snowflake_generator
    if _snowflake_generator is None:
        # 使用默认配置初始化
        init_snowflake_generator()
    return _snowflake_generator.parse_id(snowflake_id)


def get_snowflake_generator() -> SnowflakeGenerator:
    """获取雪花ID生成器实例
    
    Returns:
        SnowflakeGenerator: 生成器实例
    """
    global _snowflake_generator
    if _snowflake_generator is None:
        init_snowflake_generator()
    return _snowflake_generator