from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import ai1
import ai2
from board import Board


class InvalidMoveError(Exception):
    pass


ui = None
gameplay = None


class NotificationArea(BoxLayout):
    label = ObjectProperty()

    def notify(self, text, timeout):
        self.label.text = text
        Clock.schedule_once(self.reset, timeout)

    def reset(self, *ignore):
        self.label.text = ''


class GamePlay():
    def __init__(self):
        self.moves = []

    def init_game(self):
        ui.topbar.update()
        self.reset()

    def reset(self):
        self.moves = []
        ui.topbar.update()

    def token_move(self, row, col):
        token = self.token
        num_moves = len(self.moves)
        mod = num_moves % 4
        if mod in [1, 3]:
            last_move = self.moves[-1]
            if  last_move[-1] == 'token':
                raise InvalidMoveError("invalid move")

        # print("token %s is put on (%s %s)" % (token, row, col))
        self.moves.append((row, col, token, 'token'))
        ui.topbar.update()
        # print(self.moves)

    def rotation_move(self, row, col, clockwise):
        token = self.token
        num_moves = len(self.moves)
        mod = num_moves % 4
        if mod in [1, 3]:
            last_move = self.moves[-1]
            if  last_move[-1] == 'rotate':
                raise InvalidMoveError("invalid move")

        print("token %s rotated (%s %s)" % (token, row, col))
        self.moves.append((row, col, clockwise, 'rotate'))
        ui.topbar.update()
        print(self.moves)

    @property
    def token(self):
        num_moves = len(self.moves)
        if num_moves % 4 in [0, 1]:
            return 0
        return 1

    @property
    def rotateable(self):
        num_moves = len(self.moves)
        mod = num_moves % 4
        if mod in [0, 2]:
            return True

        last_move = self.moves[-1]
        if last_move[-1] == 'rotate':
            return False
        return True

    def undo(self):
        last_move = self.moves.pop()
        ui.topbar.update()
        return last_move


class TopBar(BoxLayout):
    token = ObjectProperty()
    rotateable = ObjectProperty()
    btn_clockwise = ObjectProperty()
    btn_anticlockwise = ObjectProperty()
    rotation = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.bind_buttons, 0)

    def bind_buttons(self, *ignore):
        self.btn_clockwise.bind(state=self.update_rotation)
        self.btn_anticlockwise.bind(state=self.update_rotation)

    def undo(self):
        try:
            last_move = gameplay.undo()
        except IndexError:
            return

        board = ui.grid.board
        if last_move[3] == 'rotate':
            row, col, clockwise, action = last_move
            clockwise = 1 - clockwise
            board.rotate(row, col, clockwise)
        elif last_move[3] == 'token':
            row, col, token, action = last_move
            board.array[row][col] = None
        ui.grid.update()
        self.update_rotation()

    def update(self):
        self.token = gameplay.token
        self.rotateable = gameplay.rotateable
        self.update_rotation()

    def update_rotation(self, *args):
        btn1 = self.btn_anticlockwise
        btn2 = self.btn_clockwise
        if btn1.state == 'down':
            self.rotation = 0
        elif btn2.state == 'down':
            self.rotation = 1
        else:
            self.rotation = None


class Cell(ButtonBehavior, Widget):
    row, col = ObjectProperty(), ObjectProperty()
    token = ObjectProperty(None)
    color = {0: (.9, .9, .9, 1),
             1: (0.1, 0, 0.5, 1),
             None: (0.1, 0.4, 0.1, 1)}

    def on_release(self, *args):
        self.parent.cell_clicked(self)


class ExampleCell(Cell):
    def on_release(self, *ignore):
        pass


class Grid(GridLayout):
    board = ObjectProperty()
    background_color = ListProperty([0.2, 0.5, 0.2, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = Board()
        self.board.empty_array()
        # self.board.array = [
        #     [None,    1, None, None, None, None],
        #     [None, None,    1, None,    0, None],
        #     [None,    0, None,    1, None,    0],
        #     [None, None, None, None,    1, None],
        #     [None, None, None,    0, None, None],
        #     [None, None, None, None, None, None],
        # ]
        self.update()

    def reset_board(self):
        self.board.empty_array()
        ui.gameplay.reset()
        self.update()
        ui.topbar.update()

    def update(self):
        self.clear_widgets()
        a = self.board.array
        for i, row in enumerate(a):
            for j, tk in enumerate(row):
                cell = Cell(token=tk, row=i, col=j)
                self.add_widget(cell)

    def ai_move(self, ai_id):
        if ai_id == 2:
            ai = ai2
        else:
            ai = ai1
        token = gameplay.token
        move = ai.move(self.board.array, token)
        coor, center, clockwise = move
        row, col = coor

        try:
            gameplay.token_move(*coor)
        except InvalidMoveError as e:
            ui.notification_area.notify("ROTATE PLEASE", timeout=1)
            return
        for cell in self.children:
            if (cell.row, cell.col) == coor:
                break
        cell.token = token
        self.board.array[row][col] = token

        try:
            gameplay.rotation_move(center[0], center[1], clockwise)
        except InvalidMoveError as e:
            ui.notification_area.notify("Invalid move!", timeout=1)
            return
        self.board.rotate(center[0], center[1], clockwise)
        ui.topbar.btn_clockwise.state = 'normal'
        ui.topbar.btn_anticlockwise.state = 'normal'

        self.update()

    def cell_clicked(self, cell):
        row, col = cell.row, cell.col
        rotation = ui.topbar.rotation
        if rotation is not None:
            if (row, col) not in ((1, 1), (4, 4), (1, 4), (4, 1)):
                return
            try:
                gameplay.rotation_move(row, col, rotation)
            except InvalidMoveError as e:
                ui.notification_area.notify("Invalid move!", timeout=1)
                return
            self.board.rotate(row, col, rotation)
            ui.topbar.btn_clockwise.state = 'normal'
            ui.topbar.btn_anticlockwise.state = 'normal'
        else:
            if cell.token is not None:
                return
            token = gameplay.token
            try:
                gameplay.token_move(row, col)
            except InvalidMoveError as e:
                ui.notification_area.notify("ROTATE PLEASE", timeout=1)
                return
            cell.token = token
            self.board.array[row][col] = token
        self.update()


class AIPanel(BoxLayout):
    label = ObjectProperty()
    def ai_move(self, ai_id):
        ui.grid.ai_move(ai_id)

    # def utility(self):
    #     token = gameplay.token
    #     state = ai.game.make_state(array=ui.grid.board.array, num_moves=token)
    #     u = ai.game.utility(state, token)
    #     self.label.text = "Utility: %.2f" % u


class UI(RelativeLayout):
    grid = ObjectProperty()
    topbar = ObjectProperty()
    notification_area = ObjectProperty()
    ai_panel = ObjectProperty()


class PentagoApp(App):
    def build(self):
        global gameplay, ui
        gameplay = GamePlay()
        ui = UI()
        gameplay.init_game()
        return ui


if __name__ == '__main__':
    app = PentagoApp()
    app.run()
