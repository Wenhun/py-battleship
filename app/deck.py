from __future__ import annotations


class Deck:
    def __init__(self,
                 row: int,
                 column: int,
                 is_alive: bool = True) -> None:

        if not self.__deck_can_be_created(row, column):
            raise RuntimeError(f"Deck ({row}, {column}) can't be created!")

        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"

    def __str__(self) -> str:
        return f"({self.row}, {self.column})"

    def __eq__(self, other: Deck) -> bool:
        return self.row == other.row and self.column == other.column

    @staticmethod
    def __deck_can_be_created(row: int,
                              column: int,) -> bool:
        """
        field should be 10 x 10 size
        """
        if row < 0 or row > 10:
            return False

        if column < 0 or column > 10:
            return False

        return True
