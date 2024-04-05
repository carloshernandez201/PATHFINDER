import pygame

from display import Node
from display import Pathfinder
def main(rows):
    pygame.init()
    super_game_manager = Pathfinder(rows)
    play = True #run in video
    commenced = False # started in video
    counter = 0
    super_game_manager.draw_all()
    print(len(super_game_manager.grid))
    print(len(super_game_manager.grid[0]))
    for i in range(len(super_game_manager.grid)):
        for j in range (len(super_game_manager.grid[0])):
            super_game_manager.grid[i][j].make_barrier()

    while play:
        for event in pygame.event.get():
            did_sum_happen = False
            super_game_manager.draw_all()
            if event.type == pygame.QUIT:
                play = False
            if commenced:
                continue
            if (counter == 0) and  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # if its the first click, this will determine start node
                click_pos = pygame.mouse.get_pos()
                row, col = super_game_manager.convert_clicK_to_node_location(click_pos[0], click_pos[1])
                start_node = super_game_manager.grid[4][4]
                start_node.make_start()
                did_sum_happen = True
            elif (counter == 1) and pygame.mouse.get_pressed()[0]:
                # if its the first click, this will determine start node
                click_pos = pygame.mouse.get_pos()
                row, col = super_game_manager.convert_clicK_to_node_location(click_pos[0], click_pos[1])
                if (super_game_manager.grid[row][col] != start_node):
                    target_node = (super_game_manager.grid[row][col])
                    target_node.make_end()
                    did_sum_happen = False
            elif pygame.mouse.get_pressed()[0]:
                click_pos = pygame.mouse.get_pos()
                row, col = super_game_manager.convert_clicK_to_node_location(click_pos[0], click_pos[1])
                barrier_node = super_game_manager.grid[row][col]
                barrier_node.make_barrier()
                did_sum_happen = False
            elif pygame.mouse.get_pressed()[1]:
                click_pos = pygame.mouse.get_pos()
                row, col = super_game_manager.convert_clicK_to_node_location(click_pos[0], click_pos[1])
                if super_game_manager.grid[row][col].is_barrier():
                    super_game_manager.reset()
                did_sum_happen = False
            if did_sum_happen:
                super_game_manager.draw_all()
            counter = counter + 1

    pygame.quit()
if __name__ == "__main__":
    main(rows=50)  # Or however many rows you want
