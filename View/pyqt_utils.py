from PyQt5.QtWidgets import QSpacerItem
"""Top Level module for useful view util methods"""

def delete_items_of_layout(layout):
    """Deletes all the widgets inside a layout and all sublayouts"""
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            if not delete_widget(item):
                delete_items_of_layout(item.layout())


def delete_widget(item):
    if isinstance(item, QSpacerItem):
        return True
    widget = item.widget()
    if widget is not None:
        widget.deleteLater()
        return True
    return False
