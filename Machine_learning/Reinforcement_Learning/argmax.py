import numpy as np
import random as pr
import gymnasium as gym

# 환경 설정
env = gym.make("FrozenLake-v1", is_slippery=False)

# Q 테이블 초기화(상태 x 행동)
Q = np.zeros((env.observation_space.n, env.action_space.n))

num_episodes = 2000
rewards_per_episode = []

# 에피소드 반복
for episode in range(num_episodes):
    state, _ = env.reset()
    done = False
    total_reward = 0

    while not done:
        # Q값이 가장 큰 행동 선택
        action = np.argmax(Q[state])

        # 행동 수행 및 결과 관찰
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated  # 종료 조건

        # Q 테이블 업데이트 (a=1, y=1 가정)
        Q[state, action] = reward + np.max(Q[next_state])

        # 다음 상태로 이동
        state = next_state
        total_reward += reward

    rewards_per_episode.append(total_reward)

# 결과 출력
print(f"\n마지막 100 에피소드 평균 보상 : {np.mean(rewards_per_episode[-100:]):.4f}")
print("최종 Q 테이블 :")
print(Q)
