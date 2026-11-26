import tkinter as tk
from tkinter import filedialog, messagebox
import os
from all import work_MidiFile, note_from_number, cutting_track_to_one_voice, time_ms_from_Midi
from all import number_from_note as n
from mido import Message


strings = {
        4:list(range(n("g3"),n("d4"))),           
        3:list(range(n("d4"),n("a4"))),           
        2:list(range(n("a4"),n("e5"))),           
        1:list(range(n("e5"),n("h5")+1)),           
}


def emma_note(note: Message) -> str:
    for i in range(max(strings)+1):
        try: 
            lad=strings[i].index(note.note)
            return f'/sn;{i};{lad}'
        except Exception as e: pass
    print(note_from_number(note.note))
    return f'/sn;=;='


tempo_BPM = 120
tempo_ms = 30000/tempo_BPM



def get_options(file_path):
    mid = work_MidiFile(file_path)
    result = {}
    for i, track in enumerate(mid.tracks):
        if len(track)!=0:
            result[i]=f'{len(track)} нот: {' '.join([note_from_number(j) for j in [k for k in track if k.type=='note_on'][:min(5,len(track))]])}...'
    return result


def process_midi(file_path, choice_key):
    mid = work_MidiFile(file_path)
    mid.ticks_per_beat
    track = mid.tracks[choice_key]
    track = cutting_track_to_one_voice(track)
    
    result = []

    for i, msg in enumerate(track):
        if msg.type == 'note_on': 
            result.append(emma_note(msg)+'\n')
            if msg.time != 0: result.append(f'/p;{round(time_ms_from_Midi(msg.time,tempo_ms,mid.ticks_per_beat))}\n')
        else:
            if msg.time != 0: result.append(f'/bow;1;{round(time_ms_from_Midi(msg.time,tempo_ms,mid.ticks_per_beat))};100\n')
    

    return result

def choose_option(options, parent):
    """
    Показывает окно со списком вариантов.
    Выбор — по одиночному клику. Возвращает ключ (int) или None.
    """
    if not options:
        return None

    result = {"key": None}
    keys = list(options.keys())

    win = tk.Toplevel(parent)
    win.title("Выберите вариант")
    win.grab_set()
    win.resizable(False, False)

    tk.Label(win, text="Кликните по нужной строке:").pack(padx=10, pady=(10, 4))

    # Высота = число строк (без прокрутки, если их немного)
    listbox = tk.Listbox(win, height=len(keys), activestyle="none",
                         exportselection=False)
    listbox.pack(fill="x", padx=10, pady=(0, 10))

    for k in keys:
        listbox.insert(tk.END, options[k])

    def on_click(event=None):
        sel = listbox.curselection()
        if not sel:
            return
        result["key"] = keys[sel[0]]
        win.destroy()

    listbox.bind("<Button-1>", lambda e: win.after(10, on_click))
    listbox.bind("<Return>", on_click)

    # Закрытие окна = отмена
    win.protocol("WM_DELETE_WINDOW", win.destroy)

    # Центрируем относительно родителя
    win.update_idletasks()
    win.wait_window()
    return result["key"]


def main():
    root = tk.Tk()
    root.withdraw()

    # 1. Выбор MIDI-файла
    midi_path = filedialog.askopenfilename(
        title="Выберите MIDI-файл",
        filetypes=[("MIDI files", "*.mid *.midi"), ("All files", "*.*")]
    )
    if not midi_path:
        return

    # 2. Окно выбора варианта (клик — и сразу закрывается)
    options = get_options(midi_path)
    if not options:
        messagebox.showerror("Ошибка", "Нет доступных вариантов")
        return

    choice_key = choose_option(options, root)
    if choice_key is None:
        return

    # 3. Сразу выбор места сохранения
    default_name = os.path.splitext(os.path.basename(midi_path))[0] + ".txt"
    txt_path = filedialog.asksaveasfilename(
        title="Сохранить результат как",
        defaultextension=".txt",
        initialfile=default_name,
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not txt_path:
        return

    # 4. Обработка и сохранение
    try:
        result = process_midi(midi_path, choice_key)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.writelines(result)
        messagebox.showinfo("Готово", f"Результат сохранён:\n{txt_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    main()
