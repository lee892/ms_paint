import pygame

from objects import Grid, Pixel, colorPalette, Tools

#Default values
pixel_width = 12
pixel_height = 12
grid_col = 50
grid_row = 50
window_width = 600
window_height = 600

pygame.init()

def initialize(width, height, rows, columns, pixel_height, pixel_width):
	global grid, color_palette, tools

	screen = pygame.display.set_mode((width, height + 200))
	screen.fill((255, 255, 255))

	#Create objects
	color_palette = colorPalette(screen)
	grid = Grid(screen, rows, columns, pixel_width, pixel_height)
	grid.clear_grid(color_palette)
	tools = Tools(screen)

	pygame.display.update()


#Main loop
initialize(window_width, window_height, grid_row, grid_col, pixel_height, pixel_width)

running = True

while running:
	ev = pygame.event.get()

	for event in ev:
		if event.type == pygame.QUIT:
			running = False

		if pygame.mouse.get_pressed()[0]:
			mouse_pos = pygame.mouse.get_pos()
			if mouse_pos[1] > window_height:
				for color_button in color_palette.color_buttons:
					if mouse_pos[0] - (mouse_pos[0] % color_button[2]) == color_button[0] and mouse_pos[1] - (mouse_pos[1] % color_button[2]) == color_button[1]:
						color_palette.select_color(color_button)
				for tool_button in tools.tool_buttons:
					if mouse_pos[0] - (mouse_pos[0] % tool_button[2]) == tool_button[0] and mouse_pos[1] - (mouse_pos[1] % tool_button[2]) == tool_button[1]:
						tools.select_tool(tool_button, color_palette, grid)
				for line_button in tools.line_width_buttons:
					if mouse_pos[0] - (mouse_pos[0] % line_button[2]) == line_button[0] and mouse_pos[1] - (mouse_pos[1] % line_button[2]) == line_button[1]:
						tools.select_line_width(line_button, color_palette)
			elif mouse_pos[1] < window_height and color_palette.current_color:
				if tools.allow_draw:
					grid.draw_on_grid(mouse_pos, color_palette, tools)
				elif tools.allow_erase:
					grid.draw_on_grid(mouse_pos, color_palette, tools)
				elif tools.allow_fill:
					grid.draw_to_fill(mouse_pos, color_palette, tools)

	pygame.display.update()

pygame.quit()
