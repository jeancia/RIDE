#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from robot import utils
from robotide.action.actioninfo import ActionInfoCollection
from robotide.context.platform import IS_WINDOWS

tree_actions ="""
[Navigate]
!Go &Back | Go back to previous location in tree | Alt-%s | ART_GO_BACK
!Go &Forward | Go forward to next location in tree | Alt-%s | ART_GO_FORWARD
""" % (('Left', 'Right') if IS_WINDOWS else ('Z', 'X'))
# Left and right cannot be overridden in tree on non Windows OSses, issue 354


class TreeController(object):

    def __init__(self, tree, action_registerer, settings, history=None):
        self._tree = tree
        self._action_registerer = action_registerer
        self.settings = settings
        self._history = history or _History()

    def register_tree_actions(self):
        actions = ActionInfoCollection(tree_actions, self, self._tree)
        self._action_registerer.register_actions(actions)

    def OnGoBack(self, event):
        node = self._history.back()
        if node:
            self._tree.SelectItem(node)

    def OnGoForward(self, event):
        node = self._history.forward()
        if node:
            self._tree.SelectItem(node)

    def add_to_history(self, node):
        self._history.change(node)

    def find_node_by_controller(self, controller):
        def match_handler(n):
            handler = self._tree._get_handler(n)
            return handler and controller is handler.controller
        return self._find_node_with_predicate(self._tree._root, match_handler)

    def find_node_with_label(self, node, label):
        matcher = lambda n: utils.eq(self._tree.GetItemText(n), label)
        return self._find_node_with_predicate(node, matcher)

    def _find_node_with_predicate(self, node, predicate):
        if node != self._tree._root and predicate(node):
            return node
        item, cookie = self._tree.GetFirstChild(node)
        while item:
            if predicate(item):
                return item
            if self._tree.ItemHasChildren(item):
                result = self._find_node_with_predicate(item, predicate)
                if result:
                    return result
            item, cookie = self._tree.GetNextChild(node, cookie)
        return None

    def get_handler(self, node=None):
        return self._tree.GetItemPyData(node or self._tree.Selection)


class _History(object):

    def __init__(self):
        self._back = []
        self._forward = []

    def change(self, state):
        if not self._back or state != self._back[-1]:
            self._back.append(state)
            self._forward = []

    def back(self):
        if not self._back:
            return None
        if len(self._back) > 1:
            self._forward.append(self._back.pop())
        return self._back[-1]

    def forward(self):
        if not self._forward:
            return None
        state = self._forward.pop()
        self._back.append(state)
        return state

    def top(self):
        return self._back and self._back[-1] or None
