import gym
import universe # register universe environment
import random
env = gym.make('flashgames.NeonRace-v0')
env.configure(remotes=1) # automatically creates a local docker container
observation_n = env.reset()
# Объявление действий
# Движение налево
left = [('KeyEvent', 'ArrowUp', True),
('KeyEvent', 'ArrowLeft', True),
('KeyEvent', 'ArrowRight', False)]
# Движение направо
right = [('KeyEvent', 'ArrowUp', True),
('KeyEvent', 'ArrowLeft', False),
('KeyEvent', 'ArrowRight', True)]
# Движение вперед
forward = [('KeyEvent', 'ArrowUp', True),
('KeyEvent', 'ArrowRight',
False),
('KeyEvent', 'ArrowLeft', False),
('KeyEvent', 'n', True)]
# Переменная turn определяет, нужно ли повернуть
turn = 0
# Все награды сохраняются в списке rewards
rewards = []
# Переменная buffer_size используется как пороговое значение
buffer_size = 100
# Изначально выбирается действие forward
action = forward
while True:
    turn -= 1
    if turn <= 0:
        action = forward
        turn = 0
    action_n = [action for ob in observation_n]
    observation_n, reward_n, done_n, info = env.step(action_n)
    rewards += [reward_n[0]]
    if len(rewards) >= buffer_size:
        mean = sum(rewards)/len(rewards)
        if mean == 0:
            turn = 20
            if random.random() < 0.5:
                action = right
            else:
                action = left
        rewards = []
env.render()