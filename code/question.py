"""
Question class
"""
import json, os
from . import data, mult

# start question OMIT
class Question:
    def __init__(self, text, buttons):
        self.text = text
        self.buttons = {k: b*mult for k, b in buttons.items()}

        vals = buttons.values()

questions = [Question(**q) for q in data]
# end question OMIT
