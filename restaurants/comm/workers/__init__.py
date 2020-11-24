"""This package contains all workers"""
from .customer_deletion import OperatorDeletionWorker


worker_list = [OperatorDeletionWorker]
