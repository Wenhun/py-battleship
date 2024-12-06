from __future__ import annotations

from app.ship import Ship


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.__ships: list[Ship] = self.fill_ships_list(ships)
        self.field: dict[tuple, Ship] = self.__feel_field(self.__ships)
        self.__validate_field()

    @staticmethod
    def fill_ships_list(ships: list[tuple]) -> list[Ship]:
        list_of_ships: list[Ship] = []
        for coordinate in ships:
            list_of_ships.append(Ship(coordinate[0], coordinate[1]))
        return list_of_ships

    def fire(self, location: tuple) -> str:
        if not self.field[location]:
            self.print_field()
            return "Miss!"

        self.field[location].fire(location[0], location[1])

        if self.field[location].is_drowned:
            self.print_field()
            return "Sunk!"
        else:
            self.print_field()
            return "Hit!"

    @staticmethod
    def __feel_field(ships: list[Ship]) -> dict[tuple, Ship | None] :
        field: dict[tuple, Ship | None] = {}

        for ship in ships:
            for deck in ship.decks:
                field[(deck.row, deck.column)] = ship

        for i_index in range(10):
            for j_index in range(10):
                _deck = (i_index, j_index)
                if _deck in field.keys():
                    continue
                else:
                    field[_deck] = None

        return field

    def __validate_field(self) -> None:
        """Check the size of the fleet"""
        expected_count_types = {"Submarine": 4,
                                "Cruiser": 3,
                                "Battleship": 2,
                                "Carrier": 1}
        count_types = {"Submarine": 0,
                       "Cruiser": 0,
                       "Battleship": 0,
                       "Carrier": 0}

        for ship in self.__ships:
            count_types[ship.type] += 1

        if count_types != expected_count_types:
            raise AssertionError(
                f"Count ships on battlefield not equal to expected! "
                f"Expected: {expected_count_types}. Actual: {count_types}")

        """Check if the field is filled in correctly"""
        for i_indx in range(10):
            for j_indx in range(10):
                if self.field[(i_indx, j_indx)]:
                    neighbors = [
                        (i_indx, j_indx + 1),
                        (i_indx, j_indx - 1),
                        (i_indx + 1, j_indx),
                        (i_indx - 1, j_indx),
                        (i_indx - 1, j_indx - 1),
                        (i_indx + 1, j_indx + 1),
                        (i_indx + 1, j_indx - 1),
                        (i_indx - 1, j_indx + 1)]
                    for ni, nj in neighbors:
                        if ni != 10 or ni != 0 or nj != 10 or nj != 0:
                            if ((ni, nj) in self.field
                                    and self.field[(ni, nj)]
                                    and (self.field[(i_indx, j_indx)]
                                         != self.field[(ni, nj)])):
                                raise RuntimeError(
                                    f"Ships don't be closer! Conflict deck: "
                                    f"({i_indx}, {j_indx}) and ({ni}, {nj})")

    def print_field(self) -> None:
        if not self.field:
            raise RuntimeError("Field is not feel!!!")

        print("   0  1  2  3  4  5  6  7  8  9 ")

        for i_indx in range(10):
            row = f"{i_indx} "
            for j_indx in range(10):
                _deck = (i_indx, j_indx)
                if not self.field[_deck]:
                    row += " ~ "
                    continue
                if self.field[_deck].is_drowned:
                    row += (" " + u"\u2715" + " ")
                    continue
                if not self.field[_deck].get_deck(i_indx , j_indx).is_alive:
                    row += " * "
                    continue
                if (self.field[_deck].get_deck(i_indx , j_indx).is_alive
                        and not self.field[_deck].is_drowned):
                    row += (" " + u"\u25A1" + " ")
                    continue
            print(row)

        print("----------------------------------")
