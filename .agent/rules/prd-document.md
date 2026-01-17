---
trigger: always_on
---

# Product Requirement Document (PRD): namAirTravel

## 1. Introduction
namAirTravel is a sales and financial management application designed for an offline travel agency shop. The system tracks ticket sales, manages debts with suppliers and agents, monitors daily expenditures, and provides financial transparency through multi-account tracking.

## 2. User Roles
| Role | Quantity | Responsibilities |
| :--- | :--- | :--- |
| **Super Admin** | 1 | Full system access, view all reports, financial oversight (Owner). |
| **Accountant** | 1 | Manage suppliers, accounts, expenditures, debt payments, and financial auditing. |
| **Salesman** | Max 10 | Register sales. Limited view (own sales). |

## 3. Key Features & Functional Requirements

### 3.1. Supplier Management
- **Actor**: Accountant
- **Actions**: Register and manage Suppliers (Airlines, Operators, etc.).
- **Data**: Supplier Name, Contact Info, Balance.
- **Logic**: 
  - Tracks "Amount We Owe Supplier" (Payables).
  - Tracks "Amount Supplier Owes Us" (Receivables - e.g., refunds/overpayments).

### 3.2. Sales Management
- **Actor**: Salesman
- **Actions**: Record a new sale.
- **Input Data**:
  1. **Date**: Current date (auto or selectable).
  2. **Supplier**: Select from active Suppliers.
  3. **Ticket Type**: Enum [Airticket, Tour, UMRA].
  4. **Destination**: Free text input (Salesman enters by hand).
  5. **Comment**: Optional notes.
  6. **Quantity**: Integer.
  7. **Purchase Price**: (Cost) Price acquired from supplier.
  8. **Sales Channel**: Enum [Agent, Individual].
  9. **Sold Price**: Price sold to the client.
- **Financial Impact**:
  - **Supplier Debt**: `Purchase Price * Quantity` added to the specific Supplier's payable balance.
  - **Revenue/Receivable**: 
    - If **Individual**: Assumed cash/immediate payment to a selected Shop Account (or Cash Drawer).
    - If **Agent**: `Sold Price * Quantity` added to the specific Agent's debt (Receivable).

### 3.3. Financial Management (Accountant)
#### 3.3.1. Accounts & Transactions
- **System**: internal accounts (e.g., "Cash Desk", "Bank A", "Safe").
- **features**:
  - View current balance of each account.
  - View transaction history (Statement) for each account.
  - **Daily Expenditures**: Record operating expenses (Rent, Utilities, Food) deducted from an Account.

#### 3.3.2. Debt Settlement
- **Supplier Payment**:
  - Accountant pays Supplier from a Shop Account.
  - Supports partial payments/installments.
  - Reduces "Amount We Owe Supplier".
- **Agent Payment** (Receiving Money):
  - Agent pays the shop.
  - Accountant records incoming payment to a Shop Account.
  - Reduces "Amount Agent Owes Us".

### 3.4. Reporting & Proof (Owner View)
All reports must provide "proof" (i.e., drill-down to specific transaction logs/sales records).

1. **Sales Performance**:
   - Total tickets sold per Salesman.
   - Breakdown by Date/Type.
2. **Supplier Balances**:
   - **Payable**: Total debt to specific suppliers.
   - **Receivable**: Total owed by specific suppliers (if any).
   - Ledger view of all credits (purchases) and debits (payments).
3. **Agent Balances**:
   - Who owes us money and how much.
   - Ledger view of Sales to Agent vs. Payments from Agent.
4. **Financial Health**:
   - **Daily Expenditures**: List of expense transactions.
   - **Account Balances**: Current funds available.
   - **Transaction Log**: All money movements.

## 4. Data Entities (Simplified Schema)

### Users
- `id`, `username`, `role`

### Suppliers
- `id`, `name`, `balance` (signed or separate debit/credit fields)

### Agents
- `id`, `name`, `balance`

### Sales
- `id`, `date`, `salesman_id`, `supplier_id`, `type` (Airticket, Tour, UMRA), `destination`, `comment`, `quantity`, `purchase_unit_price`, `total_purchase_cost`, `client_type` (Agent/Individual), `client_agent_id` (nullable), `sold_unit_price`, `total_sold_price`

### Transactions
- `id`, `date`, `source_account_id` (nullable), `destination_account_id` (nullable), `amount`, `category` (Sale, SupplierPayment, AgentPayment, Expense), `reference_id` (e.g., SaleID), `description`

## 5. System Constraints
- **Platform**: Web Application (Accessible via browser for offline shop/internal network or cloud).
- **Concurrency**: Multiple salesmen entering data simultaneously.
- **Auditability**: No deletion of financial records; use compensating transactions for corrections.