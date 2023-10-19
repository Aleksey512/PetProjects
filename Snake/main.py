import random
import sys
import time

import pygame

from generative_algorithm import crossover, mutate
from classes import Apple, Snake, Grid, GameOver
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, FPS


def calculate_fitness(snake: Snake, start_time: float) -> float:
    # Баллы за съеденное яблоко
    apple_score = len(snake.body) * 10

    # Полная приспособленность
    fitness = (time.time() - start_time) * apple_score

    return fitness


def run_game_with_genome(genome) -> float:
    start_time = time.time()
    fitness = 0
    grid = Grid()
    snake = Snake()
    apple = Apple(snake, grid)

    try:
        while genome:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Обновление направления змейки на основе генома
            if genome:
                action = genome.pop(0)  # Берем и удаляем первое действие из генома
                if action == "UP" and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif action == "DOWN" and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif action == "LEFT" and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif action == "RIGHT" and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

            DISPLAY.fill(BG_COLOR)
            grid.draw(DISPLAY)
            apple.draw(DISPLAY)
            snake.draw(DISPLAY)

            snake.move()

            if snake.check_eat_apple(apple):
                snake.add_tail()
                apple = Apple(snake, grid)

            pygame.display.flip()
            FPS_CLOCK.tick(FPS)
        else:
            fitness += calculate_fitness(snake, start_time)
            fitness += 5
            return fitness
    except GameOver:
        fitness += calculate_fitness(snake, start_time)
        fitness /= 2
    finally:
        return fitness


def main():
    population_size = 50
    mutation_rate = 0.1
    generations = 200
    genome_length = 10000

    # Создание начальной популяции
    population = [
        (random.choices(["LEFT", "RIGHT", "UP", "DOWN"], k=genome_length), 0)
        for _ in range(population_size)
    ]

    for generation in range(generations):
        for i in range(len(population)):
            current_genome, current_fitness = population[i]
            fitness = run_game_with_genome(current_genome.copy())
            print(f"\nGeneration: {generation}\nPopulation: {i}\nFitness: {fitness}\n")
            population[i] = (current_genome, fitness)

        # Селекция
        population.sort(key=lambda x: x[1], reverse=True)
        selected_parents = population[: int(0.2 * population_size)]

        # Скрещивание и мутация
        offspring = []
        for _ in range(population_size - len(selected_parents)):
            parent1, parent2 = random.sample(selected_parents, 2)
            child_genome = crossover(parent1[0], parent2[0])
            child_genome = mutate(child_genome, mutation_rate)
            offspring.append(
                (child_genome, 0)
            )  # Исправлено: добавляем fitness равное 0 для потомков

        # Формирование нового поколения
        population = selected_parents + offspring


if __name__ == "__main__":
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Wormy")

    main()
