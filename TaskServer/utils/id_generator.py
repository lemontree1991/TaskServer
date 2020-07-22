#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雪花算法生成唯一ID,毫秒级
https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
"""
import time
import logging

logger = logging.getLogger(__file__)

# 64位ID的分配 64 = 1 + 41 + 5 + 5 + 12
SIGN_BITS = 1  # 符号位
TIMESTAMP_BITS = 41  # 41位时间戳能记录69.73年 = 2**41 / 1000 /  60 / 60 / 24 /365
WORKER_ID_BITS = 5  # 机器编号
DATA_CENTER_ID_BITS = 5  # 数据中心
SEQUENCE_BITS = 12  # 序列号

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 31 = 2**5-1=  bin(MAX_WORKER_ID) = '0b11111'
MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)

# 移位偏移计算
WORKER_ID_SHIFT = SEQUENCE_BITS  # 12
DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS  # 17
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS  # 22

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)  # 4095 = 2**12 -1 = bin(12) = '0b111111111111'

# Twitter元年时间戳
TWEPOCH = 1288834974657  # '2010-11-04 09:42:54' = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TWEPOCH/1000))


class IDGenerator:
    """雪花算法ID生成器"""

    def __init__(self, data_center_id: int, worker_id: int, sequence: int = 0):

        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

        self._verify()

    def gen_id(self):
        """生成ID"""
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳

        # 当前时间小于上次的时间，则是出现时钟回拨
        if timestamp < self.last_timestamp:
            logger.error(f"clock is moving backwards.  Rejecting requests until {self.last_timestamp}.")
            raise InvalidSystemClock(
                f'Clock moved backwards.  Refusing to generate id for {self.last_timestamp - timestamp} milliseconds')

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.data_center_id << DATA_CENTER_ID_SHIFT) | \
                 (self.worker_id << WORKER_ID_SHIFT) | self.sequence
        return new_id

    def _verify(self) -> None:
        """校验数据中心id 机器id"""
        if self.worker_id > MAX_WORKER_ID or self.worker_id < 0:
            raise ValueError('worker id out of range')

        if self.data_center_id > MAX_DATA_CENTER_ID or self.data_center_id < 0:
            raise ValueError('data center id out of range')

    def _til_next_millis(self, last_timestamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def _gen_timestamp(self) -> int:
        """毫秒级时间戳"""
        return int(time.time() * 1000)


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


id_generator = IDGenerator(1, 1, 0)

if __name__ == '__main__':
    for i in range(100):
        uid = id_generator.gen_id()
        print(uid, bin(uid))
