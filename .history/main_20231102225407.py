path = os.path.abspath("module1")
sys.path.append(path)

from model.account import BudgetException
from repository.user_repository import UserRepository
if __name__ == "__main__":
    print("Account and transaction management system")

    # Create a user repository
    user_repository = UserRepository()

    # Create two users
    user_repository.create_user("joe", "2014", "joe2013@email.com", "2001-03-10")
    user_repository.create_user("alice", "alice123", "alice@email.com", "1995-05-20")

    # Deposit funds for users
    user_repository.deposit_funds(1, 100)
    user_repository.deposit_funds(2, 200)

    # Print user balances
    user1 = user_repository.get_user_by_id(1)
    user2 = user_repository.get_user_by_id(2)
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")

    # Perform a transaction from User 1 to User 2
    try:
        user_repository.withdraw_funds(1, 50)
        user_repository.deposit_funds(2, 50)
        print("Transaction successful")
    except BudgetException as e:
        print(f"Transaction failed: {e}")

    # Print updated balances
    print(f"User 1 balance: {user1.account.balance}")
    print(f"User 2 balance: {user2.account.balance}")
