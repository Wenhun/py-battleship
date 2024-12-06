from __future__ import annotations

from app.deck import Deck


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:

        if not self.__ship_can_be_created(start, end):
            raise RuntimeError(f"Ship with coordinates {start} "
                               f"and {end} can't be created!")

        self.decks: list[Deck] = self.__create_ship(start, end)

        self.is_drowned = is_drowned
        self.type = self.__detect_type_of_ship(self.decks)

    def get_deck(self, row: int, column: int) -> Deck | None:
        if self.is_drowned:
            print(f"Ship {self.type} already drowned!")
            return

        deck = Deck(row, column)

        if deck in self.decks:
            return self.decks[self.decks.index(deck)]

        print(f"Ship {self.type} not contain this deck: {deck}!")

    def fire(self, row: int, column: int) -> None:
        if self.is_drowned:
            print(f"Ship {self.type} already drowned!")
            return

        deck = Deck(row, column)

        if deck in self.decks:
            index_of_deck = self.decks.index(deck)
            if self.decks[index_of_deck].is_alive:
                self.decks[index_of_deck].is_alive = False
                self.__check_ship_health()
            else:
                print(f"Deck {deck} already destroyed!")
        else:
            print(f"Ship {self.type} not contain this deck: {deck}!")

    @staticmethod
    def __create_ship(start: tuple,
                      end: tuple) -> list[Deck]:

        ship: list[Deck] = []

        if start[0] < end[0]:
            for index in range(start[0], end[0] + 1):
                ship.append(Deck(index, start[1]))
            return ship

        if start[1] < end[1]:
            for index in range(start[1], end[1] + 1):
                ship.append(Deck(start[0], index))
            return ship

        if start[0] == end[0] and start[1] == end[1] :
            ship.append(Deck(start[0], start[1]))
            return ship

        raise RuntimeError("Error creating ship!!!")

    @staticmethod
    def __ship_can_be_created(deck_1: tuple,
                              deck_2: tuple) -> bool:
        if deck_1[0] != deck_2[0] and deck_1[1] != deck_2[1]:
            return False

        return True

    @staticmethod
    def __detect_type_of_ship(ship: list[Deck]) -> str:
        types = ("Submarine", "Cruiser", "Battleship", "Carrier")
        return types[len(ship) - 1]

    def __check_ship_health(self) -> None:
        for deck in self.decks:
            if deck.is_alive:
                return

        print(f"Ship {self.type} is drowned!")
        self.is_drowned = True

    def __repr__(self) -> str:
        return f"Ship {self.type}, coord: {self.decks}"
