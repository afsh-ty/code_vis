import tkinter as tk
from tkinter import ttk, messagebox

class UKTPaymentSimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pembayaran UKT Mahasiswa")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f8ff")
        self.root.resizable(False, False)

        # Judul
        tk.Label(root, text="UKT Payment", font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#2c3e50").pack(pady=10)
        tk.Label(root, text="Universitas Islam Ar-Raniry", font=("Arial", 12), bg="#f0f8ff").pack(pady=2)

        frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
        frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

        # Input Nama
        tk.Label(frame, text="Nama Mahasiswa", font=("Arial", 10), bg="white").pack(pady=(10, 2), anchor="w", padx=10)
        self.name_entry = ttk.Entry(frame)
        self.name_entry.pack(padx=10, fill=tk.X)

        # Input NIM
        tk.Label(frame, text="NIM", font=("Arial", 10), bg="white").pack(pady=(10, 2), anchor="w", padx=10)
        self.nim_entry = ttk.Entry(frame)
        self.nim_entry.pack(padx=10, fill=tk.X)

        # Input Jumlah
        tk.Label(frame, text="Jumlah Pembayaran (Rp)", font=("Arial", 10), bg="white").pack(pady=(10, 2), anchor="w", padx=10)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.pack(padx=10, fill=tk.X)

        # Metode Pembayaran
        tk.Label(frame, text="Metode Pembayaran", font=("Arial", 10), bg="white").pack(pady=(10, 2), anchor="w", padx=10)
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(frame, textvariable=self.method_var, state="readonly")
        self.method_combo['values'] = ("Transfer Bank", "E-Wallet", "Kartu Kredit")
        self.method_combo.current(0)
        self.method_combo.pack(padx=10, fill=tk.X, pady=(0, 10))

        # Tombol Bayar
        self.pay_btn = ttk.Button(root, text="Bayar Sekarang", command=self.process_payment)
        self.pay_btn.pack(pady=10)

    def process_payment(self):
        name = self.name_entry.get().strip()
        nim = self.nim_entry.get().strip()
        amount = self.amount_entry.get().strip()
        method = self.method_var.get()

        if not name or not nim or not amount:
            messagebox.showerror("Kesalahan", "Semua kolom wajib diisi.")
            return

        try:
            amount_float = float(amount.replace(',', '').replace('.', ''))
        except ValueError:
            messagebox.showerror("Kesalahan", "Jumlah pembayaran tidak valid.")
            return

        messagebox.showinfo(
            "Pembayaran Berhasil",
            f"Nama: {name}\nNIM: {nim}\nJumlah: Rp {amount}\nMetode: {method}"
        )

        # Reset
        self.name_entry.delete(0, tk.END)
        self.nim_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.method_combo.current(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = UKTPaymentSimpleApp(root)
    root.mainloop()
