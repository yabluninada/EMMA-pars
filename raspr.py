from unittest import result

from librosa import ex
from numpy import indices

from algo import Interval, IntervalSet, raspr_dyn_with_smych_to_good


def extract_bow_second_elements(lines: list[str]) -> list[int]:
    """
    Из строк вида '/bow;0;375;100' извлекает второй элемент после bow (375).
    Возвращает список int в порядке появления.
    """
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith("/bow;"):
            parts = line.split(";")
            # parts: ['/bow', '0', '375', '100']
            result.append(int(parts[2]))
    return result


def extract_sn_change_indices(lines: list[str]) -> list[int]:
    """
    Возвращает индексы элементов списка (из extract_bow_second_elements),
    перед которыми меняется первая цифра после /sn.

    """
    values = []
    indices = []
    current_sn_digit = None
    prev_sn_digit = None

    for line in lines:
        line = line.strip()

        if line.startswith("/sn;"):
            parts = line.split(";")
            current_sn_digit = int(parts[1])

        elif line.startswith("/bow;"):
            parts = line.split(";")
            value = int(parts[2])

            if prev_sn_digit is None:
                pass
            elif current_sn_digit != prev_sn_digit:
                indices.append(len(values))

            values.append(value)
            prev_sn_digit = current_sn_digit

    return indices


def substitute_into_bow_lines(    lines: list[str],    data: list[tuple[int, int, int]]) -> list[str]:
    """
    Подставляет значения из data в строки /bow;... исходного списка lines.

    data: список кортежей (sign, a, b), например [(1, 375, 120), (0, 375, 51)]
    lines: исходные строки, например ['/sn;3;5', '/bow;0;375;100', ...]

    Возвращает новый список строк, где каждая строка /bow;... заменена
    на /bow;sign;a;b в порядке следования.
    """
    result = []
    data_iter = iter(data)
    used = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("/bow;"):
            try:
                sign, a, b = next(data_iter)
            except StopIteration:
                raise ValueError("В data меньше элементов, чем строк /bow")

            result.append(f"/bow;{sign};{a};{b}\n")
            used += 1
        else:
            result.append(line)

    if used < len(data):
        raise ValueError("В data больше элементов, чем строк /bow")

    return result


def safity(*args, **kwargs):
    try: return raspr_dyn_with_smych_to_good(*args, **kwargs, vs=Interval(60,133), good_vs=Interval(80,120), good=IntervalSet([Interval(-1000,1000)]))
    except Exception as e: print('!!!',e)

def raspr(lines: list[str]) -> list[str]:
    for i in range(len(lines)): 
        if '/bow;' in lines[i]:
            l = lines[i].split(';')
            if int(l[2]) > 100000//61: 
                r = int(l[2]) - 100000//61  
                lines[i] = ';'.join(l[:2]+[str(100000//61)]+l[3:]) + '/p' + str(r) + '\n' 
    print(lines)
    dlit = extract_bow_second_elements(lines)
    indices = extract_sn_change_indices(lines)
    tuples = safity(dlit, indices)
    flag = 0
    if not tuples:
        print('not smych change')
        tuples = safity(dlit, indices=[])
        flag = 1
    if not tuples: return None 
    result = substitute_into_bow_lines(lines,tuples)
    if flag: print('not smych change')
    return result

if __name__ == '__main__':
    
    with open(r"D:\Лаба\эмма\партитуры\prizrak.txt", 'r') as f: lines = f. readlines()
    lines = raspr(lines)
    if lines: 
        with open(r"D:\Лаба\эмма\партитуры\prizrak.txt", 'w') as f: f. writelines(lines)