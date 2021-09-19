import pygame
import math
import sys

pygame.init()

sys.setrecursionlimit(2500)


class Grid:
	def __init__(self, screen, rows, columns, pixel_width, pixel_height):
		self.rows = rows
		self.columns = columns
		self.screen = screen
		self.grid = []
		self.pixel_width = pixel_width
		self.pixel_height = pixel_height

	def draw_on_grid(self, mouse_pos, color_palette, tools):
		row = math.floor(mouse_pos[1] / self.pixel_height)
		column = math.floor(mouse_pos[0] / self.pixel_width)
		if tools.line_width == None:
			return
		elif tools.line_width == 1:
			self.grid[row][column].draw_pixel(self.screen, color_palette.current_color)
			return
		elif tools.line_width == 2:
			line_width = tools.line_width + 1
			offset = 1
		elif tools.line_width == 3:
			line_width = tools.line_width + 2
			offset = 2
		else:
			line_width = tools.line_width + 2
			offset = 3

		for i in range(line_width):
				for j in range(line_width):
					if row + (i - 1) >= self.rows or column + (j - 1) >= self.columns or row + (i - 1) < 0 or column + (j - 1) < 0:
						continue
					self.grid[row + (i - offset)][column + (j - offset)].draw_pixel(self.screen, color_palette.current_color)


	def draw_to_fill(self, mouse_pos, color_palette, tools):
		row = math.floor(mouse_pos[1] / self.pixel_height)
		column = math.floor(mouse_pos[0] / self.pixel_width)
		if self.grid[row][column].color != color_palette.current_color:
			color_palette.fill_color = self.grid[row][column].color

			self.fill(row, column, color_palette)
			
			tools.select_tool(tools.tool_buttons[0], color_palette, self.grid)

	def fill(self, row, column, color_palette):
		self.grid[row][column].draw_pixel(self.screen, color_palette.current_color)

		#Check corners
		for i in range(2):
			if row == i * 49 and column == 1 and self.grid[i * 49][0].color == color_palette.fill_color:
				self.grid[i * 49][0].draw_pixel(self.screen, color_palette.current_color)
			if row == i * 49 and column == 48 and self.grid[i * 49][49].color == color_palette.fill_color:
				self.grid[i * 49][49].draw_pixel(self.screen, color_palette.current_color)

		if row + 1 >= self.rows or row - 1 < 0 or column + 1 >= self.columns or column - 1 < 0:
			return

		for i in range(3):
			if i == 1:
				continue
			if self.grid[row + (i - 1)][column].color == color_palette.fill_color:
				self.fill(row + (i - 1), column, color_palette)
			if self.grid[row][column + (i - 1)].color == color_palette.fill_color:
				self.fill(row, column + (i - 1), color_palette)

			
	def clear_grid(self, color_palette):
		self.grid = []
		for i in range(self.rows):
			self.grid.append([])
			for j in range(self.columns):
				self.grid[i].append(Pixel(i, j, self.pixel_width, self.pixel_height, color_palette.colors[6]))
				self.grid[i][j].draw_pixel(self.screen, color_palette.colors[6])


class Pixel:
	def __init__(self, row, column, width, height, color):
		self.width = width
		self.height = height
		self.x = column * width
		self.y = row * height
		self.color = color

	def draw_pixel(self, screen, color):
		self.color = color
		pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))


class colorPalette:
	def __init__(self, screen):
		self.screen = screen
		self.color_buttons = []
		#Yellow, orange, red, purple, blue, green, white, black
		self.colors = [(255, 255, 0), (255, 128, 0), (255, 0, 0), (128, 0, 255), (0, 0, 255), (0, 255, 0), (255, 255, 255), (0, 0, 0)]
		self.previous_color = (255, 255, 255)
		self.current_color = None
		self.fill_color = None
		self.create_color_buttons()

	def create_color_buttons(self):
		x_start = 75
		y_start = 650
		button_width = 25
		for i, color in enumerate(self.colors):
			self.color_buttons.append(pygame.Rect(x_start, y_start, button_width, button_width))
			pygame.draw.rect(self.screen, color, (x_start, y_start, button_width, button_width))
			pygame.draw.rect(self.screen, self.colors[7], (x_start, y_start, button_width, button_width), 1)
			x_start += button_width
			if i == 3:
				y_start += button_width
				x_start = 75

	def select_color(self, color_button):
		for i, button in enumerate(self.color_buttons):
			pygame.draw.rect(self.screen, self.colors[7], button, 1)
			if button == color_button:
				self.current_color = self.colors[i]
				pygame.draw.rect(self.screen, self.colors[2], button, 1)


class Tools:
	def __init__(self, screen):
		self.screen = screen
		self.line_width = None
		self.previous_line_width = None
		self.tool_buttons = []
		self.line_width_buttons = []
		self.number_of_buttons = 8
		self.allow_draw = False
		self.allow_erase = False
		self.allow_fill = False
		self.erasing = False
		self.create_tool_buttons()

	def create_tool_buttons(self):
		button_characters = ['D', 'E', 'F', 'C']
		x_start = 400
		y_start = 650
		button_width = 25
		line_thickness = 1
		black = (0, 0, 0)
		
		for i in range(self.number_of_buttons):
			if i < 4:
				self.line_width_buttons.append(pygame.Rect(x_start, y_start, button_width, button_width))
				img = pygame.font.SysFont(None, 24).render(f"{i + 1}", True, black)
			elif i == 4:
				y_start += button_width
				x_start = 400
			if i > 3:
				self.tool_buttons.append(pygame.Rect(x_start, y_start, button_width, button_width))
				img = pygame.font.SysFont(None, 24).render(button_characters[i - 4], True, black)
			self.screen.blit(img, (x_start + 7, y_start + 7))
			pygame.draw.rect(self.screen, black, (x_start, y_start, button_width, button_width), line_thickness)

			x_start += button_width

	def select_tool(self, tool_button, color_palette, grid):
		for i, button in enumerate(self.tool_buttons):
			pygame.draw.rect(self.screen, color_palette.colors[7], button, 1)
			if button == tool_button:
				pygame.draw.rect(self.screen, color_palette.colors[2], button, 1)
				self.allow_draw = False
				self.allow_erase = False
				self.allow_fill = False
				if i == 0:
					if self.erasing:
						self.line_width = self.previous_line_width
						self.select_line_width(self.line_width_buttons[self.line_width - 1], color_palette)
						color_palette.current_color = color_palette.previous_color
						color_palette.select_color(color_palette.color_buttons[color_palette.colors.index(color_palette.current_color)])
					self.allow_draw = True
					self.erasing = False
				elif i == 1:
					self.allow_erase = True
					self.erasing = True
					self.previous_line_width = self.line_width
					self.select_line_width(self.line_width_buttons[1], color_palette)
					color_palette.previous_color = color_palette.current_color
					color_palette.select_color(color_palette.color_buttons[6])
				elif i == 2:
					self.allow_fill = True
				elif i == 3:
					grid.clear_grid(color_palette)
					self.select_tool(self.tool_buttons[0], color_palette, grid)


	def select_line_width(self, line_width_button, color_palette):
		for i, button in enumerate(self.line_width_buttons):
			pygame.draw.rect(self.screen, color_palette.colors[7], button, 1)
			if button == line_width_button:
				pygame.draw.rect(self.screen, color_palette.colors[2], button, 1)
				self.line_width = i + 1