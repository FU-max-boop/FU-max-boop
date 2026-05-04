# DBT Task Brief: quickbooks001

## Instruction

Please create a table that unions all records from each model within the double_entry_transactions directory. The table should result in a comprehensive general ledger, ensuring each transaction has an offsetting debit and credit entry.

## Preflight Status

- `ready`

## Evaluation Target

- funcs: `duckdb_match`
- gold files: `quickbooks.duckdb`
- condition tables: `quickbooks__general_ledger`
- condition columns referenced: 19

## DBT Project Shape

- SQL model files: 29
- total SQL lines: 2620
- unique `source()` calls: 0
- unique `ref()` calls: 50

## Suggested Reading Order

- `int_quickbooks__account_classifications`
- `int_quickbooks__bill_double_entry`
- `int_quickbooks__bill_join`
- `int_quickbooks__bill_payment_double_entry`
- `int_quickbooks__bill_transactions`
- `int_quickbooks__credit_card_pymt_double_entry`
- `int_quickbooks__credit_memo_double_entry`
- `int_quickbooks__credit_memo_transactions`
- `int_quickbooks__deposit_double_entry`
- `int_quickbooks__deposit_transactions`
- `int_quickbooks__invoice_double_entry`
- `int_quickbooks__invoice_join`
- `int_quickbooks__invoice_transactions`
- `int_quickbooks__journal_entry_double_entry`
- `int_quickbooks__journal_entry_transactions`
- `int_quickbooks__payment_double_entry`
- `int_quickbooks__purchase_double_entry`
- `int_quickbooks__purchase_transactions`
- `int_quickbooks__refund_receipt_double_entry`
- `int_quickbooks__refund_receipt_transactions`
- `int_quickbooks__sales_receipt_double_entry`
- `int_quickbooks__sales_receipt_transactions`
- `int_quickbooks__transfer_double_entry`
- `int_quickbooks__vendor_credit_double_entry`
- `int_quickbooks__vendor_credit_transactions`
- `quickbooks__ap_ar_enhanced`
- `int_quickbooks__sales_union`
- `int_quickbooks__expenses_union`
- `quickbooks__expenses_sales_enhanced`

## Source Tables

- none

## Internal Model Refs

- `int_quickbooks__account_classifications`
- `int_quickbooks__bill_join`
- `int_quickbooks__bill_transactions`
- `int_quickbooks__credit_memo_transactions`
- `int_quickbooks__deposit_transactions`
- `int_quickbooks__expenses_union`
- `int_quickbooks__invoice_join`
- `int_quickbooks__invoice_transactions`
- `int_quickbooks__journal_entry_transactions`
- `int_quickbooks__purchase_transactions`
- `int_quickbooks__refund_receipt_transactions`
- `int_quickbooks__sales_receipt_transactions`
- `int_quickbooks__sales_union`
- `int_quickbooks__vendor_credit_transactions`
- `stg_quickbooks__account`
- `stg_quickbooks__address`
- `stg_quickbooks__bill`
- `stg_quickbooks__bill_line`
- `stg_quickbooks__bill_linked_txn`
- `stg_quickbooks__bill_payment`
- `stg_quickbooks__bill_payment_line`
- `stg_quickbooks__bundle`
- `stg_quickbooks__bundle_item`
- `stg_quickbooks__credit_card_payment_txn`
- `stg_quickbooks__credit_memo`
- `stg_quickbooks__credit_memo_line`
- `stg_quickbooks__customer`
- `stg_quickbooks__department`
- `stg_quickbooks__deposit`
- `stg_quickbooks__deposit_line`
- `stg_quickbooks__estimate`
- `stg_quickbooks__invoice`
- `stg_quickbooks__invoice_line`
- `stg_quickbooks__invoice_line_bundle`
- `stg_quickbooks__invoice_linked_txn`
- `stg_quickbooks__item`
- `stg_quickbooks__journal_entry`
- `stg_quickbooks__journal_entry_line`
- `stg_quickbooks__payment`
- `stg_quickbooks__payment_line`
- `stg_quickbooks__purchase`
- `stg_quickbooks__purchase_line`
- `stg_quickbooks__refund_receipt`
- `stg_quickbooks__refund_receipt_line`
- `stg_quickbooks__sales_receipt`
- `stg_quickbooks__sales_receipt_line`
- `stg_quickbooks__transfer`
- `stg_quickbooks__vendor`
- `stg_quickbooks__vendor_credit`
- `stg_quickbooks__vendor_credit_line`

## Model Table

| model | lines | sources | refs |
| --- | ---: | --- | --- |
| `models/double_entry_transactions/int_quickbooks__invoice_double_entry.sql` | 211 |  | `stg_quickbooks__account`, `stg_quickbooks__bundle`, `stg_quickbooks__bundle_item`, `stg_quickbooks__invoice`, `stg_quickbooks__invoice_line`, `stg_quickbooks__invoice_line_bundle`, `stg_quickbooks__item` |
| `models/quickbooks__ap_ar_enhanced.sql` | 176 |  | `int_quickbooks__bill_join`, `int_quickbooks__invoice_join`, `stg_quickbooks__address`, `stg_quickbooks__customer`, `stg_quickbooks__department`, `stg_quickbooks__vendor` |
| `models/intermediate/int_quickbooks__invoice_join.sql` | 142 |  | `stg_quickbooks__estimate`, `stg_quickbooks__invoice`, `stg_quickbooks__invoice_linked_txn`, `stg_quickbooks__payment`, `stg_quickbooks__payment_line` |
| `models/intermediate/int_quickbooks__sales_union.sql` | 121 |  | `int_quickbooks__account_classifications`, `int_quickbooks__credit_memo_transactions`, `int_quickbooks__invoice_transactions`, `int_quickbooks__refund_receipt_transactions`, `int_quickbooks__sales_receipt_transactions`, `stg_quickbooks__customer`, `stg_quickbooks__department`, `stg_quickbooks__vendor` |
| `models/intermediate/int_quickbooks__expenses_union.sql` | 117 |  | `int_quickbooks__account_classifications`, `int_quickbooks__bill_transactions`, `int_quickbooks__deposit_transactions`, `int_quickbooks__journal_entry_transactions`, `int_quickbooks__purchase_transactions`, `int_quickbooks__vendor_credit_transactions`, `stg_quickbooks__customer`, `stg_quickbooks__department`, `stg_quickbooks__vendor` |
| `models/double_entry_transactions/int_quickbooks__credit_memo_double_entry.sql` | 115 |  | `stg_quickbooks__account`, `stg_quickbooks__credit_memo`, `stg_quickbooks__credit_memo_line`, `stg_quickbooks__item` |
| `models/double_entry_transactions/int_quickbooks__sales_receipt_double_entry.sql` | 105 |  | `stg_quickbooks__item`, `stg_quickbooks__sales_receipt`, `stg_quickbooks__sales_receipt_line` |
| `models/double_entry_transactions/int_quickbooks__deposit_double_entry.sql` | 103 |  | `stg_quickbooks__account`, `stg_quickbooks__deposit`, `stg_quickbooks__deposit_line` |
| `models/intermediate/int_quickbooks__bill_join.sql` | 98 |  | `stg_quickbooks__bill`, `stg_quickbooks__bill_line`, `stg_quickbooks__bill_linked_txn`, `stg_quickbooks__bill_payment`, `stg_quickbooks__bill_payment_line` |
| `models/double_entry_transactions/int_quickbooks__bill_payment_double_entry.sql` | 98 |  | `stg_quickbooks__account`, `stg_quickbooks__bill_payment`, `stg_quickbooks__bill_payment_line` |
| `models/double_entry_transactions/int_quickbooks__payment_double_entry.sql` | 98 |  | `stg_quickbooks__account`, `stg_quickbooks__payment`, `stg_quickbooks__payment_line` |
| `models/double_entry_transactions/int_quickbooks__refund_receipt_double_entry.sql` | 97 |  | `stg_quickbooks__item`, `stg_quickbooks__refund_receipt`, `stg_quickbooks__refund_receipt_line` |
| `models/double_entry_transactions/int_quickbooks__bill_double_entry.sql` | 95 |  | `stg_quickbooks__bill`, `stg_quickbooks__bill_line`, `stg_quickbooks__item` |
| `models/double_entry_transactions/int_quickbooks__vendor_credit_double_entry.sql` | 95 |  | `stg_quickbooks__item`, `stg_quickbooks__vendor_credit`, `stg_quickbooks__vendor_credit_line` |
| `models/double_entry_transactions/int_quickbooks__purchase_double_entry.sql` | 94 |  | `stg_quickbooks__item`, `stg_quickbooks__purchase`, `stg_quickbooks__purchase_line` |
| `models/intermediate/int_quickbooks__account_classifications.sql` | 91 |  | `stg_quickbooks__account` |
| `models/transaction_lines/int_quickbooks__vendor_credit_transactions.sql` | 84 |  | `stg_quickbooks__item`, `stg_quickbooks__vendor_credit`, `stg_quickbooks__vendor_credit_line` |
| `models/double_entry_transactions/int_quickbooks__credit_card_pymt_double_entry.sql` | 72 |  | `stg_quickbooks__credit_card_payment_txn` |
| `models/transaction_lines/int_quickbooks__purchase_transactions.sql` | 72 |  | `stg_quickbooks__item`, `stg_quickbooks__purchase`, `stg_quickbooks__purchase_line` |
| `models/double_entry_transactions/int_quickbooks__transfer_double_entry.sql` | 67 |  | `stg_quickbooks__transfer` |
| `models/transaction_lines/int_quickbooks__bill_transactions.sql` | 63 |  | `stg_quickbooks__bill`, `stg_quickbooks__bill_line`, `stg_quickbooks__item` |
| `models/transaction_lines/int_quickbooks__credit_memo_transactions.sql` | 60 |  | `stg_quickbooks__credit_memo`, `stg_quickbooks__credit_memo_line`, `stg_quickbooks__item` |
| `models/transaction_lines/int_quickbooks__invoice_transactions.sql` | 60 |  | `stg_quickbooks__invoice`, `stg_quickbooks__invoice_line`, `stg_quickbooks__item` |
| `models/transaction_lines/int_quickbooks__refund_receipt_transactions.sql` | 60 |  | `stg_quickbooks__item`, `stg_quickbooks__refund_receipt`, `stg_quickbooks__refund_receipt_line` |
| `models/transaction_lines/int_quickbooks__sales_receipt_transactions.sql` | 57 |  | `stg_quickbooks__item`, `stg_quickbooks__sales_receipt`, `stg_quickbooks__sales_receipt_line` |
| `models/transaction_lines/int_quickbooks__journal_entry_transactions.sql` | 50 |  | `stg_quickbooks__journal_entry`, `stg_quickbooks__journal_entry_line` |
| `models/double_entry_transactions/int_quickbooks__journal_entry_double_entry.sql` | 46 |  | `stg_quickbooks__journal_entry`, `stg_quickbooks__journal_entry_line` |
| `models/transaction_lines/int_quickbooks__deposit_transactions.sql` | 44 |  | `stg_quickbooks__deposit`, `stg_quickbooks__deposit_line` |
| `models/quickbooks__expenses_sales_enhanced.sql` | 29 |  | `int_quickbooks__expenses_union`, `int_quickbooks__sales_union` |

## Agent Use

Before editing or generating DBT code, an agent should:

1. Check that the preflight status is `ready`.
2. Inspect the condition tables first, because evaluation only checks those outputs.
3. Read models in dependency order instead of raw filesystem order.
4. Track whether a failure is caused by missing assets, wrong DBT model selection, source/ref misunderstanding, or final SQL/table mismatch.
