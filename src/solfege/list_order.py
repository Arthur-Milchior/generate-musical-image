
from enum import Enum


class ListOrder(Enum):
    INCREASING = "INCREASING"
    DECREASING = "DECREASING"
    NOT = "NOT"

def reverse_list_order(order: ListOrder):
    if order is ListOrder.INCREASING:
        return ListOrder.DECREASING
    if order is ListOrder.DECREASING:
        return ListOrder.INCREASING
    assert order is ListOrder.NOT
    return ListOrder.NOT