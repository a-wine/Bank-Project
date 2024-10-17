#ifndef BANK_H
#define BANK_H

#include <string>
using namespace std;

// Define the Client structure
struct Client {
    string client_name;
    string ssn;
    double bank_account_number;
    double balance;
};

// Bank class declaration
class Bank {
private:
    int num_client;        // Number of clients
    Client* clients;       // Dynamic array of clients

public:
    Bank(string filename);            // Constructor to load data from file
    Bank(const Bank& other);          // Deep copy constructor
    ~Bank();                          // Destructor

    void load_clients_info(string filename);   // Load clients from file
    Client* get_clients_info();                // Return client info
    double deposit(double account_number, double amount); // Deposit money
    string withdraw(double account_number, double amount); // Withdraw money
    void saving_info(string filename);          // Save client data to file
    void find_client(double account_number);    // Find client by account number
    void add_new_client(Client new_client);     // Add new client to bank
};
extern "C" {
    const char* find_client(Bank* bank, double account_number);  // Returns client info as string
}

#endif