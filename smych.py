from bisect import bisect_right

from sqlalchemy import except_
from math import prod
maxV=100
minV=60
length=100000
maxS=length//minV
minS=length//maxV

LO, HI = -5000, length + 5000   # строгие неравенства: LO < x < HI


def split_by_bounds(items, bounds):
    """
    Разбивает items на группы по границам bounds.
    Кортеж попадает в следующую группу, если его первый элемент >= очередной границы.
    Возвращает список групп (пустые группы сохраняются).
    """
    groups = [[] for _ in range(len(bounds) + 1)]
    for item in items:
        idx = bisect_right(bounds, item[0])
        groups[idx].append(item)
    return groups


def split_by_second(groups, threshold=length):
    """
    Разбивает каждую группу кортежей: если второй элемент >= threshold,
    выносит его в отдельный одноэлементный список, а остальные подряд идущие
    элементы остаются в общей группе.
    """

    def get_num(s):
        # s — строка вида '/bow;1;500;65\n'
        # разбиваем по ';' и берём элемент с индексом 2
        # (после второй точки с запятой)
        #print(s)
        return int(s.split(';')[2])

    result = []
    for group in groups:
        current = []
        for item in group:
            num = get_num(item[1])
            if num >= threshold:
                if current:
                    result.append(current)
                    current = []
                i= item[1].split(';')
                item = (item[0],';'.join(i[:2]+[str(threshold)]+i[3:]))
                #print('item:', item)
                result.append([item])
            else:
                current.append(item)
        if current:
            result.append(current)
    return result




def extract_number(s: str, n: int = 2) -> int:
    """
    Извлекает число между второй и третьей точкой с запятой.
    Пример: '/bow;1;900;85\n' -> 900
    """
    parts = s.split(';')
    if len(parts) < 4:
        raise ValueError(f"Не удалось извлечь число из строки: {s!r}")
    try: return int(parts[n])
    except ValueError: return float(parts[n])


def split_into_groups(
    items,
    min_sum: int = minS,
    max_sum: int = maxS,
    value_getter = None,
):
    """
    Разбивает список кортежей на непрерывные группы так,
    чтобы сумма извлечённых чисел в каждой группе была от min_sum до max_sum.
    Порядок сохраняется.

    value_getter — функция, которая по элементу возвращает число.
                   По умолчанию: extract_number(item[1])
    """
    if value_getter is None:
        value_getter = lambda item: extract_number(item[1])

    n = len(items)
    values = [value_getter(item) for item in items]

    # Префиксные суммы значений
    prefix = [0] * (n + 1)
    for i, v in enumerate(values):
        prefix[i + 1] = prefix[i] + v

    # possible[i] — можно ли корректно разбить items[i:]
    possible = [False] * (n + 1)
    next_cut = [-1] * (n + 1)
    possible[n] = True

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            s = prefix[j] - prefix[i]

            if s > max_sum:
                break  # для положительных чисел дальше смысла нет

            if s >= min_sum and possible[j]:
                possible[i] = True
                next_cut[i] = j
                break

    if not possible[0]:
        return (0, [items])

    # Восстанавливаем группы
    groups = []
    i = 0
    while i < n:
        j = next_cut[i]
        groups.append(items[i:j])
        i = j

    return (1, groups)




def S(*args):
    match args:
        case (v, line, bit):
            sign = 1 if bit == 1 else -1
            return sign * v * extract_number(line[2])
        case (line,):
            sign = 1 if extract_number(line[2], 1) == 1 else -1
            return sign * extract_number(line[2], 3) * extract_number(line[2])
        case _:
            raise TypeError(f"S: неверное число аргументов: {len(args)}")

        
def iter_combinations(lines, vs, start=0, lo=LO, hi=HI):
    """
    Генератор: перебирает все комбинации (v ∈ vs, bit ∈ {0,1}) для каждого
    элемента lines, при которых накопленная сумма start + Σ S остаётся
    в интервале (lo, hi).

    yield (total_sum, [(v_0, bit_0), (v_1, bit_1), ...])
    """
    n = len(lines)

    def rec(idx, current_sum, chosen):
        if idx == n:
            yield current_sum-start, list(chosen)
            return
        line = lines[idx]
        #print(lines)
        for v in vs:
            for bit in (0, 1):
                
                s = S(v, line, bit)
                new_sum = current_sum + s
                if lo < new_sum < hi:              # проверка на КАЖДОМ шаге
                    chosen.append((v, bit))
                    yield from rec(idx + 1, new_sum, chosen)
                    chosen.pop()

    yield from rec(0, start, [])


def find_combinations(lines, vs, start, dlit, lo=LO, hi=HI):
    
    
    vs.append(round(length/dlit))
    vs.append(round(length/2/dlit))
    vs.append(round(length/3/dlit))
    vs.append(round(length/5/dlit))
    vs.append(round(length/6/dlit))
    vs.append(round(length/7/dlit))
    vs.append(round(length/8/dlit))

    vs = list(set([v for v in vs if v >= minV and v <= maxV]))



    
    ismen1=sum([S(i) for i in lines if i[1]==1]) # Изменения аналогичные тому, что уже есть в распределённых

    ismen2=(length - (start+ismen1)) - start # Изменения с реверсом последующих строк

    

    #Допуск +- 5000
    combinations = list(iter_combinations(lines, vs, start, lo, hi))

    combinations = [f for f in combinations if abs(f[0]-ismen1)<10000 or abs(f[0]-ismen2)<10000 ]

    return combinations





def find_current_S(lines,n): # Ищет положение смычка перед указанной нотой
    i=0
    s=0
    while lines[i][0]<n:
        s+=S(lines[i])
        i+=1
    return s







def raspr(x):

    x_bow = [(i,x[i]) for i in range(len(x)) if x[i].split(';')[0]=='/bow']
    x_sn = [(i,x[i]) for i in range(len(x)) if x[i].split(';')[0]=='/sn']



    #print(x_bow)
    #print(x_sn)
    print()

    """
        Возвращает индексы элементов, перед которыми значение поменялось.
    """
    indices = [x_sn[i+1][0] for i in range(len(x_sn) - 1) if x_sn[i][1][4] != x_sn[i + 1][1][4]]


    #print(indices)


    #print(indices)
    y = split_by_bounds(x_bow, indices)
    y = split_by_second(y,maxS)
    #print('y:', y)

    z = [split_into_groups(i) for i in y]

    #print('z:', z)

    napr = 1
    for ii,i in enumerate(z):
        if i[0]!=1: print(i)
        else:
            for ji,j in enumerate(i[1]):
                s = sum([extract_number(k[1]) for k in j])
                v = round(length/s, 4)
                                
                for k in range(len(j)):
                    spl = j[k][1].split(';')
                    z[ii][1][ji][k] = (j[k][0],';'.join([spl[0], str(napr), spl[2], str(v)+'\n']))

                if napr == 1: napr = 0
                else: napr = 1   
                


    result = [
        (digit2, digit1, string)
        for digit1, sublist1 in z
        for sublist2 in sublist1
        for digit2, string in sublist2
    ]


    result.sort(key=lambda x: x[0])

    is_okey = True
    l = 0
    for i in result:
        if i[1]==1:
            if extract_number(i[2], n=1)==1: zn=1
            else: zn=-1

            l+=extract_number(i[2])*zn*extract_number(i[2], n=3)

        if l>length+2000 or l<0-2000: 
            print(f'l is {l} in index {i[0]}')
            is_okey=False


    for i in range(len(result)):
        if extract_number(result[i][2],1)==extract_number(result[i-1][2],1) and result[i][1]!=0 and result[i-1][1]!=0:
            if x[result[i][0]-1].split(';')[1]!=x[result[i-1][0]-1].split(';')[1]: 
                print()
                print('Mistake')
                print(result[i-1][0]-1,x[result[i-1][0]-1],x[result[i-1][0]],x[result[i][0]-1],x[result[i][0]])
                is_okey=False


    
    print()
    if is_okey: print('All is OKey')
    else: print('There was some mistakes')
    '''
    
    vs = list(set([extract_number(i[2],3) for i in result]))     # извлекаем все вообще возможные скорости

    dop=3

    for i in range(len(result)):
        if result[i][1]==0:
            start = find_current_S(result, i-3)

            options=find_combinations(result[i-dop:i+dop+1], vs, start, extract_number(result[i][2]))
            
            
            options_clear = [j for j in options if prod([j[1][k][1]!=j[1][k+1][1] or set(range(result[i-dop:i+dop+1][k][0],result[i-dop:i+dop+1][k+1][0])).isdisjoint(indices) for k in range(len(j[1])-1)])]

            options.sort(key=lambda j: sum([j[1][k][1]!=j[1][k+1][1] or set(range(result[i-dop:i+dop+1][k][0],result[i-dop:i+dop+1][k+1][0])).isdisjoint(indices) for k in range(len(j[1])-1)]))

           
            if options_clear:
                print('can')
                my_option=options_clear[0]
            else: 
                print("can't")
                my_option=None

           
            if my_option:
                for j in range(len(result[i-dop:i+dop+1])):
                    result[j+i-dop]= (result[i-dop:i+dop+1][j][0],1,';'.join([result[i-dop:i+dop+1][j][2].split(';')[0], str(my_option[1][j][0]),result[i-dop:i+dop+1][j][2].split(';')[3], str(my_option[1][j][1])+'\n']) )

    
    '''

    for i in range(len(result)):
        spl = result[i][2].split(';')
        result[i]=(result[i][0],result[i][1],';'.join(spl[:3]+[str(round(float(spl[3][:-1])))+'\n']))
    return result





def reverse(string):
    
    x = string.split(';')
    if len(x)>0:
        if x[0]=='/bow':
            if x[1]=='1': napr='0'
            else: napr='1'
            return ';'.join([x[0]]+[napr]+x[2:])

    return string

#___________________________________________________________________________________________________________________________________________
#           Программная часть кончилась, дальше только интерфейс
#___________________________________________________________________________________________________________________________________________

import tkinter as tk
from tkinter import messagebox, filedialog


class App:
    GUTTER_WIDTH = 55

    def __init__(self, root):
        self.root = root
        root.title("Редактор с подсветкой")
        root.geometry("950x700")

        # ---- Тулбар ----
        tb = tk.Frame(root)
        tb.pack(fill="x", padx=5, pady=5)
        tk.Button(tb, text="📂 Импорт", command=self.import_file).pack(side="left")
        tk.Button(tb, text="💾 Сохранить", command=self.export_file).pack(side="left", padx=3)
        tk.Label(tb, text="│").pack(side="left", padx=5)
        tk.Button(tb, text="⚙ Распределить (весь файл)", command=self.apply_raspr).pack(side="left")
        tk.Button(tb, text="🔁 Reverse выделенных", command=self.apply_reverse).pack(side="left", padx=5)
        tk.Button(tb, text="🧹 Снять всю подсветку", command=self.clear_red).pack(side="left")
        tk.Label(tb, text="   (клик по кружку слева — вкл/выкл красный)",
                 fg="#777").pack(side="left")

        # ---- Область: gutter + text + scrollbar ----
        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=5, pady=5)

        self.gutter = tk.Canvas(main, width=self.GUTTER_WIDTH, bg="#f2f2f2",
                                highlightthickness=0)
        self.gutter.pack(side="left", fill="y")

        self.text = tk.Text(main, wrap="none", font=("Consolas", 11),
                            undo=True, autoseparators=True, maxundo=-1,
                            padx=4)
        self.text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(main, orient="vertical", command=self._on_scroll)
        sb.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=lambda *a: self._on_text_yscroll(sb, *a))

        self.text.tag_configure("red", background="#e53935", foreground="white")

        # события
        self.text.bind("<KeyRelease>", lambda e: self.redraw_gutter())
        self.text.bind("<ButtonRelease-1>", lambda e: self.redraw_gutter())
        self.text.bind("<Configure>", lambda e: self.redraw_gutter())
        self.text.bind("<<Modified>>", self._on_modified)
        self.gutter.bind("<Button-1>", self.on_gutter_click)

        # ---- Горячие клавиши (обе раскладки) ----
        self._bind_hotkeys()

        # пример текста
        self.text.insert("1.0",
                         "Привет old мир\nЭто TODO строка\nТретья строка\n"
                         "Ещё old одна\nПятая строка\n")
        self.text.edit_reset()   # очистить историю после вставки примера
        self.text.edit_modified(False)
        self.redraw_gutter()

    # ---------------- горячие клавиши ----------------
    def _bind_hotkeys(self):
        # ловим все нажатия Ctrl+<клавиша> и разбираем их вручную
        self.text.bind("<Control-KeyPress>", self._on_ctrl_key)
        self.root.bind("<Control-KeyPress>", self._on_ctrl_key)

    def _on_ctrl_key(self, event):
        # event.keycode на Windows = Virtual Key Code — НЕ зависит от раскладки
        # Ctrl+Z всегда 90, Ctrl+C всегда 67 и т.д.
        code = event.keycode
        ks = event.keysym.lower()

        action = None
        # Windows VK + дублирующая проверка по keysym (для Linux/Mac)
        if code == 90 or ks in ("z", "cyrillic_ya"):        # Z / я
            action = "undo"
        elif code == 89 or ks in ("y", "cyrillic_en"):      # Y / н
            action = "redo"
        elif code == 67 or ks in ("c", "cyrillic_es"):      # C / с
            action = "copy"
        elif code == 86 or ks in ("v", "cyrillic_em"):      # V / м
            action = "paste"
        elif code == 88 or ks in ("x", "cyrillic_che"):     # X / ч
            action = "cut"
        elif code == 65 or ks in ("a", "cyrillic_ef"):      # A / ф
            action = "select_all"
        elif code == 83 or ks in ("s", "cyrillic_yeru"):    # S / ы
            action = "save"

        if action is None:
            return None

        if action == "undo":       return self._undo()
        if action == "redo":       return self._redo()
        if action == "copy":       return self._copy()
        if action == "paste":      return self._paste()
        if action == "cut":        return self._cut()
        if action == "select_all": return self._select_all()
        if action == "save":
            self.export_file()
            return "break"

    def _undo(self, event=None):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass
        self.redraw_gutter()
        return "break"

    def _redo(self, event=None):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass
        self.redraw_gutter()
        return "break"

    def _copy(self, event=None):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.text.get("sel.first", "sel.last"))
        except tk.TclError:
            pass
        return "break"

    def _paste(self, event=None):
        try:
            data = self.root.clipboard_get()
        except tk.TclError:
            return "break"
        try:
            self.text.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        self.text.insert("insert", data)
        self.redraw_gutter()
        return "break"

    def _cut(self, event=None):
        try:
            data = self.text.get("sel.first", "sel.last")
        except tk.TclError:
            return "break"
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        self.text.delete("sel.first", "sel.last")
        self.redraw_gutter()
        return "break"

    def _select_all(self, event=None):
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "1.0")
        return "break"

    # ---------------- скролл ----------------
    def _on_scroll(self, *args):
        self.text.yview(*args)
        self.redraw_gutter()

    def _on_text_yscroll(self, sb, *args):
        sb.set(*args)
        self.redraw_gutter()

    def _on_modified(self, event):
        if self.text.edit_modified():
            self.redraw_gutter()
            self.text.edit_modified(False)

    # ---------------- gutter ----------------
    def _line_has_red(self, line_num):
        start = f"{line_num}.0"
        end = f"{line_num}.end"
        ranges = self.text.tag_ranges("red")
        for j in range(0, len(ranges), 2):
            if self.text.compare(ranges[j], "<", end) and \
               self.text.compare(ranges[j + 1], ">", start):
                return True
        return False

    def redraw_gutter(self):
        self.gutter.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y, h = dline[1], dline[3]
            line_num = str(i).split(".")[0]

            color = "#e53935" if self._line_has_red(line_num) else "#c8c8c8"
            r = (h - 6) / 2
            cx, cy = 12, y + h / 2
            self.gutter.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill=color, outline="")

            self.gutter.create_text(self.GUTTER_WIDTH - 6, cy,
                                    anchor="e", text=line_num,
                                    font=("Consolas", 9), fill="#888")
            i = self.text.index(f"{i}+1line")

    def on_gutter_click(self, event):
        y = event.y
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                return
            if dline[1] <= y < dline[1] + dline[3]:
                self.text.edit_separator()
                self.toggle_red(str(i).split(".")[0])
                return
            i = self.text.index(f"{i}+1line")

    def toggle_red(self, line_num):
        start = f"{line_num}.0"
        end = f"{line_num}.end"
        if self._line_has_red(line_num):
            ranges = self.text.tag_ranges("red")
            for j in range(0, len(ranges), 2):
                if self.text.compare(ranges[j], "<", end) and \
                   self.text.compare(ranges[j + 1], ">", start):
                    s = ranges[j] if self.text.compare(ranges[j], ">=", start) else start
                    e = ranges[j + 1] if self.text.compare(ranges[j + 1], "<=", end) else end
                    self.text.tag_remove("red", s, e)
        else:
            self.text.tag_add("red", start, end)
        self.redraw_gutter()

    # ---------------- файлы ----------------
    def import_file(self):
        path = filedialog.askopenfilename(
            title="Импорт текстового файла",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Ошибка чтения", str(e))
            return

        self.text.edit_separator()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", data)
        self.text.tag_remove("red", "1.0", "end")
        self.text.edit_separator()
        self.redraw_gutter()

    def export_file(self):
        path = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            data = self.text.get("1.0", "end-1c")
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            messagebox.showerror("Ошибка записи", str(e))

    # ---------------- действия ----------------
    def apply_raspr(self):
        content = self.text.get("1.0", "end-1c")
        lines = content.split("\n")
        raw = [l + "\n" for l in lines]

        try:
            result = raspr(raw)
        except Exception as e:
            messagebox.showerror("Ошибка raspr", str(e))
            return

        self.text.edit_separator()          # граница undo
        self.text.tag_remove("red", "1.0", "end")

        # замены
        for item in result:
            if len(item) != 3:
                continue
            idx, flag, newtext = item
            if flag == 1 and 0 <= idx < len(lines):
                ln = idx + 1
                s, e = f"{ln}.0", f"{ln}.end"
                self.text.delete(s, e)
                self.text.insert(s, newtext.rstrip("\n"))

        # подсветка
        for item in result:
            if len(item) != 3:
                continue
            idx, flag, newtext = item
            if flag == 0 and 0 <= idx < len(lines):
                ln = idx + 1
                self.text.tag_add("red", f"{ln}.0", f"{ln}.end")

        self.text.edit_separator()
        self.redraw_gutter()

    def apply_reverse(self):
        try:
            sel_start = self.text.index("sel.first")
            sel_end = self.text.index("sel.last")
        except tk.TclError:
            messagebox.showinfo("Нет выделения",
                                "Выдели строки мышкой, к которым применить reverse")
            return

        start_line = int(sel_start.split(".")[0])
        end_line = int(sel_end.split(".")[0])

        # Если выделение закончилось в САМОМ НАЧАЛЕ строки (N.0),
        # эта строка в выделение не входит — не трогаем её.
        if sel_end.split(".")[1] == "0" and end_line > start_line:
            end_line -= 1

        # Запоминаем, какие строки были красными
        red_lines = set()
        for ln in range(start_line, end_line + 1):
            if self._line_has_red(ln):
                red_lines.add(ln)

        self.text.edit_separator()

        # Идём СНИЗУ ВВЕРХ: тогда изменения номера строк не сдвигают.
        for ln in range(end_line, start_line - 1, -1):
            s = f"{ln}.0"
            e = f"{ln}.end"
            old = self.text.get(s, e)

            new = reverse(old)

            # Страховка: reverse не должна «размножать» строку.
            if not isinstance(new, str):
                new = str(new)
            new = new.replace("\r", "").replace("\n", "")

            self.text.delete(s, e)
            self.text.insert(s, new)

            # Восстанавливаем подсветку, если строка была красной
            if ln in red_lines:
                self.text.tag_add("red", f"{ln}.0", f"{ln}.end")

        self.text.edit_separator()
        self.redraw_gutter()

    def clear_red(self):
        self.text.edit_separator()
        self.text.tag_remove("red", "1.0", "end")
        self.text.edit_separator()
        self.redraw_gutter()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()

    #with open('KIW2.0.txt', 'r')  as f: x = f.readlines()
    #print(raspr(x))