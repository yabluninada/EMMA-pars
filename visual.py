import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def _get_bounds(interval):
    """Достаёт (lower, upper) из интервала с учётом разных версий interval_sets."""
    for lo, hi in [
        ('lower', 'upper'),
        ('left', 'right'),
        ('start', 'end'),
        ('begin', 'end'),
        ('a', 'b'),
    ]:
        if hasattr(interval, lo) and hasattr(interval, hi):
            return getattr(interval, lo), getattr(interval, hi)
    raise AttributeError(f"Не удалось определить границы интервала: {interval!r}")


def _draw_sets(ax, sets_array, color, bar_width=1.0,
               alpha=0.4, label=None):
    """Рисует массив интервал-сетов вертикальными прямоугольниками."""
    label_used = False
    for i, s in enumerate(sets_array):
        for interval in s:
            lo, hi = _get_bounds(interval)
            ax.add_patch(Rectangle(
                (i - bar_width / 2, lo),
                bar_width,
                hi - lo,
                facecolor=color,
                edgecolor='none',
                linewidth=0,
                alpha=alpha,
                antialiased=False,
                label=label if not label_used else None,
            ))
            label_used = True


def plot_interval_sets(
    l0,
    l1,
    p=None,
    *,
    y_min=-1000,
    y_max=101000,
    figsize=(16, 9),
    bar_width=1.0,
    alpha=0.4,
    color0='tab:blue',
    color1='tab:orange',
    label0='l0',
    label1='l1',
    p_color='red',
    p_label='p',
    separator_color='#333333',
    separator_width=0.5,
    separator_alpha=0.8,
    title='Сравнение двух массивов interval-sets',
    save_path=None,
):
    """Строит сравнение двух массивов интервал-сетов с наложением.

    Параметры
    ---------
    l0, l1 : массивы interval_sets
    p : list[float] | None
        Необязательный список Y-значений (по одному на столбец).
        Рисуется красной ломаной с точками-маркерами.
        Длина не должна превышать max(len(l0), len(l1)).
    """
    n = max(len(l0), len(l1))

    if p is not None:
        if len(p) > n:
            raise ValueError(
                f"Длина p={len(p)} превышает число столбцов n={n}"
            )

    fig, ax = plt.subplots(figsize=figsize)

    _draw_sets(ax, l0, color=color0,
               bar_width=bar_width, alpha=alpha, label=label0)
    _draw_sets(ax, l1, color=color1,
               bar_width=bar_width, alpha=alpha, label=label1)

    # --- Разделители между столбцами ---
    for i in range(n - 1):
        ax.axvline(
            i + 0.5,
            color=separator_color,
            linewidth=separator_width,
            alpha=separator_alpha,
            zorder=10,
        )

    # --- Красная ломаная с точками ---
    if p is not None and len(p) > 0:
        xs = list(range(len(p)))
        ax.plot(
            xs, p,
            color=p_color,
            linewidth=1.5,
            marker='o',
            markersize=5,
            markerfacecolor=p_color,
            markeredgecolor=p_color,
            zorder=20,
            label=p_label,
        )

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(range(n))
    ax.set_xlabel('Порядковый номер интервал-сета в массиве')
    ax.set_ylabel('Значение интервала')
    ax.set_title(title)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right', framealpha=0.9)

    fig.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=150)
    plt.show()
    return fig, ax