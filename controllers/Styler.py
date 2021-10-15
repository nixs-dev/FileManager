class Styler:
    content_idle = 'background-color: rgb(170, 255, 255);'
    content_focus = 'background-color: rgb(170, 255, 255); border: 3px solid rgb(170, 150, 255);'
    navigator_idle = 'color: rgb(0, 0, 0); border: 1px solid #000000;'
    navigator_focus = 'color: rgb(0, 0, 255); border: 1px solid #0000FF;'

    def content_mouse_enter(elem, event):
        elem.setStyleSheet(Styler.content_focus)

    def content_mouse_leave(elem, event):
        elem.setStyleSheet(Styler.content_idle)

    def navigator_mouse_enter(elem, event):
        elem.setStyleSheet(Styler.navigator_focus)

    def navigator_mouse_leave(elem, event):
        elem.setStyleSheet(Styler.navigator_idle)