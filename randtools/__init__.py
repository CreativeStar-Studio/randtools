import random
from typing import Optional, List
import ping3
import socket
import threading
from queue import Queue
import concurrent.futures
import re

def integer(a, b, pattern: Optional[str] = None) -> int:
    """
    
    随机生成一个整数。
    :param a: 范围的起始值。
    :param b: 范围的结束值。
    :param pattern: 概率模式，形如 "1:0.3,2:0.7"。
    :return: 随机生成的整数。

    Randomly generate an integer.
    :param a: The starting value of the range.
    :param b: The ending value of the range.
    :param pattern: The probability pattern, like "1:0.3,2:0.7".
    :return: The randomly generated integer.
    
    """
    if pattern is None:
        return random.randint(a, b)
    
    weights = []
    values = []
    specified_values = set()
    
    # 解析形如 "1:0.3,2:0.7" 的模式
    for match in re.finditer(r'(\d+):([\d.]+)', pattern):
        value = int(match.group(1))
        weight = float(match.group(2))
        
        if value < a or value > b:
            raise ValueError(f"Value {value} is out of range [{a}, {b}]")
            
        values.append(value)
        weights.append(weight)
        specified_values.add(value)
    
    if not values:
        raise ValueError("Invalid probability pattern")
        
    # 计算未指定值的权重
    remaining_weight = 1.0 - sum(weights)
    if remaining_weight < 0:
        raise ValueError("Probabilities sum exceeds 1")
        
    # 为未指定的值分配相等的权重
    unspecified_values = [x for x in range(a, b + 1) if x not in specified_values]
    if unspecified_values:
        weight_per_unspecified = remaining_weight / len(unspecified_values)
        values.extend(unspecified_values)
        weights.extend([weight_per_unspecified] * len(unspecified_values))
    
    return random.choices(values, weights=weights)[0]

def ascii_char(a, b, pattern: Optional[str] = None) -> str:
    """
    
    随机生成一个 ASCII 字符。
    :param a: ASCII 码的起始值。
    :param b: ASCII 码的结束值。
    :param pattern: 概率模式，形如 "1:0.3,2:0.7"。
    :return: 随机生成的 ASCII 字符。

    Randomly generate an ASCII character.
    :param a: The starting value of the ASCII code.
    :param b: The ending value of the ASCII code.
    :param pattern: The probability pattern, like "1:0.3,2:0.7".
    :return: The randomly generated ASCII character.
    
    """
    if pattern is None:
        c = random.randint(a, b)
        return chr(c)
    
    weights = []
    values = []
    specified_values = set()
    
    for match in re.finditer(r'(\d+):([\d.]+)', pattern):
        value = int(match.group(1))
        weight = float(match.group(2))
        
        if value < a or value > b:
            raise ValueError(f"ASCII value {value} is out of range [{a}, {b}]")
            
        values.append(value)
        weights.append(weight)
        specified_values.add(value)
    
    if not values:
        raise ValueError("Invalid probability pattern")
        
    remaining_weight = 1.0 - sum(weights)
    if remaining_weight < 0:
        raise ValueError("Probabilities sum exceeds 1")
        
    unspecified_values = [x for x in range(a, b + 1) if x not in specified_values]
    if unspecified_values:
        weight_per_unspecified = remaining_weight / len(unspecified_values)
        values.extend(unspecified_values)
        weights.extend([weight_per_unspecified] * len(unspecified_values))
    
    return chr(random.choices(values, weights=weights)[0])

def letter(start, end, type: Optional[bool] = False, pattern: Optional[str] = None) -> str:
    """
    
    随机生成一个字母。
    :param start: 起始字母的索引。
    :param end: 结束字母的索引。
    :param type: 是否大写。
    :param pattern: 概率模式，形如 "1:0.3,2:0.7"。
    :return: 随机生成的字母。

    Randomly generate a letter.
    :param start: The index of the starting letter.
    :param end: The index of the ending letter.
    :param type: Whether to capitalize.
    :param pattern: The probability pattern, like "1:0.3,2:0.7".
    :return: The randomly generated letter.
    
    """
    c = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
         'h', 'i', 'j', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r',
         "s", "t", "u", "v", 'w', "x",
         "y", "z"]

    if not c[start:end]:
        raise ValueError("Start and end index cannot be the same or out of range")

    if pattern is None:
        d = random.randint(0, len(c[start:end]) - 1)
        e = c[start:end][d]
    else:
        weights = []
        values = []
        specified_values = set()
        
        for match in re.finditer(r'(\d+):([\d.]+)', pattern):
            value = int(match.group(1))
            weight = float(match.group(2))
            
            if value < 0 or value >= len(c[start:end]):
                raise ValueError(f"Index {value} is out of range [0, {len(c[start:end])-1}]")
                
            values.append(value)
            weights.append(weight)
            specified_values.add(value)
        
        if not values:
            raise ValueError("Invalid probability pattern")
            
        remaining_weight = 1.0 - sum(weights)
        if remaining_weight < 0:
            raise ValueError("Probabilities sum exceeds 1")
            
        unspecified_values = [x for x in range(len(c[start:end])) if x not in specified_values]
        if unspecified_values:
            weight_per_unspecified = remaining_weight / len(unspecified_values)
            values.extend(unspecified_values)
            weights.extend([weight_per_unspecified] * len(unspecified_values))
            
        d = random.choices(values, weights=weights)[0]
        e = c[start:end][d]

    if type:
        return e.upper()
    else:
        return e.lower()

def byte(n, pattern: Optional[str] = None) -> bytes:
    """
    
    随机生成 n 个字节。
    :param n: 要生成的字节数。
    :param pattern: 概率模式，形如 "1:0.3,2:0.7"。
    :return: 随机生成的字节。

    Randomly generate n bytes.
    :param n: The number of bytes to generate.
    :param pattern: The probability pattern, like "1:0.3,2:0.7".
    :return: Randomly generated bytes.
    
    """
    if pattern is None:
        return random.randbytes(n)
    
    weights = []
    values = []
    specified_values = set()
    
    for match in re.finditer(r'(\d+):([\d.]+)', pattern):
        value = int(match.group(1))
        weight = float(match.group(2))
        
        if value < 0 or value > 255:
            raise ValueError(f"Byte value {value} is out of range [0, 255]")
            
        values.append(value)
        weights.append(weight)
        specified_values.add(value)
    
    if not values:
        raise ValueError("Invalid probability pattern")
        
    remaining_weight = 1.0 - sum(weights)
    if remaining_weight < 0:
        raise ValueError("Probabilities sum exceeds 1")
        
    unspecified_values = [x for x in range(256) if x not in specified_values]
    if unspecified_values:
        weight_per_unspecified = remaining_weight / len(unspecified_values)
        values.extend(unspecified_values)
        weights.extend([weight_per_unspecified] * len(unspecified_values))
    
    return bytes(random.choices(values, weights=weights, k=n))

def uniform(a, b, pattern: Optional[str] = None):
    """
    
    从 a 到 b 范围内随机选择一个数字。
    :param a: 范围的起始值。
    :param b: 范围的结束值。
    :param pattern: 概率模式，形如 "1:0.3,2:0.7"。
    :return: 随机选择的数字。

    Randomly select a number from a to b.
    :param a: The starting value of the range.
    :param b: The ending value of the range.
    :param pattern: The probability pattern, like "1:0.3,2:0.7".
    :return: The randomly selected number.

    """
    if pattern is None:
        return random.uniform(a, b)
    
    weights = []
    values = []
    
    for match in re.finditer(r'([\d.]+):([\d.]+)', pattern):
        value = float(match.group(1))
        weight = float(match.group(2))
        
        if value < a or value > b:
            raise ValueError(f"Value {value} is out of range [{a}, {b}]")
            
        values.append(value)
        weights.append(weight)
    
    if not values:
        raise ValueError("Invalid probability pattern")
        
    if abs(sum(weights) - 1.0) > 1e-10:
        raise ValueError("Probabilities must sum to 1")
        
    return random.choices(values, weights=weights)[0]


def choices(
        population: list,
        weights: Optional[list] = None,
        *,
        cum_weights: Optional[list] = None,
        k: int = 1) -> list:
    """
    从 population 中随机选择 k 个元素，返回一个列表。
    每个元素被选中的概率由 weights 给出。
    :param population: 要从中选择元素的列表。
    :param weights: 每个元素被选中的概率。
    :param cum_weights: 累积权重，用于优化选择过程。
    :param k: 要选择的元素数量。
    :return: 一个包含 k 个元素的列表。

    Randomly select k elements from population, return a list.
    The probability of each element being selected is given by weights.
    :param population: The list from which to select elements.
    :param weights: The probability of each element being selected.
    :param cum_weights: Cumulative weights, used to optimize the selection process.
    :param k: The number of elements to select.
    :return: A list containing k elements.
    """
    a = random.choices(population=population, weights=weights, cum_weights=cum_weights,
                       k=k)
    return a

def boolean() -> bool:
    """
    生成随机布尔值
    :return: 随机布尔值

    Generate random boolean value
    :return: Random boolean value
    """
    a = [True, False]
    b = random.choice(a)
    return b

def url(a: Optional[List[int]] = None, b: Optional[List[int]] = None, c: Optional[List[int]] = None, d: Optional[List[int]] = None, threads: Optional[int] = 16) -> str:
    """
    生成随机URL
    :param a: 第一个IP段范围 [0-255]
    :param b: 第二个IP段范围 [0-255]
    :param c: 第三个IP段范围 [0-255]
    :param d: 第四个IP段范围 [0-255]
    :return: 随机URL

    Generate random URL
    :param a: First IP segment range [0-255]
    :param b: Second IP segment range [0-255]
    :param c: Third IP segment range [0-255]
    :param d: Fourth IP segment range [0-255]
    :return: Random URL
    """
    if not a:
        a = [0, 255]
    if not b:
        b = [0, 255]
    if not c:
        c = [0, 255]
    if not d:
        d = [0, 255]

    if max(a[1], b[1], c[1], d[1]) > 255 or min(a[0], b[0], c[0], d[0]) < 0:
        raise ValueError("IP address segments must be between 0 and 255")
    
    def generate_random_ip():
        return f"{a}.{b}.{c}.{d}"
    
    def get_domain_from_ip(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
    
    def check_domain(domain):
        try:
            response_time = ping3.ping(domain)
            if response_time is not None:
                return f"https://{domain}"
        except:
            return None
    
    def worker():
        while True:
            random_ip = generate_random_ip()
            domain = get_domain_from_ip(random_ip)
            if domain:
                result = check_domain(domain)
                if result:
                    return result
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker) for _ in range(threads)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result