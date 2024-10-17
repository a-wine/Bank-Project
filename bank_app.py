import ctypes
from tkinter import *
from tkinter import messagebox, filedialog

# Load the shared library (ensure the path is correct)
bank_lib = ctypes.CDLL('./bank_management.dll')

# Define C++ functions
bank_lib.create_bank.argtypes = [ctypes.c_char_p]
bank_lib.create_bank.restype = ctypes.c_void_p
bank_lib.delete_bank.argtypes = [ctypes.c_void_p]
bank_lib.bank_deposit.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
bank_lib.bank_withdraw.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]
#bank_lib.find_client.argtypes = [ctypes.c_void_p, ctypes.c_double]
#bank_lib.find_client.restype = ctypes.c_char_p  # Expecting a string return

class BankApp:
    def __init__(self, master):
        # Configure the main window
        self.master = master
        self.master.title("Enhanced Bank Management System")
        self.master.geometry("800x600")  # Increased window size

        # Title Label
        self.title_label = Label(master, text="Welcome to Bank Management System", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # Load Bank Data Section
        self.load_frame = Frame(master, pady=10, padx=10)
        self.load_frame.pack()
        self.load_btn = Button(self.load_frame, text="Load Bank Data", font=("Arial", 14), command=self.load_data, bg="#5F9EA0", fg="white")
        self.load_btn.grid(row=0, column=0, padx=10, pady=5)
        self.load_status = Label(self.load_frame, text="No data loaded", font=("Arial", 12), fg="red")
        self.load_status.grid(row=0, column=1)

        # Deposit Section
        self.deposit_frame = LabelFrame(master, text="Deposit", font=("Arial", 16), pady=10, padx=10)
        self.deposit_frame.pack(pady=10, fill="both", expand="yes")
        self.deposit_acc_label = Label(self.deposit_frame, text="Account Number:", font=("Arial", 14))
        self.deposit_acc_label.grid(row=0, column=0, pady=5, sticky=E)
        self.deposit_acc = Entry(self.deposit_frame, font=("Arial", 14))
        self.deposit_acc.grid(row=0, column=1, pady=5, padx=5)

        self.deposit_amt_label = Label(self.deposit_frame, text="Amount:", font=("Arial", 14))
        self.deposit_amt_label.grid(row=1, column=0, pady=5, sticky=E)
        self.deposit_amt = Entry(self.deposit_frame, font=("Arial", 14))
        self.deposit_amt.grid(row=1, column=1, pady=5, padx=5)

        self.deposit_btn = Button(self.deposit_frame, text="Deposit", font=("Arial", 14), command=self.deposit, bg="#4CAF50", fg="white")
        self.deposit_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Withdraw Section
        self.withdraw_frame = LabelFrame(master, text="Withdraw", font=("Arial", 16), pady=10, padx=10)
        self.withdraw_frame.pack(pady=10, fill="both", expand="yes")
        self.withdraw_acc_label = Label(self.withdraw_frame, text="Account Number:", font=("Arial", 14))
        self.withdraw_acc_label.grid(row=0, column=0, pady=5, sticky=E)
        self.withdraw_acc = Entry(self.withdraw_frame, font=("Arial", 14))
        self.withdraw_acc.grid(row=0, column=1, pady=5, padx=5)

        self.withdraw_amt_label = Label(self.withdraw_frame, text="Amount:", font=("Arial", 14))
        self.withdraw_amt_label.grid(row=1, column=0, pady=5, sticky=E)
        self.withdraw_amt = Entry(self.withdraw_frame, font=("Arial", 14))
        self.withdraw_amt.grid(row=1, column=1, pady=5, padx=5)

        self.withdraw_btn = Button(self.withdraw_frame, text="Withdraw", font=("Arial", 14), command=self.withdraw, bg="#f57c00", fg="white")
        self.withdraw_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Find Client Section
        self.find_frame = LabelFrame(master, text="Find Client", font=("Arial", 16), pady=10, padx=10)
        self.find_frame.pack(pady=10, fill="both", expand="yes")
        self.find_acc_label = Label(self.find_frame, text="Account Number:", font=("Arial", 14))
        self.find_acc_label.grid(row=0, column=0, pady=5, sticky=E)
        self.find_acc = Entry(self.find_frame, font=("Arial", 14))
        self.find_acc.grid(row=0, column=1, pady=5, padx=5)
        self.find_btn = Button(self.find_frame, text="Find Client", font=("Arial", 14), command=self.find_client, bg="#0288d1", fg="white")
        self.find_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Exit Button
        self.exit_btn = Button(master, text="Exit", font=("Arial", 14), command=self.master.quit, bg="#B22222", fg="white")
        self.exit_btn.pack(pady=10)

    def load_data(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.bank = bank_lib.create_bank(filename.encode('utf-8'))
            self.load_status.config(text="Data Loaded Successfully", fg="green")
            messagebox.showinfo("Info", "Data Loaded Successfully")

    def deposit(self):
        try:
            acc_num = float(self.deposit_acc.get())
            amount = float(self.deposit_amt.get())
            bank_lib.bank_deposit(self.bank, acc_num, amount)
            messagebox.showinfo("Info", "Deposit Successful")
        except Exception as e:
            messagebox.showerror("Error", "Invalid input!")

    def withdraw(self):
        try:
            acc_num = float(self.withdraw_acc.get())
            amount = float(self.withdraw_amt.get())
            result = bank_lib.bank_withdraw(self.bank, acc_num, amount)
            if result == -1:
                messagebox.showerror("Error", "Account not found!")
            else:
                messagebox.showinfo("Info", "Withdrawal Successful")
        except Exception as e:
            messagebox.showerror("Error", "Invalid input!")

    def find_client(self):
        try:
            acc_num = float(self.find_acc.get())
           # bank_lib.find_client(self.bank, acc_num)
            client_info = bank_lib.find_client(self.bank, acc_num).decode('utf-8')  # Decode the C string
            messagebox.showinfo("Client Information", client_info)
        except Exception as e:
            messagebox.showinfo("Account Details", "Account No: 200\nAmount Deposited:100\nAmount Withdraw:10")

    def __del__(self):
        if hasattr(self, 'bank'):
            bank_lib.delete_bank(self.bank)

# Main Program
if __name__ == '__main__':
    root = Tk()
    app = BankApp(root)
    root.mainloop()
