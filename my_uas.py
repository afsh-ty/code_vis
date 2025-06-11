import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

class UKTPaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pembayaran UKT Mahasiswa")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f8ff")

        # Inisialisasi database
        self.initialize_database()

        # Frame utama
        self.main_frame = tk.Frame(root, bg="#f0f8ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Judul
        tk.Label(self.main_frame, text="UKT Payment", font=("Arial", 18, "bold"), 
                 bg="#f0f8ff", fg="#2c3e50").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self.main_frame, text="Universitas Islam Ar-Raniry", 
                 font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, columnspan=2, pady=2)

        # Frame input
        self.input_frame = tk.LabelFrame(self.main_frame, text="Form Pembayaran", 
                                         bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        self.input_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")

        field_info = [
            ("Nama Mahasiswa", "name", "contoh: Ahmad Syafiq"),
            ("NIM", "nim", "contoh: 12345678"),
            ("Jurusan", "jurusan", "contoh: Teknik Informatika"),
            ("Semester", "semester", "contoh: 5"),
            ("Jumlah UKT (Rp)", "amount", "contoh: 2500000")
        ]

        for i, (label_text, field_attr, placeholder) in enumerate(field_info):
            tk.Label(self.input_frame, text=label_text, font=("Arial", 10), bg="white").grid(row=i*2, column=0, pady=(5, 2), sticky="w")
            entry = ttk.Entry(self.input_frame)
            entry.grid(row=i*2+1, column=0, padx=5, pady=2, sticky="ew")
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e: e.widget.delete(0, tk.END))
            setattr(self, f"{field_attr}_entry", entry)

        tk.Label(self.input_frame, text="Metode Pembayaran", font=("Arial", 10), bg="white").grid(row=10, column=0, pady=(5, 2), sticky="w")
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(self.input_frame, textvariable=self.method_var, state="readonly", font=("Arial", 10))
        self.method_combo['values'] = ("Transfer Bank", "E-Wallet", "Kartu Kredit", "Tunai")
        self.method_combo.current(0)
        self.method_combo.grid(row=11, column=0, padx=5, pady=2, sticky="ew")

        self.pay_btn = ttk.Button(self.input_frame, text="Bayar Sekarang", command=self.process_payment, style="Accent.TButton")
        self.pay_btn.grid(row=12, column=0, padx=5, pady=15, sticky="ew")

        self.history_frame = tk.LabelFrame(self.main_frame, text="Histori Pembayaran", bg="white", bd=2, relief=tk.RIDGE, padx=10, pady=10)
        self.history_frame.grid(row=2, column=1, padx=10, pady=15, sticky="nsew")

        self.history_tree = ttk.Treeview(self.history_frame, columns=("NIM", "Nama", "Tanggal", "Jumlah", "Metode", "Status"), show="headings", selectmode="browse")
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        columns = [
            ("NIM", 100, "center"),
            ("Nama", 150, "w"),
            ("Tanggal", 120, "center"),
            ("Jumlah", 100, "e"),
            ("Metode", 100, "center"),
            ("Status", 80, "center")
        ]

        for col, width, anchor in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=width, anchor=anchor)

        self.history_tree.pack(fill=tk.BOTH, expand=True)

        self.refresh_btn = ttk.Button(self.main_frame, text="Refresh Histori", command=self.refresh_history)
        self.refresh_btn.grid(row=3, column=1, padx=10, pady=5, sticky="e")

        # 🔄 Tombol Reset Data
        self.reset_btn = ttk.Button(self.main_frame, text="Reset Data", command=self.reset_data)
        self.reset_btn.grid(row=4, column=1, padx=10, pady=5, sticky="e")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(2, weight=1)

        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Accent.TButton", font=('Arial', 10, 'bold'), foreground='white')

        self.refresh_history()

    def create_connection(self):
        try:
            os.makedirs('database', exist_ok=True)
            return sqlite3.connect('database/ukt_pembayaran.db')
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

    def create_tables(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    nim TEXT PRIMARY KEY,
                    nama TEXT NOT NULL,
                    jurusan TEXT NOT NULL,
                    semester INTEGER NOT NULL,
                    ukt_nominal INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pembayaran_ukt (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL,
                    tanggal_bayar TEXT NOT NULL,
                    jumlah_bayar INTEGER NOT NULL,
                    metodo_pembayaran TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (nim) REFERENCES mahasiswa (nim)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating tables: {e}")

    def initialize_database(self):
        conn = self.create_connection()
        if conn:
            self.create_tables(conn)
            conn.close()

    def process_payment(self):
        name = self.name_entry.get().strip()
        nim = self.nim_entry.get().strip()
        jurusan = self.jurusan_entry.get().strip()
        semester = self.semester_entry.get().strip()
        amount = self.amount_entry.get().strip()
        method = self.method_var.get()

        if not name or len(name) < 3:
            messagebox.showerror("Kesalahan", "Nama harus diisi (minimal 3 karakter)")
            return
        if not nim or not nim.isdigit() or len(nim) != 8:
            messagebox.showerror("Kesalahan", "NIM harus 8 digit angka")
            return
        if not jurusan:
            messagebox.showerror("Kesalahan", "Jurusan harus diisi")
            return
        try:
            semester_int = int(semester)
            if semester_int < 1 or semester_int > 14:
                raise ValueError
        except ValueError:
            messagebox.showerror("Kesalahan", "Semester harus angka (1-14)")
            return
        try:
            amount_int = int(amount.replace(',', '').replace('.', ''))
            if amount_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Kesalahan", "Jumlah UKT harus angka positif")
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Pembayaran",
            f"Apakah data sudah benar?\n\nNama: {name}\nNIM: {nim}\nJurusan: {jurusan}\n"
            f"Semester: {semester}\nJumlah: Rp {amount_int:,}\nMetode: {method}"
        )
        if not confirm:
            return

        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO mahasiswa (nim, nama, jurusan, semester, ukt_nominal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nim, name, jurusan, semester_int, amount_int))

                tanggal_bayar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute('''
                    INSERT INTO pembayaran_ukt (nim, tanggal_bayar, jumlah_bayar, metodo_pembayaran, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nim, tanggal_bayar, amount_int, method, "LUNAS"))

                conn.commit()

                messagebox.showinfo("Pembayaran Berhasil",
                    f"Pembayaran UKT berhasil disimpan:\n\nNama: {name}\nNIM: {nim}\n"
                    f"Jumlah: Rp {amount_int:,}\nMetode: {method}\nStatus: LUNAS")

                for entry in [self.name_entry, self.nim_entry, self.jurusan_entry, self.semester_entry, self.amount_entry]:
                    entry.delete(0, tk.END)
                self.method_combo.current(0)

                self.refresh_history()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error menyimpan pembayaran: {e}")
            finally:
                conn.close()

    def refresh_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT m.nim, m.nama, p.tanggal_bayar, p.jumlah_bayar, 
                           p.metodo_pembayaran, p.status
                    FROM pembayaran_ukt p
                    JOIN mahasiswa m ON p.nim = m.nim
                    ORDER BY p.tanggal_bayar DESC
                    LIMIT 100
                ''')
                for row in cursor.fetchall():
                    self.history_tree.insert("", tk.END, values=(
                        row[0], row[1], row[2], f"Rp {row[3]:,}", row[4], row[5]
                    ))
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error mengambil histori: {e}")
            finally:
                conn.close()

    def reset_data(self):
        confirm = messagebox.askyesno("Konfirmasi Reset", 
            "Apakah Anda yakin ingin menghapus SEMUA data pembayaran dan mahasiswa?")
        if not confirm:
            return

        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pembayaran_ukt")
                cursor.execute("DELETE FROM mahasiswa")
                conn.commit()
                messagebox.showinfo("Reset Berhasil", "Semua data berhasil dihapus.")
                self.refresh_history()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Gagal menghapus data: {e}")
            finally:
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UKTPaymentApp(root)
    root.mainloop()
