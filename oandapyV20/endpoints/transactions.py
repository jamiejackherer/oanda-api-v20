# -*- encoding: utf-8 -*-
"""Handle transactions endpoints."""
from .apirequest import APIRequest
from ..exceptions import StreamTerminated
from .decorators import dyndoc_insert, endpoint, abstractclass, extendargs
from .definitions.transactions import definitions    # flake8: noqa
from .responses.transactions import responses
from types import GeneratorType



@abstractclass
class Transactions(APIRequest):
    """Transactions - class to handle the transaction endpoints."""

    ENDPOINT = ""
    METHOD = "GET"

    @dyndoc_insert(responses)
    def __init__(self, accountID, transactionID=None):
        """Instantiate a Transactions APIRequest instance.

        Parameters
        ----------
        accountID : string (required)
            the id of the account.

        transactionID : string
            the id of the transaction

        params : dict (depends on the endpoint to access)
            parameters for the request. This applies only the GET based
            endpoints
        """
        endpoint = self.ENDPOINT.format(accountID=accountID,
                                        transactionID=transactionID)
        super(Transactions, self).__init__(endpoint,
                                           method=self.METHOD)


@endpoint("v3/accounts/{accountID}/transactions")
class TransactionList(Transactions):
    """TransactionList.

    Get a list of Transactions pages that satisfy a time-based Transaction
    query.
    """
#            {_v3_account_by_accountID_instruments_params}

    @dyndoc_insert(responses)
    def __init__(self, accountID, params=None):
        """Instantiate a TransactionList request.

        Parameters
        ----------
        accountID : string (required)
            id of the account to perform the request on.

        params : dict (optional)
            query params to send, check developer.oanda.com for details.


        Query Params example::

           {_v3_accounts_accountID_transactions_params}

        >>> import oandapyV20
        >>> import oandapyV20.endpoints.accounts as accounts
        >>> client = oandapyV20.API(access_token=...)
        >>> r = accounts.TransactionList(accountID)  # params optional
        >>> client.request(r)
        >>> print r.response

        Output::

           {_v3_accounts_accountID_transactions_resp}

        """
        super(TransactionList, self).__init__(accountID)
        self.params = params


@endpoint("v3/accounts/{accountID}/transactions/{transactionID}")
class TransactionDetails(Transactions):
    """TransactionDetails.

    Get the details of a single Account Transaction.
    """


@extendargs("params")
@endpoint("v3/accounts/{accountID}/transactions/idrange")
class TransactionIDRange(Transactions):
    """TransactionIDRange.

    Get a range of Transactions for an Account based on Transaction IDs.
    """


@extendargs("params")
@endpoint("v3/accounts/{accountID}/transactions/sinceid")
class TransactionSinceID(Transactions):
    """TransactionSinceID.

    Get a range of Transactions for an Account starting at (but not including)
    a provided Transaction ID.
    """


@extendargs("params")
@endpoint("v3/accounts/{accountID}/transactions/stream")
class TransactionsStream(Transactions):
    """TransactionsStream.

    Get a stream of Transactions for an Account starting from when the
    request is made.
    """

    STREAM = True

    def terminate(self, message=""):
        if not isinstance(self.response, GeneratorType):
            raise ValueError("request does not contain a stream response")

        self.response.throw(StreamTerminated(message))
