import time
import pygame
from screens.screen import Screen
from ui.button import Button
from model import Car, Node
from screens.solver_screen import SolverScreen

CELL_SIZE = 80
GRID_SIZE = 6
MARGIN = 30

CAR_COLORS = {
    'G': (255, 100, 100),
    'A': (100, 150, 250),
    'B': (0, 200, 100),
    'C': (255, 200, 0),
    'D': (138, 43, 226),
    'E': (255, 105, 180),
}

class MapEditorScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.cars = []

        self.target_car_placed = False
        self.instructions = "Choose the location of the target car."
        self.selected_color = 'G'
        self.current_dir = 'h'
        self.car_length = 2

        self.ok_button = Button(580, 500, 100, 40, "OK", self.place_car, self.app)
        self.solve_button = Button(580, 560, 100, 40, "Complete", self.on_solve, self.app)
        self.back_button = Button(30, 560, 100, 40, "Back", self.go_back, self.app)

        self.font = pygame.font.SysFont("Arial", 18)

        self.color_buttons = []
        self.available_colors = ['A', 'B', 'C', 'D', 'E']
        for i, color_id in enumerate(self.available_colors):
            btn = Button(580, 50 + i * 50, 40, 40, '', lambda c=color_id: self.select_color(c), bg_color=CAR_COLORS[color_id])
            self.color_buttons.append(btn)

        self.toggle_dir_button = Button(580, 320, 100, 30, "Dir: H", self.toggle_direction, self.app)
        self.length_button = Button(580, 360, 100, 30, "Len: 2", self.toggle_length, self.app)

        self.selected_cell = None

        self.instruction_popup = None
        self.instruction_timer = 0
        self.instruction_duration = 2
        self.instruction_queue = [
            "Dir means direction: H is horizontal",
            "V is vertical",
            "Len means length: only 2 or 3",
            "Click Dir or Len to change them",
            "Place target car tail at row 3",
            "Now pick a color and place a car"
        ]
        self.current_instruction_index = 0
        self.show_instruction(self.instruction_queue[self.current_instruction_index])

    def show_instruction(self, message):
        self.instruction_popup = message
        self.instruction_timer = time.time()

    def select_color(self, color_id):
        self.selected_color = color_id

    def toggle_direction(self):
        self.current_dir = 'v' if self.current_dir == 'h' else 'h'
        self.toggle_dir_button.label = f"Dir: {'V' if self.current_dir == 'v' else 'H'}"

    def toggle_length(self):
        self.car_length = 3 if self.car_length == 2 else 2
        self.length_button.label = f"Len: {self.car_length}"

    def render(self):
        self.app.screen.fill((255, 255, 230))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.app.screen, (200, 200, 200), rect, 1)
                val = self.grid[row][col]
                if val != '.':
                    color = CAR_COLORS.get(val, (150, 150, 150))
                    pygame.draw.rect(self.app.screen, color, rect)

        if self.selected_cell:
            row, col = self.selected_cell
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.app.screen, (0, 255, 0), rect, 3)

        for btn in self.color_buttons:
            btn.draw(self.app.screen)
        self.toggle_dir_button.draw(self.app.screen)
        self.length_button.draw(self.app.screen)
        self.ok_button.draw(self.app.screen)
        self.solve_button.draw(self.app.screen)
        self.back_button.draw(self.app.screen)

        lines = self.instructions.split('\n')
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (0, 0, 0))
            self.app.screen.blit(text, (MARGIN, 530 + i * 20))

        if self.instruction_popup and (time.time() - self.instruction_timer <= self.instruction_duration):
            popup_surf = pygame.Surface((520, 40))
            popup_surf.fill((255, 255, 180))
            pygame.draw.rect(popup_surf, (0, 0, 0), popup_surf.get_rect(), 2)
            text = self.font.render(self.instruction_popup, True, (0, 0, 0))
            popup_surf.blit(text, (10, 10))
            self.app.screen.blit(popup_surf, (30, 10))
        elif self.instruction_popup:
            self.instruction_popup = None
            self.current_instruction_index += 1
            if self.current_instruction_index < len(self.instruction_queue):
                self.show_instruction(self.instruction_queue[self.current_instruction_index])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    self.selected_cell = (row, col)

                if self.ok_button.is_clicked(event.pos):
                    if not (self.instruction_popup and time.time() - self.instruction_timer <= self.instruction_duration):
                        self.ok_button.on_click()

                for btn in self.color_buttons + [
                    self.solve_button,
                    self.toggle_dir_button,
                    self.length_button,
                    self.back_button
                ]:
                    if btn.is_clicked(event.pos):
                        btn.on_click()

    def place_car(self):
        if not self.selected_cell:
            self.show_instruction("Click a cell to place car.")
            self.instructions = "You must click a cell first."
            return

        if not self.target_car_placed:
            if self.current_dir != 'h':
                self.show_instruction("Target car must be horizontal.")
                self.instructions = "Change direction to H."
                return
            if self.car_length != 2:
                self.show_instruction("Target car must have length 2.")
                self.instructions = "Change length to 2."
                return
            if self.selected_cell[0] != 2:
                self.show_instruction("Target car must be on row 3.")
                self.instructions = "Place red car in row 3."
                return
        else:
            if not self.selected_color:
                self.show_instruction("Pick a color before placing.")
                self.instructions = "Click a color button first."
                return

        row, col = self.selected_cell
        size = 2 if not self.target_car_placed else self.car_length
        car_id = 'G' if not self.target_car_placed else self.selected_color
        dir = 'h' if not self.target_car_placed else self.current_dir

        coords = []
        try:
            if dir == 'h':
                for i in range(size):
                    if self.grid[row][col + i] != '.':
                        self.show_instruction("Car overlaps another.")
                        self.instructions = "Choose a free position."
                        return
                    coords.append((row, col + i))
            else:
                for i in range(size):
                    if self.grid[row + i][col] != '.':
                        self.show_instruction("Car overlaps another.")
                        self.instructions = "Choose a free position."
                        return
                    coords.append((row + i, col))
        except IndexError:
            self.show_instruction("Car out of bounds.")
            self.instructions = "Too close to edge."
            return

        for r, c in coords:
            self.grid[r][c] = car_id

        self.cars.append(Car(id=car_id, dir=dir, row=row + 2, col=col + 2, size=size))

        if not self.target_car_placed:
            self.target_car_placed = True
            self.selected_color = None
            self.show_instruction(self.instruction_queue[5])
            self.instructions = "Now pick a color,\nthen place the next car."
        else:
            if self.selected_color in self.available_colors:
                self.available_colors.remove(self.selected_color)

            self.color_buttons = [
                Button(580, 50 + i * 50, 40, 40, '', lambda c=color_id: self.select_color(c), self.app, bg_color=CAR_COLORS[color_id])
                for i, color_id in enumerate(self.available_colors)
            ]

            if not self.available_colors:
                self.selected_color = None
                self.instructions = "No more cars to place."
                self.show_instruction("You placed all cars.")
            else:
                self.selected_color = None
                self.instructions = "Pick a color for next car."

    def on_solve(self):
        if not self.target_car_placed:
            self.instructions = "Place the target car first!"
            self.show_instruction("You must place red car first.")
            return
        node = Node(self.cars)
        self.app.switch_screen(SolverScreen(self.app, node, "", car_colors=CAR_COLORS))

    def go_back(self):
        from screens.menu_screen import MenuScreen
        self.app.switch_screen(MenuScreen(self.app))
