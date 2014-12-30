import gtk

__author__ = 'corvis'


class Handler:
    def onDeleteWindow(self, *args):
        gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

builder = gtk.Builder()
builder.add_from_file('ui/ui.glade')
builder.connect_signals(Handler())
gtk.rc_parse('ui/gtkrc')
window = builder.get_object("window1")
window.show_all()

gtk.main()