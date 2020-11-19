"""This package contains all workers"""
from .customer_deletion import CustomerDeletionWorker


worker_list = [CustomerDeletionWorker]
