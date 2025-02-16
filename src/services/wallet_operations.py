"""The module responsible for wallet operations."""

from typing import Any, Callable, Dict, Set


class WalletOperations(object):
    """
    A class for performing operations on a wallet.

    This class allows you to abstract from specific names of operations.
    When adding new wallet operations, the class scales easily.
    This is achieved using the cls dictionary.__operations.
    As values, it contains the names of operations that the user can send.
    The keys are class methods that encapsulate the operation selected by the user.
    The make_things method receives information about
    the operation using the OperationSchema. Using the getattr function,
    the method performs the necessary operation and returns the result of the operation.

    Args:
        wallet_amount (int) - The initial amount of money in the wallet.
    """

    def __init__(self, wallet_amount: int = 0):
        """Initialize class."""
        self.__wallet_amount = wallet_amount
        self.__operations: Dict[str, Callable] = {
            "WITHDRAW": self.__decrease_wallet,
            "DEPOSIT": self.__increase_wallet,
        }

    @property
    def set_operations(self) -> Set[str]:
        """Return a set of operation names."""
        return set(self.__operations.keys())

    def make_things(self, operation: str, **data) -> Any:
        """
        Perform the selected operation.

        :param operation: Name of the operation.
        :raise KeyError: If the operation is not found.
        :return: The result of the operation.
        """
        try:
            return self.__operations[operation](**data)
        except KeyError:
            raise KeyError(f"Operation {operation} not found.")

    def __decrease_wallet(self, *, amount: int):
        """
        Reduce wallet account.

        :raise ValueError: Attempting to withdraw more than is available in the wallet.
        :param amount: The number of currency units to reduce the wallet account by.
        :return: Updated wallet account.
        """
        if self.__wallet_amount < amount:
            raise ValueError(
                "Attempt to withdraw more money than is available in the wallet."
            )

        self.__wallet_amount -= amount
        return self.__wallet_amount

    def __increase_wallet(self, *, amount: int):
        """
        Increase wallet account.

        :param amount: The number of currency units to increase wallet account by.
        :return: Updated wallet account.
        """
        self.__wallet_amount += amount
        return self.__wallet_amount
