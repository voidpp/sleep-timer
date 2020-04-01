from rumps import App, MenuItem as MenuItemBase, Timer, separator, SliderMenuItem
from subprocess import check_call
from datetime import timedelta

class MenuItem(MenuItemBase):

    _stored_callback = None

    def enable(self, enable: bool = True):
        if enable:
            if self._stored_callback:
                self.set_callback(self._stored_callback)
                self._stored_callback = None
        else:
            callback = self.callback
            if callback:
                self._stored_callback = callback
                self.set_callback(None)

    def disable(self):
        self.enable(False)


class SleepTimerApp:

    def __init__(self):
        self._app = App("Sleep timer")
        self._timer = Timer(self._on_tick, 1)
        self._sleep_1hours_button = MenuItem("Sleep after 1 hours", self._sleep_1hours)
        self._sleep_2hours_button = MenuItem("Sleep after 2 hours", self._sleep_2hours)
        self._stop_button = MenuItem("Stop timer", self._stop)
        self._sleep_now_button = MenuItem("Sleep now", self._sleep_now)
        self._timer_buttons = [self._sleep_1hours_button, self._sleep_2hours_button]
        self._app.menu = self._timer_buttons + [self._stop_button, self._sleep_now_button, separator]
        self._counter = 0
        self._set_title()
        self._stop_button.disable()

    def _set_title(self, msg = ""):
        self._app.title = "☾" + ((" " + msg) if msg else "")

    def _sleep_1hours(self, *args):
        self._start_delayed_sleep(3600)

    def _sleep_2hours(self, *args):
        self._start_delayed_sleep(2*3600)

    def _start_delayed_sleep(self, seconds):
        self._stop_button.enable()
        for btn in self._timer_buttons:
            btn.disable()

        self._counter = seconds
        self._timer.start()

    def _stop(self, *args):
        self._stop_button.disable()
        for btn in self._timer_buttons:
            btn.enable()
        self._counter = 0
        self._timer.stop()
        self._set_title()

    def _sleep_now(self, *args):
        self._stop()
        self._sleep()

    def _on_tick(self, timer):
        self._counter -= 1
        self._set_title(str(timedelta(seconds = self._counter)))
        if self._counter < 1:
            self._stop()
            self._sleep()

    def _sleep(self):
        check_call(['pmset', 'sleepnow'])

    def run(self):
        self._app.run()

if __name__ == "__main__":
    SleepTimerApp().run()
