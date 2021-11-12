class ItemStyler:
    elem = None
    content_idle = 'background-color: rgb(255, 255, 255);'
    content_selected = 'background-color: rgb(179, 230, 255); border: 3px solid rgb(0, 136, 204);'
    content_focus = 'border: 3px solid rgb(170, 150, 255);'

    content_state = ''

    def __init__(self, item):
        self.elem = item
        self.content_state = self.content_idle

    def content_gets_idle(self):
        self.content_state = self.content_idle
        self.elem.setStyleSheet(self.content_idle)

    def content_select(self):
        self.content_state = self.content_selected
        self.elem.setStyleSheet(self.content_selected)

    def content_mouse_enter(self, event):
        self.elem.setStyleSheet(self.content_state + self.content_focus)

    def content_mouse_leave(self, event):
        self.elem.setStyleSheet(self.content_state)