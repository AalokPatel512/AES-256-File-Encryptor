import tkinter as tk
from tkinter import filedialog, messagebox
import pyzipper
import os
import threading


class FileEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 File Encryptor (AES-256)")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # === UI Elements ===
        self.create_widgets()

    def create_widgets(self):
        # --- File Selection ---
        tk.Label(self.root, text="Select File to Encrypt:", font=("Arial", 10)).pack(pady=5)
        self.file_label = tk.Entry(self.root, width=40)
        self.file_label.pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.select_file).pack(pady=5)

        # --- Password Entry ---
        tk.Label(self.root, text="Enter Password:", font=("Arial", 10)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=40)
        self.password_entry.pack(pady=5)

        tk.Label(self.root, text="Confirm Password:", font=("Arial", 10)).pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.root, show="*", width=40)
        self.confirm_password_entry.pack(pady=5)

        # --- Encrypt Button ---
        tk.Button(self.root, text="🔐 Encrypt File", command=self.start_encryption, font=("Arial", 10), bg="green",
                  fg="white").pack(pady=15)

        # --- Status Log Area ---
        self.status_label = tk.Label(self.root, text="", fg="blue", wraplength=400, justify="center")
        self.status_label.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.delete(0, tk.END)
            self.file_label.insert(0, file_path)

    def start_encryption(self):
        file_path = self.file_label.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return
        if not password or not confirm_password:
            messagebox.showerror("Error", "Please enter and confirm a password.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        self.status_label.config(text="Encrypting file... Please wait.")
        thread = threading.Thread(target=self.encrypt_file,
                                 args=(file_path, password))
        thread.start()

    def encrypt_file(self, file_path, password):
        try:
            base_name = os.path.basename(file_path)
            output_zip = os.path.splitext(file_path)[0] + "_encrypted.zip"

            with pyzipper.AESZipFile(output_zip, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password.encode())
                zf.writestr(base_name, open(file_path, 'rb').read())

            self.status_label.config(text=f"✅ Encryption Complete!\nEncrypted file saved as:\n{output_zip}")
            messagebox.showinfo("Success", f"File encrypted successfully:\n{output_zip}")

        except Exception as e:
            self.status_label.config(text="❌ Encryption failed.")
            messagebox.showerror("Encryption Error", str(e))

# === Run App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()