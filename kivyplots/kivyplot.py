import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import NavigationToolbar2Kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import matplotlib.pyplot as plt
from kivy.properties import BooleanProperty, NumericProperty

"""
def press(event):
	print('press released from test', event.x, event.y, event.button)

def release(event):
	print('release released from test', event.x, event.y, event.button)

def keypress(event):
	print('key down', event.key)

def keyup(event):
	print('key up', event.key)

def motionnotify(event):
	print('mouse move to ', event.x, event.y)

def resize(event):
	print('resize from mpl ', event.width, event.height)

def scroll(event):
	print('scroll event from mpl ', event.x, event.y, event.step)

def figure_enter(event):
	print('figure enter mpl')

def figure_leave(event):
	print('figure leaving mpl')

def close(event):
	print('closing figure')

def enter_axes(event):
	print('enter_axes', event.inaxes)
	event.inaxes.patch.set_facecolor('yellow')
	event.canvas.draw()

def leave_axes(event):
	print('leave_axes', event.inaxes)
	event.inaxes.patch.set_facecolor('white')
	event.canvas.draw()

"""

class KivyPlot(BoxLayout):
	event_mappings = {
		'button_press_event': 'on_button_press',
		'button_release_event': 'on_button_release',
		'key_press_event': 'on_key_press',
		'key_release_event': 'on_key_release',
		'motion_notify_event': 'on_mouse_move',
		'resize_event': 'on_resize',
		'scroll_event': 'on_scroll',
		'figure_enter_event': 'on_figure_enter',
		'figure_leave_event': 'on_figure_leave',
		'axes_enter_event': 'on_axes_enter',
		'axes_leave_event': 'on_axes_leave',
		'close_event': 'on_plot_close'
	}
	plot_bar = BooleanProperty(False)
	figure_rows = NumericProperty(1)
	figure_cols = NumericProperty(1)
	def __init__(self, **kw):
		super().__init__(**kw)
		self.orientation = 'vertical'
		self.redraw_task = None
		self.bind(size=self.redraw_canvas)

	def build_plot(self):
		ax = self.init_plot()
		self.build(ax)
		self.finish_plot()

	def finish_plot(self):
		self.fig.tight_layout()
		canvas = self.fig.canvas
		if self.plot_bar:
			nav1 = NavigationToolbar2Kivy(canvas)
			self.add_widget(nav1.actionbar)
		self.add_widget(canvas)
	
	def build(self, ax):
		pass

	def init_plot(self):
		self.clear_widgets()
		self.fig, self.ax = plt.subplots(nrows=self.figure_rows, 
											ncols=self.figure_cols)
		canvas = self.fig.canvas
		f = self.event_handler
		for ev in self.event_mappings.keys():
			canvas.mpl_connect(ev, f)
		for ev in self.event_mappings.values():
			self.add_event_type(ev)
		return self.ax

	def redraw_canvas(self, *args):
		if self.redraw_task:
			self.redraw_task.cancel()
			
		self.redraw_task = Clock.schedule_once(self._redraw_canvas, 0.5)

	def _redraw_canvas(self, *args):
		print('Plot(): redraw() ...')
		self.build_plot()

	def add_event_type(self, name):
		setattr(self, name, self.default_handler)
		self.register_event_type(name)

	def default_handler(self, event):
		pass

	def event_handler(self, event):
		ev = self.event_mappings.get(event.name)
		self.dispatch(ev, event)

	def __enter__(self):
		return self.init_plot()

	def __exit__(self, *args):
		self.finish_plot()

if __name__ == '__main__':
	from kivy.app import App
	import numpy as np
	class MatplotlibTest(App):
		title = 'Matplotlib Test'

		def build(self):
			fl = KivyPlot(plot_bar=True)
			with fl as ax:
				print('ak=', ax)
				N = 5
				menMeans = (20, 35, 30, 35, 27)
				menStd = (2, 3, 4, 1, 2)

				ind = np.arange(N)  # the x locations for the groups
				width = 0.35	   # the width of the bars
				rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
				ax.set_ylabel('??????')
				ax.set_title('Scores by group and gender')
				ax.set_xticks(ind + width)
				ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))


			return fl

	MatplotlibTest().run()
