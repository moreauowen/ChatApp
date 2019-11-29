"""
Module to hold all common variables and elements.
Final Project - Network Programming, Fall 2019
Professor Salem Othman
Fri, Oct 25, 2019

:authors:
    Owen Moreau, Jian Huang, Mario La
"""
import datetime


class Message:
    def __init__(self, user):
        self.message = input(" -> ")
        self.time = datetime.datetime.now()
        self.user = user

    def __str__(self):
        print_message = "[{}]: {} - {}".format(self.user.user_name,
                                               self.message,
                                               self.time)
        return print_message


DEV_SERVER_ADDR = "169.254.128.210"
DEV_SERVER_PORT = 5000
