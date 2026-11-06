
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Python": [".py"]
}

BG = "#151922"
PANEL = "#202735"
ACCENT = "#4F8CFF"
TEXT = "#FFFFFF"
MUTED = "#AAB4C3"

root = tk.Tk()
root.title("File Organizer PRO")
root.geometry("850x700")
root.configure(bg=BG)
root.minsize(750, 600)

selected_folder = None


def get_category(file):
    extension = file.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return None


def get_unique_path(path):
    if not path.exists():
        return path

    counter = 1

    while True:
        new_path = path.with_name(
            f"{path.stem}_{counter}{path.suffix}"
        )

        if not new_path.exists():
            return new_path

        counter += 1


def choose_folder():
    global selected_folder

    folder = filedialog.askdirectory()

    if folder:
        selected_folder = Path(folder)
        folder_label.config(text=str(selected_folder))
        output.delete("1.0", tk.END)
        status_label.config(text="Folder selected")


def preview_files():
    if selected_folder is None:
        messagebox.showwarning("Warning", "Select a folder first!")
        return

    output.delete("1.0", tk.END)

    statistics = {category: 0 for category in FILE_TYPES}
    unknown = 0

    files = [
        file for file in selected_folder.iterdir()
        if file.is_file()
    ]

    for file in files:
        category = get_category(file)

        if category:
            statistics[category] += 1
            output.insert(tk.END, f"[{category}] {file.name}\n")
        else:
            unknown += 1
            output.insert(tk.END, f"[Other] {file.name}\n")

    output.insert(tk.END, "\n========== STATISTICS ==========\n")

    for category, count in statistics.items():
        output.insert(tk.END, f"{category}: {count}\n")

    output.insert(tk.END, f"Other files: {unknown}\n")
    output.insert(tk.END, f"Total files: {len(files)}\n")

    status_label.config(text="Preview completed")


def organize_files():
    if selected_folder is None:
        messagebox.showwarning("Warning", "Select a folder first!")
        return

    files = [
        file for file in selected_folder.iterdir()
        if file.is_file() and get_category(file)
    ]

    if not files:
        messagebox.showinfo("Info", "No supported files found.")
        return

    if not messagebox.askyesno(
        "Confirmation",
        f"Organize {len(files)} files?"
    ):
        return

    progress_bar["maximum"] = len(files)
    progress_bar["value"] = 0

    moved = 0
    errors = 0

    for index, file in enumerate(files, start=1):
        try:
            category = get_category(file)
            destination_folder = selected_folder / category
            destination_folder.mkdir(exist_ok=True)

            destination = get_unique_path(
                destination_folder / file.name
            )

            shutil.move(str(file), str(destination))
            moved += 1

        except OSError:
            errors += 1

        progress_bar["value"] = index
        status_label.config(
            text=f"Processing: {index}/{len(files)}"
        )
        root.update_idletasks()

    output.insert(tk.END, "\n========== RESULT ==========\n")
    output.insert(tk.END, f"Moved: {moved}\n")
    output.insert(tk.END, f"Errors: {errors}\n")

    status_label.config(text="Organization completed!")

    messagebox.showinfo(
        "Completed",
        f"Moved: {moved}\nErrors: {errors}"
    )


# HEADER

tk.Label(
    root,
    text="FILE ORGANIZER PRO",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(pady=(20, 5))

tk.Label(
    root,
    text="Smart file management system",
    font=("Arial", 11),
    bg=BG,
    fg=MUTED
).pack(pady=(0, 20))


# MAIN PANEL

panel = tk.Frame(root, bg=PANEL, padx=20, pady=20)
panel.pack(fill="x", padx=25)

tk.Label(
    panel,
    text="SELECT FOLDER",
    font=("Arial", 11, "bold"),
    bg=PANEL,
    fg=TEXT
).pack(anchor="w")

folder_label = tk.Label(
    panel,
    text="No folder selected",
    bg=PANEL,
    fg=MUTED,
    wraplength=650
)
folder_label.pack(anchor="w", pady=10)

tk.Button(
    panel,
    text="Browse Folder",
    command=choose_folder,
    bg=ACCENT,
    fg="white",
    relief="flat",
    padx=15,
    pady=8
).pack(anchor="w")


# ACTION BUTTONS

buttons = tk.Frame(root, bg=BG)
buttons.pack(pady=20)

tk.Button(
    buttons,
    text="Preview Files",
    command=preview_files,
    bg="#34445E",
    fg="white",
    relief="flat",
    padx=20,
    pady=10
).pack(side="left", padx=8)

tk.Button(
    buttons,
    text="Organize Files",
    command=organize_files,
    bg=ACCENT,
    fg="white",
    relief="flat",
    padx=20,
    pady=10
).pack(side="left", padx=8)


# PROGRESS BAR

tk.Label(
    root,
    text="ORGANIZATION PROGRESS",
    bg=BG,
    fg=TEXT,
    font=("Arial", 10, "bold")
).pack(pady=(5, 8))

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Custom.Horizontal.TProgressbar",
    troughcolor=PANEL,
    background=ACCENT,
    thickness=14
)

progress_bar = ttk.Progressbar(
    root,
    style="Custom.Horizontal.TProgressbar",
    length=700,
    mode="determinate"
)
progress_bar.pack(padx=25)


# OUTPUT

tk.Label(
    root,
    text="FILE REPORT",
    bg=BG,
    fg=TEXT,
    font=("Arial", 11, "bold")
).pack(anchor="w", padx=30, pady=(20, 8))

output = tk.Text(
    root,
    height=13,
    bg=PANEL,
    fg=TEXT,
    insertbackground=TEXT,
    font=("Consolas", 10),
    relief="flat",
    padx=12,
    pady=12
)
output.pack(fill="both", expand=True, padx=25, pady=(0, 15))


# STATUS BAR

status_label = tk.Label(
    root,
    text="Ready",
    bg=BG,
    fg=MUTED,
    font=("Arial", 9)
)
status_label.pack(pady=(0, 12))


root.mainloop()
