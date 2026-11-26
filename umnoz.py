import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# ============ ФУНКЦИЯ f ============
def f(lines, old_value, new_value, flag1=False, flag2=False,
      flag3=False, flag4=False, flag5=False):
    for i in range(len(lines)):
        l=lines[i].split(';')

        if l[0]=='/bow':
            if not flag1:
                l[2]=str(round(int(l[2])*old_value/new_value))
                l[3]=str(round(int(l[3])*new_value/old_value))
            else:
                l[2]=str(round(timings[1][i]*timings[0]/new_value))
                l[3]=str(round(smych[i]/int(l[2]))) 
                
        elif l[0]=='/p':
            if not flag1:
                l[1]=str(round(int(l[1])*old_value/new_value))
            else:
                l[1]=str(round(timings[1][i]*timings[0]/new_value))
        else: pass

    
        lines[i]=';'.join(l)

    return lines
# ========================================


# ============ ВАЛИДАТОР ============
def validator(lines):

    a=[]
    sm=0
    bown=0
    for i in range(len(lines)):
        l=lines[i].split(';')
        
        if len(l)>=4:
            if l[0]=='/bow':
                bown+=1
                if l[1]=='1': zn=1
                else: zn=-1
                sm+=int(l[2])*zn*int(l[3])

                if int(l[-1])<=55: a.append((i+1,f'малая скорость смычка '+l[-1]))

                

        if sm>100000+2000 or sm<0-2000: 
            a.append((i,f'смычок на {sm}'))

        if bown > 2 and l[0]=='/bow':
            ls = lines[:i]
            ls = [j for j in ls if '/sn' in j or '/bow' in j]
            l1=ls[-2].split(';')
            s=ls[-1].split(';')
            s1=ls[-3].split(';')

            if l1[1]==l[1] and s1[1]!=s[1]: a.append((i,f'отсуутствует смена смычка при переходе'))

        

                                        
    
    return a



# ========================================



timings = (120,[])
smych = []


# ============ ФУНКЦИЯ G ============
def G(lines, temp):



    x_bow = [(i,lines[i].split(';')) for i in range(len(lines)) if lines[i].split(';')[0]=='/bow']
    x_p = [(i,lines[i].split(';')) for i in range(len(lines)) if lines[i].split(';')[0]=='/p']

    global timings
    global smych
    z = {i[0]: int(i[1][2]) for i in x_bow}
    for i in x_p: z[i[0]] = int(i[1][1])
    timings=(temp, z)
    smych={i[0]: int(i[1][2])*int(i[1][3]) for i in x_bow}

    
    return lines
# ========================================


class App:
    GUTTER_WIDTH = 55
    RIGHT_PANEL_WIDTH = 320

    def __init__(self, root):
        self.root = root
        root.title("Редактор со слайдером и валидатором")
        root.geometry("1400x740")
        root.configure(bg="#fafafa")

        # ---------------- стили ----------------
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=(10, 6), font=("Segoe UI", 10))
        style.configure("TScale", background="white")

        # ---------------- верхняя панель ----------------
        tb = ttk.Frame(root)
        tb.pack(fill="x", padx=12, pady=(12, 0))
        ttk.Button(tb, text="📂  Импорт", command=self.import_file).pack(side="left")
        ttk.Button(tb, text="💾  Сохранить", command=self.export_file).pack(side="left", padx=6)
        ttk.Button(tb, text="✅  Валидатор", command=self.run_validator).pack(side="left", padx=(20, 0))

        # ---------------- карточка параметров ----------------
        card = tk.Frame(root, bg="white", highlightthickness=1,
                        highlightbackground="#e3e3e3")
        card.pack(fill="x", padx=12, pady=10)
        inner = tk.Frame(card, bg="white")
        inner.pack(fill="x", padx=16, pady=14)

        tk.Label(inner, text="Значение", bg="white",
                 font=("Segoe UI", 10, "bold"), fg="#333"
                 ).grid(row=0, column=0, sticky="w")

        self.slider_var = tk.IntVar(value=120)
        self.slider = ttk.Scale(inner, from_=1, to=400, orient="horizontal",
                                variable=self.slider_var, length=420,
                                command=self._on_slider)
        self.slider.grid(row=0, column=1, padx=(12, 12), sticky="ew")

        self.value_label = tk.Label(inner, text="120", width=5, bg="white",
                                    font=("Consolas", 12, "bold"),
                                    fg="#1976d2")
        self.value_label.grid(row=0, column=2, sticky="w")

        inner.columnconfigure(1, weight=1)

        tk.Frame(inner, bg="#ececec", height=1
                 ).grid(row=1, column=0, columnspan=3, sticky="ew", pady=12)

        tk.Label(inner, text="Опции", bg="white",
                 font=("Segoe UI", 10, "bold"), fg="#333"
                 ).grid(row=2, column=0, sticky="nw")

        flags_frame = tk.Frame(inner, bg="white")
        flags_frame.grid(row=2, column=1, columnspan=2, sticky="w")

        self.bool_vars = [tk.BooleanVar(value=False) for _ in range(5)]
        LABELS = ["Строгая зависимость от импорта", "Опция 2", "Опция 3", "Опция 4", "Опция 5"]
        for i, v in enumerate(self.bool_vars):
            cb = tk.Checkbutton(
                flags_frame, text=LABELS[i], variable=v, bg="white",
                font=("Segoe UI", 10), activebackground="white",
                selectcolor="white", cursor="hand2",
                command=self._on_flags,
            )
            cb.pack(side="left", padx=(0, 18))



        # ---------------- редактор ----------------
        main = ttk.Frame(root)
        main.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.gutter = tk.Canvas(main, width=self.GUTTER_WIDTH, bg="#f0f0f0",
                                highlightthickness=0)
        self.gutter.pack(side="left", fill="y")

        self.text = tk.Text(main, wrap="none", font=("Consolas", 11),
                            undo=True, autoseparators=True, maxundo=-1,
                            padx=8, pady=6, relief="flat",
                            bg="white", insertbackground="#333",
                            selectbackground="#bcd6ff")
        self.text.pack(side="left", fill="both", expand=True)

        # правая панель заметок (read-only canvas)
        self.right_panel = tk.Canvas(main, width=self.RIGHT_PANEL_WIDTH,
                                     bg="#fff8f8", highlightthickness=0)
        self.right_panel.pack(side="left", fill="y")

        sb = ttk.Scrollbar(main, orient="vertical", command=self._on_scroll)
        sb.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=lambda *a: self._on_text_yscroll(sb, *a))

        self.text.tag_configure("red", background="#e53935", foreground="white")

        # ---------------- состояние ----------------
        self.source_lines = []
        self._updating = False
        self._slider_job = None
        self._old_slider_value = self.slider_var.get()
        self.validator_notes = {}   # {номер_строки(1-based): текст_комментария}

        # ---------------- события ----------------
        self.text.bind("<KeyRelease>", lambda e: self.redraw_gutter())
        self.text.bind("<ButtonRelease-1>", lambda e: self.redraw_gutter())
        self.text.bind("<Configure>", lambda e: self.redraw_gutter())
        self.text.bind("<<Modified>>", self._on_modified)
        self.gutter.bind("<Button-1>", self.on_gutter_click)

        self._bind_hotkeys()

        example = (
            "Первая строка сценария\n"
            "Вторая, довольно длинная строка для примера\n"
            "Третья\n"
            "Четвёртая тоже длинная строка для демонстрации работы\n"
            "Пятая"
        )
        self.source_lines = example.split("\n")
        self._updating = True
        self.text.insert("1.0", example)
        self._updating = False
        self.text.edit_reset()
        self.text.edit_modified(False)
        self.redraw_gutter()

    # ============ параметры ============
    def _on_slider(self, _=None):
        self.value_label.configure(text=str(self.slider_var.get()))
        if self._slider_job:
            self.root.after_cancel(self._slider_job)
        self._slider_job = self.root.after(60, self._apply_f)

    def _on_flags(self):
        self._apply_f()

    def _apply_f(self):
        self._slider_job = None
        if not self.source_lines:
            return

        new_value = self.slider_var.get()
        old_value = self._old_slider_value

        try:
            result = f(
                self.source_lines,
                old_value,
                new_value,
                *[v.get() for v in self.bool_vars],
            )
        except Exception as e:
            messagebox.showerror("Ошибка f", str(e))
            return

        if result is None:
            return

        if isinstance(result, str):
            result = result.split("\n")
        result = [str(x).rstrip("\r\n") for x in result]

        self.text.edit_separator()
        self._updating = True
        try:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "\n".join(result))
            self.text.tag_remove("red", "1.0", "end")
        finally:
            self._updating = False
        self.text.edit_separator()

        # текст изменился — старые валидаторские заметки больше не при делах
        self.validator_notes = {}

        self._old_slider_value = new_value
        self.redraw_gutter()

    # ============ валидатор ============
    def run_validator(self):
        # всё старое стираем
        self.validator_notes = {}
        self.text.tag_remove("red", "1.0", "end")

        if not self.source_lines:
            self.redraw_gutter()
            return

        try:
            result = validator(self.source_lines)
        except Exception as e:
            messagebox.showerror("Ошибка валидатора", str(e))
            self.redraw_gutter()
            return

        if not result:
            self.redraw_gutter()
            return

        # определяем число строк в текущем редакторе (для отсечения выходов за пределы)
        total_lines = int(self.text.index("end-1c").split(".")[0])

        for item in result:
            try:
                line_num, note = item[0], item[1]
            except (TypeError, IndexError):
                continue
            try:
                ln = int(line_num)
            except (TypeError, ValueError):
                continue
            if ln < 1 or ln > total_lines:
                continue
            self.validator_notes[ln] = str(note)
            self.text.tag_add("red", f"{ln}.0", f"{ln}.end")

        self.text.edit_separator()
        self.redraw_gutter()

    # ============ синхронизация источника ============
    def _on_modified(self, event):
        if self.text.edit_modified():
            if not self._updating:
                self.source_lines = self.text.get("1.0", "end-1c").split("\n")
            self.redraw_gutter()
            self.text.edit_modified(False)

    # ============ горячие клавиши ============
    def _bind_hotkeys(self):
        self.text.bind("<Control-KeyPress>", self._on_ctrl_key)
        self.root.bind("<Control-KeyPress>", self._on_ctrl_key)

    def _on_ctrl_key(self, event):
        code = event.keycode
        ks = event.keysym.lower()

        if code == 90 or ks in ("z", "cyrillic_ya"):
            return self._undo()
        if code == 89 or ks in ("y", "cyrillic_en"):
            return self._redo()
        if code == 67 or ks in ("c", "cyrillic_es"):
            return self._copy()
        if code == 86 or ks in ("v", "cyrillic_em"):
            return self._paste()
        if code == 88 or ks in ("x", "cyrillic_che"):
            return self._cut()
        if code == 65 or ks in ("a", "cyrillic_ef"):
            return self._select_all()
        if code == 83 or ks in ("s", "cyrillic_yeru"):
            self.export_file()
            return "break"
        return None

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

    # ============ скролл ============
    def _on_scroll(self, *args):
        self.text.yview(*args)
        self.redraw_gutter()

    def _on_text_yscroll(self, sb, *args):
        sb.set(*args)
        self.redraw_gutter()

    # ============ gutter + правая панель ============
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
        self.right_panel.delete("all")

        # подгоняем высоту правой панели под высоту текстового поля
        try:
            self.right_panel.configure(height=self.text.winfo_height())
        except tk.TclError:
            pass

        # лёгкая вертикальная разделительная линия
        self.right_panel.create_line(0, 0, 0, self.right_panel.winfo_height(),
                                     fill="#f0d0d0")

        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y, h = dline[1], dline[3]
            line_num = str(i).split(".")[0]
            ln_int = int(line_num)

            has_red = self._line_has_red(line_num)

            # -------- gutter --------
            color = "#e53935" if has_red else "#c8c8c8"
            r = (h - 6) / 2
            cx, cy = 12, y + h / 2
            self.gutter.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    fill=color, outline="")
            self.gutter.create_text(self.GUTTER_WIDTH - 6, cy,
                                    anchor="e", text=line_num,
                                    font=("Consolas", 9), fill="#888")

            # -------- правая панель --------
            if has_red and ln_int in self.validator_notes:
                note = self.validator_notes[ln_int]
                self.right_panel.create_rectangle(
                    1, y, self.RIGHT_PANEL_WIDTH, y + h,
                    fill="#fdecea", outline="#f5c6c6"
                )
                self.right_panel.create_text(
                    8, y + h / 2, anchor="w",
                    text=note,
                    font=("Consolas", 10),
                    fill="#b71c1c",
                    width=self.RIGHT_PANEL_WIDTH - 16,
                )

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
            # заметку НЕ удаляем из словаря — при повторном включении
            # красного она снова появится справа
        else:
            self.text.tag_add("red", start, end)
        self.redraw_gutter()

    # ============ файлы ============
    def import_file(self):
        path = filedialog.askopenfilename(
            title="Импорт текстового файла",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fp:
                data = fp.read()
        except Exception as e:
            messagebox.showerror("Ошибка чтения", str(e))
            return

        raw_lines = data.split("\n")

        # ---- прогоняем через G ----
        try:
            processed = G(raw_lines,  self.slider_var.get())
        except Exception as e:
            messagebox.showerror("Ошибка G", str(e))
            return

        if processed is None:
            final_lines = raw_lines
        elif isinstance(processed, str):
            final_lines = processed.split("\n")
        else:
            final_lines = [str(x).rstrip("\r\n") for x in processed]

        self.source_lines = final_lines
        self.validator_notes = {}

        new_text = "\n".join(final_lines)

        self._updating = True
        try:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", new_text)
            self.text.tag_remove("red", "1.0", "end")
        finally:
            self._updating = False
        self.text.edit_reset()
        self.text.edit_modified(False)
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
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(data)
        except Exception as e:
            messagebox.showerror("Ошибка записи", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()

    with open('KIW2.0.txt', 'r')  as f: x = f.readlines()
    print(validator(x))