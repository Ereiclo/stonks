from rest_framework.exceptions import APIException


class UserNotEnoughMoney(APIException):
    status_code = 400
    default_detail = 'User does not have enough money to perform this action.'
    default_code = 'api_not_enough_money'


class UserNotEnoughStocks(APIException):
    status_code = 400
    default_detail = 'User does not have enough stocks to perform this action.'
    default_code = 'api_not_enough_stocks'


class UnexpectedOrderError(APIException):
    status_code = 500
    default_detail = 'Unexpected order error.'
    default_code = 'api_unexpected_error'
