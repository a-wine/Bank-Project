#include "bank.h"
#include <iostream>
#include <fstream>
#include <fstream>
#include <cstring>  // Include the cstring header for strcpy
#include <string>   // Include string for std::string
#include "bank.h"
using namespace std;

// Constructor: load clients from a file
Bank::Bank(string filename) {
    load_clients_info(filename);
}

// Deep copy constructor
Bank::Bank(const Bank& other) {
    num_client = other.num_client;
    clients = new Client[num_client];
    for (int i = 0; i < num_client; i++) {
        clients[i] = other.clients[i];
    }
}

// Destructor
Bank::~Bank() {
    delete[] clients;
}

// Load client data from a file
void Bank::load_clients_info(string filename) {
    ifstream infile(filename);
    if (!infile) {
        cerr << "Unable to open file!";
        return;
    }
    infile >> num_client;
    clients = new Client[num_client];
    for (int i = 0; i < num_client; i++) {
        infile >> clients[i].client_name >> clients[i].ssn >> clients[i].bank_account_number >> clients[i].balance;
    }
    infile.close();
}

// Return client information
Client* Bank::get_clients_info() {
    return clients;
}

// Deposit function
double Bank::deposit(double account_number, double amount) {
    for (int i = 0; i < num_client; i++) {
        if (clients[i].bank_account_number == account_number) {
            clients[i].balance += amount;
            return clients[i].balance;
        }
    }
    return -1; // Account not found
}

// Withdraw function
string Bank::withdraw(double account_number, double amount) {
    for (int i = 0; i < num_client; i++) {
        if (clients[i].bank_account_number == account_number) {
            if (clients[i].balance >= amount) {
                clients[i].balance -= amount;
                return "Withdrawal successful!";
            } else {
                return "Insufficient balance!";
            }
        }
    }
    return "Account not found!";
}

// Save updated client data to a file
void Bank::saving_info(string filename) {
    ofstream outfile(filename);
    if (!outfile) {
        cerr << "Unable to open file for saving!";
        return;
    }
    outfile << num_client << endl;
    for (int i = 0; i < num_client; i++) {
        outfile << clients[i].client_name << " " << clients[i].ssn << " " << clients[i].bank_account_number << " " << clients[i].balance << endl;
    }
    outfile.close();
}

// Find a client by account number
void Bank::find_client(double account_number) {
    for (int i = 0; i < num_client; i++) {
        if (clients[i].bank_account_number == account_number) {
            cout << "Client Name: " << clients[i].client_name << ", Balance: " << clients[i].balance << endl;
			char* result = new char[info.length() + 1];
            strcpy(result, info.c_str());
            return;
        }
    }
    cout << "Client does not exist!" << endl;
}

// Add a new client
void Bank::add_new_client(Client new_client) {
    Client* temp = new Client[num_client + 1];
    for (int i = 0; i < num_client; i++) {
        temp[i] = clients[i];
    }
    temp[num_client] = new_client;
    delete[] clients;
    clients = temp;
    num_client++;
}

// Wrapper functions for connecting with Python
extern "C" {
    Bank* create_bank(char* filename) { return new Bank(filename); }
    void delete_bank(Bank* b) { delete b; }
    void bank_deposit(Bank* b, double acc_num, double amount) { b->deposit(acc_num, amount); }
    void bank_withdraw(Bank* b, double acc_num, double amount) { b->withdraw(acc_num, amount); }
}

extern "C" {
    const char* find_client(Bank* bank, double account_number) {
        for (int i = 0; i < bank->num_client; ++i) {
            if (bank->clients[i].bank_account_number == account_number) {
                // Construct client information as a string
                std::string info = "Name: " + bank->clients[i].client_name + 
                                   ", Balance: " + std::to_string(bank->clients[i].balance);
                // Allocate memory for the C-string
                char* result = new char[info.length() + 1];
                strcpy(result, info.c_str());  // Copy the std::string to C-string
                return result;  // Return the C-string
            }
        }
        // Return a "Client not found" message if the account doesn't exist
        return "Client not found";
    }
}